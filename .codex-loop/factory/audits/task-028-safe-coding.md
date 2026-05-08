# Task 028 Safe-Coding / Privacy Review

## Alcance

- Tarea auditada: `[P1][copilot_owner_28_as_is_discovery]`
- Copilot: `as_is_discovery`
- Room: `Control Room`
- Frontier: `runtime-contracts`
- Fecha: 2026-05-05
- Workspace: `NuevoProyecto` local only

## Veredicto

PASS con una correccion operativa menor durante la auditoria.

El incremento mantiene equivalencia entre Codex, Claude, GitHub Copilot y LangChain para el Copiloto de Discovery AS-IS. No se encontraron credenciales reales, tokens persistidos, datos de cliente, datos de billing ni rutas locales sensibles en los artefactos revisados.

## Hallazgos

| Severidad | Estado | Hallazgo | Evidencia | Accion |
|---|---|---|---|---|
| P2 | Corregido | La prueba local de importacion de LangChain genero `__pycache__` bajo `dist/copilots`, lo que rompe release readiness porque el validador bloquea bytecode en artefactos de release. | `python tools/validate_copilot_factory.py` fallo inicialmente con 4 entradas `__pycache__`/`.pyc`. | Se eliminaron los dos `.pyc` exactos y los directorios vacios con comprobacion de ruta bajo `dist/copilots`; los validadores se reejecutaron con `PYTHONDONTWRITEBYTECODE=1`. |
| Informativo | Cerrado | Los conectores declaran nombres de variables, no valores de credenciales. | `dist/copilots/as_is_discovery/shared/spec.json`, `dist/copilots/as_is_discovery/github-copilot/mcp-placeholders.json`. | Sin parche requerido. |
| Informativo | Cerrado | LangChain valida entrada y evidencia, limita longitud/profundidad y redacta claves o valores sensibles antes de renderizar prompts. | `dist/copilots/_runtime_safety.py`, prueba sintetica de `render_prompt`. | Sin parche requerido. |
| Informativo | Cerrado | Equivalencia de runtime y presupuesto de prompts permanecen dentro de contrato. | Validadores de factory, prompt quality y runtime equivalence en PASS. | Sin parche requerido. |

## Parches hechos

- Eliminado bytecode cache generado durante la auditoria:
  - `dist/copilots/__pycache__/_runtime_safety.cpython-314.pyc`
  - `dist/copilots/as_is_discovery/langchain/__pycache__/agent.cpython-314.pyc`
  - directorios `__pycache__` vacios correspondientes
- Creado este informe:
  - `.codex-loop/factory/audits/task-028-safe-coding.md`

No se modificaron prompts, schemas ni contratos de runtime porque no habia malas practicas obvias que corregir en los archivos objetivo.

## Comandos ejecutados

- `Get-Command rg -ErrorAction SilentlyContinue | Select-Object -ExpandProperty Source`
- `git status --short`
  - Resultado: no aplica; este directorio no es un repo git.
- `rg --files dist/copilots/as_is_discovery generated .codex-loop/factory/audits`
- `Get-Content -Raw` sobre:
  - `dist/copilots/as_is_discovery/shared/spec.json`
  - `dist/copilots/as_is_discovery/shared/output_schema.json`
  - `dist/copilots/as_is_discovery/shared/codex_tool_protocol.json`
  - `dist/copilots/as_is_discovery/shared/claude_project_instructions.json`
  - `dist/copilots/as_is_discovery/codex/AGENT.md`
  - `dist/copilots/as_is_discovery/claude/AGENT.md`
  - `dist/copilots/as_is_discovery/github-copilot/copilot-agent.md`
  - `dist/copilots/as_is_discovery/github-copilot/mcp-placeholders.json`
  - `dist/copilots/as_is_discovery/langchain/agent.py`
  - `dist/copilots/_runtime_safety.py`
- Busqueda dirigida de secretos/rutas locales con `rg -n` para patrones tipo `ghp_`, `github_pat_`, `sk-`, `Bearer`, `AKIA`, private key y rutas de perfil local de Windows.
- Prueba sintetica de LangChain:
  - `render_prompt` redacto token, secreto local y dato de cliente.
  - `plan('   ', {})` devolvio `ValueError: LangChain request cannot be empty.`
- Limpieza controlada de bytecode cache con script Python local que valida `Path.resolve()` bajo `dist/copilots`.
- `$env:PYTHONDONTWRITEBYTECODE='1'; python tools/validate_copilot_factory.py`
  - PASS: 18 copilots, 50 agents, 50 tasks.
- `$env:PYTHONDONTWRITEBYTECODE='1'; python tools/validate_prompt_quality.py`
  - PASS: 18 copilots, 72 runtime prompts.
- `$env:PYTHONDONTWRITEBYTECODE='1'; python tools/validate_runtime_equivalence.py`
  - PASS: 18 copilots checked.
- Verificacion final:
  - `Get-ChildItem -LiteralPath 'dist/copilots' -Recurse -Directory -Filter '__pycache__'`
  - Sin resultados.
  - Busqueda final de secretos/rutas locales en artefactos afectados.
  - Sin resultados.

## Checklist defensivo

- Credenciales reales / tokens: PASS. Solo aparecen nombres de variables como `GITHUB_TOKEN`.
- Entradas de usuario: PASS. LangChain exige string no vacio, normaliza espacios y limita longitud.
- Evidencia de usuario: PASS. Tipos, profundidad, numero de items, longitud de claves y longitud de strings tienen limites.
- Auth/sesion/CORS: No aplica. El incremento revisado no expone servidor, sesion ni CORS.
- Aislamiento multi-tenant/SaaS: No aplica como runtime local; los datos `customer`, `tenant` y `billing` se tratan como sensibles y se redactan.
- Dependencias/scripts: PASS. No se detectaron scripts de instalacion/despliegue peligrosos en el alcance auditado.
- Billing: PASS. `mcp-placeholders.json` marca `billingDataAllowed: false` y no almacena credenciales.
- Trazabilidad/coste: PASS. Contrato `python_first_llm_sparse`, `max_unexplained_drift: 0` y validadores en PASS.

## Riesgos residuales

- Los validadores importan adaptadores Python; si se ejecutan sin `PYTHONDONTWRITEBYTECODE=1`, pueden volver a crear `__pycache__` y fallar la puerta de release readiness. Recomendacion: mantener esa variable en jobs locales/CI o excluir bytecode antes de empaquetar.
- No hay evidencia de conector GitHub real en esta auditoria local; el contrato lo trata correctamente como placeholder pendiente de activacion por operador.
