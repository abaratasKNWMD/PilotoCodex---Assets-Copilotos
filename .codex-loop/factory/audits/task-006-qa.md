# Task 006 QA Audit

Fecha: 2026-05-04

Tarea auditada: `[P0][factory_agent_06_design] Audits domain boundaries, contracts and handoff clarity.`

Resultado: **PASS con parches aplicados**.

## Hallazgos

1. **Corregido - deriva real de contrato en LangChain.**
   Los cinco copilotos con fase `design` tenian `handoff` requerido en `shared/output_schema.json` y `shared/spec.json`, pero el `OUTPUT_SCHEMA` embebido en `dist/copilots/*/langchain/agent.py` no lo marcaba como requerido. Esto rompia la equivalencia real entre Codex, Claude, GitHub Copilot y LangChain para el handoff.

2. **Corregido - el validador no cubria el schema embebido del runtime LangChain.**
   `tools/validate_runtime_equivalence.py` comparaba spec, perfil y schema compartido, pero no parseaba el `OUTPUT_SCHEMA` literal dentro del agente Python. Se anadio esa comprobacion.

3. **Corregido - riesgo de regeneracion no reproducible.**
   `tools/generate_copilot_factory.py` y `tools/elevate_copilot_prompts.py` no preservaban completamente la superficie `design_boundary_audit` al regenerar/elevatar artefactos. Se anadieron contratos, perfiles, politica de indice, seccion de matriz SDLC, artefacto `design_boundary_audit.json`, referencias en runtime injection map y markers en runtime contracts/adaptadores.

4. **No aplica UI/frontend.**
   El incremento no expone pantalla, formulario, loading state ni navegacion. La revision UX se limita a claridad de artefactos, rutas CLI y payloads de handoff.

## Parches hechos

- Sincronizados los `OUTPUT_SCHEMA` embebidos en:
  - `dist/copilots/aida_architecture/langchain/agent.py`
  - `dist/copilots/angular_18/langchain/agent.py`
  - `dist/copilots/java_architect/langchain/agent.py`
  - `dist/copilots/java_generic/langchain/agent.py`
  - `dist/copilots/nodejs/langchain/agent.py`
- `tools/validate_runtime_equivalence.py` ahora parsea el AST de `langchain/agent.py` y falla si `OUTPUT_SCHEMA` deriva de `shared/output_schema.json`.
- `tools/elevate_copilot_prompts.py` ahora emite contratos Design Boundary, requiere `handoff` para copilotos de design y preserva evidencia en runtime map/adaptadores.
- `tools/generate_copilot_factory.py` ahora renderiza perfiles, politica de indice, contrato de agente y matriz SDLC para Design Boundary.
- `tools/validate_copilot_factory.py` ahora valida que el generador conserve la politica, agente y perfiles Design Boundary.

## Comandos ejecutados

- `Get-Command rg -ErrorAction SilentlyContinue`
- `git status --short` (sin repo Git en este workspace)
- `python tools/validate_copilot_factory.py`
- `python tools/semantic_router.py python ci routing`
- `python tools/validate_runtime_equivalence.py`
- `python -m py_compile tools/elevate_copilot_prompts.py tools/generate_copilot_factory.py tools/validate_copilot_factory.py tools/validate_runtime_equivalence.py tools/semantic_router.py`
- `python tools/semantic_router.py design domain boundaries contracts handoff`
- `python tools/semantic_router.py diseno dominio contratos limites handoff`
- Chequeo AST local: los 18 `dist/copilots/*/langchain/agent.py` tienen `OUTPUT_SCHEMA` igual a `shared/output_schema.json`.
- `python tools/validate_prompt_quality.py`

## Evidencia de verificacion

- `python tools/validate_copilot_factory.py` -> PASS: 18 copilots, 50 agents, 50 tasks.
- `python tools/validate_runtime_equivalence.py` -> PASS: 18 copilots checked.
- `python tools/validate_prompt_quality.py` -> PASS: 18 copilots, 72 runtime prompts.
- Routing `python ci routing` mantiene `python` como top route y conserva `runtime_trace` + `routing_evidence`.
- Routing `design domain boundaries contracts handoff` devuelve copilotos de design con `design_audit:shared_contract`, `cheap_path: true` y `design_boundary_audit.source_of_truth`.
- Routing localizado `diseno dominio contratos limites handoff` queda en cheap path y expone `design_boundary_audit`.

## Riesgos residuales

- No se ejecuto `python tools/generate_copilot_factory.py` completo para evitar reemitir todos los artefactos con timestamps nuevos; el contrato del generador fue validado por `validate_copilot_factory.py` y por compilacion/import.
- No hay Git metadata en el workspace, asi que no existe diff formal. La auditoria se basa en inspeccion local, validadores y artefactos generados.
- `tools/__pycache__` contiene bytecode generado por las validaciones/compilacion; esta cubierto por `.gitignore` y no forma parte de la superficie de release.
