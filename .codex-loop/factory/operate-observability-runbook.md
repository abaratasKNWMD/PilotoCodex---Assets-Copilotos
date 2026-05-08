# Operate Observability Runbook

Policy version: `operate-observability-incident-runbook-audit-1.0`

Owner: `factory_agent_13_operate`

Mission: `Audits observability, incident playbooks and runbooks.`

## Signal Contract

| Signal | Source | Gate |
|---|---|---|
| state_lock_heartbeat | `.codex-loop/run.lock.json` | Lock fields are present, workspace matches and heartbeat order is valid. |
| validation_gate_reports | `generated/validation-report.json` | Factory validation passes and includes `operateAuditor.pass=true`. |
| prompt_quality_gate | `generated/prompt-quality-report.json` | Prompt quality passes without secret or local-path findings. |
| runtime_equivalence_gate | `generated/runtime-equivalence-report.json` | Runtime drift remains at max unexplained drift 0. |
| runtime_incident_summary | `.codex-loop/factory/codex-runtime-incidents.md` | Only sanitized incident classes and remediation pointers are used. |

## Incident Playbooks

### state-lock-stale

Trigger: state lock is missing, belongs to another workspace, has timestamp inversion or has an old heartbeat.

Response:

1. Pause new factory starts in this workspace.
2. Inspect `.codex-loop/run.lock.json` and current worker ownership.
3. Create a rollback snapshot before touching declared files.
4. Run `python tools/validate_copilot_factory.py`.

### validation-report-regression

Trigger: `generated/validation-report.json` or `generated/prompt-quality-report.json` reports `pass=false`.

Response:

1. Read the failing report issue list first.
2. Scope the fix to declared files or documented factory roots.
3. Re-run the validation command that produced the regression.
4. Record residual risk if a non-product gate is intentionally not applicable.

### runtime-equivalence-drift

Trigger: Codex, Claude, GitHub Copilot or LangChain diverges from the shared spec or trace map.

Response:

1. Treat `dist/copilots/<copilot>/shared/spec.json` as canonical.
2. Repair all runtime adapters or record explicit unsupported drift.
3. Run `python tools/validate_runtime_equivalence.py`.
4. Keep `generated/runtime-injection-map.json` as trace evidence.

### observability-signal-gap

Trigger: a required telemetry signal source is missing or no longer resolves to an artifact.

Response:

1. Confirm whether the signal is local factory evidence or product-specific evidence.
2. Restore the local source or mark product-specific evidence as residual risk.
3. Update the contract and scorecard in the same patch.
4. Run `python tools/validate_copilot_factory.py`.

### privacy-log-exposure

Trigger: a report, runbook or prompt includes raw logs, credentials, local personal paths or customer data.

Response:

1. Stop propagation of the affected artifact.
2. Replace raw values with placeholders or sanitized evidence references.
3. Run `python tools/validate_prompt_quality.py`.
4. Keep only local defensive engineering context in follow-up notes.

## Review Gate

Before closing an Operate task, confirm:

1. Owner review: contract and scorecard agree with `data/agent_roster.json`.
2. QA review: the two required validators pass.
3. Safe-coding/privacy review: no raw logs, credentials, personal paths or customer data were introduced.
4. Release review: no product build, browser or packaging claim is made without product-specific evidence.
