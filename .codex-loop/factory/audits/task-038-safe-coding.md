# Safe-Coding / Privacy Audit - Task 038

## Alcance

- Copilot auditado: `qa_general` / Copiloto QA General.
- Archivos revisados: `dist/copilots/qa_general/shared/spec.json`, adaptadores `codex`, `claude`, `github-copilot`, `langchain`, contratos compartidos y reportes `generated/*` declarados por la tarea.
- Enfoque: privacidad, credenciales, validacion de entradas, permisos de conectores, aislamiento de datos y equivalencia runtime.

## Hallazgos

| Severidad | Hallazgo | Evidencia | Estado |
|---|---|---|---|
| Info | No se detectaron secretos reales, tokens con forma valida ni rutas absolutas locales en los artefactos declarados. | Busquedas `rg` sobre `dist/copilots/qa_general` y reportes `generated/*` de la tarea sin coincidencias para patrones de secretos/rutas locales. | Sin parche requerido |
| Info | El contrato mantiene controles de gobierno y trazabilidad: no secretos en repo, aprobacion humana para seguridad/release/conectores y `maxUnexplainedDrift = 0`. | `dist/copilots/qa_general/shared/spec.json` declara `noSecretsInRepo`, `humanApprovalForWrites`, `promptBodiesStored: false`, `evidenceMode: paths_refs_summaries_and_schema_fields_only` y campos de traza obligatorios. | Sin parche requerido |
| Info | El placeholder GitHub MCP no almacena credenciales ni datos de cliente/billing y requiere activacion/aprobacion del operador. | `dist/copilots/qa_general/github-copilot/mcp-placeholders.json` declara `defaultEnabled: false`, `credentialValue: ""`, `credentialValuesStored: false`, `customerDataAllowed: false`, `billingDataAllowed: false`, `operatorApprovalRequiredForWrites: true`. | Sin parche requerido |
| Info | El adaptador LangChain valida y normaliza entradas, limita tamano/profundidad de evidencia y redacta claves/datos sensibles antes de construir prompts. | `dist/copilots/_runtime_safety.py` y `dist/copilots/qa_general/langchain/agent.py` usan `validate_request`, `validate_evidence` y `redact_value` en `render_prompt`. | Sin parche requerido |

## Parches hechos

- No se modificaron los contratos ni adaptadores del copilot porque no aparecieron malas practicas obvias relacionadas con la tarea.
- Se agrego este informe obligatorio: `.codex-loop/factory/audits/task-038-safe-coding.md`.

## Comandos ejecutados

- `Get-Command rg -ErrorAction SilentlyContinue`
- `git status --short` (sin repo Git en esta carpeta)
- `Get-Content -Raw` sobre los contratos y adaptadores objetivo.
- `rg` para patrones de secretos, tokens, claves privadas, bearer tokens y rutas locales absolutas en `dist/copilots/qa_general` y reportes `generated/*` declarados.
- `python tools/validate_copilot_factory.py` -> PASS.
- `python tools/validate_prompt_quality.py` -> PASS.
- `python tools/validate_runtime_equivalence.py` -> PASS.
- Prueba manual LangChain de redaccion/validacion de entrada -> PASS tras corregir el harness de import dinamico.

## Riesgos residuales

- No hay verificacion de conectores reales porque la tarea y los artefactos mantienen MCP como placeholder local sin credenciales.
- La carpeta no es un repositorio Git, por lo que no hay diff formal; la auditoria se baso en el estado local del workspace y validadores generados.
- Los reportes `generated/*` contienen fixtures negativos y texto de auditoria; se revisaron como artefactos defensivos, no como datos reales de cliente.
