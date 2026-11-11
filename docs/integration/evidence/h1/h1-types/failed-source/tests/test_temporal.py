from datetime import UTC, datetime, timedelta

import pytest
from pydantic import ValidationError

from bot_trader.lab.temporal import (
    ObservationWindow,
    TemporalPlan,
    TimePartition,
    WalkForwardPlan,
    eligible_observation_ids,
    make_walk_forward_plan,
)

START = datetime(2020, 1, 1, tzinfo=UTC)


def at(seconds: int) -> datetime:
    return START + timedelta(seconds=seconds)


def observation(
    identifier: str,
    feature: int,
    end: int,
    *,
    available: int | None = None,
    label_available: int | None = None,
) -> ObservationWindow:
    return ObservationWindow(
        id=identifier,
        feature_time=at(feature),
        information_available_at=at(feature if available is None else available),
        label_end=at(end),
        label_available_at=at(end if label_available is None else label_available),
    )


def plan(purge: int = 0, embargo: int = 0) -> TemporalPlan:
    return TemporalPlan(
        partitions=(
            TimePartition(role="development", start=at(0), end=at(100)),
            TimePartition(role="validation", start=at(100), end=at(150)),
            TimePartition(role="final", start=at(200), end=at(250)),
        ),
        purge_seconds=purge,
        embargo_seconds=embargo,
    )


def test_training_membership_excludes_unavailable_features_labels_and_overlap() -> None:
    records = (
        observation("safe", 10, 20),
        observation("late-feature", 20, 30, available=101),
        observation("late-label", 30, 40, label_available=100),
        observation("crossing-label", 40, 101),
        observation("boundary-label", 50, 100),
        observation("validation-feature", 100, 110),
        observation("before-development", -10, -1),
        observation("safe-last", 90, 99),
    )
    assert plan().training_ids(records) == ("safe", "safe-last")
    assert plan(purge=10).training_ids(records) == ("safe",)


def test_inclusive_label_end_purge_and_half_open_embargo_boundaries() -> None:
    excluded = TimePartition(role="validation", start=at(100), end=at(150))
    records = (
        observation("before-purge", 50, 89),
        observation("purge-boundary", 60, 90),
        observation("overlap", 95, 105),
        observation("embargo", 150, 160),
        observation("embargo-boundary", 170, 180),
        observation("still-unavailable", 180, 190, label_available=201),
    )
    assert eligible_observation_ids(
        records,
        excluded,
        known_at=at(200),
        purge_seconds=10,
        embargo_seconds=20,
    ) == ("before-purge", "embargo-boundary")


def test_plan_is_immutable_serializable_metadata_without_payload_access() -> None:
    original = plan(purge=10, embargo=20)
    assert TemporalPlan.model_validate_json(original.model_dump_json()) == original
    with pytest.raises(ValidationError):
        original.purge_seconds = 0
    assert original.partitions[2].role == "final"
    assert "payload" not in original.model_dump_json()


@pytest.mark.parametrize(
    "values",
    [
        {
            "feature_time": at(10),
            "information_available_at": at(9),
            "label_end": at(20),
            "label_available_at": at(20),
        },
        {
            "feature_time": at(10),
            "information_available_at": at(10),
            "label_end": at(9),
            "label_available_at": at(20),
        },
        {
            "feature_time": at(10),
            "information_available_at": at(10),
            "label_end": at(20),
            "label_available_at": at(19),
        },
        {
            "feature_time": datetime(2020, 1, 1),
            "information_available_at": at(10),
            "label_end": at(20),
            "label_available_at": at(20),
        },
    ],
)
def test_observation_contract_rejects_impossible_or_timezone_free_times(
    values: dict[str, datetime],
) -> None:
    with pytest.raises(ValidationError):
        ObservationWindow.model_validate({"id": "invalid"} | values)


