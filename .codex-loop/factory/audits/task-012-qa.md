# Task 012 QA Audit

Scope: `Audits package readiness, scorecards and exit criteria.`

Date: 2026-05-04

## Findings

- Fixed: release runtime traces used `generated/factory-audit.json#/releaseAudit/scorecards/<copilot_id>` as `scorecardRef`, but `scorecards` is an array. That JSON Pointer did not resolve to a scorecard, so traceability could pass syntactic checks while pointing to no concrete scorecard.
- Confirmed: this increment is metadata and release-governance only. No web, desktop, SEO, form, loading, or error-state product flow is claimed by the artifacts; the release audit keeps those criteria as residual-risk/not-applicable until product evidence exists.
- Confirmed: runtime parity remains Codex, Claude, GitHub Copilot and LangChain with deterministic Python-first validation and no new credential, billing, customer-data, or connector activation surface.

## Patches Made

- `factory.config.json`: added `scorecardIndex` under `controlRoom.releaseTruthGate.releaseReadinessAudit`.
- `generated/factory-audit.json`: added `releaseAudit.scorecardIndex`, added `releaseAudit.scorecardsByCopilot`, and added per-copilot scorecard evidence refs.
- `generated/runtime-injection-map.json`: updated every release `scorecardRef` to the by-copilot scorecard index.
- `tools/validate_copilot_factory.py`: now requires `scorecardIndex`, verifies `scorecardsByCopilot` equality with the ordered scorecard list, verifies runtime scorecard refs resolve, and adds a `missing_scorecard_index` negative fixture.
- `generated/validation-report.json` / `.md`, `generated/prompt-quality-report.json` / `.md`, and `generated/runtime-equivalence-report.json` / `.md`: refreshed by validators.

## Commands Executed

- `Get-Command rg -ErrorAction SilentlyContinue`
- `git status --short` -> failed because this workspace is not a git repository.
- `python -m py_compile tools\validate_copilot_factory.py` -> created local bytecode cache; subsequent validator caught it.
- `python tools/validate_copilot_factory.py` -> first run failed only on `tools/__pycache__` created by `py_compile`.
- Removed the generated `tools/__pycache__` after resolving the path inside the workspace.
- `python tools/validate_copilot_factory.py` -> PASS.
- `python tools/validate_prompt_quality.py` -> PASS.
- `python tools/validate_runtime_equivalence.py` -> PASS.
- `python tools/validate_copilot_factory.py && python tools/validate_prompt_quality.py && python tools/validate_runtime_equivalence.py` -> PASS.

## Residual Risks

- No product build, browser render, SEO artifact, or desktop executable is claimed by this task. External release remains blocked until product-specific evidence is attached under `products/<slug>/` and registry evidence is updated.
- `tools/run_factory.py` was inspected but not executed because the required DoD verifier for this task is the three-command validation chain above; a full regeneration would touch broader generated surfaces outside this QA patch.
