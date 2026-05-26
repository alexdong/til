import os
import re
import sqlite3
from datetime import UTC, datetime
from html import escape
from pathlib import Path
from urllib.parse import quote
from zoneinfo import ZoneInfo

import boto3
import markdown
from flask import Flask, g, redirect, render_template_string, request, url_for
from pydantic_ai import Agent
from pydantic_ai.models.bedrock import BedrockConverseModel
from pydantic_ai.providers.bedrock import BedrockProvider


DATA_DIR = Path(os.getenv("TIL_DATA_DIR", "."))
DB = DATA_DIR / "til.db"
LOCAL_TZ = ZoneInfo("Pacific/Auckland")
MODEL = os.getenv("BEDROCK_MODEL", "global.anthropic.claude-sonnet-4-6")
REGION = "us-east-1"
SCHEMA = """create table if not exists notes (
    id integer primary key autoincrement,
    slug text not null unique,
    title text not null default '',
    body text not null,
    tags text not null default '',
    created_at integer not null
)"""
TAG_RE = re.compile(r"(?<![\w`])#([A-Za-z][A-Za-z0-9_-]*)\b")
HTML_TAG_RE = re.compile(r"(<[^>]+>)")
DEFAULT_HUMANISE_INSTRUCTION = "Rewrite this personal TIL note into clear, natural English."
HUMANISE_PROMPT = """{instruction}

Keep the author's meaning. Preserve Markdown structure where it helps.
Do not add facts, summaries, introductions, or commentary.
Return Markdown only.

Note:
{body}"""

