# QA Audit Task 016

Fecha: 2026-05-04
Perfil: strict
Tarea auditada: `[P1][factory_agent_16_github] Builds GitHub Copilot profile docs and MCP placeholders.`

## Veredicto

Pass con parche aplicado.

La mision GitHub Copilot esta reflejada en artefactos verificables: 18 `copilot-agent.md`, 18 `copilot-profile.json`, 18 `mcp-placeholders.json`, `generated/runtime-injection-map.json` y `generated/runtime-equivalence-report.*`.

## Hallazgos

- P1 corregido: `mcp-placeholders.json` generaba `envReference` por conector, pero `tools/validate_runtime_equivalence.py` no verificaba que coincidiera con la env var declarada. Eso podia dejar pasar un placeholder apuntando a otra variable sin romper el gate.
- P1 corregido: `copilot-profile.json` generaba `costControl`, pero el validador no exigia sus campos. Para el objetivo de equivalencia sin inflar costes, ese contrato no podia quedar solo como texto descriptivo.
- Sin hallazgos de secretos reales, datos de cliente o billing en la politica MCP compartida. Los placeholders siguen deshabilitados, sin valores de credenciales y con activacion de operador.
- No hay superficie UI/frontend. Los checks de UX aplican aqui como ergonomia operativa: documentos Markdown legibles, JSON trazable y errores de validador accionables.

## Parches Hechos

- `tools/validate_runtime_equivalence.py`: se agrego validacion de `github_mcp_<connector>_env_reference` para exigir `envReference == ${ENV_DECLARADA}`.
- `tools/validate_runtime_equivalence.py`: se agrego validacion de `github_profile_cost_control_*` para exigir `promptExpansion`, `deterministicPythonFirst` y `llmEscalation`.
- `tools/validate_runtime_equivalence.py`: se agregaron los casos negativos `github_mcp_env_reference_drift` y `github_profile_cost_control_drift`.
- Reportes regenerados por validadores: `generated/runtime-equivalence-report.*`, `generated/prompt-quality-report.*` y `generated/validation-report.*`.

## Comandos Ejecutados

- `Get-Command rg -ErrorAction SilentlyContinue`: `rg` disponible como shim local.
- `git status --short`: fallo esperado; el workspace no es un repositorio Git.
- `python tools/validate_copilot_factory.py`: PASS inicial, 18 copilots, 50 agents, 50 tasks.
- `python tools/validate_prompt_quality.py`: PASS inicial, 18 copilots, 72 runtime prompts.
- `python tools/validate_runtime_equivalence.py`: PASS inicial, 18 copilots checked.
- Revision de muestra: `dist/copilots/python/github-copilot/copilot-agent.md`, `copilot-profile.json`, `mcp-placeholders.json` y `shared/spec.json`.
- `python tools/validate_runtime_equivalence.py`: PASS despues del parche; el reporte incluye los nuevos negativos detectados.
- `Select-String generated\runtime-equivalence-report.md`: confirma `github_mcp_env_reference_drift` y `github_profile_cost_control_drift` con `failureDetected=True`.
- `python tools/validate_copilot_factory.py`: PASS despues del parche.
- `python tools/validate_prompt_quality.py`: PASS despues del parche.
- `python -m py_compile tools/validate_runtime_equivalence.py`: ejecucion de sintaxis satisfactoria, pero genero `tools/__pycache__`.
- Limpieza local de `tools/__pycache__` creado por QA, con comprobacion de ruta dentro del workspace.
- Conteos PowerShell finales: 18 `copilot-profile.json`, 18 `mcp-placeholders.json`, 18 `copilot-agent.md` bajo `github-copilot`.
- `python tools/validate_copilot_factory.py; if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }; python tools/validate_prompt_quality.py; if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }; python tools/validate_runtime_equivalence.py`: PASS completo final.
- `Test-Path tools\__pycache__`: `False`.

## Riesgos Residuales

- No hay metadata Git local, asi que la trazabilidad de diff depende de esta auditoria y de los reportes generados.
- No se regenero toda la fabrica con `tools/elevate_copilot_prompts.py` para evitar churn amplio; el generador ya emite los campos ahora validados.
- La equivalencia sigue siendo estatica sobre contratos Markdown/JSON/Python generados; no ejecuta un agente GitHub Copilot real ni un MCP runtime con credenciales activadas.
