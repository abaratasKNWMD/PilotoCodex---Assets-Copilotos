# Task 013 Safe-Coding / Privacy Review

Scope: `Audits observability, incident playbooks and runbooks.`

Date: 2026-05-04

## Findings

1. Severity: low. The Operate validator already enforced the live contract, but its negative fixtures did not explicitly exercise privacy failures for raw-log prompt allowance, unsanitized evidence allowance or telemetry privacy text that permits raw logs. Patched in `tools/validate_copilot_factory.py`.
2. Severity: informational. No live credentials, billing data, customer records, connector activation, external network dependency or local absolute path leak was found in the reviewed task artifacts.
3. Severity: informational. Operate artifacts keep observability evidence local and metadata-based: `.codex-loop/factory/codex-runtime-incidents.md` references sanitized incident classes and relative archive pointers, not raw log bodies.
4. Severity: informational. Product auth/session, tenant isolation, CORS and billing checks are not applicable because this task changed factory Operations runbooks and validation evidence, not a SaaS product surface.

## Patches Made

- Updated `tools/validate_copilot_factory.py` so `detect_operate_fixture_issues()` now detects:
  - `rawLogPromptsAllowed` values other than `false`.
  - `sanitizedEvidenceOnly` values other than `true`.
  - telemetry privacy text that allows raw logs.
- Added Operate negative fixtures for `raw_log_prompt_allowed`, `unsanitized_evidence_allowed` and `raw_log_privacy_text`.
- Regenerated validation evidence by running the required validators after the patch.
- Updated this audit artifact with findings, severity, patches, commands and residual risks.

## Commands Executed

- `Get-Command rg -ErrorAction SilentlyContinue`
- `git status --short` -> not a Git repository; review used direct workspace inspection.
- `rg` scans for credential-shaped values, local absolute paths, raw-log references and Operate markers across `README.md`, `factory-prompt.md`, `.vscode/settings.json`, `.codex-loop/factory`, `generated` and `tools/validate_copilot_factory.py`.
- `python tools/validate_copilot_factory.py` -> PASS.
- `python tools/validate_prompt_quality.py` -> PASS.
- `python tools/validate_runtime_equivalence.py` -> PASS.

## Residual Risks

- The local factory state lock can contain local runtime metadata by design; reports should continue to reference it by relative path only.
- `.codex-loop/codex-runs/*.jsonl` remains local runtime archive material and must not be copied into prompts or release reports.
- Live telemetry backend, paging integration, product-specific auth, tenant isolation, CORS and billing controls remain out of scope until a product workspace exists.
