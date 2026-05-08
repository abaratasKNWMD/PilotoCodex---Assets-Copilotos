# Task 035 Safe Coding / Privacy Audit

Fecha: 2026-05-05

## Alcance

- Copiloto auditado: `angular_18`.
- Archivos foco: `dist/copilots/angular_18/shared/spec.json`, adaptadores Codex, Claude, GitHub Copilot y LangChain.
- Frontera: mantenimiento local de contrato runtime, prompts, schema, trazabilidad y privacidad. No se revisaron servicios externos en vivo.

## Hallazgos

1. Severidad P2 media - Schema de salida demasiado permisivo en la raiz y en `actions.items`.
   - Evidencia: `shared/output_schema.json`, `shared/spec.json`, los prompts runtime y el perfil LangChain ya bloqueaban propiedades extra en `evidence`, `handoff` e `implementation`, pero no en la raiz del objeto ni en cada item de `actions`.
   - Riesgo: un runtime podia aceptar campos no declarados, incluyendo datos de cliente, billing, tenant o trazas no previstas, reduciendo privacidad y trazabilidad.
   - Estado: corregido.

2. Severidad informativa - Secretos/rutas locales.
   - Evidencia: escaneos de patrones de secreto real y rutas absolutas sobre `dist/copilots/angular_18`, `generated` y `.codex-loop/factory/audits`.
   - Resultado: sin tokens reales, claves privadas, bearer tokens largos ni rutas locales sensibles. `GITHUB_TOKEN` aparece solo como nombre de variable de entorno/placeholder.
   - Estado: sin parche necesario.

3. Severidad informativa - Auth, CORS, billing y multi-tenant.
   - Evidencia: el incremento es de prompts/schema/contrato de copiloto, no de servidor HTTP ni flujo SaaS.
   - Resultado: no aplican CORS, sesiones ni billing runtime. La politica mantiene conectores como capacidades declaradas, no credenciales, y exige aprobacion humana para writes de seguridad/release/conectores.

## Parches hechos

- Endurecido `dist/copilots/angular_18/shared/output_schema.json`:
  - `additionalProperties: false` en la raiz del output.
  - `additionalProperties: false` en cada item de `actions`.
- Sincronizado el mismo contrato en `dist/copilots/angular_18/shared/spec.json`.
- Sincronizados los prompts/runtime docs:
  - `dist/copilots/angular_18/codex/AGENT.md`
  - `dist/copilots/angular_18/claude/AGENT.md`
  - `dist/copilots/angular_18/github-copilot/copilot-agent.md`
- Sincronizado LangChain:
  - `dist/copilots/angular_18/langchain/agent.py`
  - `dist/copilots/angular_18/langchain/agent_profile.json`
  - `dist/copilots/angular_18/langchain/agent_contract.json`
- Actualizados los digests canonicos de schema en:
  - `dist/copilots/angular_18/shared/codex_tool_protocol.json`
  - `dist/copilots/angular_18/shared/claude_project_instructions.json`
  - `dist/copilots/angular_18/github-copilot/copilot-profile.json`
  - `dist/copilots/angular_18/langchain/agent_contract.json`
- Regenerados por validadores los reportes de `generated/` asociados a factory, prompt quality y runtime equivalence.

## Comandos ejecutados

- `if (Get-Command rg -ErrorAction SilentlyContinue) { 'RG_AVAILABLE' } else { 'RG_MISSING' }`
- `git status --short` -> no hay metadata `.git` en este workspace.
- Lectura de artefactos objetivo con `Get-Content -Raw`.
- Escaneo de secretos/rutas con `rg` y patrones de alta confianza.
- `python tools/validate_copilot_factory.py` -> PASS.
- `python tools/validate_prompt_quality.py` -> PASS.
- `python tools/validate_runtime_equivalence.py` -> PASS final.
- `python -m py_compile dist/copilots/angular_18/langchain/agent.py`; el `__pycache__` temporal fue eliminado dentro del workspace.
- Comprobaciones JSON con `ConvertFrom-Json` para confirmar `additionalProperties: false` en schema compartido, spec y perfil LangChain.

Nota: una ejecucion intermedia de `validate_runtime_equivalence.py` fallo por usar inicialmente hash de archivo en vez de digest canonico JSON para `outputSchemaSha256`. Se corrigio al digest canonico esperado y la repeticion final paso.

## Riesgos residuales

- No hay repositorio Git disponible en `NuevoProyecto`, por lo que no se pudo usar diff nativo para separar cambios previos de cambios de esta auditoria.
- La equivalencia depende de que futuras regeneraciones de fabrica preserven el endurecimiento de `additionalProperties`. La suite actual lo valida por igualdad de schema y digest.
- No se verificaron conectores GitHub reales porque el contrato declara placeholders/env names only y no activa credenciales.
