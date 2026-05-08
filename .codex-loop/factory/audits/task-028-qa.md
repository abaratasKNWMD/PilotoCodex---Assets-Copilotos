# Task 028 QA Audit - Copiloto de Discovery AS-IS

Fecha: 2026-05-05
Perfil QA: strict

## Alcance revisado

- `dist/copilots/as_is_discovery/shared/spec.json`
- `dist/copilots/as_is_discovery/shared/output_schema.json`
- `dist/copilots/as_is_discovery/shared/runtime_contract.md`
- `dist/copilots/as_is_discovery/codex/AGENT.md`
- `dist/copilots/as_is_discovery/claude/AGENT.md`
- `dist/copilots/as_is_discovery/github-copilot/copilot-agent.md`
- `dist/copilots/as_is_discovery/github-copilot/copilot-profile.json`
- `dist/copilots/as_is_discovery/github-copilot/mcp-placeholders.json`
- `dist/copilots/as_is_discovery/langchain/agent.py`
- `dist/copilots/as_is_discovery/langchain/agent_contract.json`
- Reportes generados por los validadores en `generated/`

## Hallazgos

1. Corregido: los adapters markdown de Codex, Claude y GitHub Copilot enlazaban `../shared/output_schema.json`, pero la seccion `Outputs` presentaba el JSON como "preferred machine-readable shape" sin nombrar `runtime_contract`. El schema compartido si incluye `runtime_contract`, y LangChain lo expone en `plan()` y `render_prompt()`. Esto podia hacer que tres runtimes omitieran evidencia de paridad cuando el entregable pidiera runtime-contracts.

2. Sin fallo de credenciales: `mcp-placeholders.json` mantiene `credentialValue` vacio, `credentialValuesStored=false`, `customerDataAllowed=false` y el conector `github_mcp` deshabilitado por defecto.

3. Sin fallo funcional en LangChain: `agent.py` compila, valida request/evidence, redacta valores sensibles en `render_prompt()` y devuelve `runtime_contract` en `plan()`.

4. No aplica UX visual: el incremento es una superficie de prompts, contratos JSON y runtime Python. No hay flujo web, formulario, responsive UI, loading state o navegacion que auditar.

## Parches hechos

- `dist/copilots/as_is_discovery/codex/AGENT.md`: aclarada la seccion `Outputs` para indicar que el contrato completo esta en `../shared/output_schema.json` y que `runtime_contract` debe incluirse cuando haya entregable de paridad runtime.
- `dist/copilots/as_is_discovery/claude/AGENT.md`: mismo ajuste.
- `dist/copilots/as_is_discovery/github-copilot/copilot-agent.md`: mismo ajuste.
- Eliminados caches Python `__pycache__` generados durante la comprobacion local para no dejar artefactos de release.

## Comandos ejecutados

- `Get-Command rg -ErrorAction SilentlyContinue | Select-Object -ExpandProperty Source`
  - Resultado: `rg` disponible como shim local en `.codex-loop/tool-shims/rg.ps1`.
- `git status --short`
  - Resultado: no es un repositorio Git, por lo que la auditoria se baso en lectura directa de archivos.
- `python tools\validate_copilot_factory.py`
  - Resultado final: PASS, `18 copilots, 50 agents, 50 tasks`.
- `python tools\validate_prompt_quality.py`
  - Resultado final: PASS, `18 copilots, 72 runtime prompts`.
- `python tools\validate_runtime_equivalence.py`
  - Resultado final: PASS, `18 copilots checked`.
- `python -c "... missing_runtime_contract_refs ..."`
  - Resultado: `missing_runtime_contract_refs=[]`.
- `python -m py_compile dist\copilots\as_is_discovery\langchain\agent.py`
  - Resultado: PASS.
- Import smoke de `dist/copilots/as_is_discovery/langchain/agent.py`
  - Resultado: `audit.pass=True` con evidencia minima y redaccion de token simulada en `render_prompt()`.
- `Get-ChildItem -Path dist\copilots -Recurse -Directory -Filter __pycache__`
  - Resultado final: sin caches Python en `dist/copilots`.

## Riesgos residuales

- Los validadores obligatorios comprueban la equivalencia real contra `shared/output_schema.json`, pero no fallaban por la ambiguedad textual del bloque `Outputs` en markdown. El parche cierra AS-IS sin tocar otros copilots para mantener el alcance de la tarea.
- La generacion futura podria sobrescribir estos tres markdown si la plantilla global no incorpora la misma aclaracion. Recomendacion: en una tarea separada, mover esta frase a la plantilla generadora para todos los copilots.
- No hay Git metadata local para confirmar diferencias exactas; la evidencia queda en este informe, los archivos modificados y los reportes regenerados.
