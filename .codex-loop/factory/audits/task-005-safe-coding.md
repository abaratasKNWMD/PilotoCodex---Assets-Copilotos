# Task 005 Safe-Coding / Privacy Review

Scope: Architecture Board increment for `Audits principles, ADRs and technical decision quality.`

## Findings

- Severity: Medium. `dist/copilots/aida_architecture/langchain/agent.py` accepted raw `request` values and included the evidence object in `render_prompt()`. That could leak user-provided sensitive values or oversized local evidence into an LLM payload.
- Severity: Low. The factory validator did not prove the Architecture LangChain adapter rejected empty requests or redacted prompt-bound sensitive request text.
- Informational. No high-confidence secrets, bearer values, GitHub token values or local absolute user paths were found in the scoped release artifacts after patching. Declared env var names such as `GITHUB_TOKEN` remain capability placeholders, not credential values.

## Patches Made

- `dist/copilots/aida_architecture/langchain/agent.py`
  - Added compact request validation for non-empty strings capped at 2000 chars.
  - Redacts prompt-bound secret-like request fragments before building the user payload.
  - Stops sending raw evidence values through `render_prompt()`; the prompt receives only whether evidence was provided, while deterministic audit logic still checks required evidence locally.
  - Keeps Architecture Board evidence blocking in Python before any LLM escalation.

- `tools/validate_copilot_factory.py`
  - Added behavior checks for empty-request rejection and prompt redaction.
  - Added the new checks to `generated/validation-report.md` output.

- Generated reports refreshed by validators:
  - `generated/validation-report.json`
  - `generated/validation-report.md`
  - `generated/prompt-quality-report.json`
  - `generated/prompt-quality-report.md`
  - `generated/runtime-equivalence-report.json`
  - `generated/runtime-equivalence-report.md`

## Commands Executed

- `Get-Command rg -ErrorAction SilentlyContinue | Select-Object -ExpandProperty Source` -> found local shim.
- `git status --short` -> failed because this workspace is not a Git repository.
- `Get-ChildItem -Force` -> workspace inventory.
- `Select-String` scoped secret/path scans over task artifacts and `dist/copilots/aida_architecture` -> no final matches.
- `python tools\validate_copilot_factory.py` -> PASS.
- `python tools\semantic_router.py python ci routing` -> PASS; top routes include `python` and `cicd` with runtime traces.
- `python tools\semantic_router.py architecture adr principles` -> PASS; top route is `aida_architecture` with `architecture_decision_audit.source_of_truth`.
- `python tools\validate_prompt_quality.py` -> initially failed while the hardening patch was too large; after compacting, PASS.
- `python tools\validate_runtime_equivalence.py` -> PASS.

## Residual Risks

- No auth, session, CORS, tenant isolation or billing surface is present in this local factory increment.
- `render_prompt()` now avoids raw evidence values for privacy and cost control. A future runtime that needs evidence excerpts should pass a separate reviewed, size-limited evidence bundle rather than reintroducing raw evidence into the prompt payload.
- The workspace has no Git metadata, so review is file-based and validator/report based rather than diff-based.
