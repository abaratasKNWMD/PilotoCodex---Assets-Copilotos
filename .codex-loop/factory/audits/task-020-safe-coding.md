# Safe Coding / Privacy Audit - Task 020

Task: `[P1][factory_agent_20_cost] Routes cheap deterministic work to Python and expensive judgement to LLMs.`

Scope reviewed:

- `README.md`
- `factory-prompt.md`
- `.vscode/settings.json`
- `.codex-loop/factory/cost-routing-contract.json`
- `.codex-loop/factory/cost-routing-scorecard.json`
- `.codex-loop/factory/cost-routing-policy.md`
- `tools/validate_copilot_factory.py`
- generated validation, prompt quality, runtime equivalence, documentation and test strategy reports

## Findings

- Severity: Low. The Cost Routing contract already set `rawLogPromptsAllowed=false`, and `.vscode/settings.json` already had `codexLoop.rawLogPromptsAllowed=false`, but the Cost Routing auditor did not require that VS Code setting as part of its own required settings list. This was a traceability and privacy-hardening gap: a future config drift could allow raw-log prompts without failing the Cost Routing gate.
- Severity: Informational. Secret-pattern scan found only synthetic negative-test placeholders and redaction fixture variable names in `tools/validate_copilot_factory.py`. No live token, API key, password, billing credential, customer identifier, tenant secret or local absolute path was found in the audited artifacts.
- Severity: Informational. Auth, session, CORS, tenant isolation and billing flows are not runtime surfaces for this task. Billing-related terms are policy placeholders only; no real billing integration or credential was introduced.

## Patches Made

- Added `codexLoop.rawLogPromptsAllowed` to `COST_REQUIRED_SETTINGS` in `tools/validate_copilot_factory.py`.
- Added an executable expectation that `.vscode/settings.json` keeps `codexLoop.rawLogPromptsAllowed=false`.
- Added `codexLoop.rawLogPromptsAllowed` to `.codex-loop/factory/cost-routing-contract.json` validation required settings.
- Added `raw_log_prompts_blocked_setting` to `.codex-loop/factory/cost-routing-scorecard.json`.
- Updated `README.md` and `factory-prompt.md` so operators see that raw-log prompt blocking is part of the Cost Routing gate, not only descriptive policy text.
- Regenerated validation artifacts through the requested validators.

## Commands Executed

- `Get-Command rg -ErrorAction SilentlyContinue` - confirmed `rg` is available.
- `git status --short` - failed because this workspace is not a Git repository.
- `Get-ChildItem -Force` - inspected workspace root.
- `rg` secret/privacy scans over the task files and generated reports - only synthetic placeholders were detected.
- `Get-Content` reads for the cost-routing contract, scorecard, policy, settings, README, factory prompt and validator sections.
- `python tools/validate_copilot_factory.py` - pass: 18 copilots, 50 agents, 50 tasks.
- `python tools/validate_prompt_quality.py` - pass: 18 copilots, 72 runtime prompts.
- `rg` post-patch checks for `rawLogPromptsAllowed` and `raw_log_prompts_blocked_setting` - confirmed the gate is present in contract, scorecard, validator and generated validation report.

## Residual Risks

- The workspace has no Git metadata, so change attribution is based on file inspection and generated reports rather than a VCS diff.
- The audit is limited to local product-engineering artifacts in `NuevoProyecto`; no external connector or live runtime was exercised.
- LLM judgement quality remains an accepted operational risk, mitigated by Python-first gates, trace-required judgement work and the raw-log prompt block enforced here.
