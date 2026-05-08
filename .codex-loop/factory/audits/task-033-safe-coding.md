# Task 033 Safe-Coding Audit - Copiloto Java Generico

Fecha: 2026-05-05
Perfil: strict
Scope auditado:

- `dist/copilots/java_generic/shared/spec.json`
- `dist/copilots/java_generic/shared/output_schema.json`
- `dist/copilots/java_generic/codex/AGENT.md`
- `dist/copilots/java_generic/claude/AGENT.md`
- `dist/copilots/java_generic/github-copilot/copilot-agent.md`
- `dist/copilots/java_generic/github-copilot/mcp-placeholders.json`
- `dist/copilots/java_generic/langchain/agent.py`
- `dist/copilots/java_generic/langchain/agent_contract.json`
- `dist/copilots/java_generic/langchain/agent_profile.json`
- reportes generados bajo `generated/`

## Hallazgos

- Medium, corregido: `dist/copilots/java_generic/langchain/agent.py` anadia `dist/copilots` al final de `sys.path` antes de importar `_runtime_safety`. En un runtime local, eso podia permitir shadowing del helper de validacion/redaccion por otro modulo `_runtime_safety` resuelto antes en `sys.path`.
- Info, sin parche: no se encontraron credenciales reales ni valores de token. Las apariciones de `GITHUB_TOKEN` son nombres de variable de entorno o referencias placeholder; `mcp-placeholders.json` mantiene `credentialValue` vacio, `credentialValuesStored=false`, `customerDataAllowed=false` y `billingDataAllowed=false`.
- Info, sin parche: no hay superficie CORS, sesion web, billing real ni datos multi-tenant en los archivos auditados. El aislamiento aplicable queda documentado como conectores offline/placeholder y no envio de customer/billing data.
- Info, sin parche: las entradas del adaptador LangChain pasan por `validate_request`, `validate_evidence` y `redact_value`, con limites de longitud, profundidad, numero de items y redaccion de secretos/rutas locales.

## Parches hechos

- `dist/copilots/java_generic/langchain/agent.py`: cambiado `sys.path.append(...)` a `sys.path.insert(0, ...)` para priorizar el helper comun esperado de `dist/copilots/_runtime_safety.py`; se recorto el docstring no contractual para mantener el presupuesto de coste.
- `tools/validate_runtime_equivalence.py`: actualizado el validador estatico para aceptar `sys.path.insert` como variante permitida del ajuste local de path que ya se permitia para `append`.
- Reportes regenerados por los validadores en `generated/`.

## Comandos ejecutados

- `Get-Command rg -ErrorAction SilentlyContinue | Select-Object -ExpandProperty Source`
  - Resultado: `rg` disponible como shim local en `.codex-loop/tool-shims/rg.ps1`.
- `git status --short`
  - Resultado: no hay repositorio Git inicializado en este workspace.
- Lectura/revision de los artefactos Java Generic, `dist/copilots/_runtime_safety.py`, reportes `generated/*` y el informe QA de la tarea.
- Busqueda de patrones de secreto y rutas locales en `dist/copilots/java_generic`, `generated`, `.codex-loop/factory/audits/task-033-qa.md` y este informe.
  - Resultado: sin valores de secreto reales ni rutas absolutas locales.
- Smoke directo:
  - `python -B -c "... build_agent(); render_prompt(...); ..."`
  - Resultado: PASS; `render_prompt` devuelve 3 mensajes, redacta valores sinteticos sensibles y el schema exige `phase` y `expected_outputs`.
- `python tools/validate_copilot_factory.py`
  - Resultado: PASS, 18 copilots, 50 agents, 50 tasks.
- `python tools/validate_prompt_quality.py`
  - Resultado: PASS, 18 copilots, 72 runtime prompts. Java Generic LangChain queda en `growthRatio=0.0856`, limite `0.1`.
- `python tools/validate_runtime_equivalence.py`
  - Resultado: PASS, 18 copilots checked; `generated/runtime-equivalence-report.json` mantiene `secretPatternLeaks=0` y `localPathLeaks=0`.
- `Get-ChildItem -Path dist\copilots\java_generic -Recurse -Directory -Filter __pycache__`
  - Resultado: sin caches bajo el artefacto Java Generic.

## Riesgos residuales

- La revision de conector GitHub MCP sigue siendo contractual/offline: no se probo activacion real porque el conector permanece correctamente como placeholder sin credenciales.
- El parche endurece la precedencia del helper comun, pero no convierte la importacion en carga por ruta absoluta con `importlib`; esa opcion requeriria ampliar mas la politica estatica de imports.
- No hay historial Git local para comparar diffs; la trazabilidad depende de los reportes generados y de este audit file.
