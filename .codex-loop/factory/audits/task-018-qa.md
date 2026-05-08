# QA Audit Task 018

Fecha: 2026-05-04
Perfil: strict
Tarea auditada: `[P1][factory_agent_18_mcp] Audits connector declarations and env placeholders.`

## Veredicto

Pass con parches aplicados.

La mision MCP queda reflejada en artefactos verificables: `config/.env.example`, `config/mcp-connectors.example.json`, `tools/validate_copilot_factory.py` y `generated/validation-report.json#/mcpConnectorAuditor`.

## Hallazgos

- P1 corregido: el auditor MCP validaba presencia y formato de `allowed_operations` y `denied_operations`, pero no fallaba si una operacion aparecia simultaneamente como permitida y denegada. Eso debilitaba el contrato de access control para conectores.
- P2 corregido: el reporte de negativos MCP podia duplicar el detector `non-empty env placeholder`, reduciendo claridad operativa.
- P2 corregido: `README.md` y `OPERATING_SYSTEM.md` no documentaban la nueva superficie `config/.env.example` + `config/mcp-connectors.example.json` ni el gate `mcpConnectorAuditor`.
- Sin superficie UI/frontend. La revision de UX aplica como ergonomia operativa: nombres claros, reportes accionables, rutas de evidencia y comandos reproducibles.
- Sin secretos reales, datos de cliente ni billing encontrados en los artefactos revisados. Los env examples se mantienen con valores vacios.

## Parches Hechos

- `tools/validate_copilot_factory.py`: el detector MCP ahora falla ante conflictos entre `allowed_operations` y `denied_operations`.
- `tools/validate_copilot_factory.py`: se agregaron negativos `allowed_denied_operation_conflict` y `risky_allowed_operation` al auditor MCP.
- `tools/validate_copilot_factory.py`: se deduplican los detectores negativos para mantener reportes mas claros.
- `README.md`: se documentaron los contratos `config/.env.example`, `config/mcp-connectors.example.json` y `generated/validation-report.json#/mcpConnectorAuditor`.
- `OPERATING_SYSTEM.md`: se amplio la politica MCP para placeholders unicos, ausencia de huerfanos sensibles, runtimes equivalentes y coherencia de operaciones.
- `generated/validation-report.*` y `generated/prompt-quality-report.*`: regenerados por los gates finales.

## Comandos Ejecutados

- `Get-Command rg -ErrorAction SilentlyContinue`: `rg` disponible.
- `git status --short`: fallo esperado; el workspace no contiene metadata Git.
- `python tools/validate_copilot_factory.py`: PASS inicial.
- `python tools/validate_prompt_quality.py`: PASS inicial.
- `python -m py_compile tools/validate_copilot_factory.py`: sintaxis correcta, pero genero `tools/__pycache__`.
- `python tools/validate_copilot_factory.py`: FAIL esperado tras el bytecode generado; el gate bloqueo `tools/__pycache__`.
- Limpieza segura con APIs .NET tras comprobar que `tools/__pycache__` resolvia dentro del workspace.
- `python -B tools/validate_copilot_factory.py`: PASS.
- `python -B tools/validate_prompt_quality.py`: PASS.
- `python tools/validate_copilot_factory.py`: PASS final, 18 copilots, 50 agents, 50 tasks.
- `python tools/validate_prompt_quality.py`: PASS final, 18 copilots, 72 runtime prompts.
- `Get-ChildItem -Path . -Directory -Recurse -Filter __pycache__`: sin resultados finales.
- `rg` sobre `generated/validation-report.json`: confirma negativos MCP nuevos con `passedExpectation=true`.

## Riesgos Residuales

- No hay metadata Git local; la trazabilidad de diff depende de este informe y de los reportes generados.
- La auditoria valida contratos locales y placeholders, no conectividad real contra GitHub, SonarQube o Confluence.
- La activacion real de conectores sigue fuera de repo y requiere operador, secreto local y aprobacion explicita para escrituras.
