from __future__ import annotations

from collections.abc import Iterable

from .models import InningsScore, Match

MAX_TELEGRAM_MESSAGE_LENGTH = 3900


def format_match_list(matches: Iterable[Match], *, limit: int = 8) -> str:
    selected = list(matches)[:limit]
    if not selected:
        return "No matching cricket fixtures found."

    return "\n\n".join(format_match(match, index=index) for index, match in enumerate(selected, start=1))


def format_match(match: Match, *, index: int | None = None) -> str:
    title = f"{index}. {match.name}" if index is not None else match.name
    lines = [title, f"Status: {match.status}"]

    if match.match_type:
        lines.append(f"Format: {match.match_type.upper()}")

    if match.venue:
        lines.append(f"Venue: {match.venue}")

    if match.scores:
        lines.extend(format_innings_score(score) for score in match.scores)

    lines.append(f"ID: {match.match_id}")
    return "\n".join(lines)


def format_innings_score(score: InningsScore) -> str:
    if not score.has_score:
        return f"{score.inning}: score unavailable"

    overs = f" ({score.overs} ov)" if score.overs else ""
    return f"{score.inning}: {score.runs}/{score.wickets}{overs}"


def split_message(text: str, *, limit: int = MAX_TELEGRAM_MESSAGE_LENGTH) -> list[str]:
    if limit < 1:
        raise ValueError("limit must be greater than zero.")

    if len(text) <= limit:
        return [text]

    chunks: list[str] = []
    current = ""
    for paragraph in text.split("\n\n"):
        for piece in _split_oversized_paragraph(paragraph, limit):
            candidate = piece if not current else f"{current}\n\n{piece}"
            if len(candidate) <= limit:
                current = candidate
                continue

            if current:
                chunks.append(current)
            current = piece

    if current:
        chunks.append(current)

    return chunks


def _split_oversized_paragraph(paragraph: str, limit: int) -> list[str]:
    if len(paragraph) <= limit:
        return [paragraph]

    return [paragraph[index : index + limit] for index in range(0, len(paragraph), limit)]
