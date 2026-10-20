"""Ms. Minchin: manually invoked alignment review prototype."""
import json
import os
import re
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse, PlainTextResponse

ROOT = Path(__file__).parent
load_dotenv(ROOT / ".env")
app = FastAPI(title="Ms. Minchin")


def read_sources():
    return (
        (ROOT / "data/agent_instructions.md").read_text(encoding="utf-8"),
        (ROOT / "data/personalization.txt").read_text(encoding="utf-8"),
        json.loads((ROOT / "data/skill_registry.json").read_text(encoding="utf-8")),
    )


def demo_review(task: str, response: str, registry: dict) -> str:
    """Demonstration rules only; this is NOT the AI mode."""
    concerns = []
    task_l = task.lower()
    response_l = response.lower()
    if (re.search(r"\b(rewrite|revise|correct|edit|update)\b", task_l)
            and re.search(r"\b(only the (changed|edited) (part|section)|replace this paragraph|just the excerpt)\b", response_l)
            and not re.search(r"\b(only|just) (the )?(excerpt|section|part)\b", task_l)):
        concerns.append(("Partial revision supplied", "Full revised deliverable requirement",
                         "Return the entire revised artifact unless explicitly asked for an excerpt."))
    for skill in registry["skills"]:
        if any(re.search(r"(?<!\w)" + re.escape(trigger.lower()) + r"(?!\w)", task_l)
               for trigger in skill["triggers"]):
            concerns.append(("Explicit skill trigger found",
                             skill["name"] + ": " + skill["path"],
                             "Retrieve and apply the authoritative skill file if the trigger is an instruction."))
    if not concerns:
        return "NO_INTERVENTION\n\n(Demo mode only checks limited rules; no AI assessment.)"
    return "\n\n".join(
        f"Ms. Minchin\nIssue: {issue}\nApplicable instruction/skill: {source}\nRequired correction: {fix}"
        for issue, source, fix in concerns
    )


def review(task: str, response: str, mode: str) -> str:
    instructions, personalization, registry = read_sources()
    if mode == "demo":
        return demo_review(task, response, registry)
    if not os.getenv("OPENAI_API_KEY"):
        return "AI mode needs an OPENAI_API_KEY in the private .env file."
    from openai import OpenAI
    client = OpenAI()
    prompt = ("PERSONALIZATION (local snapshot):\n" + personalization
              + "\nSKILL ROUTING (snapshot, not full files):\n" + json.dumps(registry)
              + "\nORIGINAL TASK:\n" + task
              + "\nASSISTANT RESPONSE OR PLAN:\n" + response)
    result = client.responses.create(
        model=os.getenv("OPENAI_MODEL", "gpt-4.1-mini"),
        instructions=instructions,
        input=prompt,
    )
    return result.output_text


PAGE = """<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Ms. Minchin</title><style>
body{font:16px system-ui;max-width:760px;margin:36px auto;padding:0 18px;background:#1d1d20;color:#eee}
h1{color:#efc9d5}textarea,select{width:100%;box-sizing:border-box;background:#29282c;color:#fff;
border:1px solid #5a555d;border-radius:8px;padding:12px}textarea{height:115px}
label{display:block;margin:16px 0 7px}button{margin-top:18px;background:#eac0ce;color:#242126;
border:none;border-radius:8px;padding:12px 20px;font-weight:bold}
small{color:#c6c0c5}</style></head><body><h1>Ms. Minchin</h1>
<p>Personalization &amp; Library skill alignment reviewer</p>
<small>Manually invoked only. No access to other ChatGPT chats or live Library contents.</small>
<form action="/review" method="post"><label>Original task</label><textarea name="task" required></textarea>
<label>Assistant response or proposed action</label><textarea name="response" required></textarea>
<label>Mode</label><select name="mode"><option value="demo">Demo (no key)</option>
<option value="ai">AI review (API key required)</option></select>
<button type="submit">Review</button></form></body></html>"""


@app.get("/", response_class=HTMLResponse)
def home():
    return PAGE


@app.post("/review", response_class=PlainTextResponse)
def submit(task: str = Form(...), response: str = Form(...), mode: str = Form("demo")):
    if mode not in ("demo", "ai"):
        return "Invalid mode."
    try:
        return review(task[:20000], response[:20000], mode)
    except Exception as exc:
        return "Review failed (" + type(exc).__name__ + "). Check private server logs."
