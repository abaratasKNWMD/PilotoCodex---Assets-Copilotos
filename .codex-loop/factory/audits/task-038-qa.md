# Task 038 QA Audit - Copiloto QA General

## Scope

Audited the `qa_general` runtime contract surface for Codex, Claude, GitHub Copilot and LangChain:

- `dist/copilots/qa_general/shared/spec.json`
- `dist/copilots/qa_general/codex/AGENT.md`
- `dist/copilots/qa_general/claude/AGENT.md`
- `dist/copilots/qa_general/github-copilot/copilot-agent.md`
- `dist/copilots/qa_general/langchain/agent.py`
- Generated validator reports under `generated/`

No Git metadata is available in this workspace, so review used the current filesystem state.

## Findings

1. P2 fixed: `QaGeneralAgent.runtime_parity_contract()` exposed a reduced contract compared with `shared/spec.json#/runtimeParityContract`.
   - Evidence: `dist/copilots/qa_general/langchain/agent.py` had source/schema/runtimes/required fields/cost/drift only, but the shared contract also declares `adapterFiles`, `recommendedTraceFields`, full cost-control evidence mode and LLM escalation, and `equivalenceChecks`.
   - Risk: LangChain consumers could pass validators while losing traceability fields used by Codex, Claude and GitHub Copilot.

2. P3 fixed during verification: local Python compile/import checks created `__pycache__` release artifacts.
   - Evidence: `python tools\validate_copilot_factory.py` blocked `dist/copilots/qa_general/langchain/__pycache__` and later `dist/copilots/__pycache__`.
   - Risk: generated package would contain transient bytecode files.

## Patches Made

- Updated `dist/copilots/qa_general/langchain/agent.py` so `RUNTIME_PARITY_CONTRACT` matches the shared runtime parity contract exactly.
- Removed non-functional prose/whitespace in `agent.py` to keep prompt-cost growth within the existing validator budget.
- Removed transient `__pycache__` folders created by local smoke checks.

## Commands Executed

- `Get-Command rg -ErrorAction SilentlyContinue`
- `git status --short` -> failed because this directory is not a Git repository.
- `Get-Content` / `Select-String` inspections for target artifacts and validators.
- `python -m py_compile dist\copilots\qa_general\langchain\agent.py` -> passed; created bytecode cache that was removed.
- `python -c "... len(agent.py) ..."` -> final size `15771`.
- `python tools\validate_copilot_factory.py` -> final pass.
- `python tools\validate_prompt_quality.py` -> final pass.
- `python tools\validate_runtime_equivalence.py` -> final pass.
- Direct parity smoke with `PYTHONDONTWRITEBYTECODE=1`: `runtime_parity_contract_match= True`.
- Cache hygiene check: no `__pycache__` directories or `*.pyc` files remain under `dist/copilots`.

## Verification Evidence

- `generated/validation-report.json`: `pass=true`
- `generated/prompt-quality-report.json`: `pass=true`
- `generated/runtime-equivalence-report.json`: `pass=true`
- QA LangChain prompt budget: `15771` chars, baseline `14360`, growth `0.0983`, max `0.1`, status `pass`.
- Runtime markers checked for QA: `codex`, `claude`, `github-copilot`, `langchain`.

## Residual Risks

- The QA LangChain adapter is close to the cost-growth ceiling (`0.0983` vs `0.1`), so future additions should replace or compact existing text rather than append prompt surface.
- The manual parity fix is in the generated runtime artifact. If a future generator path rewrites `langchain/agent.py`, rerun the direct parity smoke plus the three validators before release.