PAGE = """<!doctype html>
<title>til</title>
<style>
:root{color-scheme:light}
body{font:16px/1.4 Arial,Helvetica,sans-serif;margin:8px 12px;color:#000;background:#fff}
header{margin-bottom:12px}
form{margin:8px 0 12px}
textarea,input{font:inherit;box-sizing:border-box;width:100%;padding:2px 4px}
textarea{min-height:320px;display:block}
button{font:inherit;padding:2px 8px}
h1,h2{margin:0 0 12px;font-size:inherit;font-weight:bold}
a{color:#00c}
a:visited{color:#551a8b}
.muted{color:#000}
.error{color:#b00020}
.actions{display:flex;gap:8px;align-items:center}
.editor{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:16px;max-width:1160px}
.field{margin:8px 0 0}
.note{margin:0 0 16px}
.note p,.note ul,.note ol,.note pre,.note blockquote{margin:0 0 12px}
.note ul,.note ol{padding-left:20px}
.note pre{white-space:pre-wrap;overflow-x:auto}
.note code{font-family:monospace}
.note blockquote{border-left:2px solid #ccc;padding-left:10px}
.note table{border-collapse:collapse;margin:0 0 12px}
.note th,.note td{border:1px solid #ccc;padding:2px 6px;text-align:left}
.note th{font-weight:bold}
.codehilite{margin:0 0 12px}
.codehilite pre{margin:0}
.codehilite .k,.codehilite .kn,.codehilite .kd{font-weight:bold}
.codehilite .s,.codehilite .s1,.codehilite .s2{color:#070}
.codehilite .c,.codehilite .c1,.codehilite .cm{color:#666}
.codehilite .m,.codehilite .mi,.codehilite .mf{color:#164}
.codehilite .nf,.codehilite .na{color:#007}
.preview{min-height:320px}
.date{font-family:monospace}
.tags{margin:0 0 12px}
footer{margin-top:16px}
@media (max-width:800px){.editor{display:block}.preview{margin-top:12px}}
</style>
<main>
<header>
  <h1><a href="/">til</a></h1>
</header>
{% if error %}<p class="error">{{ error }}</p>{% endif %}
{% if view in ["fabiao", "edit"] %}
  <h2>{% if view == "edit" %}Edit note{% else %}New note{% endif %}</h2>
  <form method="post" action="{{ form_action }}">
    <div class="editor">
      <div>
        <textarea id="body" name="body" placeholder="paste a TIL note" autofocus>{{ body }}</textarea>
        <p class="field"><input id="tags" name="tags" placeholder="tags" value="{{ tags }}"></p>
      </div>
      <article id="preview" class="note preview"></article>
    </div>
    <p class="field"><input id="humanise-instruction" placeholder="humanise instruction"></p>
    <p class="actions"><button id="humanise" type="button">humanise</button></p>
    <p class="actions"><button type="submit">{% if view == "edit" %}save{% else %}publish{% endif %}</button></p>
  </form>
  <script>
  const body = document.getElementById("body");
  const preview = document.getElementById("preview");
  const humanise = document.getElementById("humanise");
  const humaniseInstruction = document.getElementById("humanise-instruction");
  const tags = document.getElementById("tags");
  let previewTimer;
  let tagsEdited = tags.value.trim().length > 0;
  function extractTags(value) {
    return Array.from(new Set((value.match(/(^|[^\\w`])#([A-Za-z][A-Za-z0-9_-]*)\\b/g) || [])
      .map((tag) => tag.match(/#([A-Za-z][A-Za-z0-9_-]*)\\b/)[1].toLowerCase())));
  }
  function syncTags() {
    if (!tagsEdited) tags.value = extractTags(body.value).join(", ");
  }
  async function renderPreview() {
    const res = await fetch("/preview", {
      method: "POST",
      headers: {"Content-Type": "application/x-www-form-urlencoded"},
      body: new URLSearchParams({body: body.value})
    });
    preview.innerHTML = await res.text();
  }
  body.addEventListener("input", () => {
    syncTags();
    clearTimeout(previewTimer);
    previewTimer = setTimeout(renderPreview, 120);
  });
  tags.addEventListener("input", () => {
    tagsEdited = true;
  });
  humanise.addEventListener("click", async () => {
    humanise.disabled = true;
    humanise.textContent = "humanising";
    try {
      const res = await fetch("/humanise", {
        method: "POST",
        headers: {"Content-Type": "application/x-www-form-urlencoded"},
        body: new URLSearchParams({body: body.value, instruction: humaniseInstruction.value})
      });
      if (!res.ok) throw new Error(await res.text());
      body.value = await res.text();
      syncTags();
      renderPreview();
    } catch (err) {
      alert(err.message || "Humanise failed.");
    } finally {
      humanise.disabled = false;
      humanise.textContent = "humanise";
    }
  });
  syncTags();
  renderPreview();
  </script>
{% elif note %}
  {% if note["title"] %}<h2>{{ note["title"] }}</h2>{% endif %}
  <p class="date">{{ note["date"] }}</p>
  {% if note["tags"] %}<p class="tags">{% for tag in note["tags"] %}<a href="/?tag={{ tag }}">#{{ tag }}</a>{% if not loop.last %} {% endif %}{% endfor %}</p>{% endif %}
  <article class="note">{{ note["html"]|safe }}</article>
  <p><a class="muted" href="/{{ note['slug'] }}/edit">edit</a></p>
  <script>
  document.addEventListener("keydown", (event) => {
    if (event.metaKey && event.shiftKey && event.ctrlKey && event.key.toLowerCase() === "e") {
      event.preventDefault();
      const path = location.pathname.endsWith("/") ? location.pathname.slice(0, -1) : location.pathname;
      location.href = path + "/" + "edit";
    }
  });
  </script>
{% else %}
  <p><a class="muted" href="/fabiao">publish</a></p>
  {% if active_tag %}<p>Tag: <a href="/?tag={{ active_tag }}">#{{ active_tag }}</a> <a class="muted" href="/">all</a></p>{% endif %}
  {% if notes %}
    {% for note in notes %}
      <p><span class="date">{{ note["date"] }}</span>: <a href="/{{ note['slug'] }}">{{ note["title"] or note["preview"] }}</a>{% if note["tags"] %} <span class="tags">{% for tag in note["tags"] %}<a href="/?tag={{ tag }}">#{{ tag }}</a>{% if not loop.last %} {% endif %}{% endfor %}</span>{% endif %}</p>
    {% endfor %}
  {% else %}
    <p>No notes yet.</p>
  {% endif %}
{% endif %}
</main>"""


