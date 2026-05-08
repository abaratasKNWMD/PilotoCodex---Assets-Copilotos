# Task 030 QA Audit - Copiloto Firefly v5

Fecha: 2026-05-05
Perfil QA: strict

## Alcance revisado

- `dist/copilots/firefly_v5/shared/spec.json`
- `dist/copilots/firefly_v5/shared/output_schema.json`
- `dist/copilots/firefly_v5/shared/implementation_plan_audit.json`
- `dist/copilots/firefly_v5/codex/AGENT.md`
- `dist/copilots/firefly_v5/claude/AGENT.md`
- `dist/copilots/firefly_v5/github-copilot/copilot-agent.md`
- `dist/copilots/firefly_v5/github-copilot/copilot-profile.json`
- `dist/copilots/firefly_v5/github-copilot/mcp-placeholders.json`
- `dist/copilots/firefly_v5/langchain/agent.py`
- `dist/copilots/firefly_v5/langchain/agent_contract.json`
- `dist/copilots/firefly_v5/langchain/agent_profile.json`
- `dist/copilots/firefly_v5/README.md`
- Reportes generados por los validadores en `generated/`

## Hallazgos

1. Corregido: `dist/copilots/firefly_v5/langchain/agent.py` aceptaba un artefacto con `copilot_id: wrong` en `validate_output_contract()`. Eso rompia el `const` del esquema compartido y podia permitir trazabilidad cruzada entre copilots. Ahora el runtime LangChain rechaza cualquier `copilot_id` distinto de `firefly_v5`.

2. Corregido: `dist/copilots/firefly_v5/README.md` no documentaba `python tools/validate_runtime_equivalence.py` en el runbook, aunque es parte del DoD de esta tarea. Se anadio el comando para que la documentacion operativa coincida con el contrato de equivalencia.

3. Corregido durante la auditoria: el primer smoke funcional genero `__pycache__` bajo `dist/copilots/`, y `validate_copilot_factory.py` lo bloqueo como artefacto no apto para release. Se eliminaron los caches generados y las verificaciones finales se ejecutaron con `PYTHONDONTWRITEBYTECODE=1`.

4. Sin deriva detectada en los adaptadores: Codex, Claude, GitHub Copilot y LangChain mantienen el mismo `systemPrompt`, `developerPrompt`, esquema compartido, conectores declarativos, env keys y contrato `maxUnexplainedDrift = 0`.

5. No aplica UX visual: el incremento es de prompts, contratos JSON, documentacion operativa y runtime Python. No hay navegacion, formularios, responsive UI, loading state visual ni empty state visual que auditar.

## Parches hechos

- `dist/copilots/firefly_v5/langchain/agent.py`: anadida validacion explicita de `copilot_id` contra `OUTPUT_SCHEMA["properties"]["copilot_id"]["const"]`.
- `dist/copilots/firefly_v5/README.md`: anadido `python tools/validate_runtime_equivalence.py` al runbook de handoff.
- Limpieza de release: eliminados `dist/copilots/__pycache__/` y `dist/copilots/firefly_v5/langchain/__pycache__/` generados por el smoke local.
- Regenerados por ejecucion de validadores: reportes JSON/MD en `generated/` y recibos en `generated/validator-smoke/`.

## Comandos ejecutados

- `Get-Command rg -ErrorAction SilentlyContinue | Select-Object -ExpandProperty Source`
  - Resultado: `rg` disponible como shim local en `.codex-loop/tool-shims/rg.ps1`.
- `git status --short`
  - Resultado: no es un repositorio Git; la auditoria se baso en lectura directa de archivos.
- Smoke funcional de `dist/copilots/firefly_v5/langchain/agent.py` con `PYTHONDONTWRITEBYTECODE=1`
  - Resultado antes del parche: `wrong_id_contract {'pass': True, ...}`.
  - Resultado final: artefacto valido `pass=True`; `copilot_id: wrong` devuelve `pass=False` con `invalid copilot_id`.
- `python tools/validate_copilot_factory.py`
  - Resultado inicial: FAIL por caches Python bajo `dist/copilots/`.
  - Resultado final: PASS, `18 copilots, 50 agents, 50 tasks`.
- `python tools/validate_prompt_quality.py`
  - Resultado final: PASS, `18 copilots, 72 runtime prompts`.
  - Control de coste Firefly v5 LangChain: `growthRatio=0.0952`, limite `0.1`, estado `pass`.
- `python tools/validate_runtime_equivalence.py`
  - Resultado final: PASS, `18 copilots checked`.
- Lectura de `generated/validation-report.json`, `generated/prompt-quality-report.json`, `generated/runtime-equivalence-report.json` y `generated/validator-smoke-report.json`
  - Resultado final: todos con `pass=true` e `issues=0`.
- `Get-ChildItem -Recurse -Directory 'dist/copilots' -Filter '__pycache__'`
  - Resultado final: sin caches Python en `dist/copilots`.

## Riesgos residuales

- No hay metadata Git local para comparar diffs exactos; la evidencia queda en este informe, los archivos modificados y los reportes regenerados.
- El presupuesto de prompt de Firefly v5 LangChain queda valido pero relativamente ajustado: 9.52% de crecimiento frente al limite de 10%. Futuras ampliaciones deberian compactar texto o mover evidencia a referencias compartidas.
- No se activaron conectores reales `github_mcp` ni `sonarqube_mcp`; la auditoria valida el contrato offline y los placeholders, no credenciales ni conectividad externa.
