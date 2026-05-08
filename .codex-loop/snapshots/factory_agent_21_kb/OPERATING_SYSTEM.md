# Copilot Factory Operating System

## Mission

Create equivalent, auditable copilots for Codex, Claude, GitHub Copilot Agents and LangChain while keeping token cost low. The Factory Director owns the whole run, keeps gates honest and prevents scope drift through verifiable state locks, report gates and runtime-equivalence evidence.

## Abstraction Layers

1. Catalog Brain: Python owns copilot definitions, connectors, env names, outputs and SDLC phases.
2. Semantic Brain: Python routes requests using stack tags, phase tags, connector requirements and output contracts.
3. Prompt Brain: Python renders system/developer prompts from shared copilot specs, so runtime prompts do not drift.
4. Runtime Adapters: Codex, Claude, GitHub Copilot and LangChain receive the same operating contract in runtime-native form.
5. SDLC Committee: Discovery, Architecture, Design, Build, Test, Security, DevOps, Cloud, Release and Operate auditors can verify each artifact.
6. LLM Cerebellum: Codex/Claude are used only for narrow judgement, code edits and final synthesis after Python prepared the evidence.

## Cost Policy

Python first. LLM second. Human approval for secrets, connector activation, production writes and release.

## Quality Policy

A copilot prompt is not accepted unless `python tools/validate_prompt_quality.py` passes.

Cross-runtime drift is not accepted unless `python tools/validate_runtime_equivalence.py` passes.

## Control Room Gate

The Control Room is serial. `factory_agent_01_director` owns this gate before any task is declared complete:

1. State lock: respect `.codex-loop/run.lock.json`; verify required fields, workspace match, timestamp order and snapshot evidence when Git metadata is absent before treating the run as owned.
2. Scope lock: edit only declared task files unless a minimal verifier or generated report is required; product output stays under `products/<slug>/`.
3. Gate honesty: "done" requires evidence, not intent. Structure, prompt quality and runtime equivalence reports are the acceptance artifacts.
4. Runtime parity: `shared/spec.json` is canonical; Codex, Claude, GitHub Copilot and LangChain adapters must remain explainably equivalent.
5. Cost trace: Python deterministic checks run first; LLM work stays sparse and must point back to concrete artifacts.
6. Final truth: unresolved frontier risks stay explicit instead of being hidden behind a passing compile or partial report.

## Connector Policy

Declare MCP connectors by env var name only. Never store token values.

`config/mcp-connectors.example.json` is the connector source of truth. `config/.env.example` must contain each connector env key exactly once with an empty value, and no sensitive env placeholder may be orphaned.

Connector declarations must default to disabled, require operator activation, preserve the same contract for Codex, Claude, GitHub Copilot and LangChain, and keep `allowed_operations` coherent with `denied_operations`.

## Codex Loop Modes

- `Prompt libre`: load `factory-prompt.md` when you want planning and selective improvements.
- `Ejecutar solo tasks.json`: consume the factory-grade queue when you want controlled autonomous work.
