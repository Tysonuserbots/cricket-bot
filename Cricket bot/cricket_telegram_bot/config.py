from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    telegram_bot_token: str
    cricapi_key: str | None
    cricket_provider: str


def load_settings() -> Settings:
    _load_dotenv()

    token = os.getenv("TELEGRAM_BOT_TOKEN", "").strip()
    if not token:
        raise RuntimeError("TELEGRAM_BOT_TOKEN is required. Create one with BotFather and add it to .env.")

    provider = os.getenv("CRICKET_PROVIDER", "auto").strip().lower() or "auto"
    if provider not in {"auto", "cricapi", "demo"}:
        raise RuntimeError("CRICKET_PROVIDER must be one of: auto, cricapi, demo.")

    return Settings(
        telegram_bot_token=token,
        cricapi_key=os.getenv("CRICAPI_KEY", "").strip() or None,
        cricket_provider=provider,
    )


def _load_dotenv() -> None:
    try:
        from dotenv import load_dotenv
    except ImportError:
        return

    load_dotenv()

