# Safe-Coding / Privacy Audit Task 018

Fecha: 2026-05-04
Perfil: strict
Tarea auditada: `[P1][factory_agent_18_mcp] Audits connector declarations and env placeholders.`
Frontera: sensitive-data

## Veredicto

Pass con parche defensivo aplicado.

La mision MCP queda reflejada en artefactos ejecutables: `config/.env.example`, `config/mcp-connectors.example.json`, `tools/validate_copilot_factory.py` y `generated/validation-report.json#/mcpConnectorAuditor`.

## Hallazgos

- P2 corregido: el contrato MCP declaraba `deny_credential_shaped_values=true`, pero los fixtures negativos no tenian un caso especifico que probara un placeholder con forma de token. Se agrego `credential_shaped_env_placeholder` para verificar que el auditor detecta `credential-shaped env value`.
- Pass: `config/.env.example` mantiene `GITHUB_TOKEN`, `SONARQUBE_TOKEN` y `CONFLUENCE_TOKEN_OPTIONAL` con valores vacios.
- Pass: `config/mcp-connectors.example.json` declara conectores deshabilitados por defecto, activacion de operador, aprobacion para escrituras, operaciones permitidas/denegadas y trazabilidad por conector.
- Pass: la equivalencia Codex, Claude, GitHub Copilot y LangChain se conserva mediante `runtime_equivalence` y `allowed_runtimes` comunes.
- Pass: no se encontraron secretos reales, tokens con forma conocida, rutas locales sensibles ni datos de cliente en `config`, `generated` o `tools` durante el barrido defensivo.
- No aplica: no hay superficie web/API en esta tarea para CORS, sesion, auth o aislamiento multi-tenant runtime. El aislamiento relevante aqui es de secretos por entorno local/CI y placeholders vacios en repo.
- No aplica: billing no aparece en la activacion MCP; las politicas revisadas bloquean administracion de billing en `denied_operations`.

## Parches Hechos

- `tools/validate_copilot_factory.py`: se agrego el caso negativo `credential_shaped_env_placeholder` al auditor MCP.
- `generated/validation-report.json` y `generated/validation-report.md`: regenerados por `python tools/validate_copilot_factory.py`; el reporte contiene el nuevo fixture con `passedExpectation=true`.
- `generated/prompt-quality-report.json` y `generated/prompt-quality-report.md`: regenerados por `python tools/validate_prompt_quality.py`.

## Comandos Ejecutados

- `Get-Command rg -ErrorAction SilentlyContinue`: `rg` disponible como shim local.
- `git status --short`: fallo esperado; este directorio no contiene metadata Git.
- `rg` sobre `tools/validate_copilot_factory.py`, `generated/validation-report.*`, `config`, `generated` y `tools` para revisar contrato MCP, placeholders y patrones de secreto.
- `python tools/validate_copilot_factory.py`: PASS, `18 copilots, 50 agents, 50 tasks`.
- `python tools/validate_prompt_quality.py`: PASS, `18 copilots, 72 runtime prompts`.
- `rg -n "credential_shaped_env_placeholder|credential-shaped env value" generated/validation-report.json generated/validation-report.md`: confirma el fixture nuevo en `generated/validation-report.json`.
- `Get-ChildItem -Path . -Directory -Recurse -Filter __pycache__`: sin bytecode residual.
- `rg` con patrones `sk-*`, `github_pat_*`, `gh[pousr]_*` y `Bearer ...` sobre `config`, `generated` y `tools`: sin coincidencias reales.

## Riesgos Residuales

- No hay metadata Git local; la trazabilidad del incremento depende de este informe y de los reportes generados.
- La revision es estatica y local; no prueba conectividad real contra GitHub, SonarQube o Confluence.
- La activacion real de conectores sigue dependiendo de secretos fuera del repo, aprobacion explicita del operador y controles del entorno donde se ejecuten.
