# QA Audit Task 041 - Copiloto Journey to Cloud

Fecha: 2026-05-05
Perfil: strict
Alcance: `dist/copilots/journey_to_cloud/shared/spec.json`, prompts de Codex/Claude/GitHub Copilot, `dist/copilots/journey_to_cloud/langchain/agent.py`, artefactos shared y reportes generados por los validadores.

## Hallazgos

- P2 corregido: `dist/copilots/journey_to_cloud/langchain/agent.py` exponia `runtime_contract()` con una version resumida de `runtimeEquivalenceContract` y `cloudMigrationAudit`. La API LangChain devolvia claves abreviadas (`assertions`) y `sourceOfTruth = shared/spec.json`, mientras el contrato canonico en `shared/spec.json` exige `sourceOfTruth = dist/copilots/journey_to_cloud/shared/spec.json`, `validationCommands`, `requiredRuntimeAssertions`, `costControl`, `auditSource` y `requiredCloudMigrationFields`. Esto dejaba los prompts Markdown coherentes, pero debilitaba la equivalencia real para consumidores Python/LangChain.
- Los validadores oficiales pasaban antes del parche, por lo que el fallo era de calidad practica de runtime-contracts, no de sintaxis ni de cobertura declarativa.
- Sin hallazgos de UX: no hay UI, formularios, navegacion ni estados visuales en este incremento; la superficie auditada es contrato, prompts, schema, Python runtime y trazabilidad.
- Sin hallazgos de secretos: los artefactos revisados declaran solo `GITHUB_TOKEN` como nombre de variable y usan placeholders; no se observaron valores de credenciales, billing ni datos de cliente.

## Parches Hechos

- Actualizado `dist/copilots/journey_to_cloud/langchain/agent.py` para que `JourneyToCloudAgent.runtime_contract()` lea `dist/copilots/journey_to_cloud/shared/spec.json` en tiempo de ejecucion y devuelva `runtimeEquivalenceContract` y `cloudMigrationAudit` canonicos, con fallback a las constantes locales si el spec no estuviera disponible.
- Verificado que el cambio no rompe el presupuesto de coste: `journey_to_cloud/langchain` queda en 17,974 chars, growth ratio 0.0849, limite 0.10.
- Limpiados los directorios `__pycache__` creados por el smoke local de importacion para no contaminar artefactos de release.

## Comandos Ejecutados

- `Get-Command rg -ErrorAction SilentlyContinue | Select-Object -ExpandProperty Source` -> disponible como shim local.
- `git status --short` -> no aplicable: el workspace no es un repositorio Git.
- Lectura de `shared/spec.json`, `shared/output_schema.json`, `shared/cloud_migration_audit.json`, prompts runtime y `langchain/agent.py` -> revisados.
- `python tools/validate_copilot_factory.py` -> PASS: 18 copilots, 50 agents, 50 tasks.
- `python tools/validate_prompt_quality.py` -> PASS: 18 copilots, 72 runtime prompts.
- `python tools/validate_runtime_equivalence.py` -> PASS: 18 copilots checked.
- Smoke dirigido con `python -B`: `build_agent().runtime_contract()["runtime_equivalence"] == spec["runtimeEquivalenceContract"]` -> `True`.
- Smoke dirigido con `python -B`: `requiredCloudMigrationFields` presente en `runtime_contract()["cloud_migration_audit"]` -> `True`.
- Syntax smoke sin bytecode con `python -B` y `compile(...)` sobre `dist/copilots/journey_to_cloud/langchain/agent.py` -> `syntax_ok=True`.

## Riesgos Residuales

- Los validadores actuales no detectaban que `runtime_contract()` devolviera una version resumida del contrato; el parche corrige `journey_to_cloud`, pero conviene endurecer `validate_runtime_equivalence.py` para comparar tambien la API runtime de LangChain contra `spec.json`.
- Los reportes en `generated/` se reescriben al ejecutar validadores con timestamps/digests nuevos; es esperado para evidencia reproducible.
