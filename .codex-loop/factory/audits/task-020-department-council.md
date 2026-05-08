# Department Council Audit - Task 020

Task: `[P1][factory_agent_20_cost] Routes cheap deterministic work to Python and expensive judgement to LLMs.`

Scope: `README.md`, `factory-prompt.md`, `.vscode/settings.json`, `.codex-loop/factory`, generated reports and `tools/validate_copilot_factory.py`.

Verification executed:

- `python tools/validate_copilot_factory.py` - PASS: 18 copilots, 50 agents, 50 tasks.
- `python tools/validate_prompt_quality.py` - PASS: 18 copilots, 72 runtime prompts.
- `python tools/validate_runtime_equivalence.py` - PASS: 18 copilots checked.
- `python tools/semantic_router.py python ci routing` - PASS: top route `python`, `cheap_path=true`, `routing_evidence.llm_assist_used=false`.

| Departamento | PASS-FAIL | Evidencia | Cambios | Riesgos |
| --- | --- | --- | --- | --- |
| Product | PASS | La mision esta materializada en `.codex-loop/factory/cost-routing-contract.json`, `.codex-loop/factory/cost-routing-scorecard.json`, `.codex-loop/factory/cost-routing-policy.md`, `README.md` y `factory-prompt.md`. `generated/validation-report.json#/costRoutingAuditor` reporta `pass=true`. | Sin parche funcional nuevo; se crea este informe de council. | Riesgo residual aceptado: el juicio LLM sigue siendo cualitativo, mitigado por gates Python previos y trazas obligatorias. |
| Engineering | PASS | `tools/validate_copilot_factory.py` valida `COST_REQUIRED_SETTINGS`, contrato, scorecard, policy doc, runtime equivalence, traceability, cheap work y judgement work. El gate actual paso. | Sin cambios adicionales; los parches previos ya agregaron el policy doc al docs auditor y `codexLoop.rawLogPromptsAllowed` al gate de coste. | Sin Git metadata local; la reproducibilidad se apoya en lock, snapshots y reportes generados. |
| Web/UI/Design | PASS | No hay superficie browser/UI en esta tarea. La experiencia operativa queda en README, factory prompt y policy doc con comandos y artefactos trazables. | No aplica parche UI. | Browser QA no aplica para este incremento local de contratos y validadores. |
| Creative Studio | PASS | No se introducen assets, imagenes, mockups, deck ni motion. La tarea no requiere contenido visual para demostrar el DoD. | No aplica cambio creativo. | Riesgo residual bajo: ausencia deliberada de assets por no ser producto visual. |
| QA | PASS | `generated/test-strategy-audit-report.json` reporta `pass=true`, 6 pairwise cases entre Codex, Claude, GitHub Copilot y LangChain, negative cases detectados y route sample barato. Validadores actuales pasaron. | Sin parche nuevo; QA previo documento el fix de cobertura del cost-routing policy en docs auditor. | Cobertura centrada en contratos deterministicos; no ejecuta conectores externos reales. |
| Safe-coding/Privacy | PASS | `.vscode/settings.json` mantiene `codexLoop.rawLogPromptsAllowed=false`; el contrato fija `placeholderOnlyCredentials=true`; `generated/validation-report.json#/securityAuditor` y `#/mcpConnectorAuditor` reportan pass y placeholders vacios. | Sin parche nuevo; Safe-coding previo endurecio `rawLogPromptsAllowed` como required setting del auditor de coste. | Sin runtime externo ejercitado; secretos reales deben seguir fuera del workspace. |
| Growth/SEO/Content | PASS | README y `factory-prompt.md` explican el Cost Routing Governor sin claims comerciales ni expansion de alcance. `generated/documentation-audit-report.json` incluye `.codex-loop/factory/cost-routing-policy.md` en operator docs. | No aplica parche SEO/content nuevo. | SEO/landing no aplica; el entregable es interno de operaciones. |
| Legal/Risk | PASS | No hay scraping, datos de cliente, billing real ni credenciales. Los conectores MCP son declarativos, deshabilitados y con env placeholders. | Sin cambios legales. | Riesgo residual: claims de equivalencia dependen de los validadores locales y no de certificacion externa. |
| Packaging/Release | PASS | `generated/validation-report.json` mantiene `pass=true`; `generated/prompt-quality-report.json` mantiene presupuesto de coste con `maxGrowthRatio=0.1`; `generated/runtime-equivalence-report.json` mantiene 18 copilots equivalentes. | Sin parche de packaging. | No hay artefacto instalable ni release externo en scope. |
| Commercial/Finance | PASS | La politica evita inflar coste: cheap deterministic work va a Python y judgement LLM requiere `python_gates_pass`; el scorecard incluye `prompt_growth_budget_traced`. | Sin cambios comerciales. | Hipotesis financiera no cuantificada en euros/dolares; aceptado porque la tarea pide control de routing, no pricing. |

Council result: PASS. No FAIL accionable nuevo fue encontrado durante la revision cruzada; los riesgos restantes quedan documentados como residuales y mitigados por los gates Python-first, equivalencia de runtime y bloqueo de prompts con logs crudos.