def test_partition_overlap_roles_and_buffers_cannot_admit_final_reuse() -> None:
    original = plan()
    development, validation, final = original.partitions
    invalid_partitions = (
        (validation, development, final),
        (development, TimePartition(role="validation", start=at(99), end=at(150)), final),
        (development, validation, TimePartition(role="final", start=at(149), end=at(250))),
    )
    for partitions in invalid_partitions:
        with pytest.raises(ValidationError):
            TemporalPlan(partitions=partitions)
    for purge, embargo in ((100, 0), (0, 51), (-1, 0), (0, -1)):
        with pytest.raises(ValidationError):
            plan(purge=purge, embargo=embargo)
    with pytest.raises(ValidationError):
        TimePartition(role="development", start=at(10), end=at(10))


def test_duplicates_and_unbounded_input_are_rejected() -> None:
    entry = observation("one", 10, 20)
    with pytest.raises(ValueError, match="unique"):
        plan().training_ids((entry, entry))
    records = tuple(observation(f"row-{index}", 10, 20) for index in range(10_001))
    with pytest.raises(ValueError, match="bounded"):
        plan().training_ids(records)
    outside = observation("one", 300, 350)
    with pytest.raises(ValueError, match="unique"):
        plan().training_ids((entry, outside))
    for purge, embargo in ((-1, 0), (0, -1)):
        with pytest.raises(ValueError):
            eligible_observation_ids(
                (entry,),
                plan().partitions[1],
                known_at=at(100),
                purge_seconds=purge,
                embargo_seconds=embargo,
            )


def test_expanding_walk_forward_schedule_keeps_one_untouched_final_interval() -> None:
    final = TimePartition(role="final", start=at(400), end=at(500))
    schedule = make_walk_forward_plan(
        development_start=at(0),
        initial_training_seconds=100,
        validation_seconds=50,
        step_seconds=70,
        folds=3,
        final=final,
        purge_seconds=10,
        embargo_seconds=20,
    )
    assert [fold.partitions[0].end for fold in schedule.folds] == [at(100), at(170), at(240)]
    assert all(fold.partitions[2] == final for fold in schedule.folds)
    records = (observation("earlier-validation", 120, 140),)
    assert schedule.folds[0].training_ids(records) == ()
    assert schedule.folds[1].training_ids(records) == ("earlier-validation",)
    assert WalkForwardPlan.model_validate_json(schedule.model_dump_json()) == schedule


@pytest.mark.parametrize(
    "overrides",
    [
        {"folds": 0},
        {"folds": 101},
        {"initial_training_seconds": 0},
        {"step_seconds": 0},
        {"validation_seconds": -1},
        {"step_seconds": 69},
        {"final": TimePartition(role="final", start=at(280), end=at(500))},
        {"final": TimePartition(role="validation", start=at(400), end=at(500))},
    ],
)
def test_invalid_or_overlapping_walk_forward_schedule_is_rejected(
    overrides: dict[str, object],
) -> None:
    arguments: dict[str, object] = {
        "development_start": at(0),
        "initial_training_seconds": 100,
        "validation_seconds": 50,
        "step_seconds": 70,
        "folds": 3,
        "final": TimePartition(role="final", start=at(400), end=at(500)),
        "purge_seconds": 10,
        "embargo_seconds": 20,
    }
    with pytest.raises(ValueError):
        make_walk_forward_plan(**(arguments | overrides))  # type: ignore[arg-type]


def test_manual_folds_cannot_change_final_origin_or_buffer_policy() -> None:
    first = plan()
    next_plan = TemporalPlan(
        partitions=(
            TimePartition(role="development", start=at(0), end=at(150)),
            TimePartition(role="validation", start=at(150), end=at(180)),
            first.partitions[2],
        ),
    )
    WalkForwardPlan(folds=(first, next_plan))
    alternatives = (
        next_plan.model_copy(update={"purge_seconds": 1}),
        TemporalPlan(
            partitions=(
                TimePartition(role="development", start=at(1), end=at(150)),
                next_plan.partitions[1],
                next_plan.partitions[2],
            )
        ),
        TemporalPlan(
            partitions=(
                next_plan.partitions[0],
                next_plan.partitions[1],
                TimePartition(role="final", start=at(201), end=at(250)),
            )
        ),
        first,
    )
    for alternative in alternatives:
        with pytest.raises(ValidationError):
            WalkForwardPlan(folds=(first, alternative))
