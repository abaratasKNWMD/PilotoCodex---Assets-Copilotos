# QA Audit - Task 036 - Copiloto Node.js

Fecha: 2026-05-05
Perfil: strict
Scope auditado: equivalencia runtime Node.js entre Codex, Claude, GitHub Copilot y LangChain, con foco en prompts, schema, trazabilidad y contrato de coste.

## Hallazgos

1. **Rutas de herramientas Python no ejecutables desde los adapters Markdown.**
   - Evidencia: `dist/copilots/nodejs/codex/AGENT.md`, `dist/copilots/nodejs/claude/AGENT.md` y `dist/copilots/nodejs/github-copilot/copilot-agent.md` apuntaban a `../../../tools/semantic_router.py` y `../../../tools/validate_prompt_quality.py`.
   - Riesgo: desde `dist/copilots/nodejs/<runtime>/`, esa ruta resuelve a `dist/tools/...`, que no existe. El prompt declaraba disciplina Python-first, pero un operador siguiendo la tarjeta runtime no podia ejecutar los checks indicados.
   - Severidad: P2, release readiness/runtime contract.

2. **Equivalencia funcional general validada.**
   - Evidencia: `dist/copilots/nodejs/shared/spec.json`, `dist/copilots/nodejs/shared/output_schema.json`, `dist/copilots/nodejs/langchain/agent_contract.json` y `dist/copilots/nodejs/langchain/agent.py` conservan `nodejs-runtime-contracts-1.0`, outputs `node_patch_plan`/`api_contract_report`, `python_first_llm_sparse`, `maxEvidenceRefs: 12` y conectores/env names sin valores secretos.
   - Los validadores obligatorios pasan despues del parche.

3. **UX/UI checklist.**
   - No aplica directamente: el incremento no anade UI renderizable, formularios, estados de carga ni navegacion. La revision equivalente fue sobre usabilidad operativa de prompts, rutas, contratos y errores de runtime local.

## Parches hechos

- `dist/copilots/nodejs/codex/AGENT.md`
- `dist/copilots/nodejs/claude/AGENT.md`
- `dist/copilots/nodejs/github-copilot/copilot-agent.md`
  - Corregidas las rutas de `Python router` y `Prompt quality gate` a `../../../../tools/...`, que si resuelven desde cada carpeta runtime.

## Comandos ejecutados

- `Get-Command rg -ErrorAction SilentlyContinue`
  - Resultado: `rg` disponible como shim local en `.codex-loop/tool-shims/rg.ps1`.
- `git status --short`
  - Resultado: no disponible; el workspace actual no es un repositorio Git.
- `python tools/validate_copilot_factory.py`
  - Resultado inicial: PASS.
  - Resultado intermedio: FAIL solo por `dist/copilots/__pycache__` generado al ejecutar el smoke local del agente Python.
  - Resultado final: PASS, 18 copilots, 50 agents, 50 tasks.
- `python tools/validate_prompt_quality.py`
  - Resultado final: PASS, 18 copilots, 72 runtime prompts.
- `python tools/validate_runtime_equivalence.py`
  - Resultado final: PASS, 18 copilots checked.
- `python dist/copilots/nodejs/langchain/agent.py node typescript build patch`
  - Resultado: el agente LangChain ejecuta y devuelve plan/audit con contrato Node.js; genero bytecode local, limpiado antes de la validacion final.
- `Test-Path '../../../../tools/semantic_router.py'` y `Test-Path '../../../../tools/validate_prompt_quality.py` desde `dist/copilots/nodejs/codex`, `claude` y `github-copilot`
  - Resultado: `True` para ambas rutas en los tres adapters.
- `Get-ChildItem -Recurse -Directory -Filter '__pycache__'`
  - Resultado final: sin caches Python residuales.

## Riesgos residuales

- Las rutas corregidas estaban ya presentes en `tools/elevate_copilot_prompts.py`, pero los artefactos Node.js auditados estaban desfasados. Si otro generador o snapshot antiguo regenera estas tarjetas, podria reintroducir la ruta incorrecta.
- No se anadieron tests nuevos porque el riesgo estaba en documentacion ejecutable de runtime y queda cubierto por checks de ruta mas los tres validadores obligatorios.
- No se ejecuto una validacion JSON Schema con instancia real `node_patch_plan`/`api_contract_report`; el repo no declara fixture Node.js de salida. La coherencia schema/spec/runtime queda cubierta por `validate_runtime_equivalence.py`.
