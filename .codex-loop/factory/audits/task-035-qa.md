# QA Audit - Task 035 - Copiloto Angular 18

Fecha: 2026-05-05
Perfil: strict
Scope auditado: contrato runtime Angular 18 entre Codex, Claude, GitHub Copilot y LangChain.

## Hallazgos

1. **Schema no hacía cumplir trazas que el contrato declaraba obligatorias.**
   - Evidencia: `dist/copilots/angular_18/shared/spec.json` y los prompts runtime indicaban que cada salida debe incluir `phase` y `expected_outputs`, pero `dist/copilots/angular_18/shared/output_schema.json` no los tenía en `required`.
   - Riesgo: un runtime podía emitir una salida validable sin fase SDLC ni outputs declarados, rompiendo trazabilidad real aunque los prompts dijeran lo contrario.
   - Severidad: P2, contrato/runtime.

2. **El validador solo comprobaba `runtimeParityContract.requiredTraceFields`.**
   - Evidencia: `tools/validate_runtime_equivalence.py` ignoraba `runtimeContract.requiredTraceFields`; Angular 18 usa `runtimeContract`.
   - Riesgo: futuros cambios del contrato Angular 18 podían dejar de exigir trazas sin que la equivalencia runtime fallara.
   - Severidad: P2, cobertura de test/validator.

3. **UX/UI checklist.**
   - No aplica directamente: el incremento no añade UI renderizable, formularios ni navegación. La revisión equivalente fue sobre contrato de salida, prompts, adaptadores y errores de runtime.

## Parches hechos

- `dist/copilots/angular_18/shared/output_schema.json`
  - Añadidos `phase` y `expected_outputs` a `required`.
  - Añadido `minItems: 1` a `expected_outputs`.
- `dist/copilots/angular_18/shared/spec.json`
  - Sincronizado `outputSchema`.
  - Añadido `runtimeContract.requiredTraceFields` con `phase` y `expected_outputs`.
- `dist/copilots/angular_18/codex/AGENT.md`
- `dist/copilots/angular_18/claude/AGENT.md`
- `dist/copilots/angular_18/github-copilot/copilot-agent.md`
  - Sincronizado el schema embebido en prompts.
- `dist/copilots/angular_18/langchain/agent.py`
- `dist/copilots/angular_18/langchain/agent_profile.json`
  - Sincronizado `OUTPUT_SCHEMA` y perfil LangChain.
- `dist/copilots/angular_18/shared/codex_tool_protocol.json`
- `dist/copilots/angular_18/shared/claude_project_instructions.json`
- `dist/copilots/angular_18/github-copilot/copilot-profile.json`
- `dist/copilots/angular_18/langchain/agent_contract.json`
  - Actualizados digests estables del output schema.
- `tools/validate_runtime_equivalence.py`
  - La validación de trazas ahora lee `requiredTraceFields` tanto desde `runtimeParityContract` como desde `runtimeContract`.

## Comandos ejecutados

- `git status --short`
  - Resultado: no disponible; el workspace actual no es un repositorio Git.
- `python -m py_compile dist\copilots\angular_18\langchain\agent.py tools\validate_runtime_equivalence.py`
  - Resultado: compila, pero generó `__pycache__`; se limpiaron los cachés dentro del workspace antes de la validación final.
- `python tools/validate_copilot_factory.py`
  - Primer resultado: falló solo por `__pycache__` generado durante la comprobación local.
  - Resultado final: PASS, 18 copilots, 50 agents, 50 tasks.
- `python tools/validate_prompt_quality.py`
  - Resultado final: PASS, 18 copilots, 72 runtime prompts.
- `python tools/validate_runtime_equivalence.py`
  - Resultado intermedio: falló por digest drift tras cambiar schema.
  - Resultado final: PASS, 18 copilots checked.
- Smoke específico:
  - Comando: comprobación Python local de `spec.outputSchema == output_schema`, `LangChain OUTPUT_SCHEMA == output_schema`, `phase`/`expected_outputs` requeridos y `runtimeContract.requiredTraceFields` presente.
  - Resultado: `Angular 18 contract smoke PASS`.
- `Get-ChildItem -Recurse -Directory -Filter __pycache__`
  - Resultado final: sin cachés Python residuales.

## Riesgos residuales

- El generador `tools/generate_copilot_factory.py` parece no ser la única fuente actual de los artefactos V2; si se regenera desde una plantilla anterior, podría sobrescribir este endurecimiento. Riesgo aceptado para esta tarea porque el DoD y los validadores operan sobre los artefactos runtime actuales.
- No se ejecutó una validación JSON Schema con instancias reales porque el repo no declara fixture de salida Angular 18; el smoke cubre coherencia estructural y los validadores cubren equivalencia runtime.
- No hay verificación visual porque no se modificó producto frontend renderizable.
