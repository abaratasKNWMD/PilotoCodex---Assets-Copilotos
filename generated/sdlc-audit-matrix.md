# SDLC Audit Matrix

| Copilot | discovery | as_is | architecture | design | build | test | security | devops | cloud | release | operate |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Copiloto DevEx | yes |  |  |  | yes | yes |  |  |  | yes |  |
| Copiloto de Principios de Arquitectura AIDA |  |  | yes | yes |  |  |  |  |  | yes |  |
| Copiloto de Discovery AS-IS | yes | yes |  |  |  |  |  |  |  |  |  |
| Copiloto Registro Unico | yes |  |  |  |  |  |  |  |  |  | yes |
| Copiloto Firefly v5 |  |  |  |  | yes | yes |  | yes |  |  |  |
| Copiloto Firefly v6 |  |  |  |  | yes | yes |  | yes |  |  |  |
| Copiloto Moonshine |  |  |  |  | yes | yes |  |  |  |  | yes |
| Copiloto Java Generico |  |  |  | yes | yes | yes |  |  |  |  |  |
| Copiloto Java Architect |  |  | yes | yes |  |  |  |  |  | yes |  |
| Copiloto Angular 18 |  |  |  | yes | yes | yes |  |  |  |  |  |
| Copiloto Node.js |  |  |  | yes | yes | yes |  |  |  |  | yes |
| Copiloto Python |  |  |  |  | yes | yes |  |  |  |  | yes |
| Copiloto QA General |  |  |  |  |  | yes |  |  |  | yes |  |
| Copiloto SonarQube Remediacion |  |  |  |  |  | yes | yes |  |  | yes |  |
| Copiloto CI/CD |  |  |  |  |  |  |  | yes |  | yes | yes |
| Copiloto Journey to Cloud |  |  | yes |  |  |  |  |  | yes | yes |  |
| Copilots Manager | yes |  |  |  |  |  |  |  |  |  | yes |
| Copiloto Firefly Marketplace |  |  |  |  |  |  |  |  |  | yes | yes |

## Design Boundary Contract Evidence

| Copilot | Contract artifact | Required evidence | Required handoff fields | Runtime equivalence |
|---|---|---|---|---|
| Copiloto de Principios de Arquitectura AIDA | `dist/copilots/aida_architecture/shared/design_boundary_audit.json` | `domain_boundaries`, `contracts`, `handoff_clarity`, `validation` | `next_owner`, `next_runtime`, `next_action`, `excluded_scope`, `dependency_direction`, `evidence_pack`, `validation_command`, `stop_condition` | Codex, Claude, GitHub Copilot and LangChain share `maxUnexplainedDrift = 0` |
| Copiloto Java Generico | `dist/copilots/java_generic/shared/design_boundary_audit.json` | `domain_boundaries`, `contracts`, `handoff_clarity`, `validation` | `next_owner`, `next_runtime`, `next_action`, `excluded_scope`, `dependency_direction`, `evidence_pack`, `validation_command`, `stop_condition` | Codex, Claude, GitHub Copilot and LangChain share `maxUnexplainedDrift = 0` |
| Copiloto Java Architect | `dist/copilots/java_architect/shared/design_boundary_audit.json` | `domain_boundaries`, `contracts`, `handoff_clarity`, `validation` | `next_owner`, `next_runtime`, `next_action`, `excluded_scope`, `dependency_direction`, `evidence_pack`, `validation_command`, `stop_condition` | Codex, Claude, GitHub Copilot and LangChain share `maxUnexplainedDrift = 0` |
| Copiloto Angular 18 | `dist/copilots/angular_18/shared/design_boundary_audit.json` | `domain_boundaries`, `contracts`, `handoff_clarity`, `validation` | `next_owner`, `next_runtime`, `next_action`, `excluded_scope`, `dependency_direction`, `evidence_pack`, `validation_command`, `stop_condition` | Codex, Claude, GitHub Copilot and LangChain share `maxUnexplainedDrift = 0` |
| Copiloto Node.js | `dist/copilots/nodejs/shared/design_boundary_audit.json` | `domain_boundaries`, `contracts`, `handoff_clarity`, `validation` | `next_owner`, `next_runtime`, `next_action`, `excluded_scope`, `dependency_direction`, `evidence_pack`, `validation_command`, `stop_condition` | Codex, Claude, GitHub Copilot and LangChain share `maxUnexplainedDrift = 0` |

