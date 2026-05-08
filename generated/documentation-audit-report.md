# Documentation Audit Report

Pass: True

Policy version: `generated-readme-operator-docs-audit-1.0`

Owner: `factory_agent_19_docs`

Mission: `Audits generated READMEs and operator docs.`

Report JSON: `generated/documentation-audit-report.json`

Validation commands:

- `python tools/validate_copilot_factory.py`
- `python tools/validate_prompt_quality.py`

## Copilot README Checks

| Copilot | Status | Sections | Runtime refs | Operator refs |
|---|---|---:|---:|---:|
| devex | pass | 6 | 8 | 8 |
| aida_architecture | pass | 6 | 8 | 8 |
| as_is_discovery | pass | 6 | 8 | 8 |
| single_registry | pass | 6 | 8 | 8 |
| firefly_v5 | pass | 6 | 8 | 8 |
| firefly_v6 | pass | 6 | 8 | 8 |
| moonshine | pass | 6 | 8 | 8 |
| java_generic | pass | 6 | 8 | 8 |
| java_architect | pass | 6 | 8 | 8 |
| angular_18 | pass | 6 | 8 | 8 |
| nodejs | pass | 6 | 8 | 8 |
| python | pass | 6 | 8 | 8 |
| qa_general | pass | 6 | 8 | 8 |
| sonarqube_remediation | pass | 6 | 8 | 8 |
| cicd | pass | 6 | 8 | 8 |
| journey_to_cloud | pass | 6 | 8 | 8 |
| copilots_manager | pass | 6 | 8 | 8 |
| firefly_marketplace | pass | 6 | 8 | 8 |

## Operator Doc Checks

| Path | Status | Markers |
|---|---|---:|
| README.md | pass | 3 |
| OPERATING_SYSTEM.md | pass | 3 |
| factory-prompt.md | pass | 3 |
| .codex-loop/factory/operate-observability-runbook.md | pass | 3 |
| .codex-loop/factory/incident-runbook.md | pass | 3 |
| .codex-loop/factory/cost-routing-policy.md | pass | 4 |

## Cost And Traceability

- Deterministic Python first: True
- LLM escalation: disabled_for_marker_and_reference_audit
- Runtime trace evidence: `generated/documentation-audit-report.json#/readmeChecks`
- Max unexplained drift: 0

## Issues

- none
