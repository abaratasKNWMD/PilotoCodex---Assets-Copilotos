# Safe-coding/privacy audit - task 024

## Alcance

- Tarea auditada: `[P1][factory_agent_24_matrix] Maintains the SDLC x Copilot x Runtime matrix.`
- Archivos revisados: `tools/validate_copilot_factory.py`, `tools/validate_prompt_quality.py`, `tools/validate_runtime_equivalence.py` y los reportes `generated/*` listados para la tarea.
- Enfoque: secretos, rutas locales, placeholders de credenciales, datos de cliente/billing, validacion de entradas, trazabilidad de la matriz y equivalencia entre `codex`, `claude`, `github-copilot` y `langchain`.

## Hallazgos

| Severidad | Estado | Hallazgo |
| --- | --- | --- |
| Low | Corregido | `tools/validate_prompt_quality.py` usaba `id` del catalogo para construir rutas de runtime sin validarlo antes como segmento seguro. Se agrego validacion defensiva y error comprensible antes de leer `dist/copilots/<id>`. |
| Low | Corregido | Los detectores de secretos de `tools/validate_copilot_factory.py` y `tools/validate_prompt_quality.py` eran mas estrechos que los de equivalencia runtime. Se ampliaron para cubrir patrones comunes de VCS, cloud, JWT, bearer, Slack y bloques de clave privada sin almacenar valores reales. |
| Info | Revisado | No se detectaron credenciales reales, valores con forma de secreto, rutas locales absolutas, datos de cliente ni datos de billing en los reportes `generated/*` auditados. Los matches residuales son nombres de variables, texto de politica o patrones defensivos en codigo. |
| Info | No aplica | No hay servicio HTTP, auth/sesion, CORS, permisos SaaS, aislamiento tenant ni billing real en este incremento; el alcance es local, de validadores y artefactos de matriz. |

## Parches hechos

- Actualizado `tools/validate_prompt_quality.py` con `SAFE_COPILOT_ID_RE`, validacion de entradas de catalogo y rechazo de IDs no seguros antes de construir rutas.
- Ampliados los patrones de deteccion de secretos en `tools/validate_prompt_quality.py`.
- Agregado caso negativo `expanded_secret_patterns` en `tools/validate_prompt_quality.py` para que el reporte pruebe que los detectores ampliados funcionan sin exponer payloads.
- Ampliados los patrones de deteccion de secretos en `tools/validate_copilot_factory.py` para mantener consistencia con el auditor de equivalencia runtime.
- Regenerados los reportes de `generated/` mediante los validadores requeridos.

## Comandos ejecutados

- `Get-Command rg -ErrorAction SilentlyContinue` -> `rg` disponible como shim local.
- `git status --short` -> no hay metadatos git en este workspace.
- `Select-String` sobre archivos de alcance para patrones de secretos, rutas locales absolutas y terminos sensibles.
- `python tools/validate_copilot_factory.py` -> PASS: 18 copilots, 50 agents, 50 tasks.
- `python tools/validate_prompt_quality.py` -> PASS: 18 copilots, 72 runtime prompts.
- `python tools/validate_runtime_equivalence.py` -> PASS: 18 copilots checked.
- `Select-String` final sobre `generated/*` auditados -> sin coincidencias de secretos reales ni rutas locales absolutas.

## Riesgos residuales

- Los detectores son controles estaticos locales; no sustituyen escaneo de secretos corporativo antes de publicar fuera del workspace.
- La ausencia de repositorio git limita la trazabilidad a artefactos locales y snapshots de `.codex-loop`.
- Los conectores y credenciales siguen modelados como placeholders; cualquier activacion real debe mantenerse fuera del repo y con aprobacion operativa.
