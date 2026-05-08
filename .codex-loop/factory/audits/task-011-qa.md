# Task 011 QA Audit

Fecha: 2026-05-04
Perfil: strict
Tarea: `[P1][factory_agent_11_cloud] Audits migration, target platform and modernization increments.`

## Resultado

PASS con parches.

El incremento ya deja evidencia verificable para `factory_agent_11_cloud` y `journey_to_cloud`: el contrato compartido exige `cloud_migration`, el validador lo comprueba, los cuatro runtimes siguen trazando al mismo `shared/spec.json`, y el coste de prompt permanece dentro del limite configurado.

## Hallazgos

1. P1 - Deriva entre auditoria cloud y output contract.
   - Evidencia: `dist/copilots/journey_to_cloud/shared/cloud_migration_audit.json` y `generated/factory-audit.json` exigian `cloud_migration`, pero `dist/copilots/journey_to_cloud/shared/output_schema.json` no lo requeria ni lo definia.
   - Impacto: la mision cloud quedaba descrita en la auditoria, pero no era exigible por el contrato de salida del copilot.
   - Estado: corregido.

2. P2 - El generador de prompts no conocia el contrato cloud.
   - Evidencia: `tools/elevate_copilot_prompts.py` no generaba `cloudMigrationAudit`, `cloud_migration_audit.json` ni schema cloud.
   - Impacto: una regeneracion podia perder el incremento de Task 011.
   - Estado: corregido.

3. P2 - Falta de test/regresion para el nuevo campo cloud.
   - Evidencia: `python tools/validate_copilot_factory.py` pasaba aunque el schema no exigia `cloud_migration`.
   - Impacto: el fallo podia repetirse sin bloquear el gate.
   - Estado: corregido en el validador.

## Parches Hechos

- `dist/copilots/journey_to_cloud/shared/output_schema.json`: requiere `cloud_migration`, sus 9 subcampos obligatorios y al menos 3 `migration_increments`.
- `dist/copilots/journey_to_cloud/shared/spec.json`, `langchain/agent_profile.json` y `langchain/agent.py`: sincronizados con el schema compartido.
- `dist/copilots/journey_to_cloud/{codex,claude,github-copilot}` y `shared/runtime_contract.md`: mantienen referencia compacta al schema compartido para no inflar coste.
- `generated/runtime-injection-map.json`: incluye el contrato `cloudMigrationAudit` con campos requeridos y runtime equivalence.
- `tools/elevate_copilot_prompts.py`: genera el contrato cloud y usa referencia compacta en prompts Markdown.
- `tools/validate_copilot_factory.py`: comprueba que `cloud_migration` sea requerido y que spec/profile/contract no deriven del schema compartido.
- `README.md`: documenta el artefacto `cloud_migration_audit.json`.

## Comandos Ejecutados

- `Get-Command rg -ErrorAction SilentlyContinue`
- `git status --short` (fallo esperado: no hay repositorio Git)
- `python tools/validate_copilot_factory.py`
- `python tools/validate_prompt_quality.py`
- `python tools/validate_runtime_equivalence.py`
- `python -B -` con `compile(...)` sobre `tools/elevate_copilot_prompts.py`, `tools/validate_copilot_factory.py` y `dist/copilots/journey_to_cloud/langchain/agent.py`
- `Get-ChildItem -Recurse -Directory -Filter __pycache__ tools,dist`

Nota: `python -m py_compile` creo `__pycache__`; se eliminaron los bytecode generados en `tools/__pycache__` y `dist/copilots/journey_to_cloud/langchain/__pycache__` antes de la verificacion final.

## Verificacion Final

- `python tools/validate_copilot_factory.py` -> PASS
- `python tools/validate_prompt_quality.py` -> PASS
- `python tools/validate_runtime_equivalence.py` -> PASS
- `compile(...)` sin bytecode -> PASS
- `__pycache__` en `tools` y `dist` -> ninguno

Evidencia clave:

- `generated/validation-report.json.cloudAuditor.pass`: `true`
- `schemasRequireCloudMigration`: `true`
- `cloudMigrationSchemaChecked`: `true`
- `negativeCasesDetected`: `true`
- `sampleTopRoute`: `journey_to_cloud`
- Prompt cost `journey_to_cloud/langchain`: growth `0.0977`, dentro del maximo `0.10`

## Riesgos Residuales

- No hay metadata Git local; la auditoria se hizo sobre el arbol de archivos disponible.
- No se activo ningun conector real (`github_mcp` queda como contrato de capacidad), asi que la evidencia cloud sigue siendo local/offline.
- El schema valida estructura minima; la calidad semantica de una decision real de plataforma sigue requiriendo evidencia de inventario, restricciones y revision humana antes de produccion.
