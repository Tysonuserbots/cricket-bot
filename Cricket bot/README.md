# Cricket Telegram Bot

A small Telegram bot for cricket scores. It can run immediately with demo data, then switch to live cricket data when you add a CricketData/CricAPI key.

## Features

- `/start` and `/help` with command hints.
- `/live` for current, recent, and upcoming cricket matches.
- `/live india` to filter by team or match text.
- `/score <match_id_or_team>` for one match.
- Demo provider for local Telegram testing without a cricket API key.
- CricketData/CricAPI provider using `https://api.cricapi.com/v1/currentMatches`.

## Setup

1. Create a Telegram bot with BotFather and copy the token.
2. Create a virtual environment and install dependencies:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

3. Copy `.env.example` to `.env` and set at least:

```text
TELEGRAM_BOT_TOKEN=your-telegram-token
```

4. Optional: add live cricket data:

```text
CRICAPI_KEY=your-cricketdata-api-key
CRICKET_PROVIDER=auto
```

When `CRICAPI_KEY` is absent, `CRICKET_PROVIDER=auto` uses the bundled demo data. To force demo mode, set `CRICKET_PROVIDER=demo`. To require live API mode, set `CRICKET_PROVIDER=cricapi`.

## Run

```powershell
python -m cricket_telegram_bot
```

Then open your bot in Telegram and try:

```text
/live
/live india
/score demo-1
```

## Tests

```powershell
python -m unittest discover -s tests
```

## Data Provider Notes

The CricketData/CricAPI docs describe the current matches endpoint as:

```text
https://api.cricapi.com/v1/currentMatches?apikey=[YOUR_API_KEY]&offset=0
```

That endpoint returns current matches with match details and a `score` object when score data is available.
