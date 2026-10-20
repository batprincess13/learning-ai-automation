# Ms. Minchin — learning prototype

Ms. Minchin is a manually invoked reviewer of an assistant's draft or plan against supplied personalization instructions and a snapshot of a ChatGPT Library skill registry. It **cannot automatically monitor ChatGPT conversations** or sync to the Library.

## Files and their roles
- `data/agent_instructions.md`: behavior and boundaries (the agent's instructions).
- `data/personalization.txt`: starter summary of preferences, **not live settings**.
- `data/skill_registry.json`: verified registry snapshot, **not the full SKILL.md files**.
- `app.py`: browser form, demonstration checks, and optional OpenAI model call.
- `tests/test_agent.py`: examples checking three basic rules.

## Run and test
Requires Python 3.10+.
```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
python -m unittest discover -s tests -v
uvicorn app:app --reload
```
Open http://127.0.0.1:8000 and try Demo. Demo uses simple rules and is **not an AI review**.

For AI review, create a private `.env` file containing OPENAI_API_KEY, and switch to AI in the form. Do not put keys in GitHub. API billing is separate from ChatGPT. This is a learning prototype with no authentication; do not deploy publicly or use for sensitive customer data.

## Next learning tasks
1. Supply current full personalization and authoritative skill files via a secure source.
2. Test AI-mode reliability on cases and counterexamples.
3. Add secure review invocation from an application that you control.
