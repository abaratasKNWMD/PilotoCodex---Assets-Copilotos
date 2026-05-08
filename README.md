# Copilot Factory

This project builds a product-grade copilot ecosystem for Codex, Claude, GitHub Copilot Agents and LangChain-compatible Python agents.

Version: `copilot-factory-0.2.0`

## What changed in v2

- The first version was only a structural scaffold. V2 turns every copilot into a real runtime contract.
- Every copilot now has system prompt, developer prompt, output schema, SDLC playbook, quality rubric and runtime-specific injection files.
- Python is the brain: catalog generation, semantic routing, prompt quality validation, schema validation and audit reports.
- Codex, Claude, GitHub Copilot and LangChain are adapters over the same shared spec, not four unrelated prompt piles.

## Commands

```powershell
python tools/generate_copilot_factory.py
python tools/validate_copilot_factory.py
python tools/validate_prompt_quality.py
python tools/validate_runtime_equivalence.py
python tools/semantic_router.py python ci routing
python tools/run_factory.py
```

`tools/semantic_router.py` requires a non-empty routing request and exits non-zero for empty input.

## Outputs

- `tasks.json`: 50 factory-grade Codex Loop tasks.
- `factory-prompt.md`: free-prompt briefing for Codex Loop.
- `data/copilots.json`: canonical 18-copilot catalog.
- `config/.env.example`: placeholder-only env contract. Connector env keys must be present with empty values.
- `config/mcp-connectors.example.json`: disabled MCP connector declaration contract, including owners, least-privilege scopes, allowed and denied operations, runtime parity and trace refs.
- `generated/copilot-index.json`: normalized IDs, connector names, env names, outputs and runtime traces.
- `dist/copilots/<copilot>/shared/spec.json`: source of truth.
- `dist/copilots/<copilot>/shared/implementation_plan_audit.json`: Build Auditor contract for implementation plans and stack-specific rules where applicable.
- `dist/copilots/journey_to_cloud/shared/cloud_migration_audit.json`: Cloud Auditor contract for migration, target platform and modernization increments.
- `dist/copilots/<copilot>/codex/AGENT.md`: Codex injection.
- `dist/copilots/<copilot>/claude/AGENT.md`: Claude injection.
- `dist/copilots/<copilot>/github-copilot/copilot-agent.md`: GitHub Copilot profile.
- `dist/copilots/<copilot>/github-copilot/copilot-profile.json`: GitHub Copilot profile contract.
- `dist/copilots/<copilot>/github-copilot/mcp-placeholders.json`: disabled MCP connector placeholders.
- `dist/copilots/<copilot>/langchain/agent.py`: Python/LangChain brain.
- `generated/factory-audit.json`: factory-level pass/fail summary, including Build, Cloud and Packager evidence.
- `generated/factory-audit.json#/releaseAudit/distributionManifest`: distribution manifest for the eight release target copilot packages.
- `generated/phase-verdict-report.*`: QA Committee Chair pass/fail consolidation across every SDLC phase, backed by `dist/copilots/qa_general/shared/phase_verdict_report_contract.json`.
- `generated/phase-verdict-evidence-map.*`: machine-readable phase verdict trace map with explicit pass booleans, sources, evidence refs, runtime equivalence gate state and negative fixture outcomes.
- `generated/runtime-injection-map.json`: where each prompt and runtime contract lives.
- `generated/runtime-injection-map.json#/distributionFileIndex`: file index for shared specs, schemas and Codex, Claude, GitHub Copilot and LangChain adapter files per release target copilot.
- `generated/sdlc-runtime-matrix.*`: SDLC x Copilot x Runtime matrix owned by `factory_agent_24_matrix`, with one cell per declared phase, copilot and runtime.
- `generated/sdlc-runtime-matrix-maintenance.*`: maintenance receipt for matrix coverage, trace ledger digests, prompt-budget gates and cell equivalence.
- `generated/validation-report.json#/mcpConnectorAuditor`: executable evidence for connector declarations, env placeholders, orphan placeholder detection, negative cases and runtime equivalence across Codex, Claude, GitHub Copilot and LangChain.
- `generated/prompt-quality-report.*`: prompt-depth QA gate.
- `generated/runtime-equivalence-report.*`: cross-runtime drift gate.
- `generated/validator-smoke-report.*`: smoke evidence that the generated validators ran, wrote receipts and reported blockers without recursive validator execution.
- `generated/validator-smoke/<validator>.json`: per-validator receipt with command, report digest, pass state and blocker summary.
- `generated/documentation-audit-report.*`: Documentation Auditor evidence for generated READMEs and operator docs.
- `.codex-loop/factory/cost-routing-contract.json`: Cost Routing Governor source of truth for Python-first deterministic work and LLM-only judgement work.
- `.codex-loop/factory/cost-routing-scorecard.json`: executable scorecard checked by `generated/validation-report.json#/costRoutingAuditor`.
- `.codex-loop/factory/cost-routing-policy.md`: operator policy for routing cheap work to Python without runtime drift.

