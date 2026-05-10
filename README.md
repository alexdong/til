# til

Minimal Flask app for personal TIL notes.

Notes are stored as Markdown and rendered as HTML.

Inline `#tags` are extracted into note metadata, removed from rendered note text, and exposed as public filters.

## Run

```bash
uv sync
FLASK_SKIP_DOTENV=1 uv run flask --app main run --debug
```

## Publish

The private publishing URL opens the note form.

The answer gate is currently commented out in `main.py`.

## Deploy

This mirrors `/home/ubuntu/wordsmith`:

- app: `/home/ubuntu/til`
- local service: `127.0.0.1:9003`
- public hostname: `til.alexdong.com`
- tunnel: existing `alexdong` Cloudflare tunnel

Install/update:

```bash
sudo cp /home/ubuntu/til/deploy/til.service /etc/systemd/system/til.service
sudo systemctl daemon-reload
sudo systemctl enable --now til.service
sudo systemctl status til.service --no-pager
```

Cloudflare ingress should include:

```yaml
  - hostname: til.alexdong.com
    service: http://127.0.0.1:9003
```
