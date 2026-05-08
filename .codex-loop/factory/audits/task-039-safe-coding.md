# Safe-Coding / Privacy Audit - Task 039

## Alcance

- Copilot auditado: `sonarqube_remediation` / Copiloto SonarQube Remediacion.
- Archivos revisados: `dist/copilots/sonarqube_remediation/shared/spec.json`, adaptadores `codex`, `claude`, `github-copilot`, `langchain`, contratos compartidos y reportes `generated/*` declarados por la tarea.
- Enfoque: privacidad, credenciales, validacion de entradas, permisos de conectores, aislamiento de datos, scripts/dependencias y equivalencia runtime.

## Hallazgos

| Severidad | Hallazgo | Evidencia | Estado |
|---|---|---|---|
| Medium | El adaptador LangChain cargaba el helper `_runtime_safety` despues de las rutas ya presentes en `sys.path`, lo que podia permitir sombreado accidental del helper de seguridad. | `dist/copilots/sonarqube_remediation/langchain/agent.py` usaba `sys.path.append(...)` antes de importar `redact_value`, `validate_evidence` y `validate_request`. | Parcheado |
| Info | No se detectaron secretos reales, tokens con forma valida, bearer/JWT ni rutas absolutas locales en los archivos auditados. | Escaneo acotado con `Select-String` sobre los archivos de la tarea y reportes generados, sin coincidencias para patrones de credencial ni rutas absolutas de usuario Windows. | Sin parche requerido |
| Info | Los conectores se mantienen como contratos/placeholders, sin credenciales ni activacion por defecto. | `spec.json` declara solo nombres `GITHUB_TOKEN` y `SONARQUBE_TOKEN`; `mcp-placeholders.json` mantiene `defaultEnabled: false`, `credentialValue: ""`, `credentialValuesStored: false`, `customerDataAllowed: false` y `billingDataAllowed: false`. | Sin parche requerido |
| Info | La entrada y evidencia del runtime LangChain estan validadas y redactadas antes de construir prompts. | `dist/copilots/_runtime_safety.py` limita longitud/profundidad/tipos y `agent.py` usa `validate_request`, `validate_evidence` y `redact_value` en `render_prompt`. | Sin parche requerido |

## Parches hechos

- Cambiado `sys.path.append(...)` por `sys.path.insert(0, ...)` en `dist/copilots/sonarqube_remediation/langchain/agent.py` para priorizar el helper local `dist/copilots/_runtime_safety.py` frente a posibles modulos homonimos en rutas previas.
- Se agrego este informe obligatorio: `.codex-loop/factory/audits/task-039-safe-coding.md`.

## Comandos ejecutados

- `Get-Command rg -ErrorAction SilentlyContinue`
- `git status --short` (la carpeta actual no es un repositorio Git)
- `Get-Content -Raw` sobre contratos, adaptadores y reportes objetivo.
- `rg --ignore-case ...` y `Select-String` para patrones de secretos, tokens, claves privadas, bearer/JWT y rutas locales absolutas.
- `python tools/validate_copilot_factory.py` -> PASS.
- `python tools/validate_prompt_quality.py` -> PASS.
- `python tools/validate_runtime_equivalence.py` -> PASS.

## Riesgos residuales

- No se verificaron conectores reales de GitHub/SonarQube porque los artefactos auditados declaran placeholders locales sin credenciales.
- La carpeta no tiene metadatos Git, por lo que la revision se baso en archivos locales y validadores, no en un diff formal.
- Los reportes `generated/*` contienen casos negativos esperados de validacion; se revisaron como fixtures defensivos, no como datos reales de cliente.
