# Task 030 Safe-Coding / Privacy Review

## Alcance

- Tarea auditada: `[P1][copilot_owner_30_firefly_v5]`
- Copilot: `firefly_v5`
- Room: `Control Room`
- Frontier: `runtime-contracts`
- Fecha: 2026-05-05
- Workspace: `NuevoProyecto` local only

## Veredicto

PASS sin parche de producto.

El incremento mantiene equivalencia entre Codex, Claude, GitHub Copilot y LangChain para `Copiloto Firefly v5`. No se encontraron credenciales reales, tokens persistidos, datos de cliente, datos de billing ni rutas locales sensibles en los artefactos revisados.

## Hallazgos

| Severidad | Estado | Hallazgo | Evidencia | Accion |
|---|---|---|---|---|
| Informativo | Cerrado | Los conectores estan declarados como contratos de capacidad, no como credenciales. | `dist/copilots/firefly_v5/shared/spec.json`; `dist/copilots/firefly_v5/github-copilot/mcp-placeholders.json` usa placeholders vacios, `defaultEnabled: false`, `credentialValuesStored: false`, `customerDataAllowed: false` y `billingDataAllowed: false`. | Sin parche de producto requerido. |
| Informativo | Cerrado | El adaptador LangChain valida entrada y evidencia, limita tamano/profundidad y redacta claves o valores sensibles antes de renderizar prompts. | `dist/copilots/firefly_v5/langchain/agent.py`; `dist/copilots/_runtime_safety.py`; prueba sintetica de `render_prompt`. | Sin parche de producto requerido. |
| Informativo | Cerrado | La equivalencia de runtime, schema compartido, trazabilidad y control de coste permanecen dentro de contrato. | `python tools/validate_copilot_factory.py`, `python tools/validate_prompt_quality.py`, `python tools/validate_runtime_equivalence.py` en PASS. | Sin parche de producto requerido. |
| Informativo | Cerrado | El arnes inicial de prueba dinamica fallo por no registrar el modulo en `sys.modules` antes de aplicar `dataclass`; no fue un fallo del producto. | Primer comando sintetico con `importlib.util.spec_from_file_location` devolvio `AttributeError` dentro de `dataclasses.py`. | Se repitio la prueba con importacion normal desde el directorio del adaptador. |

## Parches hechos

- Creado este informe:
  - `.codex-loop/factory/audits/task-030-safe-coding.md`

No se modificaron prompts, schemas, contratos ni adaptadores de producto porque no habia una mala practica obvia que corregir en el alcance auditado.

## Comandos ejecutados

- `Get-Command rg -ErrorAction SilentlyContinue | Select-Object -ExpandProperty Source`
  - Resultado: `rg` disponible como shim local en `.codex-loop/tool-shims/rg.ps1`.
- `git status --short`
  - Resultado: no aplica; este directorio no es un repo Git.
- `Get-ChildItem -Path dist\copilots\firefly_v5 -Recurse`
- `Get-Content -Raw` sobre:
  - `dist/copilots/firefly_v5/shared/spec.json`
  - `dist/copilots/firefly_v5/shared/output_schema.json`
  - `dist/copilots/firefly_v5/shared/runtime_contract.md`
  - `dist/copilots/firefly_v5/shared/implementation_plan_audit.json`
  - `dist/copilots/firefly_v5/codex/AGENT.md`
  - `dist/copilots/firefly_v5/claude/AGENT.md`
  - `dist/copilots/firefly_v5/github-copilot/copilot-agent.md`
  - `dist/copilots/firefly_v5/github-copilot/mcp-placeholders.json`
  - `dist/copilots/firefly_v5/langchain/agent.py`
  - `dist/copilots/firefly_v5/langchain/agent_contract.json`
  - `dist/copilots/_runtime_safety.py`
- Busqueda dirigida de secretos/rutas locales en `dist/copilots/firefly_v5/**` y `generated/**` para patrones tipo `sk-`, `github_pat_`, `ghp_`, `glpat-`, `AKIA`, `ASIA`, `AIza`, `xoxb-`, `Bearer`, private key y rutas de perfil local.
  - Resultado: sin coincidencias en el alcance auditado.
- `python tools/validate_copilot_factory.py`
  - PASS: 18 copilots, 50 agents, 50 tasks.
- `python tools/validate_prompt_quality.py`
  - PASS: 18 copilots, 72 runtime prompts.
- `python tools/validate_runtime_equivalence.py`
  - PASS: 18 copilots checked.
- Prueba sintetica de privacidad de LangChain con `PYTHONDONTWRITEBYTECODE=1`.
  - Primer intento con arnes de importacion dinamica: FAIL por arnes, no por producto.
  - Segundo intento con importacion normal: PASS. `render_prompt` no conservo token sintetico, PAT sintetico, ruta local sintetica, `customer_id` ni `access_token`; `score`/`audit` devolvieron `ValueError` comprensible para request no string, request vacio y evidence no dict.
- `Get-ChildItem -LiteralPath dist\copilots -Recurse -Directory -Filter __pycache__`
  - Resultado: sin caches de bytecode generadas.

## Checklist defensivo

- Credenciales reales / tokens: PASS. Solo aparecen nombres de variables como `GITHUB_TOKEN` y `SONARQUBE_TOKEN`; los placeholders de MCP no almacenan valores.
- Entradas de usuario: PASS. LangChain exige string no vacio, normaliza espacios y limita longitud.
- Evidencia de usuario: PASS. Tipos, profundidad, numero de items, longitud de claves y longitud de strings tienen limites; claves sensibles se sustituyen por `[REDACTED]`.
- Auth/sesion/CORS: No aplica. El incremento revisado no expone servidor, sesion, cookies ni politica CORS.
- Aislamiento multi-tenant/SaaS: No aplica como runtime local. Aun asi, claves `customer`, `tenant` y `billing` se tratan como sensibles en `_runtime_safety.py`.
- Dependencias/scripts: PASS. El adaptador LangChain no tiene dependencia dura de LangChain ni ejecuta instalacion/despliegue.
- Billing: PASS. `mcp-placeholders.json` marca `billingDataAllowed: false` y no almacena credenciales.
- Trazabilidad/coste: PASS. Contrato `python_first_llm_sparse`, `promptBodiesStored: false`, `maxUnexplainedDrift: 0` y validadores en PASS.

## Riesgos residuales

- No se activo ningun conector GitHub o SonarQube real durante esta auditoria local; cualquier uso con credenciales reales debe mantener activacion por operador, redaccion de logs y evidencia pendiente cuando el conector no este disponible.
- Si se importan adaptadores Python sin `PYTHONDONTWRITEBYTECODE=1`, Python podria crear `__pycache__` bajo `dist/copilots`; esta auditoria verifico que no quedaron caches tras la prueba.
