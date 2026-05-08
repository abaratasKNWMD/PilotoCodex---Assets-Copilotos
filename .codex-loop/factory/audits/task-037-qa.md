# QA Audit - Task 037 - Copiloto Python

Fecha: 2026-05-05
Perfil: strict
Scope auditado: equivalencia runtime de Copiloto Python entre Codex, Claude, GitHub Copilot y LangChain, con foco en prompts, schema, contrato, coste y trazabilidad.

## Hallazgos

1. **Rutas de herramientas Python no ejecutables desde los adapters Markdown.**
   - Evidencia: `dist/copilots/python/codex/AGENT.md`, `dist/copilots/python/claude/AGENT.md` y `dist/copilots/python/github-copilot/copilot-agent.md` apuntaban a `../../../tools/semantic_router.py` y `../../../tools/validate_prompt_quality.py`.
   - Riesgo: desde `dist/copilots/python/<runtime>/`, esa ruta resuelve a `dist/tools/...`, que no existe. El contrato declaraba Python-first, pero un operador siguiendo la tarjeta runtime no podia ejecutar los checks indicados.
   - Severidad: P2, release readiness/runtime contract.

2. **Equivalencia funcional general validada.**
   - Evidencia: `dist/copilots/python/shared/spec.json`, `dist/copilots/python/shared/output_schema.json`, `dist/copilots/python/langchain/agent_contract.json` y `dist/copilots/python/langchain/agent.py` conservan el source of truth `dist/copilots/python/shared/spec.json`, outputs `python_patch_plan`/`automation_report`, `python_first_llm_sparse`, `maxUnexplainedDrift: 0` y conectores/env names sin valores secretos.
   - `generated/runtime-equivalence-report.json` marca `python` con 4 runtimes comprobados.
   - `generated/prompt-quality-report.json` marca prompts Python con profundidad suficiente: Codex 14991 chars, Claude 14898 chars, GitHub Copilot 15279 chars y LangChain 18202 chars tras el parche.

3. **Runtime LangChain cubre happy path, empty state y redaccion.**
   - Smoke local: `build_agent().plan(...)` devuelve auditoria passing cuando recibe evidence completo; una request vacia lanza `ValueError`; `render_prompt(...)` devuelve roles `system`, `developer`, `user` y redacta patrones tipo `sk-*`/`github_pat_*`.

4. **UX/UI checklist.**
   - No aplica directamente: el incremento no anade UI renderizable, navegacion, formularios ni estados loading/error visuales. La revision equivalente fue de usabilidad operativa de prompts, rutas ejecutables, contratos y errores runtime.

## Parches hechos

- `dist/copilots/python/codex/AGENT.md`
- `dist/copilots/python/claude/AGENT.md`
- `dist/copilots/python/github-copilot/copilot-agent.md`
  - Corregidas las rutas de `Python router` y `Prompt quality gate` a `../../../../tools/...`, que resuelven correctamente desde cada carpeta runtime.

No se modificaron `spec.json`, `output_schema.json` ni `langchain/agent.py`: el contrato compartido ya era coherente y los cambios necesarios estaban en la documentacion ejecutable de los adapters.

## Comandos ejecutados

- `Get-Command rg -ErrorAction SilentlyContinue`
  - Resultado: `rg` disponible como shim local en `.codex-loop/tool-shims/rg.ps1`.
- `git status --short`
  - Resultado: no disponible; el workspace actual no es un repositorio Git.
- `python tools/validate_copilot_factory.py`
  - Resultado inicial: PASS.
  - Resultado intermedio: FAIL solo por `__pycache__` generado al ejecutar el smoke local del agente Python.
  - Resultado final: PASS, 18 copilots, 50 agents, 50 tasks.
- `python tools/validate_prompt_quality.py`
  - Resultado final: PASS, 18 copilots, 72 runtime prompts.
- `python tools/validate_runtime_equivalence.py`
  - Resultado final: PASS, 18 copilots checked.
- Smoke local de `dist/copilots/python/langchain/agent.py` con `importlib`
  - Resultado: plan happy path passing, empty request rechazada, roles de prompt correctos y redaccion de secretos correcta.
- `Test-Path '../../../../tools/semantic_router.py'` y `Test-Path '../../../../tools/validate_prompt_quality.py` desde `dist/copilots/python/codex`, `claude` y `github-copilot`
  - Resultado: `True` para ambas rutas en los tres adapters.
- `rg -n "../../../tools/(semantic_router|validate_prompt_quality)\\.py" dist/copilots/python`
  - Resultado final: sin coincidencias.
- `Get-ChildItem -Path "dist/copilots" -Recurse -Directory -Filter "__pycache__"`
  - Resultado final: sin caches Python residuales.

## Riesgos residuales

- El fallo de ruta puede reaparecer si un generador antiguo vuelve a emitir tarjetas runtime con `../../../tools/...`; conviene mantener este chequeo en QA de adapters o elevarlo al validador.
- No se anadieron tests persistentes porque el riesgo estaba en documentacion ejecutable de runtime. Quedo cubierto por checks de ruta mas los tres validadores obligatorios.
- No se ejecuto una validacion JSON Schema con una instancia real `python_patch_plan`/`automation_report`; el repositorio no declara fixture Python de salida. La coherencia schema/spec/runtime queda cubierta por `validate_runtime_equivalence.py`.
