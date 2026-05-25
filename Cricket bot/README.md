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

## Deploy on Render

The bot polls Telegram, so the clean production option is a Render Background Worker. If you want to use Render's free plan, deploy it as a Web Service. This repo includes a small health server that listens on Render's `PORT`, so the Web Service can start successfully while the bot keeps polling Telegram.

### Option A: Free Render Web Service

1. Push this project to GitHub.
2. In Render, choose **New** then **Web Service**.
3. Connect the GitHub repo.
4. Use these settings:

```text
Runtime: Python
Build Command: pip install -r requirements.txt
Start Command: python -m cricket_telegram_bot
Instance Type: Free
```

5. Add environment variables in Render:

```text
TELEGRAM_BOT_TOKEN=your-telegram-token
CRICKET_PROVIDER=demo
```

6. Optional live cricket data:

```text
CRICAPI_KEY=your-cricketdata-api-key
CRICKET_PROVIDER=auto
```

Do not add your token to GitHub. Add it only in Render's environment variable settings.

Free Render Web Services can spin down after 15 minutes without inbound HTTP traffic. If that happens, the bot may stop answering until the service wakes again. For an always-on bot, use a paid instance or a Background Worker.

### Option B: Render Blueprint

This repo also includes `render.yaml`. In Render, choose **New** then **Blueprint**, connect the repo, and Render will read the build/start settings. You still need to enter `TELEGRAM_BOT_TOKEN` as an environment variable/secret.

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