app = Flask(__name__)
app.secret_key = os.getenv("TIL_SECRET_KEY", "dev-only-change-me")
bedrock_client = boto3.client(
    "bedrock-runtime",
    region_name=REGION,
    aws_access_key_id=os.getenv("AWS_BEDROCK_ACCESS_KEY_ID") or os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_BEDROCK_SECRET_ACCESS_KEY") or os.getenv("AWS_SECRET_ACCESS_KEY"),
)
provider = BedrockProvider(bedrock_client=bedrock_client)
agent = Agent(BedrockConverseModel(MODEL, provider=provider), system_prompt="You polish personal notes into concise, natural English.")


def init_db():
    DB.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(DB) as db:
        db.execute(SCHEMA)
        columns = {row[1] for row in db.execute("pragma table_info(notes)")}
        if "title" not in columns:
            db.execute("alter table notes add column title text not null default ''")
        if "tags" not in columns:
            db.execute("alter table notes add column tags text not null default ''")


def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(DB)
        g.db.row_factory = sqlite3.Row
        g.db.execute(SCHEMA)
    return g.db


@app.teardown_appcontext
def close_db(_):
    if db := g.pop("db", None):
        db.close()


# def expected_answer():
#     return datetime.now(LOCAL_TZ).strftime("%Y%m%d") + "11"


def note_date(created_at):
    return datetime.fromtimestamp(created_at, LOCAL_TZ).strftime("%Y-%m-%d")


def make_slug(body, created_at):
    stem = re.sub(r"[^a-z0-9]+", "-", body.strip().splitlines()[0][:48].casefold()).strip("-") or "note"
    day = datetime.fromtimestamp(created_at, LOCAL_TZ).strftime("%Y%m%d")
    slug = f"{day}-{stem}"
    exists = get_db().execute("select 1 from notes where slug = ?", (slug,)).fetchone()
    if not exists:
        return slug
    suffix = 2
    while True:
        candidate = f"{slug}-{suffix}"
        exists = get_db().execute("select 1 from notes where slug = ?", (candidate,)).fetchone()
        if not exists:
            return candidate
        suffix += 1


def preview(body):
    text = re.sub(r"\s+", " ", body).strip()
    return text[:80] + ("..." if len(text) > 80 else "")


def normalize_tags(value):
    seen = set()
    tags = []
    for tag in re.split(r"[\s,]+", value.strip()):
        tag = tag.removeprefix("#").strip().casefold()
        tag = re.sub(r"[^a-z0-9_-]+", "", tag)
        if tag and tag not in seen:
            tags.append(tag)
            seen.add(tag)
    return tags


def extract_tags(body):
    return normalize_tags(" ".join(match.group(1) for match in TAG_RE.finditer(body)))


def strip_tags(body):
    lines = []
    for line in body.splitlines():
        stripped = TAG_RE.sub("", line)
        stripped = re.sub(r"[ \t]{2,}", " ", stripped).rstrip()
        if stripped.strip():
            lines.append(stripped)
        elif line.strip():
            continue
        else:
            lines.append("")
    return "\n".join(lines).strip()


def clean_title(line):
    title = TAG_RE.sub("", line).strip()
    title = re.sub(r"^#{1,6}\s+", "", title).strip()
    title = re.sub(r"[*_`~]+", "", title).strip()
    return re.sub(r"\s+", " ", title)


def split_title(body):
    lines = body.strip().splitlines()
    if not lines:
        return "", ""
    title = clean_title(lines[0])
    return title, "\n".join(lines[1:]).strip()


def prepare_note(body, tags):
    body_tags = extract_tags(body)
    title, body = split_title(body)
    field_tags = normalize_tags(tags)
    merged_tags = normalize_tags(" ".join([*field_tags, *body_tags]))
    return title, strip_tags(body), merged_tags


def linkify_hashtags(html):
    parts = HTML_TAG_RE.split(html)
    for i, part in enumerate(parts):
        if part.startswith("<") and part.endswith(">"):
            continue
        parts[i] = TAG_RE.sub(lambda match: f'<a href="/?tag={quote(match.group(1).casefold())}">#{escape(match.group(1))}</a>', part)
    return "".join(parts)


def render_markdown(body):
    html = markdown.markdown(
        body,
        extensions=["extra", "sane_lists", "tables", "fenced_code", "codehilite"],
        extension_configs={"codehilite": {"guess_lang": False, "use_pygments": True}},
        output_format="html",
    )
    return linkify_hashtags(html)


