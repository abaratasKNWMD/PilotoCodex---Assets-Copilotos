# Safe-coding / Privacy Audit - Task 036 - Copiloto Node.js

Fecha: 2026-05-05
Perfil: strict
Scope: `dist/copilots/nodejs` y reportes generados listados para la tarea 036.

## Hallazgos

1. Severidad media - import precedence en LangChain corregido.
   - Evidencia: `dist/copilots/nodejs/langchain/agent.py` usaba `sys.path.append(...)` antes de importar `_runtime_safety`.
   - Riesgo: si el agente se ejecutaba en un contexto con otro modulo `_runtime_safety` ya priorizado en `sys.path`, podia degradarse la validacion/redaccion comun de request y evidence.
   - Estado: corregido con `sys.path.insert(0, ...)` para priorizar `dist/copilots/_runtime_safety.py`.

2. Severidad informativa - secretos, rutas locales y placeholders.
   - No se encontraron credenciales reales, bearer tokens largos, claves privadas, PATs, claves `sk-`, rutas locales del usuario ni datos de cliente/billing en los artefactos auditados.
   - `GITHUB_TOKEN` aparece solo como nombre de variable de entorno o referencia placeholder. `mcp-placeholders.json` mantiene `defaultEnabled=false`, `enabled=false`, `credentialValue=""`, `credentialValuesStored=false`, `customerDataAllowed=false` y `billingDataAllowed=false`.

3. Severidad informativa - auth, CORS, permisos, SaaS y billing.
   - No hay servicio HTTP, sesiones, CORS, plano SaaS multi-tenant ni integracion de billing ejecutable en este incremento. El control aplicable es local: no activar conectores sin aprobacion, no guardar credenciales y redactar datos sensibles antes de renderizar prompts.

## Parches hechos

- `dist/copilots/nodejs/langchain/agent.py`
  - Cambio: `sys.path.append(str(Path(__file__).resolve().parents[2]))` -> `sys.path.insert(0, str(Path(__file__).resolve().parents[2]))`.
  - Motivo: endurecer la carga del helper comun `_runtime_safety` que valida entradas y redacta secretos, rutas locales, tenant/customer/billing data antes del payload para LLM.

## Comandos ejecutados

- `if (Get-Command rg -ErrorAction SilentlyContinue) { 'RG_AVAILABLE' } else { 'RG_MISSING' }`
  - Resultado: `RG_AVAILABLE`.
- `git status --short`
  - Resultado: no hay repositorio Git inicializado en el workspace.
- Lectura de `dist/copilots/nodejs/shared/spec.json`, `codex/AGENT.md`, `claude/AGENT.md`, `github-copilot/copilot-agent.md`, `langchain/agent.py`, `langchain/agent_contract.json`, `github-copilot/mcp-placeholders.json` y `shared/output_schema.json`.
- Busquedas `rg.exe` acotadas para secretos, tokens, claves privadas, rutas locales, datos customer/tenant/billing y placeholders MCP activos.
  - Resultado final: sin coincidencias de valores sensibles reales ni placeholders activados.
- `python tools/validate_copilot_factory.py`
  - Resultado: PASS, 18 copilots, 50 agents, 50 tasks.
- `python tools/validate_prompt_quality.py`
  - Resultado: PASS, 18 copilots, 72 runtime prompts.
- `python tools/validate_runtime_equivalence.py`
  - Resultado: PASS, 18 copilots checked.
- Smoke local con `python -B -` cargando `dist/copilots/nodejs/langchain/agent.py`.
  - Resultado: roles `system`, `developer`, `user`; `_runtime_safety` resuelve a `dist/copilots/_runtime_safety.py`; bearer sintetico, API key sintetica, tenant sintetico y ruta local sintetica quedan redactados.
- `Get-ChildItem dist\copilots -Recurse -Directory -Filter __pycache__`
  - Resultado final: sin caches Python residuales.

## Riesgos residuales

- La revision es offline/local. No prueba GitHub MCP real ni permisos de proveedor; cualquier activacion de conector debe seguir usando secretos externos al repo, scopes minimos y aprobacion operativa.
- Los validadores cubren equivalencia de contrato, prompts y reportes generados, pero no ejecutan una instancia real de `node_patch_plan` o `api_contract_report` contra JSON Schema.
- Si un generador externo antiguo reescribe `dist/copilots/nodejs/langchain/agent.py`, podria reintroducir `sys.path.append(...)`; debe mantenerse el patron `insert(0, ...)` en futuras regeneraciones.
