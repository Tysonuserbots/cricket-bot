import unittest

from cricket_telegram_bot.formatting import format_match, format_match_list, split_message
from cricket_telegram_bot.models import InningsScore, Match
from cricket_telegram_bot.providers import parse_cricapi_match


class FormattingTests(unittest.TestCase):
    def test_format_match_includes_scores_and_id(self) -> None:
        match = Match(
            match_id="abc-123",
            name="India vs Australia",
            status="India need 42 runs",
            venue="Mumbai",
            match_type="odi",
            scores=(InningsScore("India Inning 1", runs=230, wickets=5, overs="45"),),
        )

        output = format_match(match)

        self.assertIn("India vs Australia", output)
        self.assertIn("India Inning 1: 230/5 (45 ov)", output)
        self.assertIn("ID: abc-123", output)

    def test_format_match_list_handles_empty_results(self) -> None:
        self.assertEqual(format_match_list([]), "No matching cricket fixtures found.")

    def test_parse_cricapi_match_accepts_common_payload_shape(self) -> None:
        raw = {
            "id": "match-1",
            "name": "Team A vs Team B",
            "matchType": "t20",
            "status": "Team A won by 5 runs",
            "venue": "Example Ground",
            "teamInfo": [{"name": "Team A", "shortname": "A"}, {"name": "Team B", "shortname": "B"}],
            "score": [{"r": 170, "w": 6, "o": 20, "inning": "Team A Inning 1"}],
        }

        match = parse_cricapi_match(raw)

        self.assertEqual(match.match_id, "match-1")
        self.assertEqual(match.teams, ("A", "B"))
        self.assertEqual(match.scores[0].runs, 170)
        self.assertEqual(match.scores[0].overs, "20")

    def test_parse_cricapi_match_handles_null_lists(self) -> None:
        match = parse_cricapi_match({"id": "match-2", "teamInfo": None, "score": None})

        self.assertEqual(match.match_id, "match-2")
        self.assertEqual(match.teams, ())
        self.assertEqual(match.scores, ())

    def test_split_message_keeps_short_text_as_one_chunk(self) -> None:
        self.assertEqual(split_message("short text", limit=20), ["short text"])

    def test_split_message_chunks_oversized_paragraph(self) -> None:
        chunks = split_message("x" * 25, limit=10)

        self.assertEqual(chunks, ["x" * 10, "x" * 10, "x" * 5])


if __name__ == "__main__":
    unittest.main()
