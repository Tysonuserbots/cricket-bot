# Render Deploy Checklist

Copy these files and folders into the **root** of your GitHub repo on the `main` branch:

```text
cricket_telegram_bot/
tests/
.env.example
.gitignore
.python-version
DEPLOY_RENDER.md
main.py
Procfile
README.md
render.yaml
requirements.txt
```

The important part: `requirements.txt`, `main.py`, and `render.yaml` must be in the top level of the repo, not inside another folder.

## Render Settings

Create a Render **Web Service** from your GitHub repo.

```text
Branch: main
Root Directory: leave blank
Build Command: pip install -r requirements.txt
Start Command: python main.py
```

## Render Environment Variables

Add these in Render under **Environment**:

```text
TELEGRAM_BOT_TOKEN=your-real-token-from-BotFather
CRICKET_PROVIDER=demo
```

Do not put the real token in GitHub.

Optional live cricket scores:

```text
CRICAPI_KEY=your-cricketdata-api-key
CRICKET_PROVIDER=auto
```

## Common Error

If Render says:

```text
Could not open requirements file: No such file or directory: 'requirements.txt'
```

then either:

- `requirements.txt` is not in the GitHub repo root, or
- Render's **Root Directory** is pointing at the wrong folder.

Fix it by moving `requirements.txt` to the repo root or by clearing the Root Directory field in Render.