def row_to_note(row):
    return {
        "slug": row["slug"],
        "title": row["title"] if "title" in row.keys() else "",
        "body": row["body"],
        "html": render_markdown(row["body"]),
        "tags": normalize_tags(row["tags"]),
        "date": note_date(row["created_at"]),
        "preview": preview(row["body"]),
    }


def fetch_note(slug):
    return get_db().execute("select * from notes where slug = ?", (slug,)).fetchone()


@app.route("/")
def index():
    active_tag = normalize_tags(request.args.get("tag", ""))
    if active_tag:
        rows = get_db().execute(
            "select * from notes where instr(' ' || tags || ' ', ?) > 0 order by created_at desc, id desc",
            (f" {active_tag[0]} ",),
        ).fetchall()
    else:
        rows = get_db().execute("select * from notes order by created_at desc, id desc").fetchall()
    notes = [row_to_note(row) for row in rows]
    return render_template_string(PAGE, notes=notes, note=None, view="index", error=None, active_tag=active_tag[0] if active_tag else None)


@app.route("/fabiao", methods=["GET", "POST"])
def fabiao():
    error = None
    body = ""
    tags = ""
    # authed = session.get("publish_ok") is True
    # if request.method == "POST" and not authed:
    #     if request.form.get("answer", "").strip() == expected_answer():
    #         session["publish_ok"] = True
    #         return redirect(url_for("fabiao"))
    #     error = "Wrong number."
    if request.method == "POST":
        body = request.form.get("body", "").strip()
        tags = request.form.get("tags", "").strip()
        if body:
            title, body, note_tags = prepare_note(body, tags)
            if not title:
                error = "Paste a note first."
                return render_template_string(PAGE, view="fabiao", form_action=url_for("fabiao"), body=request.form.get("body", "").strip(), tags=tags, error=error, note=None)
            created_at = int(datetime.now(UTC).timestamp())
            slug = make_slug(title, created_at)
            get_db().execute(
                "insert into notes (slug, title, body, tags, created_at) values (?, ?, ?, ?, ?)",
                (slug, title, body, " ".join(note_tags), created_at),
            )
            get_db().commit()
            return redirect(url_for("show_note", slug=slug))
        error = "Paste a note first."
    return render_template_string(PAGE, view="fabiao", form_action=url_for("fabiao"), body=body, tags=tags, error=error, note=None)


@app.route("/<slug>/edit", methods=["GET", "POST"])
def edit_note(slug):
    row = fetch_note(slug)
    if not row:
        return redirect(url_for("index"))
    error = None
    body = "\n\n".join(part for part in [row["title"], row["body"]] if part)
    tags = ", ".join(normalize_tags(row["tags"]))
    if request.method == "POST":
        body = request.form.get("body", "").strip()
        tags = request.form.get("tags", "").strip()
        if body:
            title, body, note_tags = prepare_note(body, tags)
            if title:
                get_db().execute(
                    "update notes set title = ?, body = ?, tags = ? where slug = ?",
                    (title, body, " ".join(note_tags), slug),
                )
                get_db().commit()
                return redirect(url_for("show_note", slug=slug))
        error = "Paste a note first."
    return render_template_string(PAGE, view="edit", form_action=url_for("edit_note", slug=slug), body=body, tags=tags, error=error, note=None)


@app.post("/preview")
def markdown_preview():
    title, body, _ = prepare_note(request.form.get("body", ""), "")
    html = f"<h2>{escape(title)}</h2>" if title else ""
    return html + render_markdown(body)


@app.post("/humanise")
def humanise_note():
    body = request.form.get("body", "").strip()
    instruction = request.form.get("instruction", "").strip() or DEFAULT_HUMANISE_INSTRUCTION
    if not body:
        return "Paste a note first.", 400
    try:
        return agent.run_sync(HUMANISE_PROMPT.format(instruction=instruction, body=body)).output
    except Exception as exc:
        app.logger.exception("humanise failed")
        return str(exc), 500


@app.route("/<slug>")
def show_note(slug):
    row = fetch_note(slug)
    if not row:
        return redirect(url_for("index"))
    return render_template_string(PAGE, note=row_to_note(row), notes=None, view="note", error=None)


init_db()
