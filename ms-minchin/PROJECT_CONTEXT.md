# Ms. Minchin — Project Context
Last verified: 2026-10-31
Status: Development prototype; no verified ChatGPT integration.

## Purpose
Independent AI supervisory agent evaluating reliability, critical reasoning, instruction adherence, conversation continuity, and execution of the primary ChatGPT assistant. Detect substantive failures, explain evidence, and recommend corrective actions. The primary assistant remains responsible for completing user work.

## Scope and decisions
- Preserve the user's existing ChatGPT workflow, context, and memories.
- Favor manually invoked checkpoints using supplied verbatim transcript segments over automatic continuous monitoring.
- Evaluate the next claim independently even following an apology or correction; do not mistake agreement or admissions for improved behavior.
- Distinguish intended topic shifts from genuine drift; avoid false positives.
- Proposed integration: private MCP app/tool, potentially `review_transcript`; not implemented or verified.
- The intended workflow is transcript review with actionable findings returned to the primary assistant; current code only reviews one supplied task plus one assistant response.

## Verified repository state
- Repo: `batprincess13/learning-ai-automation`; branch: `feature/ms-minchin-agent`; project directory: `ms-minchin/`.
- `app.py`: FastAPI browser form with demo heuristics and optional OpenAI API mode.
- `data/agent_instructions.md`: current narrow alignment-review instructions.
- `data/personalization.txt`: explicitly unsynchronized starter summary.
- `data/skill_registry.json`: explicitly unsynchronized 2026-10-20 skill snapshot.
- `tests/test_agent.py`: three unittest cases; runtime execution unverified.
- `requirements.txt`: Python dependencies.
- `README.md`: learning-prototype description and local setup commands.
- No authentication in prototype; do not expose publicly or use sensitive client data.

## Gaps and uncertainties
- Actual API-mode execution, tests, deployment and end-to-end behavior remain unverified.
- No authenticated MCP bridge, conversation integration, or live synchronization.
- Separate Library `/Ms Minchin/` folder appears empty; a Library `README.txt` describes the broader long-term project. Do not duplicate authoritative continuity there.
- Project's source of truth for implementation and continuity is this repository subdirectory.

## Resume point
1. Retain the existing functioning prototype and all application code.
2. Define a secure transcript checkpoint input/output contract and evaluation cases before designing MCP connection.
3. Test existing demo and AI review modes, including false-positive counterexamples and post-correction uncritical-agreement scenarios.
4. Evaluate integration security and explicit invocation. No automatic access to unrelated conversations may be assumed.
5. Record coding, testing, integration, and deployment states separately.
