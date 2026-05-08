# Task 029 Safe-Coding / Privacy Review

## Alcance

- Tarea auditada: `[P1][copilot_owner_29_single_registry]`
- Copilot: `single_registry`
- Room: `Control Room`
- Frontier: `runtime-contracts`
- Fecha: 2026-05-05
- Workspace: `NuevoProyecto` local only

## Veredicto

PASS con una correccion operativa menor durante la auditoria.

El incremento mantiene equivalencia entre Codex, Claude, GitHub Copilot y LangChain para `Copiloto Registro Unico`. No se encontraron credenciales reales, tokens persistidos, datos de cliente, datos de billing ni rutas locales sensibles en los artefactos revisados.

## Hallazgos

| Severidad | Estado | Hallazgo | Evidencia | Accion |
|---|---|---|---|---|
| P2 | Corregido | La prueba local de importacion de LangChain genero `__pycache__` bajo `dist/copilots`, lo que rompe release readiness porque el validador bloquea bytecode en artefactos de release. | `python tools/validate_copilot_factory.py` fallo inicialmente con 4 entradas `__pycache__`/`.pyc`. | Se eliminaron los dos `.pyc` exactos y los directorios vacios; los validadores se reejecutaron con `PYTHONDONTWRITEBYTECODE=1`. |
| Informativo | Cerrado | Los conectores declaran nombres de variables, no valores de credenciales. | `dist/copilots/single_registry/shared/spec.json`, `dist/copilots/single_registry/github-copilot/mcp-placeholders.json`. | Sin parche de producto requerido. |
| Informativo | Cerrado | LangChain valida request/evidence y redacta datos sensibles antes de renderizar prompts. | `dist/copilots/single_registry/langchain/agent.py`, `dist/copilots/_runtime_safety.py`, prueba sintetica de `render_prompt`. | Sin parche de producto requerido. |
| Informativo | Cerrado | Equivalencia de runtime, schema compartido y presupuesto de prompts permanecen dentro de contrato. | Validadores de factory, prompt quality y runtime equivalence en PASS. | Sin parche de producto requerido. |

## Parches hechos

- Eliminado bytecode cache generado durante la auditoria:
  - `dist/copilots/__pycache__/_runtime_safety.cpython-314.pyc`
  - `dist/copilots/single_registry/langchain/__pycache__/agent.cpython-314.pyc`
  - directorios `__pycache__` vacios correspondientes
- Creado este informe:
  - `.codex-loop/factory/audits/task-029-safe-coding.md`

No se modificaron prompts, schemas ni contratos de runtime porque no habia malas practicas obvias que corregir en los archivos objetivo.

## Comandos ejecutados

- `Get-Command rg -ErrorAction SilentlyContinue | Select-Object -ExpandProperty Source`
- `git status --short`
  - Resultado: no aplica; este directorio no es un repo git.
- `Get-Content -Raw` sobre:
  - `dist/copilots/single_registry/shared/spec.json`
  - `dist/copilots/single_registry/shared/output_schema.json`
  - `dist/copilots/single_registry/codex/AGENT.md`
  - `dist/copilots/single_registry/claude/AGENT.md`
  - `dist/copilots/single_registry/github-copilot/copilot-agent.md`
  - `dist/copilots/single_registry/github-copilot/copilot-profile.json`
  - `dist/copilots/single_registry/github-copilot/mcp-placeholders.json`
  - `dist/copilots/single_registry/langchain/agent.py`
  - `dist/copilots/single_registry/langchain/agent_contract.json`
  - `dist/copilots/single_registry/langchain/agent_profile.json`
  - `dist/copilots/_runtime_safety.py`
- Busqueda dirigida de secretos/rutas locales en los archivos objetivo y reportes generados para patrones tipo `ghp_`, `github_pat_`, `sk-`, `Bearer`, `AKIA`, private key y rutas de perfil local.
  - Resultado: sin coincidencias en el alcance auditado.
- Prueba sintetica de LangChain:
  - `render_prompt` no conservo el token sintetico, el PAT sintetico, el bearer sintetico, la ruta local sintetica ni `customer_id`.
  - `score`/`audit` devolvieron `ValueError` comprensible para request no string, request vacio y evidence no dict.
- `python tools/validate_copilot_factory.py`
  - Resultado inicial: FAIL por `__pycache__` generado por la prueba local.
- Limpieza controlada de bytecode cache con script Python local que valida `Path.resolve()` bajo el workspace antes de eliminar.
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

- Credenciales reales / tokens: PASS. Solo aparecen nombres de variables como `GITHUB_TOKEN` y placeholders vacios.
- Entradas de usuario: PASS. LangChain exige string no vacio, normaliza espacios y limita longitud.
- Evidencia de usuario: PASS. Tipos, profundidad, numero de items, longitud de claves y longitud de strings tienen limites.
- Auth/sesion/CORS: No aplica. El incremento revisado no expone servidor, sesion ni CORS.
- Aislamiento multi-tenant/SaaS: No aplica como runtime local; claves `customer`, `tenant` y `billing` se tratan como sensibles y se redactan.
- Dependencias/scripts: PASS. No se detectaron scripts de instalacion/despliegue peligrosos en el alcance auditado.
- Billing: PASS. `mcp-placeholders.json` marca `billingDataAllowed: false` y no almacena credenciales.
- Trazabilidad/coste: PASS. Contrato `python_first_llm_sparse`, `promptBodiesStored: false`, `maxUnexplainedDrift: 0` y validadores en PASS.

## Riesgos residuales

- Si se importan adaptadores Python sin `PYTHONDONTWRITEBYTECODE=1`, Python puede volver a crear `__pycache__` bajo `dist/copilots` y bloquear la puerta de release readiness.
- No hay evidencia de conector GitHub real en esta auditoria local; el contrato lo trata correctamente como placeholder pendiente de activacion por operador.
