from __future__ import annotations

import logging

from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

from .config import Settings, load_settings
from .formatting import format_match, format_match_list, split_message
from .health import start_health_server_from_env
from .providers import CricketApiError, CricketProvider, build_provider

LOGGER = logging.getLogger(__name__)

HELP_TEXT = """Cricket bot commands:

/live - Show latest live, recent, and upcoming matches.
/live india - Filter matches by a team or word.
/score demo-1 - Show one match by ID.
/score india - Search for the first matching team or match.
/help - Show this help message."""


def create_application(settings: Settings) -> Application:
    provider = build_provider(settings.cricket_provider, settings.cricapi_key)
    application = Application.builder().token(settings.telegram_bot_token).build()
    application.bot_data["cricket_provider"] = provider

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("live", live_command))
    application.add_handler(CommandHandler("score", score_command))

    return application


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await _reply(update, "Ready for cricket.\n\n" + HELP_TEXT)


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await _reply(update, HELP_TEXT)


async def live_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = " ".join(context.args).strip().lower()

    try:
        matches = await _provider(context).current_matches()
    except CricketApiError as exc:
        LOGGER.warning("Cricket API error: %s", exc)
        await _reply(update, f"I could not fetch cricket scores right now.\n\n{exc}")
        return

    if query:
        matches = [match for match in matches if query in match.searchable_text()]

    text = format_match_list(matches)
    await _reply_long(update, text)


async def score_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = " ".join(context.args).strip().lower()
    if not query:
        await _reply(update, "Send a match ID or team name. Example: /score demo-1")
        return

    try:
        matches = await _provider(context).current_matches()
    except CricketApiError as exc:
        LOGGER.warning("Cricket API error: %s", exc)
        await _reply(update, f"I could not fetch cricket scores right now.\n\n{exc}")
        return

    exact = next((match for match in matches if match.match_id.lower() == query), None)
    fuzzy = next((match for match in matches if query in match.searchable_text()), None)
    match = exact or fuzzy

    if not match:
        await _reply(update, "No match found. Try /live to see available match IDs.")
        return

    await _reply(update, format_match(match))


def main() -> None:
    logging.basicConfig(
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
        level=logging.INFO,
    )
    settings = load_settings()
    start_health_server_from_env()
    application = create_application(settings)
    application.run_polling(allowed_updates=Update.ALL_TYPES)


def _provider(context: ContextTypes.DEFAULT_TYPE) -> CricketProvider:
    return context.application.bot_data["cricket_provider"]


async def _reply(update: Update, text: str) -> None:
    if update.effective_message:
        await update.effective_message.reply_text(text)


async def _reply_long(update: Update, text: str) -> None:
    for chunk in split_message(text):
        await _reply(update, chunk)
