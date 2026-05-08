# Safe-coding/privacy audit - task 026

## Alcance

- Tarea auditada: `[P1][copilot_owner_26_devex] Room: Control Room | Goal: own product quality for Copiloto DevEx.`
- Archivos revisados: `dist/copilots/devex/shared/spec.json`, `dist/copilots/devex/codex/AGENT.md`, `dist/copilots/devex/claude/AGENT.md`, `dist/copilots/devex/github-copilot/copilot-agent.md`, `dist/copilots/devex/langchain/agent.py`, artefactos `generated/*` declarados para la tarea y contratos auxiliares de DevEx.
- Enfoque: secretos, rutas locales, placeholders de credenciales, datos de cliente/billing, validacion de entradas, trazabilidad, control de costes y equivalencia runtime entre `codex`, `claude`, `github-copilot` y `langchain`.

## Hallazgos

| Severidad | Estado | Hallazgo |
| --- | --- | --- |
| Media | Corregido | `dist/copilots/devex/langchain/agent.py` cargaba `_runtime_safety` despues de anadir el directorio del helper al final de `sys.path`. En un runtime Python con otro modulo `_runtime_safety` ya visible, podia cargar el helper equivocado y debilitar redaccion/validacion. |
| Info | Revisado | No se detectaron credenciales reales, tokens, claves privadas, rutas locales absolutas, datos de cliente ni datos de billing en los artefactos DevEx auditados. `GITHUB_TOKEN` aparece solo como nombre de variable de entorno/placeholder. |
| Info | Revisado | Los placeholders MCP de GitHub estan deshabilitados por defecto, no almacenan valores de credencial, bloquean datos de cliente/billing y requieren activacion/aprobacion operativa para writes. |
| Info | Revisado | Los reportes generados declaran `promptBodiesStored=false`, `maxUnexplainedDrift=0`, runtime coverage para `codex`, `claude`, `github-copilot`, `langchain` y casos negativos de secretos/rutas locales. |
| Info | No aplica | No hay servicio HTTP, auth/sesion, CORS, permisos SaaS, aislamiento tenant ni billing real en este incremento; el alcance es local, de prompts/contratos/adaptadores y reportes generados. |

## Parches hechos

- `dist/copilots/devex/langchain/agent.py`: se cambio la preparacion de import para anteponer explicitamente `dist/copilots` antes de importar `_runtime_safety`, priorizando el helper generado del workspace sobre modulos homonimos ya presentes en `sys.path`.
- Se genero este artefacto de auditoria en `.codex-loop/factory/audits/task-026-safe-coding.md`.

## Comandos ejecutados

- `Get-Command rg -ErrorAction SilentlyContinue` -> `rg` disponible como shim local; el shim no acepto `-i`, por lo que el escaneo se hizo con `Select-String`.
- `git status --short` -> no hay metadatos git en este workspace.
- `Get-Content -Raw` sobre los prompts/contratos DevEx y reportes generados -> revision manual de contratos y politica de datos.
- `Select-String` con patrones de tokens, claves privadas, bearer tokens, claves cloud y rutas locales de perfil Windows sobre `dist/copilots/devex` y `generated` -> sin hallazgos.
- `python tools\validate_copilot_factory.py` -> PASS: 18 copilots, 50 agents, 50 tasks.
- `python tools\validate_prompt_quality.py` -> PASS: 18 copilots, 72 runtime prompts.
- `python tools\validate_runtime_equivalence.py` -> PASS: 18 copilots checked.
- `python dist\copilots\devex\langchain\agent.py "build implementation plan validation"` -> ejecucion local correcta; el agente devuelve contrato DevEx y evidencia faltante sin exponer secretos.
- Limpieza defensiva de bytecode generado por la prueba directa del agente -> `dist/copilots/__pycache__` eliminado y comprobado ausente.
- Reejecucion final de `python tools\validate_copilot_factory.py`, `python tools\validate_prompt_quality.py` y `python tools\validate_runtime_equivalence.py` -> PASS en los tres validadores.
- Barrido final acotado con `Select-String` sobre `dist/copilots/devex`, `generated` y este informe -> sin secretos ni rutas locales absolutas en artefactos de la tarea.

## Riesgos residuales

- La carpeta no expone metadatos git, asi que la trazabilidad se apoya en artefactos locales, validadores y este informe.
- El parche esta aplicado en el artefacto DevEx generado; si una plantilla externa regenera `agent.py`, conviene confirmar que conserva el prepend defensivo del helper `_runtime_safety`.
- Los conectores siguen siendo placeholders. Cualquier activacion real de `github_mcp` debe usar variables de entorno fuera del repo, aprobacion operativa y logs con redaccion.
