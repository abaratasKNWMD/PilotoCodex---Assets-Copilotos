# Task 033 QA Audit - Copiloto Java Generico

Fecha: 2026-05-05
Perfil: strict
Scope auditado:

- `dist/copilots/java_generic/shared/spec.json`
- `dist/copilots/java_generic/shared/output_schema.json`
- `dist/copilots/java_generic/codex/AGENT.md`
- `dist/copilots/java_generic/claude/AGENT.md`
- `dist/copilots/java_generic/github-copilot/copilot-agent.md`
- `dist/copilots/java_generic/github-copilot/copilot-profile.json`
- `dist/copilots/java_generic/langchain/agent.py`
- `dist/copilots/java_generic/langchain/agent_contract.json`
- `dist/copilots/java_generic/langchain/agent_profile.json`
- reportes generados bajo `generated/`

## Hallazgos

- Bloqueante corregido: `runtimeParityContract.requiredTraceFields` exigia `phase` y `expected_outputs`, pero el JSON Schema del copilot los dejaba opcionales. Eso rompia trazabilidad real entre contrato de paridad y salida validable.
- Release readiness corregido: el smoke local creo `dist/copilots/java_generic/langchain/__pycache__/`, y `validate_copilot_factory.py` lo rechazo como artefacto de release.
- Coste corregido: al endurecer el schema, `validate_prompt_quality.py` detecto que LangChain quedaba justo por encima del presupuesto de crecimiento. Se redujo texto no contractual del docstring sin tocar prompts, schema ni contrato.
- UX/frontend: no aplica; la superficie auditada es runtime/contrato. El empty/error state operacional queda cubierto por `evidence_needed`, fallback offline de conector y handoff.
- Privacidad/acceso: los conectores se mantienen como nombres de capacidad (`github_mcp`) y env var names (`GITHUB_TOKEN`), sin valores de credencial ni customer/billing data.

## Parches hechos

- `phase` y `expected_outputs` son ahora obligatorios en el schema compartido y en las copias embebidas de `spec.json`, `agent_profile.json`, `agent.py` y los bloques de schema de Codex/Claude/GitHub Copilot.
- Actualizados los `outputSchemaSha256` en `codex_tool_protocol.json`, `claude_project_instructions.json`, `copilot-profile.json` y `agent_contract.json`.
- Aniadida prueba defensiva en `tools/validate_runtime_equivalence.py`: los campos de `runtimeParityContract.requiredTraceFields` deben existir en `output_schema.required`; tambien se anadio fixture negativa `runtime_trace_fields_schema`.
- Recortado el docstring de `dist/copilots/java_generic/langchain/agent.py` para mantener el presupuesto de coste. Resultado final: LangChain `growthRatio=0.0894`, limite `0.1`.
- Regenerados reportes de validacion y matriz SDLC para sincronizar digests tras los cambios.
- Eliminado `dist/copilots/java_generic/langchain/__pycache__/`.
- Creado este informe: `.codex-loop/factory/audits/task-033-qa.md`.

## Comandos ejecutados

- `Get-Command rg -ErrorAction SilentlyContinue | Select-Object -ExpandProperty Source`
  - Resultado: `rg` disponible como shim local en `.codex-loop/tool-shims/rg.ps1`.
- `git status --short`
  - Resultado: no hay repositorio Git inicializado en este workspace.
- `python tools/validate_copilot_factory.py`
  - Resultado inicial tras smoke de sintaxis: FAIL por `__pycache__` en `dist/copilots/java_generic/langchain/`.
- `python tools/validate_prompt_quality.py`
  - Resultado intermedio tras endurecer schema: FAIL por presupuesto LangChain (`cost_budget`).
- `python tools/validate_runtime_equivalence.py`
  - Resultado intermedio tras recortar docstring: FAIL por digests obsoletos en `generated/sdlc-runtime-matrix.json`.
- Smoke LangChain con `PYTHONDONTWRITEBYTECODE=1`, import dinamico con `sys.modules`, `plan()`, `output_schema()` y `render_prompt()`.
  - Resultado final: PASS; schema contiene `phase` y `expected_outputs`, y secreto sintetico GitHub queda redactado.
- Check determinista de paridad schema/trace fields en todos los copilots.
  - Resultado: PASS; no quedan `requiredTraceFields` fuera de `required`.
- Secuencia final DoD:
  - `python tools/validate_copilot_factory.py`: PASS, 18 copilots, 50 agents, 50 tasks.
  - `python tools/validate_prompt_quality.py`: PASS, 18 copilots, 72 runtime prompts.
  - `python tools/validate_runtime_equivalence.py`: PASS, 18 copilots checked.
- `Get-ChildItem -Path dist\copilots\java_generic -Recurse -Directory -Filter __pycache__`
  - Resultado: sin caches bajo el artefacto Java Generic.

## Evidencia de reportes

- `generated/validation-report.json`: `pass=true`.
- `generated/prompt-quality-report.json`: `pass=true`; Java Generic LangChain `growthRatio=0.0894`.
- `generated/runtime-equivalence-report.json`: `pass=true`; fixture negativa `runtime_trace_fields_schema` detectada.

## Riesgos residuales

- La equivalencia validada es local y contractual; no prueba una llamada real a GitHub MCP porque el conector permanece correctamente como placeholder/offline.
- No hay historial Git en este workspace, asi que la trazabilidad depende de los reportes generados y de este audit file.
- No se ejecuta un LLM real generando un `java_patch_plan`; el riesgo queda mitigado por schema, prompts compartidos, adapter LangChain y validadores de runtime.