## MCP Connector Contract

MCP connector examples are declaration-only. `config/mcp-connectors.example.json` is the source of truth and `config/.env.example` mirrors each connector env key exactly once with an empty value. Real tokens belong only in a local shell, OS secret store, CI secret store or approved MCP runtime environment.

The connector gate is `generated/validation-report.json#/mcpConnectorAuditor`, produced by `python tools/validate_copilot_factory.py`. It verifies disabled defaults, lower_snake_case connector names, UPPER_SNAKE_CASE env names, owner and rotation owner, least-privilege scope, runtime allowlists, traceability refs, unique placeholders and coherent allowed/denied operations.

## Control Room Director Contract

`factory_agent_01_director` is the run owner. Its mission is encoded as a machine-readable control contract in `factory.config.json` under `controlRoom`, and as the first queue gate in `tasks.json`.

The director cannot mark a run done unless these artifacts exist and agree:

- State lock evidence: `.codex-loop/run.lock.json` exists, has the required fields (`id`, `pid`, `workspace`, `startedAt`, `heartbeatAt`, `mode`), matches this workspace and has a heartbeat that does not precede the start time.
- Gate evidence: `generated/validation-report.json`, `generated/prompt-quality-report.json` and `generated/runtime-equivalence-report.json` are the truth sources for structure, prompt depth and runtime drift.
- Scope evidence: task files must stay inside the declared task file list or documented factory roots; product code belongs under `products/<slug>/` with registry updates when a product is created.
- Equivalence evidence: `dist/copilots/<copilot>/shared/spec.json` remains canonical, with Codex, Claude, GitHub Copilot and LangChain treated as runtime adapters over that spec.
- Cost evidence: deterministic Python gates run before any sparse LLM judgement, so traceability comes from generated reports instead of repeated prompt expansion.

## Operate Evidence

Operate evidence is tracked through `.codex-loop/factory/operate-observability-contract.json` and `generated/validation-report.json#/operateAuditor`. Runtime incidents, stale state locks and validation report regressions must stay linked to the local operate runbooks before release handoff.

## Cost Routing Governor Evidence

`factory_agent_20_cost` owns the mission `Routes cheap deterministic work to Python and expensive judgement to LLMs.` Its machine-readable contract is `.codex-loop/factory/cost-routing-contract.json`, with score evidence in `.codex-loop/factory/cost-routing-scorecard.json` and operator policy in `.codex-loop/factory/cost-routing-policy.md`.

The gate is `generated/validation-report.json#/costRoutingAuditor`, produced by `python tools/validate_copilot_factory.py`. It verifies that catalog generation, semantic routing, schema validation, prompt-size budgets, runtime equivalence diffs and documentation marker audits route to Python, while architecture tradeoffs, non-trivial code changes and final operator synthesis require prior Python gate evidence before LLM judgement. Codex, Claude, GitHub Copilot and LangChain must keep one shared policy with `maxUnexplainedDrift=0`, and `.vscode/settings.json` must keep `codexLoop.rawLogPromptsAllowed=false` so cost traces use report references instead of raw logs.

