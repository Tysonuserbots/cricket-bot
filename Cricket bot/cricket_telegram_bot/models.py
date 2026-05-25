from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class InningsScore:
    inning: str
    runs: int | None = None
    wickets: int | None = None
    overs: str | None = None

    @property
    def has_score(self) -> bool:
        return self.runs is not None and self.wickets is not None


@dataclass(frozen=True)
class Match:
    match_id: str
    name: str
    status: str
    venue: str | None = None
    match_type: str | None = None
    teams: tuple[str, ...] = field(default_factory=tuple)
    scores: tuple[InningsScore, ...] = field(default_factory=tuple)

    def searchable_text(self) -> str:
        return " ".join([self.match_id, self.name, self.status, *self.teams]).lower()

