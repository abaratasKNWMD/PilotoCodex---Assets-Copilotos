# Task 029 QA Audit - Copiloto Registro Unico

Fecha: 2026-05-05
Perfil QA: strict

## Alcance revisado

- `dist/copilots/single_registry/shared/spec.json`
- `dist/copilots/single_registry/shared/output_schema.json`
- `dist/copilots/single_registry/codex/AGENT.md`
- `dist/copilots/single_registry/claude/AGENT.md`
- `dist/copilots/single_registry/github-copilot/copilot-agent.md`
- `dist/copilots/single_registry/github-copilot/copilot-profile.json`
- `dist/copilots/single_registry/github-copilot/mcp-placeholders.json`
- `dist/copilots/single_registry/langchain/agent.py`
- `dist/copilots/single_registry/langchain/agent_contract.json`
- `dist/copilots/single_registry/langchain/agent_profile.json`
- `dist/copilots/single_registry/README.md`
- Reportes generados por los validadores en `generated/`

## Hallazgos

1. Corregido: `dist/copilots/single_registry/README.md` documentaba `validate_copilot_factory.py` y `validate_prompt_quality.py`, pero omitia `validate_runtime_equivalence.py`. Para una tarea cuyo objetivo es mantener equivalencia entre Codex, Claude, GitHub Copilot y LangChain, esa omision dejaba el runbook incompleto frente al DoD.

2. Corregido durante la auditoria: `python tools/validate_copilot_factory.py` fallo inicialmente por un cache Python en `dist/copilots/__pycache__/`. Era un residuo de ejecucion dentro del artefacto de distribucion y bloqueaba release readiness. Se elimino el `.pyc` y el directorio vacio.

3. Sin deriva de contrato: `shared/spec.json`, `shared/output_schema.json`, los tres adapters markdown y `langchain/agent.py` mantienen el mismo `copilot_id`, outputs declarados, conectores, env keys, reglas de evidencia y modo de coste `python_first_llm_sparse`.

4. Sin fallo funcional en LangChain: el agente carga con Python, el happy path de `plan()` pasa con evidencia minima, `audit()` bloquea correctamente cuando falta evidencia y `render_prompt()` redacta un token simulado.

5. No aplica UX visual: el incremento es una superficie de prompts, contratos JSON, documentacion operativa y runtime Python. No hay formulario, navegacion web, responsive UI, loading state visual ni empty state visual que auditar.

## Parches hechos

- `dist/copilots/single_registry/README.md`: anadido `python tools/validate_runtime_equivalence.py` al runbook previo al handoff.
- Eliminado `dist/copilots/__pycache__/_runtime_safety.cpython-314.pyc` y el directorio `dist/copilots/__pycache__/` vacio para no dejar bytecode en el artefacto de release.

## Comandos ejecutados

- `Get-Command rg -ErrorAction SilentlyContinue | Select-Object -ExpandProperty Source`
  - Resultado: `rg` disponible como shim local en `.codex-loop/tool-shims/rg.ps1`.
- `git status --short`
  - Resultado: no es un repositorio Git; la auditoria se baso en lectura directa de archivos.
- `python tools/validate_copilot_factory.py`
  - Resultado inicial: FAIL por `dist/copilots/__pycache__/`.
  - Resultado final: PASS, `18 copilots, 50 agents, 50 tasks`.
- `python tools/validate_prompt_quality.py`
  - Resultado final: PASS, `18 copilots, 72 runtime prompts`.
- `python tools/validate_runtime_equivalence.py`
  - Resultado final: PASS, `18 copilots checked`.
- Smoke de `dist/copilots/single_registry/langchain/agent.py` con `python -B -`
  - Resultado: `happy_pass=true`, `empty_pass=false`, `empty_evidence_needed=["source_refs","validation"]`, roles `system/developer/user`, token simulado redactado.
- `Get-ChildItem -Recurse -Force -Directory -LiteralPath 'dist/copilots' -Filter '__pycache__'`
  - Resultado final: sin caches Python en `dist/copilots`.
- Lectura de `generated/validation-report.json`, `generated/prompt-quality-report.json`, `generated/runtime-equivalence-report.json` y `generated/validator-smoke-report.json`
  - Resultado: todos con `pass=true`.

## Riesgos residuales

- No hay metadata Git local para comparar diffs exactos; la evidencia queda en este informe, los archivos modificados y los reportes regenerados.
- El README del copilot se corrigio manualmente. Si una regeneracion futura sobrescribe READMEs desde una plantilla global que no incluya `validate_runtime_equivalence.py`, la omision podria reaparecer en este u otros copilots.
- La equivalencia depende de los validadores generados y del contrato compartido actual; no se hizo activacion real de `github_mcp`, por lo que la evidencia de conector queda correctamente como declaracion offline y no como prueba de credenciales.
