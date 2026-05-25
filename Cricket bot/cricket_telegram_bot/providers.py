from __future__ import annotations

from typing import Any, Protocol

from .models import InningsScore, Match


class CricketProvider(Protocol):
    async def current_matches(self) -> list[Match]:
        ...


class CricketApiError(RuntimeError):
    pass


class DemoCricketProvider:
    async def current_matches(self) -> list[Match]:
        return [
            Match(
                match_id="demo-1",
                name="India vs Australia",
                status="India need 42 runs in 30 balls",
                venue="Wankhede Stadium, Mumbai",
                match_type="odi",
                teams=("India", "Australia"),
                scores=(
                    InningsScore("Australia Inning 1", runs=271, wickets=8, overs="50"),
                    InningsScore("India Inning 1", runs=230, wickets=5, overs="45"),
                ),
            ),
            Match(
                match_id="demo-2",
                name="England Women vs New Zealand Women",
                status="New Zealand Women opt to bat",
                venue="County Ground",
                match_type="t20",
                teams=("England Women", "New Zealand Women"),
                scores=(
                    InningsScore("New Zealand Women Inning 1", runs=87, wickets=3, overs="11.2"),
                ),
            ),
            Match(
                match_id="demo-3",
                name="Royal Challengers Bengaluru vs Gujarat Titans",
                status="Match starts soon",
                venue="Himachal Pradesh Cricket Association Stadium",
                match_type="t20",
                teams=("Royal Challengers Bengaluru", "Gujarat Titans"),
            ),
        ]


class CricketDataProvider:
    BASE_URL = "https://api.cricapi.com/v1/currentMatches"

    def __init__(self, api_key: str, *, timeout_seconds: float = 12.0) -> None:
        self.api_key = api_key
        self.timeout_seconds = timeout_seconds

    async def current_matches(self) -> list[Match]:
        try:
            import httpx
        except ImportError as exc:
            raise CricketApiError("Install dependencies with: pip install -r requirements.txt") from exc

        async with httpx.AsyncClient(timeout=self.timeout_seconds) as client:
            response = await client.get(self.BASE_URL, params={"apikey": self.api_key, "offset": 0})

        try:
            response.raise_for_status()
        except httpx.HTTPStatusError as exc:
            raise CricketApiError(f"Cricket API returned HTTP {response.status_code}.") from exc

        try:
            payload = response.json()
        except ValueError as exc:
            raise CricketApiError("Cricket API returned an invalid JSON response.") from exc

        if payload.get("status") not in {None, "success"}:
            reason = payload.get("reason") or payload.get("message") or "Cricket API request failed."
            raise CricketApiError(str(reason))

        return [parse_cricapi_match(raw) for raw in payload.get("data") or [] if isinstance(raw, dict)]


def build_provider(provider_name: str, api_key: str | None) -> CricketProvider:
    if provider_name == "demo":
        return DemoCricketProvider()

    if provider_name == "cricapi":
        if not api_key:
            raise RuntimeError("CRICAPI_KEY is required when CRICKET_PROVIDER=cricapi.")
        return CricketDataProvider(api_key)

    if api_key:
        return CricketDataProvider(api_key)

    return DemoCricketProvider()


def parse_cricapi_match(raw: dict[str, Any]) -> Match:
    team_names = tuple(
        team.get("shortname") or team.get("name")
        for team in raw.get("teamInfo") or []
        if isinstance(team, dict) and (team.get("shortname") or team.get("name"))
    )

    return Match(
        match_id=str(raw.get("id") or raw.get("unique_id") or raw.get("match_id") or "unknown"),
        name=str(raw.get("name") or _name_from_teams(team_names) or "Unknown match"),
        status=str(raw.get("status") or "Status unavailable"),
        venue=_optional_str(raw.get("venue")),
        match_type=_optional_str(raw.get("matchType") or raw.get("match_type")),
        teams=team_names,
        scores=tuple(_parse_score(score) for score in raw.get("score") or [] if isinstance(score, dict)),
    )


def _parse_score(raw: dict[str, Any]) -> InningsScore:
    return InningsScore(
        inning=str(raw.get("inning") or "Inning"),
        runs=_optional_int(raw.get("r")),
        wickets=_optional_int(raw.get("w")),
        overs=_optional_str(raw.get("o")),
    )


def _name_from_teams(teams: tuple[str, ...]) -> str | None:
    if len(teams) >= 2:
        return f"{teams[0]} vs {teams[1]}"
    return teams[0] if teams else None


def _optional_int(value: Any) -> int | None:
    if value is None or value == "":
        return None
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def _optional_str(value: Any) -> str | None:
    if value is None:
        return None
    text = str(value).strip()
    return text or None
