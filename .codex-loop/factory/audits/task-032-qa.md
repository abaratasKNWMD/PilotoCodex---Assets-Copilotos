# Task 032 QA Audit - Copiloto Moonshine

Fecha: 2026-05-05
Perfil: strict
Scope auditado:

- `dist/copilots/moonshine/shared/spec.json`
- `dist/copilots/moonshine/shared/output_schema.json`
- `dist/copilots/moonshine/shared/runtime_contract.md`
- `dist/copilots/moonshine/codex/AGENT.md`
- `dist/copilots/moonshine/claude/AGENT.md`
- `dist/copilots/moonshine/github-copilot/copilot-agent.md`
- `dist/copilots/moonshine/langchain/agent.py`
- `dist/copilots/moonshine/langchain/agent_contract.json`
- `dist/copilots/moonshine/langchain/agent_profile.json`
- reportes generados bajo `generated/`

## Hallazgos

- Bloqueantes: ninguno.
- El contrato compartido mantiene equivalencia entre Codex, Claude, GitHub Copilot y LangChain: mismo `copilot_id`, mismo schema, mismos evidence gates, mismos conectores declarados y mismos comandos de validacion.
- El adapter LangChain ejecuta el flujo principal: `plan()` clasifica Moonshine backend build, exige evidencia cuando falta, pasa con evidencia completa, conserva comandos de validacion y `render_prompt()` redacta un patron de secreto sintetico.
- Hallazgo operativo corregido: el smoke local de import creo `__pycache__` en `dist/`, que el release gate rechaza. Se eliminaron solo los caches generados dentro de `dist/copilots/`.
- UX/frontend: no aplica; el incremento no anade superficie visual, formularios, navegacion ni estados loading/error de UI. La superficie de producto es de contrato/runtime y cubre el empty/error state operacional mediante `evidence_needed`, fallback offline de conector y handoff.
- Privacidad/acceso: los conectores siguen como nombres de capacidad (`github_mcp`) y env var names (`GITHUB_TOKEN`) sin valores de credencial. La auditoria de runtime reporta `dataHygienePass=true`.
- Documentacion: `dist/copilots/moonshine/README.md` y `shared/runtime_contract.md` apuntan a spec/schema, runtime files y validadores. No se requieren cambios adicionales.

## Parches hechos

- Creado este informe: `.codex-loop/factory/audits/task-032-qa.md`.
- Eliminados caches Python generados por el smoke QA:
  - `dist/copilots/__pycache__/`
  - `dist/copilots/moonshine/langchain/__pycache__/`
- No se parchearon archivos de producto Moonshine: no hubo fallo claro reproducible en contrato, prompts, schema o adapter runtime.
- Los validadores reescribieron sus reportes generados con resultados actuales, como parte normal de la verificacion.

## Comandos ejecutados

- `Get-Command rg -ErrorAction SilentlyContinue | Select-Object -ExpandProperty Source`
  - Resultado: `rg` disponible como shim local en `.codex-loop/tool-shims/rg.ps1`.
- `git status --short`
  - Resultado: no hay repositorio Git inicializado en este workspace.
- `python tools/validate_copilot_factory.py`
  - Resultado inicial: PASS, 18 copilots, 50 agents, 50 tasks.
- `python tools/validate_prompt_quality.py`
  - Resultado inicial: PASS, 18 copilots, 72 runtime prompts.
- `python tools/validate_runtime_equivalence.py`
  - Resultado inicial: PASS, 18 copilots checked.
- `python dist/copilots/moonshine/langchain/agent.py build moonshine backend patch plan`
  - Resultado: PASS funcional; score 8, Moonshine seleccionado, audit falla de forma esperada sin evidencia y pide `source_refs`, `implementation_plan`, `stack_rules`, `affected_files`, `validation`.
- Import dinamico estandar de `dist/copilots/moonshine/langchain/agent.py` con `sys.modules` registrado, seguido de `plan()` y `render_prompt()`.
  - Resultado: PASS; audit con evidencia completa `true`, roles `system/developer/user`, secreto sintetico redactado.
- `python tools/semantic_router.py moonshine backend build patch plan`
  - Resultado: PASS; Moonshine top route, confidence 96, cheap path true, runtime trace cubre los 4 runtimes.
- Revalidacion final despues de limpiar `__pycache__`:
  - `python tools/validate_copilot_factory.py`: PASS, 18 copilots, 50 agents, 50 tasks.
  - `python tools/validate_prompt_quality.py`: PASS, 18 copilots, 72 runtime prompts.
  - `python tools/validate_runtime_equivalence.py`: PASS, 18 copilots checked.
- `Get-ChildItem -Recurse -Directory -Filter '__pycache__' -LiteralPath 'dist' | Select-Object -ExpandProperty FullName`
  - Resultado: sin caches bajo `dist/`.

## Evidencia de reportes

- `generated/validation-report.json`: `pass=true`, `issues=0`.
- `generated/prompt-quality-report.json`: `pass=true`, `issues=0`.
- `generated/runtime-equivalence-report.json`: `pass=true`, `issues=0`, `langchainAgentAudit.pass=true`, `dataHygieneAudit.pass=true`.

## Riesgos residuales

- La equivalencia validada es de contrato, prompts, schema, rutas y adapter local; no prueba llamadas reales a GitHub MCP porque el conector esta correctamente en modo placeholder/offline.
- No hay historial Git en el workspace, por lo que la trazabilidad de cambios depende de los reportes generados y este audit file, no de diff/commit local.
- La validacion de salida comprueba el schema declarado, pero no ejecuta un LLM real generando `backend_patch_plan` o `runtime_diagnostics`; ese riesgo queda cubierto parcialmente por prompts y schema compartido.
