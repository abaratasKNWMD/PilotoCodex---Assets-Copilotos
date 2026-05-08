# Task 029 Department Council - Copiloto Registro Unico

Scope: runtime-contract review for `dist/copilots/single_registry/*`, focused on real equivalence across Codex, Claude, GitHub Copilot and LangChain without cost inflation or traceability loss.

Verification run:

- `python tools/validate_copilot_factory.py` - PASS: 18 copilots, 50 agents, 50 tasks.
- `python tools/validate_prompt_quality.py` - PASS: 18 copilots, 72 runtime prompts.
- `python tools/validate_runtime_equivalence.py` - PASS: 18 copilots checked.
- Structured parity smoke with `python -B -` - PASS: `PROFILE`, `OUTPUT_SCHEMA`, runtime set, `python_first_llm_sparse` and `maxUnexplainedDrift = 0` match `shared/spec.json`.

| Departamento | PASS-FAIL | Evidencia | Cambios | Riesgos |
|---|---|---|---|---|
| Product | PASS | `shared/spec.json` keeps the mission narrow: normalize technical information into one canonical registry; outputs remain `technical_registry` and `normalization_report`; phases remain `discovery` and `operate`. | No product-scope patch needed. | Residual: live GitHub evidence is pending until `github_mcp` is activated by an operator. |
| Engineering | PASS | Codex, Claude and GitHub Copilot adapters reference `../shared/spec.json` and `../shared/output_schema.json`; LangChain constants match shared id, outputs, connectors, env keys, schema, runtime set and cost mode. | No additional runtime-contract patch needed. | Residual: generated adapters embed copied prompt/schema bodies, so future generator drift must keep running the equivalence validator. |
| Web/UI/Design | PASS | No UI, navigation, responsive layout, form, render surface or accessibility surface exists in this task; the reviewed package is prompts, JSON contracts and Python runtime adapter. | None. | None for this scope. |
| Creative Studio | PASS | No image, mockup, motion, deck or social asset surface exists in the scoped files. | None. | None for this scope. |
| QA | PASS | Required validators all pass; prior task-029 QA audit records the README handoff fix so `validate_runtime_equivalence.py` is included with the other two validators. | No additional QA patch in this council; relied on current passing validator state. | Residual: validators prove static contract and prompt parity, not live connector behavior. |
| Safe-coding/Privacy | PASS | Connector declarations use env var names only (`GITHUB_TOKEN`); prompt rules forbid storing secrets, fake connector access and fake CI inspection; no `__pycache__` remains under `dist/copilots`. | No additional safety patch in this council. | Residual: importing Python adapters without `python -B` or `PYTHONDONTWRITEBYTECODE=1` can recreate bytecode caches that release validation blocks. |
| Growth/SEO/Content | PASS | No landing page, SEO metadata, blog, funnel copy or marketing claim surface exists in scope. | None. | None for this scope. |
| Legal/Risk | PASS | Runtime prompts state connector declarations are capability contracts, not credentials; evidence gates require file/log/catalog/connector/user-source evidence before claims. | None. | Residual: external repository facts must not be claimed until connector evidence is actually available. |
| Packaging/Release | PASS | All three release validators pass; `dist/copilots/single_registry/README.md` lists `validate_copilot_factory.py`, `validate_prompt_quality.py` and `validate_runtime_equivalence.py`; workspace has no Git metadata, so release evidence is file/validator based. | Created this department-council report. | Residual: no local `.git` means diff traceability depends on audit files and generated validation reports. |
| Commercial/Finance | PASS | No pricing, billing workflow, customer data or sales-promise surface exists in the scoped runtime contract; cost discipline remains `python_first_llm_sparse` and prompt bodies are not stored in reports. | None. | Residual: commercial demos must keep using placeholders for credentials, billing and customer data. |

Council decision: PASS. No new concrete defect was found during the cross-review after the existing QA/Safe-coding fixes; remaining items are documented residual risks with validator evidence.
