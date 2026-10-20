"""Finite technical tasks and inert research proposals, never executable text."""

from typing import Literal

from pydantic import Field, field_validator

from bot_trader.core.contracts import (
    FrozenContract,
    Identifier,
    SourceReference,
    VersionedReference,
)


class TechnicalRunSpec(FrozenContract):
    mode: Literal["technical"] = "technical"
    task: Literal["quality_check", "transform_check", "ledger_check", "failure_fixture"]
    dataset_id: Identifier
    dataset_version: int = Field(ge=1)
    seed: int = Field(default=0, ge=0, le=2**32 - 1)
    window: int = Field(default=5, ge=2, le=500)
    hypotheses: tuple[VersionedReference, ...] = Field(default=(), max_length=25)

    @field_validator("hypotheses")
    @classmethod
    def validate_associations(
        cls, references: tuple[VersionedReference, ...]
    ) -> tuple[VersionedReference, ...]:
        if any(reference.kind != "hypothesis" for reference in references):
            raise ValueError("Technical tasks only accept hypothesis associations.")
        if len({reference.id for reference in references}) != len(references):
            raise ValueError("Each hypothesis can be associated only once per attempt.")
        return references


class ResearchProposal(FrozenContract):
    title: str = Field(min_length=1, max_length=200)
    rationale: str = Field(min_length=1, max_length=4000)
    null_hypothesis: str = Field(min_length=1, max_length=2000)
    refutation: str = Field(min_length=1, max_length=2000)
    sources: tuple[SourceReference, ...] = Field(default=(), max_length=10)
    duplicate_ids: tuple[Identifier, ...] = Field(default=(), max_length=25)
    model_version: str | None = Field(default=None, max_length=200)
    prompt_version: str | None = Field(default=None, max_length=200)
    provenance: str = Field(min_length=1, max_length=2000)
    requested_budget_units: int = Field(default=1, ge=1, le=100)
    mode: Literal["proposal_only"] = "proposal_only"