## Build Implementation Contract Evidence

| Copilot | Contract artifact | Required evidence | Required implementation fields | Runtime equivalence |
|---|---|---|---|---|
| Copiloto DevEx | `dist/copilots/devex/shared/implementation_plan_audit.json` | `implementation_plan`, `stack_rules`, `affected_files`, `validation` | `target_stack`, `affected_files`, `plan_steps`, `stack_rules_checked`, `validation_commands`, `rollback_plan`, `out_of_scope`, `evidence_pack` | Codex, Claude, GitHub Copilot and LangChain share `maxUnexplainedDrift = 0` |
| Copiloto Firefly v5 | `dist/copilots/firefly_v5/shared/implementation_plan_audit.json` | `implementation_plan`, `stack_rules`, `affected_files`, `validation` | `target_stack`, `affected_files`, `plan_steps`, `stack_rules_checked`, `validation_commands`, `rollback_plan`, `out_of_scope`, `evidence_pack` | Codex, Claude, GitHub Copilot and LangChain share `maxUnexplainedDrift = 0` |
| Copiloto Firefly v6 | `dist/copilots/firefly_v6/shared/implementation_plan_audit.json` | `implementation_plan`, `stack_rules`, `affected_files`, `validation` | `target_stack`, `affected_files`, `plan_steps`, `stack_rules_checked`, `validation_commands`, `rollback_plan`, `out_of_scope`, `evidence_pack` | Codex, Claude, GitHub Copilot and LangChain share `maxUnexplainedDrift = 0` |
| Copiloto Moonshine | `dist/copilots/moonshine/shared/implementation_plan_audit.json` | `implementation_plan`, `stack_rules`, `affected_files`, `validation` | `target_stack`, `affected_files`, `plan_steps`, `stack_rules_checked`, `validation_commands`, `rollback_plan`, `out_of_scope`, `evidence_pack` | Codex, Claude, GitHub Copilot and LangChain share `maxUnexplainedDrift = 0` |
| Copiloto Java Generico | `dist/copilots/java_generic/shared/implementation_plan_audit.json` | `implementation_plan`, `stack_rules`, `affected_files`, `validation` | `target_stack`, `affected_files`, `plan_steps`, `stack_rules_checked`, `validation_commands`, `rollback_plan`, `out_of_scope`, `evidence_pack` | Codex, Claude, GitHub Copilot and LangChain share `maxUnexplainedDrift = 0` |
| Copiloto Angular 18 | `dist/copilots/angular_18/shared/implementation_plan_audit.json` | `implementation_plan`, `stack_rules`, `affected_files`, `validation` | `target_stack`, `affected_files`, `plan_steps`, `stack_rules_checked`, `validation_commands`, `rollback_plan`, `out_of_scope`, `evidence_pack` | Codex, Claude, GitHub Copilot and LangChain share `maxUnexplainedDrift = 0` |
| Copiloto Node.js | `dist/copilots/nodejs/shared/implementation_plan_audit.json` | `implementation_plan`, `stack_rules`, `affected_files`, `validation` | `target_stack`, `affected_files`, `plan_steps`, `stack_rules_checked`, `validation_commands`, `rollback_plan`, `out_of_scope`, `evidence_pack` | Codex, Claude, GitHub Copilot and LangChain share `maxUnexplainedDrift = 0` |
| Copiloto Python | `dist/copilots/python/shared/implementation_plan_audit.json` | `implementation_plan`, `stack_rules`, `affected_files`, `validation` | `target_stack`, `affected_files`, `plan_steps`, `stack_rules_checked`, `validation_commands`, `rollback_plan`, `out_of_scope`, `evidence_pack` | Codex, Claude, GitHub Copilot and LangChain share `maxUnexplainedDrift = 0` |
