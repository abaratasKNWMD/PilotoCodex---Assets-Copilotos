# Task 015 Safe-Coding / Privacy Audit

Scope: local review of task 015 artifacts for `Builds Claude-facing project instructions and agent cards.`

Files reviewed:
- `dist/copilots/**/claude/AGENT.md`
- `dist/copilots/**/shared/claude_project_instructions.json`
- `generated/prompt-quality-report.json`
- `generated/prompt-quality-report.md`
- `generated/runtime-equivalence-report.json`
- `generated/runtime-equivalence-report.md`
- `generated/runtime-injection-map.json`
- `generated/test-strategy-audit-report.json`
- `generated/test-strategy-audit-report.md`
- `generated/validation-report.json`
- `generated/validation-report.md`
- `tools/validate_runtime_equivalence.py`

## Findings

### F-015-01 - Runtime map ID path validation gap

Severity: Medium

`tools/validate_runtime_equivalence.py` consumed copilot IDs from `generated/runtime-injection-map.json` and used them to build `dist/copilots/<copilot_id>/...` paths. The map was checked for coverage, but the ID itself was not required to be a safe repository path segment before filesystem reads.

Impact: a malformed future runtime map could introduce path separators or traversal-like IDs and make the validator read unexpected paths before reporting map drift.

Patch made:
- Added `SAFE_COPILOT_ID_RE` and `is_safe_copilot_id`.
- Reject unsafe copilot IDs from `generated/runtime-injection-map.json` before constructing runtime artifact paths.
- Reject unsafe IDs from `data/copilots.json` before adding them to expected coverage.
- Added the negative runtime-equivalence case `unsafe_copilot_id`.

Result after patch:
- `generated/runtime-equivalence-report.json` passes with 18 copilots checked.
- Negative case count is now 8.
- `unsafe_copilot_id` is detected by `runtime_map_copilot_id`.

### F-015-02 - Text input errors were too silent

Severity: Low

Required markdown and Python runtime files were read through `read_text`, which returned an empty string for every read failure. Downstream checks would usually fail, but the root cause could be unclear.

Patch made:
- `read_text` now reports missing text files, invalid UTF-8 and OS read errors as `text_input` issues with the relative artifact path.
- Main runtime reads and QA runtime marker checks now pass the issue collector into `read_text`.

### F-015-03 - Sensitive data scan

Severity: Info

Targeted scans found no real credential-shaped values, bearer tokens, GitHub tokens, OpenAI-style keys, local absolute user paths, `/home` paths or `/Users` paths in the reviewed task artifacts.

Patch made: none beyond F-015-01/F-015-02.

### F-015-04 - Auth, CORS, tenancy and billing applicability

Severity: Info

The increment is a local prompt/runtime-contract generation and validation surface. No web server, browser session, CORS policy, tenant datastore, payment flow or billing integration was in scope. Claude-facing artifacts declare connector names and environment variable names only; no credential values were present.

Patch made: none.

## Commands Executed

- `Get-Command rg -ErrorAction SilentlyContinue | Select-Object -ExpandProperty Source`
  - Result: local PowerShell `rg` shim found.
- `git status --short`
  - Result: failed because this workspace is not a Git repository.
- `rg --files dist/copilots generated tools .codex-loop/factory 2>$null`
  - Result: file inventory gathered; later scans used PowerShell fallback because the `rg` shim did not support normal ripgrep flags.
- `Get-ChildItem -Path dist\copilots,generated,tools -Recurse -File | Select-String ...`
  - Result: broad keyword scan found policy/test-fixture references only.
- Targeted Python scan using token-shaped and local-path regexes across the changed generated artifacts and `tools/validate_runtime_equivalence.py`.
  - Result: `secret 0`, `local_path 0`.
- JSON summary checks for `generated/runtime-injection-map.json` and `generated/runtime-equivalence-report.json`.
  - Result: Claude adapter protocol is present; runtime equivalence pass is true; data hygiene pass is true.
- `python tools\validate_copilot_factory.py`
  - Result: `Copilot factory validation PASS: 18 copilots, 50 agents, 50 tasks.`
- `python tools\validate_prompt_quality.py`
  - Result: `Prompt quality validation PASS: 18 copilots, 72 runtime prompts.`
- `python tools\validate_runtime_equivalence.py`
  - Result: `Runtime equivalence PASS: 18 copilots checked.`

## Residual Risks

- Secret detection remains pattern-based and should not be treated as full DLP.
- Because the workspace is not a Git repository, review was based on file inventory, generated reports and validator behavior rather than a Git diff.
- External connector behavior was not exercised; connector declarations must continue to be treated as capability contracts until credentials are configured outside these artifacts.

Overall result: Pass after defensive validator patch.
