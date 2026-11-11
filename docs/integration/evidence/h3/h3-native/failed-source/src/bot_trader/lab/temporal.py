"""Immutable temporal protocol preparation; no fitting or dataset access.

Intervals are half-open. An observation's label endpoint is inclusive, so a
label ending exactly at an evaluation boundary is excluded from training.
The purge/embargo helper describes overlap exclusions; it does not claim that
temporal splitting repairs unknown publication times or pretrained-model leaks.
"""

from collections.abc import Sequence
from datetime import datetime, timedelta
from typing import Self

from pydantic import Field, model_validator

from bot_trader.core.contracts import FrozenContract, Identifier, Partition, UTCDateTime, utc_time


class ObservationWindow(FrozenContract):
    id: Identifier
    feature_time: UTCDateTime
    information_available_at: UTCDateTime
    label_end: UTCDateTime
    label_available_at: UTCDateTime

    @model_validator(mode="after")
    def validate_times(self) -> Self:
        if self.feature_time > self.information_available_at:
            raise ValueError("Information availability cannot precede the feature event.")
        if self.label_end < self.feature_time or self.label_available_at < self.label_end:
            raise ValueError("Label availability must follow its inclusive observation interval.")
        return self


class TimePartition(FrozenContract):
    role: Partition
    start: UTCDateTime
    end: UTCDateTime

    @model_validator(mode="after")
    def validate_interval(self) -> Self:
        if self.end <= self.start:
            raise ValueError("A partition must be a nonempty half-open interval.")
        return self


def _validate_observations(observations: Sequence[ObservationWindow]) -> None:
    if len(observations) > 10_000:
        raise ValueError("Temporal fixture plans are bounded to 10000 observations.")
    if len({item.id for item in observations}) != len(observations):
        raise ValueError("Observation identities must be unique.")


def eligible_observation_ids(
    observations: Sequence[ObservationWindow],
    excluded: TimePartition,
    *,
    known_at: datetime,
    purge_seconds: int = 0,
    embargo_seconds: int = 0,
) -> tuple[str, ...]:
    """Exclude unavailable labels/features and overlap with a buffered evaluation.

    An embargo after evaluation matters when candidate training intervals occur
    after it. A strictly past-only training set has no such observations. This
    function is a contract utility, not authorization to use final payloads.
    """
    if purge_seconds < 0 or embargo_seconds < 0:
        raise ValueError("Purge and embargo must be nonnegative.")
    _validate_observations(observations)
    known_at = utc_time(known_at)
    lower = excluded.start - timedelta(seconds=purge_seconds)
    upper = excluded.end + timedelta(seconds=embargo_seconds)
    return tuple(
        item.id
        for item in observations
        if item.information_available_at <= known_at
        and item.label_available_at <= known_at
        and (item.label_end < lower or item.feature_time >= upper)
    )


class TemporalPlan(FrozenContract):
    partitions: tuple[TimePartition, TimePartition, TimePartition]
    purge_seconds: int = Field(default=0, ge=0, le=31_536_000)
    embargo_seconds: int = Field(default=0, ge=0, le=31_536_000)

    @model_validator(mode="after")
    def validate_partitions(self) -> Self:
        if tuple(item.role for item in self.partitions) != ("development", "validation", "final"):
            raise ValueError("Partitions must be ordered development, validation, final.")
        development, validation, final = self.partitions
        if development.end > validation.start or validation.end > final.start:
            raise ValueError("Chronological partitions cannot overlap.")
        if validation.start - timedelta(seconds=self.purge_seconds) <= development.start:
            raise ValueError("Purge must leave a nonempty development interval.")
        if validation.end + timedelta(seconds=self.embargo_seconds) > final.start:
            raise ValueError("The final partition must start after the validation embargo.")
        return self

    def training_ids(self, observations: Sequence[ObservationWindow]) -> tuple[str, ...]:
        """Prepare training membership using only information known before validation."""
        _validate_observations(observations)
        development, validation, _ = self.partitions
        candidates = tuple(
            item
            for item in observations
            if development.start <= item.feature_time < development.end
            and item.information_available_at < validation.start
            and item.label_available_at < validation.start
        )
        return eligible_observation_ids(
            candidates,
            validation,
            known_at=validation.start,
            purge_seconds=self.purge_seconds,
            embargo_seconds=self.embargo_seconds,
        )


class WalkForwardPlan(FrozenContract):
    """A finite expanding-window schedule sharing one reserved final interval."""

    folds: tuple[TemporalPlan, ...] = Field(min_length=1, max_length=100)

    @model_validator(mode="after")
    def validate_folds(self) -> Self:
        first = self.folds[0]
        for current in self.folds:
            if current.partitions[2] != first.partitions[2]:
                raise ValueError("All folds must share the same reserved final partition.")
            if current.partitions[0].start != first.partitions[0].start:
                raise ValueError("Expanding folds must share their development origin.")
            if (current.purge_seconds, current.embargo_seconds) != (
                first.purge_seconds,
                first.embargo_seconds,
            ):
                raise ValueError("A walk-forward schedule must keep one buffer policy.")
        for previous, current in zip(self.folds, self.folds[1:], strict=False):
            if current.partitions[0].end <= previous.partitions[0].end:
                raise ValueError("Training intervals must expand strictly forward.")
            previous_end = previous.partitions[1].end + timedelta(seconds=previous.embargo_seconds)
            if current.partitions[1].start < previous_end:
                raise ValueError("Validation intervals and their embargo gaps cannot overlap.")
        return self


def make_walk_forward_plan(
    *,
    development_start: datetime,
    initial_training_seconds: int,
    validation_seconds: int,
    step_seconds: int,
    folds: int,
    final: TimePartition,
    purge_seconds: int = 0,
    embargo_seconds: int = 0,
) -> WalkForwardPlan:
    """Build a prespecified finite schedule, without selecting horizons by results.

    Earlier validation periods may enter a later expanding training window after
    their labels become available. This is walk-forward preparation, not repeated
    final testing. The final interval is metadata only and is never opened here.
    """
    if not 1 <= folds <= 100:
        raise ValueError("A technical walk-forward plan requires 1 to 100 folds.")
    if min(initial_training_seconds, validation_seconds, step_seconds) <= 0:
        raise ValueError("Training, validation and step durations must be positive.")
    if final.role != "final":
        raise ValueError("The reserved partition must have the final role.")
    start = utc_time(development_start)
    plans = []
    for index in range(folds):
        split = start + timedelta(seconds=initial_training_seconds + index * step_seconds)
        plans.append(
            TemporalPlan(
                partitions=(
                    TimePartition(role="development", start=start, end=split),
                    TimePartition(
                        role="validation",
                        start=split,
                        end=split + timedelta(seconds=validation_seconds),
                    ),
                    final,
                ),
                purge_seconds=purge_seconds,
                embargo_seconds=embargo_seconds,
            )
        )
    return WalkForwardPlan(folds=tuple(plans))
