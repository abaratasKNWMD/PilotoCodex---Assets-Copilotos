# QA audit task 002

Scope: `factory_agent_02_catalog`, catalog normalization, semantic router output and runtime trace index.

Date: 2026-05-04

## Verdict

Pass with patches. The audited mission is now backed by executable checks and regeneration-safe templates, not only by descriptive JSON.

## Findings

1. Fixed: `tools/semantic_router.py` silently routed empty input to the sample request `java ci sonar remediation`. That could hide a caller bug and produce a plausible but wrong route. The CLI now requires a non-empty request and exits non-zero with usage text.
2. Fixed: `tools/generate_copilot_factory.py` still rendered the old router and a non-normalized `generated/copilot-index.json`. A factory regeneration would have lost the normalization evidence. The generator now emits normalized catalog metadata, normalized lookup fields, runtime traces, and the current router template.
3. Fixed: `tools/validate_copilot_factory.py` did not prove the task-specific normalization contract. It now checks lower/upper snake case rules, duplicate canonical fields, catalog normalization metadata, `factory_agent_02_catalog` outputs/contract, `generated/copilot-index.json` normalized fields, lookup trace completeness and normalization audit flags.
4. Fixed: README and README generator templates did not document the router request requirement or the normalized index artifact.

## Patches made

- `tools/semantic_router.py`: added explicit `main()` and empty-input usage failure.
- `tools/generate_copilot_factory.py`: added normalization helpers, normalized catalog/index generation, catalog agent contract generation and updated router/README templates.
- `tools/validate_copilot_factory.py`: added task-specific normalization and traceability validation.
- `tools/elevate_copilot_prompts.py`: updated generated root README content.
- `README.md`: documented `python tools/semantic_router.py python ci routing`, empty-input behavior and `generated/copilot-index.json`.
- Generated validation reports were refreshed by validators.

## Commands executed

- `Get-Command rg -ErrorAction SilentlyContinue` - `rg` wrapper is available.
- `git status --short` - failed because this workspace has no `.git` metadata.
- `python -m py_compile tools\semantic_router.py tools\generate_copilot_factory.py tools\validate_copilot_factory.py tools\elevate_copilot_prompts.py` - pass.
- `python tools\validate_copilot_factory.py` - pass: 18 copilots, 50 agents, 50 tasks.
- `python tools\validate_prompt_quality.py` - pass: 18 copilots, 72 runtime prompts.
- `python tools\validate_runtime_equivalence.py` - pass: 18 copilots checked.
- `python tools\semantic_router.py python ci routing` - pass; top route is `python`, second route is `cicd`, and each returned route includes normalization and runtime trace fields.
- `python tools\semantic_router.py` - expected non-zero empty-state check; prints `Usage: python tools/semantic_router.py <routing request>`.
- Read-only template checks:
  - `root_readme_template_matches_current: True`
  - `router_template_matches_current: True`
  - `index_template_matches_current_shape: True`

## QA checklist notes

- Happy path: required DoD command passes and returns normalized routing payloads with runtime trace evidence.
- Empty/error state: router no longer fabricates a default request; it fails clearly on empty input.
- Loading/UI/responsive/forms/accessibility: not applicable to this increment; it is CLI/data/tooling only.
- Code quality: regeneration drift and missing task-specific validation were patched.
- Tests: existing validator now covers the normalization contract directly.
- Documentation: README and generation templates describe the router usage and normalized index.

## Residual risks

- Full `python tools/generate_copilot_factory.py` was not run to avoid broad timestamp/content churn outside the narrow audit patch. Instead, generator templates were compared against current router, README and index shape.
- The workspace has no Git metadata, so file-level diff provenance is limited to local inspection and validator output.
