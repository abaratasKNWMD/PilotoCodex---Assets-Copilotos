# Copilot Factory Prompt

Este workspace es una fabrica de copilotos multiplataforma.

Objetivo operativo:

- Mantener 18 copilotos equivalentes en Codex, Claude, GitHub Copilot y LangChain.
- Tratar Python como cerebro determinista para catalogo, routing, validacion y auditoria.
- Usar LLM solo para juicio fino, copy final o diseno de cambios no triviales.
- Ejecutar el Control Room desde `factory.config.json/controlRoom`: el director posee la corrida, bloquea deriva de alcance y exige evidencia antes de declarar done.

Instrucciones para Codex Loop:

1. Trabaja solo dentro de `NuevoProyecto/`.
2. Antes de editar, inspecciona `.codex-loop/run.lock.json`, `data/copilots.json`, `data/agent_roster.json`, `generated/runtime-injection-map.json` y el copilot afectado.
3. No rompas equivalencia entre runtimes: si cambias `shared/spec.json`, revisa Codex, Claude, GitHub Copilot y LangChain.
4. Valida con:
   - `python tools/validate_copilot_factory.py`
   - `python tools/validate_prompt_quality.py`
   - `python tools/validate_runtime_equivalence.py`
5. Evita meter secretos, tokens o credenciales reales. Solo nombres de variables de entorno.
6. Mantén las tareas acotadas y deja evidencia verificable.

Contrato del Factory Director:

- State lock: respeta `.codex-loop/run.lock.json`; comprueba campos requeridos, workspace, orden de timestamps y snapshot local si no hay Git.
- Gate honesty: no aceptes "done" sin reports generados o riesgo residual explicito.
- Runtime parity: usa `dist/copilots/<copilot>/shared/spec.json` como canon y `generated/runtime-injection-map.json` como mapa de trazabilidad.
- Cost trace: ejecuta Python primero y reserva LLM para juicio escaso, cambios de codigo y sintesis final.
- Cost Routing Governor: aplica `.codex-loop/factory/cost-routing-contract.json`; el auditor `generated/validation-report.json#/costRoutingAuditor` debe demostrar que el trabajo determinista barato queda en Python y que el juicio LLM solo ocurre despues de evidencia de gates Python.
- Scope lock: toca solo archivos declarados o tooling minimo de verificacion; productos nuevos van bajo `products/<slug>/` con registry.

Operate Auditor Contract:

- `factory_agent_13_operate` audita observability, incident playbooks and runbooks desde `.codex-loop/factory/operate-observability-contract.json`.
- La evidencia verificable vive en `.codex-loop/factory/operate-observability-scorecard.json`, `.codex-loop/factory/operate-observability-runbook.md` y `generated/validation-report.json#/operateAuditor`.
- No uses logs crudos en prompts o reportes; referencia artefactos sanitizados como `.codex-loop/factory/codex-runtime-incidents.md`.
- Mantén equivalencia real entre Codex, Claude, GitHub Copilot y LangChain con `runtimeEquivalence.maxUnexplainedDrift=0`.

Cost Routing Contract:

- `factory_agent_20_cost` posee la mision `Routes cheap deterministic work to Python and expensive judgement to LLMs.`.
- Artefactos obligatorios: `.codex-loop/factory/cost-routing-contract.json`, `.codex-loop/factory/cost-routing-scorecard.json` y `.codex-loop/factory/cost-routing-policy.md`.
- Codex, Claude, GitHub Copilot y LangChain comparten la misma politica de coste: `sameCostRoutingPolicy=true`, `sameTraceFields=true` y `maxUnexplainedDrift=0`.
- `.vscode/settings.json` debe mantener `codexLoop.rawLogPromptsAllowed=false` como gate verificable del auditor de coste.
- Las rutas baratas deben registrar `routing_evidence.llm_assist_used=false`; las rutas de juicio deben apuntar a reports y no a logs crudos ni credenciales.
