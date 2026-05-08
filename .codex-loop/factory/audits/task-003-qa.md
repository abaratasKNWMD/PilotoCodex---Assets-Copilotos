# Task 003 QA Audit

Fecha: 2026-05-04

Perfil: strict

## Alcance

- Tarea auditada: `factory_agent_03_semantics`
- Mision: `Uses deterministic Python scoring before any LLM assist.`
- Superficie revisada: catalogo de copilotos, roster de agentes, indice generado, router semantico, validadores y reportes generados.
- No hay interfaz frontend nueva; la revision de UX aplica al CLI, mensajes de error y artefactos de operador.

## Hallazgos

1. **Corregido - drift del generador rompe el DoD en regeneracion.**
   `tools/generate_copilot_factory.py` seguia renderizando un `semantic_router.py` sin `routing_evidence` y generaba catalogo/indice/roster sin el contrato semantico completo. El estado actual pasaba, pero ejecutar el comando documentado `python tools/generate_copilot_factory.py` podia borrar la evidencia verificable de `score_before_llm_assist`, `llm_assist_used=false` y la equivalencia de runtimes.

2. **Sin bloqueo - runtime actual correcto.**
   `python tools/semantic_router.py python ci routing` devuelve `python` como top route, `cheap_path=true`, `routing_evidence.deterministic_python_first=true`, `score_before_llm_assist=true` y `llm_assist_used=false`.

3. **Sin bloqueo - estados de error CLI cubiertos.**
   El router rechaza peticion vacia y limites fuera de rango con mensajes explicitos. No hay loading state porque la superficie es CLI local sin espera asincrona.

## Parches Hechos

- `tools/generate_copilot_factory.py`
  - Se anadieron constantes y helpers de contrato semantico (`semantic_routing_profile`, `semantic_routing_policy`, `semantic_routing_audit`).
  - El catalogo generado conserva `semantic_routing` para el copilot `python`.
  - El indice generado conserva `normalizationPolicy.semanticRouting` y `semanticRoutingAudit`.
  - El roster generado conserva `factory_agent_03_semantics.outputs` y `deterministic_scoring_contract`.
  - El template de `semantic_router.py` generado incluye `routing_evidence`, `CHEAP_PATH_THRESHOLD`, `SCORE_INPUTS`, `EXECUTION_ORDER` y `llm_assist_used=false`.

- `tools/validate_copilot_factory.py`
  - Se anadio `validate_generator_contract()`, que importa el generador, compila el router renderizado y verifica que el indice, roster y perfil Python generados mantengan el contrato antes de dar PASS.
  - `generated/validation-report.json` y `.md` ahora incluyen evidencia `generator.*` para que el DoD no dependa solo del estado actual de archivos escritos.

- Limpieza
  - Se eliminaron bytecodes generados por esta auditoria en `tools/__pycache__` para `generate_copilot_factory`, `semantic_router` y `validate_copilot_factory`.

## Comandos Ejecutados

- `Get-Command rg -ErrorAction SilentlyContinue | Select-Object -ExpandProperty Source` -> `rg` disponible como shim local.
- `git status --short` -> no hay metadata Git en este workspace.
- `python tools/validate_copilot_factory.py` -> PASS: 18 copilots, 50 agents, 50 tasks; repetido tras escribir este informe.
- `python tools/semantic_router.py python ci routing` -> PASS; top route `python`, score `7.0`, `llm_assist_used=false`.
- `python -B -c "from pathlib import Path; files=['tools/generate_copilot_factory.py','tools/semantic_router.py','tools/validate_copilot_factory.py']; [compile(Path(f).read_text(encoding='utf-8'), f, 'exec') for f in files]; print('compile-ok')"` -> PASS, sin escribir `.pyc`.
- `python -B -c "... dry-run generator ..."` -> PASS; generator produce score model, audit, guard y perfil Python correctos.
- `python tools/validate_prompt_quality.py` -> PASS: 18 copilots, 72 runtime prompts.
- `python tools/validate_runtime_equivalence.py` -> PASS: 18 copilots checked.
- `python tools\semantic_router.py` -> salida de uso esperada para peticion vacia, exit non-zero.
- `$env:PYTHONDONTWRITEBYTECODE='1'; python -c "... invalid cases ..."` -> PASS; errores esperados: limite fuera de rango y peticion vacia.

## Riesgos Residuales

- No hay repositorio Git, asi que la auditoria no pudo usar diff real. La verificacion se baso en los artefactos actuales, validadores y dry-run del generador.
- No ejecute `python tools/generate_copilot_factory.py` para evitar una regeneracion amplia de artefactos no necesarios. En su lugar valide sus funciones puras (`copilot_index`, `agent_roster`, `normalized_copilots`, `render_semantic_router`) sin escribir archivos.
- `python -m py_compile` recrea bytecode aunque se invoque con `-B`; las verificaciones de release deben usar `compile()` en memoria o limpiar `tools/__pycache__` despues.

## Veredicto

PASS con parche. La mision queda reflejada en comportamiento ejecutable, validacion del router, contrato del agente, indice generado y ahora tambien en el generador que recrea esos artefactos.
