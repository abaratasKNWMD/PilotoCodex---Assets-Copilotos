# QA Audit Task 017

Fecha: 2026-05-04
Perfil: strict
Tarea auditada: `[P1][factory_agent_17_langchain] Builds Python/LangChain compatible agent specs.`

## Veredicto

Pass con parche aplicado.

La mision LangChain queda reflejada en artefactos verificables: 18 `langchain/agent.py`, 18 `langchain/agent_profile.json`, 18 `langchain/agent_contract.json`, `generated/runtime-injection-map.json` y `generated/runtime-equivalence-report.*`.

## Hallazgos

- P1 corregido: `tools/validate_runtime_equivalence.py` verificaba `render_prompt` por marcadores estaticos, pero no ejecutaba los agentes LangChain. Eso podia dejar pasar una implementacion que declarase `safe_prompt_rendering` sin demostrar redaccion real ni forma de mensajes.
- P2 corregido durante QA: la comprobacion de sintaxis con `py_compile` genero directorios `__pycache__` dentro de artefactos de release. Se limpiaron y la verificacion final se ejecuto con `python -B`.
- Sin hallazgos de secretos reales, datos de cliente o billing en los artefactos revisados. Las pruebas sinteticas usan placeholders y construyen la ruta local por concatenacion para no dejar una ruta absoluta literal en el fuente.
- No hay superficie UI/frontend. La revision UX aplica aqui como ergonomia operativa: contratos JSON trazables, Markdown legible y errores de validador accionables.

## Parches Hechos

- `tools/validate_runtime_equivalence.py`: se agrego import dinamico de cada `dist/copilots/<copilot>/langchain/agent.py`, ejecucion de `build_agent()` y smoke de `render_prompt()`.
- `tools/validate_runtime_equivalence.py`: se agrego validacion runtime de forma `system/developer/user`, contenido no vacio, ausencia de patrones de secreto y ausencia de rutas locales absolutas en el prompt renderizado.
- `tools/validate_runtime_equivalence.py`: se agrego el caso negativo `unsafe_langchain_render_prompt`.
- `generated/runtime-equivalence-report.*`: regenerado por el validador; ahora expone `runtimeSmoke: true` para los 18 contratos LangChain y detecta el negativo nuevo.
- Limpieza de `__pycache__` generado por la auditoria bajo `tools/` y `dist/copilots/`.

## Comandos Ejecutados

- `Get-Command rg -ErrorAction SilentlyContinue`: `rg` disponible como shim local.
- `git status --short`: fallo esperado; el workspace no es un repositorio Git.
- `python tools/validate_copilot_factory.py`: PASS inicial, 18 copilots, 50 agents, 50 tasks.
- `python tools/validate_prompt_quality.py`: PASS inicial, 18 copilots, 72 runtime prompts.
- `python tools/validate_runtime_equivalence.py`: PASS inicial, 18 copilots checked.
- `python -m py_compile tools\validate_runtime_equivalence.py` y compilacion de `dist/copilots/*/langchain/agent.py`: sintaxis correcta, pero genero `__pycache__`.
- Smoke ad hoc de 18 agentes LangChain: import, `build_agent()`, `render_prompt()`, `output_schema()` y redaccion de secreto/ruta local; PASS tras corregir el harness de import.
- `python tools\validate_runtime_equivalence.py`: PASS despues del parche.
- Limpieza PowerShell con comprobacion de ruta dentro del workspace usando `[System.IO.File]::Delete` y `[System.IO.Directory]::Delete` para los `__pycache__`.
- `python -B tools/validate_copilot_factory.py`: PASS final.
- `python -B tools/validate_prompt_quality.py`: PASS final.
- `python -B tools/validate_runtime_equivalence.py`: PASS final.
- `Get-ChildItem -Path . -Directory -Recurse -Filter __pycache__`: 0 directorios finales.
- `Select-String generated\runtime-equivalence-report.json`: confirma `runtimeSmoke: true` y `unsafe_langchain_render_prompt` con `failureDetected=true`.

## Riesgos Residuales

- No hay metadata Git local, asi que la trazabilidad de diff depende de esta auditoria y de los reportes generados.
- El smoke ejecuta la API Python compatible, pero no envuelve los agentes en una instalacion real de LangChain Tool/Runnable para evitar introducir una dependencia dura y coste externo.
- La equivalencia de Codex, Claude y GitHub Copilot sigue validandose sobre artefactos Markdown/JSON generados; no ejecuta runtimes externos.