## Documentation Auditor Evidence

`factory_agent_19_docs` owns generated README and operator doc checks. Its machine evidence lives in `generated/documentation-audit-report.json` and is surfaced in `generated/validation-report.json#/docsAuditor`.

The check is deterministic: each `dist/copilots/<copilot>/README.md` must map Codex, Claude, GitHub Copilot and LangChain back to `shared/spec.json`, include operator runbook commands, and keep privacy and cost trace markers.

## QA Phase Verdict Evidence

`factory_agent_22_qa` owns the mission `Consolidates all phase verdicts into a pass/fail report.` The executable contract is `dist/copilots/qa_general/shared/phase_verdict_report_contract.json`; `python tools/validate_copilot_factory.py` emits `generated/phase-verdict-report.json` and `generated/phase-verdict-report.md`.

The report consolidates discovery, as_is, architecture, design, build, test, security, devops, cloud, release and operate verdicts from `generated/validation-report.json`, using explicit `pass` booleans and `pass` or `fail` verdict values only. It also consumes `generated/runtime-equivalence-report.json` and only passes when that gate passes with `maxUnexplainedDrift=0` and zero issues, plus negative fixtures proving missing phases, invalid verdicts, inferred passes, runtime gate failures and inconsistent aggregation are detected.

`generated/phase-verdict-evidence-map.json` is emitted by the same validation gate and is the operator-facing audit map: it records phase count, pass/fail counts, failed gates, source report refs, evidence refs per phase and the negative fixture result set without requiring raw prompt logs.

The gate rejects drift between a phase `verdict`, its explicit `pass` boolean, `summaryPass`, `failedPhases` and `failedGates`, so the operator report cannot pass with contradictory machine fields.

## SDLC Runtime Matrix Evidence

`factory_agent_24_matrix` owns the mission `Maintains the SDLC x Copilot x Runtime matrix.` The executable evidence is generated by `python tools/validate_copilot_factory.py` in `generated/sdlc-runtime-matrix.json` and `generated/sdlc-runtime-matrix.md`.

The matrix records every declared SDLC phase, copilot and runtime cell for Codex, Claude, GitHub Copilot and LangChain. It stores adapter paths and SHA-256 digests only, not prompt bodies, and links each cell back to `generated/runtime-injection-map.json`, `dist/copilots/<copilot>/shared/spec.json` and `dist/copilots/<copilot>/shared/output_schema.json`.

`generated/sdlc-runtime-matrix-maintenance.json` is the maintenance receipt. It checks matrix cell coverage, trace ledger coverage, prompt-budget rules, cell equivalence and runtime drift, and is cross-validated by `generated/validation-report.json#/sdlcRuntimeMatrix`, `generated/prompt-quality-report.json#/sdlcRuntimeMatrixAudit` and `generated/runtime-equivalence-report.json#/sdlcRuntimeMatrixAudit`.

## Validator Smoke Evidence

`factory_agent_25_smoke` owns the mission `Runs generated validators and reports blockers.` Each validator writes a receipt under `generated/validator-smoke/` after its normal report is emitted:

- `generated/validator-smoke/copilot-factory.json`
- `generated/validator-smoke/prompt-quality.json`
- `generated/validator-smoke/runtime-equivalence.json`

`generated/validator-smoke-report.json` aggregates those receipts and only passes when all three expected receipts are present, each source report passes, blocker count is zero, receipt shape is valid, prompt bodies are not stored and runtime equivalence points back to `data/agent_roster.json#/factory_agent_25_smoke`. The smoke report stores relative paths, SHA-256 report digests and blocker summaries only.
