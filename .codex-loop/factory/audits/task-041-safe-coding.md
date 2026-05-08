# Task 041 Safe-Coding / Privacy Review

## Alcance

- Copiloto auditado: `journey_to_cloud`.
- Superficies revisadas: `dist/copilots/journey_to_cloud/shared/spec.json`, runtimes Codex/Claude/GitHub Copilot, `dist/copilots/journey_to_cloud/langchain/agent.py`, artefactos `generated/*` listados y reportes de validacion.
- Perfil: strict, defensive product quality, sin credenciales reales ni datos de cliente.

## Hallazgos

| Severidad | Hallazgo | Estado |
|---|---|---|
| Low | La trazabilidad de los comandos obligatorios de equivalencia runtime no estaba explicitada en las tarjetas de los runtimes Markdown ni en el fallback local de LangChain, aunque el contrato compartido ya existia en `spec.json`. | Corregido |
| Info | `GITHUB_TOKEN` aparece solo como nombre de variable de entorno/placeholder. No se detectaron tokens, claves privadas, secretos reales ni rutas locales sensibles en el barrido de alta confianza. | Sin parche |
| Info | El runtime LangChain usa `validate_request`, `validate_evidence` y `redact_value` desde `_runtime_safety.py`; hay limites de tamano/profundidad, normalizacion de request y redaccion por claves/patrones sensibles. | Sin parche |

## Parches hechos

- `dist/copilots/journey_to_cloud/codex/AGENT.md`: agregado el bloque `Required verification commands` al contrato de equivalencia runtime.
- `dist/copilots/journey_to_cloud/claude/AGENT.md`: agregado el mismo bloque para mantener equivalencia documental.
- `dist/copilots/journey_to_cloud/github-copilot/copilot-agent.md`: agregado el mismo bloque para mantener equivalencia documental.
- `dist/copilots/journey_to_cloud/langchain/agent.py`: agregado `validationCommands` al fallback `RUNTIME_EQUIVALENCE_CONTRACT`.

Nota: se probo inicialmente mover el tercer comando al artefacto `cloud_migration_audit.json`, pero el validador lo rechazo como drift del contrato de fase cloud. Se dejo ese artefacto con su contrato canonico y se documento el tercer comando en el contrato runtime, que es su frontera correcta.

## Comandos ejecutados

- `Get-Command rg -ErrorAction SilentlyContinue`
- `git status --short` -> no aplica: el workspace no es un repositorio Git.
- Barrido con `Select-String` para patrones de secretos/rutas locales en `dist/copilots/journey_to_cloud` y `generated`.
- `python tools/validate_copilot_factory.py` -> PASS final: 18 copilots, 50 agents, 50 tasks.
- `python tools/validate_prompt_quality.py` -> PASS final: 18 copilots, 72 runtime prompts.
- `python tools/validate_runtime_equivalence.py` -> PASS final: 18 copilots checked.

## Riesgos residuales

- No hay app SaaS ni capa auth/CORS en los archivos revisados; aislamiento tenant queda como requisito documental dentro de impactos de datos/seguridad, no como control ejecutable.
- Los reportes generados dependen de los validadores para evitar prompt bodies, secretos y drift; mantener los tres validadores como gate obligatorio antes de release.
- El workspace no tiene metadatos Git disponibles, por lo que la revision se baso en contenido local y validadores, no en diff formal.
