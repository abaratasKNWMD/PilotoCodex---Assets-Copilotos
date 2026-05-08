# Task 016 Safe-Coding And Privacy Audit

Fecha: 2026-05-04

## Alcance

Revision defensiva de la tarea 16/50: `Builds GitHub Copilot profile docs and MCP placeholders.`

Archivos y superficies revisadas:

- `dist/copilots/*/github-copilot/copilot-profile.json`
- `dist/copilots/*/github-copilot/mcp-placeholders.json`
- `dist/copilots/*/github-copilot/copilot-agent.md`
- `generated/runtime-injection-map.json`
- `generated/runtime-equivalence-report.json`
- `generated/validation-report.json`
- `config/.env.example`
- `config/mcp-connectors.example.json`
- `tools/elevate_copilot_prompts.py`
- `tools/validate_runtime_equivalence.py`
- `README.md`
- `OPERATING_SYSTEM.md`

## Hallazgos

| Severidad | Hallazgo | Evidencia | Estado |
|---|---|---|---|
| Info | No se detectaron credenciales reales hardcodeadas en los artefactos revisados. | Busqueda de patrones `sk-*`, `github_pat_*`, `gh*_*`, `Bearer`, `password`, `api_key`, `secret`, `token`. Las coincidencias fueron nombres de variables vacias o prefijos prohibidos documentados. | Aceptado |
| Info | No se detectaron rutas absolutas locales en los artefactos de la tarea. | Busqueda de patrones de directorios home locales de Windows, macOS y Linux sin coincidencias en artefactos release. | Aceptado |
| Info | Los placeholders MCP estan deshabilitados por defecto y no almacenan valores de credencial. | `mcp-placeholders.json` usa `enabled: false`, `credentialValue: ""`, `credentialValuesStored: false`, `customerDataAllowed: false` y `billingDataAllowed: false`. | Aceptado |
| Info | La equivalencia runtime para Codex, Claude, GitHub Copilot y LangChain esta cubierta por artefactos verificables. | `generated/runtime-injection-map.json` apunta a perfiles GitHub Copilot, placeholders MCP y adapters por runtime; `tools/validate_runtime_equivalence.py` valida deriva y sanitizacion basica. | Aceptado |
| Low | La activacion real de MCP queda fuera de este incremento y depende de operador. | La politica exige activacion manual, aprobacion para escrituras y redaccion de tokens. | Riesgo residual documentado |

## Parches Hechos

- Creado este informe obligatorio: `.codex-loop/factory/audits/task-016-safe-coding.md`.
- No se modificaron contratos Copilot/MCP ni validadores porque no se encontro una mala practica obvia relacionada con credenciales, rutas locales, datos de cliente, billing, permisos o runtime equivalence.

## Comandos Ejecutados

```powershell
Get-Command rg -ErrorAction SilentlyContinue | Select-Object -ExpandProperty Source
```

Resultado: `rg` disponible como shim local en `.codex-loop/tool-shims/rg.ps1`.

```powershell
git status --short
```

Resultado: no aplica, el workspace actual no es un repositorio Git.

```powershell
rg -n "(?i)(sk-[A-Za-z0-9_-]{20,}|github_pat_|gh[pousr]_|Bearer\s+[A-Za-z0-9._~+/=-]{20,}|password\s*[:=]|api[_-]?key\s*[:=]|secret\s*[:=]|token\s*[:=])" factory.config.json OPERATING_SYSTEM.md README.md generated/runtime-injection-map.json tools/elevate_copilot_prompts.py tools/validate_runtime_equivalence.py dist/copilots config
```

Resultado: sin secretos reales; solo variables placeholder vacias y prefijos prohibidos documentados en `config/mcp-connectors.example.json`.

```powershell
rg -n "<patrones-de-home-local>" factory.config.json OPERATING_SYSTEM.md README.md generated/runtime-injection-map.json tools/elevate_copilot_prompts.py tools/validate_runtime_equivalence.py dist/copilots config
```

Resultado: sin coincidencias.

```powershell
python tools\validate_copilot_factory.py
python tools\validate_prompt_quality.py
python tools\validate_runtime_equivalence.py
```

Resultados:

- `Copilot factory validation PASS: 18 copilots, 50 agents, 50 tasks.`
- `Prompt quality validation PASS: 18 copilots, 72 runtime prompts.`
- `Runtime equivalence PASS: 18 copilots checked.`

## Riesgos Residuales

- MCP sigue siendo una capacidad externa cuando un operador la active fuera de los placeholders. Mantener tokens fuera del repositorio y usar secreto local, CI secret store o runtime aprobado.
- Las escrituras por conectores deben seguir requiriendo aprobacion explicita de operador y respetar las politicas de branch/review.
- La revision no cubre ejecucion contra servicios reales, CORS, sesiones ni multi-tenant SaaS porque este incremento produce perfiles, placeholders y contratos locales, no una superficie web/API desplegada.
