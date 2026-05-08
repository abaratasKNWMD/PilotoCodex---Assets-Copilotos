# Phase Verdict Evidence Map

Pass: True

Overall verdict: pass

Source report: `generated/phase-verdict-report.json`

Contract: `dist/copilots/qa_general/shared/phase_verdict_report_contract.json`

Consolidation:

- Required phases: 11
- Phases present: 11
- Phase pass count: 11
- Phase fail count: 0
- Failed phases: none
- Failed gates: none
- Explicit pass required: True
- Deterministic Python first: True

| Phase | Verdict | Pass | Pass inferred | Source | Evidence refs |
|---|---|---|---|---|---:|
| discovery | pass | True | False | `generated/validation-report.json#/discoveryAuditor` | 2 |
| as_is | pass | True | False | `generated/validation-report.json#/discoveryAuditor` | 2 |
| architecture | pass | True | False | `generated/validation-report.json#/architectureAuditor` | 2 |
| design | pass | True | False | `generated/validation-report.json#/designAuditor` | 2 |
| build | pass | True | False | `generated/validation-report.json#/buildAuditor` | 2 |
| test | pass | True | False | `generated/validation-report.json#/testStrategyAudit` | 2 |
| security | pass | True | False | `generated/validation-report.json#/securityAuditor` | 3 |
| devops | pass | True | False | `generated/validation-report.json#/devopsAuditor` | 3 |
| cloud | pass | True | False | `generated/validation-report.json#/cloudAuditor` | 2 |
| release | pass | True | False | `generated/validation-report.json#/releaseAuditor` | 2 |
| operate | pass | True | False | `generated/validation-report.json#/operateAuditor` | 2 |

Runtime equivalence gate:

- Source: `generated/runtime-equivalence-report.json`
- Runtimes: codex, claude, github-copilot, langchain
- Report pass: True
- Issues count: 0
- Negative cases detected: True
- Max unexplained drift: 0

Negative fixtures:

- `valid_control`: expectedFailure=False failureDetected=False passedExpectation=True
- `missing_phase`: expectedFailure=True failureDetected=True passedExpectation=True
- `invalid_verdict`: expectedFailure=True failureDetected=True passedExpectation=True
- `inconsistent_overall`: expectedFailure=True failureDetected=True passedExpectation=True
- `inconsistent_phase_pass`: expectedFailure=True failureDetected=True passedExpectation=True
- `inconsistent_failed_phases`: expectedFailure=True failureDetected=True passedExpectation=True
- `missing_cost_control`: expectedFailure=True failureDetected=True passedExpectation=True
- `inferred_phase_pass`: expectedFailure=True failureDetected=True passedExpectation=True
- `runtime_gate_failed`: expectedFailure=True failureDetected=True passedExpectation=True
