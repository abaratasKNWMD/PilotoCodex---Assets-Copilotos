# Task 007 Safe-Coding / Privacy Review

Fecha: 2026-05-04

Alcance: tarea 7/50, `factory_agent_07_build`, mision `Audits implementation plans and stack-specific rules.` Revision local dentro de `NuevoProyecto` sobre configuracion MCP, runtime adapters, validadores y artefactos generados.

## Hallazgos

1. Severidad media: `config/mcp-connectors.example.json` dejaba `github_mcp` activado en el ejemplo con alcance `repo read/write as allowed by operator`.
   - Riesgo: un operador podia copiar el ejemplo y activar un conector con permisos de escritura como defecto, en contra de minimo privilegio.
   - Estado: corregido.

2. Severidad media: `dist/copilots/_runtime_safety.py` redaccion de prompts cubria valores con patrones de alta entropia y claves exactas como `token`, pero no nombres de entorno o campos compuestos como `GITHUB_TOKEN` o `client_secret` cuando el valor era corto.
   - Riesgo: evidencia entregada a `render_prompt()` podia conservar secretos de baja entropia o placeholders operativos bajo claves sensibles.
   - Estado: corregido y convertido en check verificable.

3. Severidad informativa: `agent.log` contiene rutas absolutas locales, pero esta marcado como artefacto runtime local.
   - Estado: no se edito el log; ya esta en `.gitignore` y los validadores lo excluyen de artefactos de release. No se detectaron rutas locales materializadas en artefactos no runtime; solo aparecieron regex defensivas de deteccion.

## Parches Hechos

- `config/mcp-connectors.example.json`
  - `github_mcp.enabled` pasa a `false`.
  - El alcance pasa a `read-only by default; write actions require explicit operator approval per task`.

- `dist/copilots/_runtime_safety.py`
  - Se anadio clasificacion de claves sensibles por partes normalizadas (`token`, `secret`, `password`, `credential`, `authorization`, `pat`) y nombres especificos (`api_key`, `private_key`, `access_token`, `client_secret`, `bearer`).
  - `redact_value()` ahora redacta valores bajo claves tipo `GITHUB_TOKEN`, `GITHUB_PAT`, `client_secret`, etc.
  - `SECRET_RE` cubre asignaciones `KEY=value` y `KEY: value` para nombres sensibles compuestos.

- `tools/validate_copilot_factory.py`
  - El check de Build/LangChain ahora prueba redaccion de `GITHUB_TOKEN=short-local-token` y `client_secret=short-client-secret`, ademas de patrones `sk-*`, `ghp_*`, `Bearer`, `token=...`, `password` y rutas locales.

- `generated/validation-report.json` y `generated/validation-report.md`
  - Refrescados por `python tools/validate_copilot_factory.py`.

- `generated/prompt-quality-report.json` y `generated/prompt-quality-report.md`
  - Refrescados por `python tools/validate_prompt_quality.py`.

## Comandos Ejecutados

- `Get-Command rg -ErrorAction SilentlyContinue`
  - Resultado: existe un shim local de `rg`; sus flags no eran compatibles con el uso esperado en PowerShell, se uso `Select-String`.

- `git status --short`
  - Resultado: la carpeta no tiene metadatos Git.

- Busquedas defensivas con `Get-ChildItem` + `Select-String`
  - Secretos reales: sin coincidencias en artefactos no runtime.
  - Rutas locales: solo coincidencias en regex defensivas de validadores/redactor; `agent.log` se trato como runtime local ignorado.

- `python tools/validate_copilot_factory.py`
  - Resultado: PASS, `18 copilots`, `50 agents`, `50 tasks`.

- `python tools/validate_prompt_quality.py`
  - Resultado: PASS, `18 copilots`, `72 runtime prompts`.

- Smoke defensivo de redaccion LangChain
  - Resultado: `True`; `GITHUB_TOKEN`, `client_secret` y `token=...` quedaron fuera del prompt renderizado.

## Riesgos Residuales

- No hay repositorio Git en `NuevoProyecto`, asi que no fue posible aislar el incremento mediante diff; la revision se hizo contra contenido actual y reportes regenerados.
- Los logs runtime locales pueden contener rutas absolutas del host. Permanecen ignorados por `.gitignore` y no deben publicarse como artefactos de release.
- No se probaron conectores reales ni credenciales reales. La revision se limita a placeholders, contratos locales y validacion deterministica.
