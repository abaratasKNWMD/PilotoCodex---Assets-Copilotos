# Task 033 Department Council - Copiloto Java Generico

Fecha: 2026-05-05
Perfil: strict
Scope: `dist/copilots/java_generic/shared/spec.json`, adapters Codex/Claude/GitHub Copilot/LangChain, contratos auxiliares, validadores y reportes generados.

## Tabla de revision cruzada

| Departamento | PASS-FAIL | Evidencia | Cambios | Riesgos |
|---|---|---|---|---|
| Product | PASS | `spec.json` mantiene una necesidad concreta: desarrollo Java empresarial, refactoring y mantenibilidad. Limita stacks a `java`, `spring`, `maven`, `gradle`; fases a `design`, `build`, `test`; outputs a `java_patch_plan` y `test_plan`. | Sin cambio de alcance de producto. | Riesgo residual: no se ejecuto un LLM real produciendo un `java_patch_plan`; se valida contrato local, prompts y adapter. |
| Engineering | FAIL corregido -> PASS | QA detecto que `runtimeParityContract.requiredTraceFields` exigia `phase` y `expected_outputs` mientras el schema no los hacia obligatorios. La suite final confirma paridad: `validate_runtime_equivalence.py` PASS y smoke directo muestra ambos campos en `OUTPUT_SCHEMA.required`. | `phase` y `expected_outputs` quedaron obligatorios en `shared/output_schema.json`, `shared/spec.json`, prompts runtime y copias LangChain; `tools/validate_runtime_equivalence.py` valida que los trace fields requeridos esten en el schema. | Riesgo residual bajo: hay duplicacion intencional del schema en prompts/adapters para compatibilidad; queda controlada por digest y validadores. |
| Web/UI/Design | PASS / No aplica | No hay UI, navegacion, render, responsive ni accesibilidad en este incremento; la superficie es runtime-contracts. | Sin cambios. | Ninguno especifico de UI. |
| Creative Studio | PASS / No aplica | No se introducen imagenes, mockups, pitch deck, motion, storytelling ni assets sociales. | Sin cambios. | Ninguno para assets creativos. |
| QA | FAIL corregido -> PASS | Informe QA registra correccion de schema/parity, limpieza de `__pycache__` y ajuste de coste. Verificacion final: `validate_copilot_factory.py` PASS, `validate_prompt_quality.py` PASS, `validate_runtime_equivalence.py` PASS. | Reportes `generated/*` regenerados; validadores ejecutados en serie; matriz/digests actualizados por los scripts. | Riesgo residual: la cobertura es determinista/local y no prueba conectores remotos ni generacion externa. |
| Safe-coding/Privacy | FAIL corregido -> PASS | Safe-coding detecto precedencia debil al importar `_runtime_safety` desde LangChain. Smoke directo actual: 3 mensajes, redaccion de `github_pat_...` y `Bearer ...`, `phase_required=true`, `expected_outputs_required=true`. Busqueda de secretos/rutas en Java Generic y audits task-033 sin hallazgos. | `dist/copilots/java_generic/langchain/agent.py` usa `sys.path.insert(0, ...)`; `tools/validate_runtime_equivalence.py` acepta esa variante en la politica estatica. MCP queda placeholder: `credentialValue=""`, `credentialValuesStored=false`, `customerDataAllowed=false`, `billingDataAllowed=false`. | Riesgo residual: GitHub MCP no se activo porque no hay credenciales ni aprobacion de operador; la revision es offline por diseno. |
| Growth/SEO/Content | PASS / No aplica | No hay landing, metadata, blog, copy SEO ni funnel en los archivos auditados. | Sin cambios. | Ninguno para SEO/content. |
| Legal/Risk | PASS | El contrato usa nombres de capacidad y variables (`github_mcp`, `GITHUB_TOKEN`) sin valores. `mcp-placeholders.json` mantiene conector deshabilitado y sin customer/billing data. | Sin cambios legales directos; riesgo residual documentado. | Sin repositorio Git inicializado; trazabilidad depende de reportes generados y audits locales, no de commits. |
| Packaging/Release | FAIL corregido -> PASS | QA registro que un smoke local habia creado `__pycache__` bajo `dist/copilots/java_generic/langchain/`, rechazado por release gate. Check actual no devuelve caches bajo `dist/copilots/java_generic`. | Cache eliminado; smoke actual ejecutado con `python -B`; validadores oficiales pasan. | Riesgo residual bajo: imports manuales sin bytecode desactivado podrian recrear cache, pero el flujo de validacion oficial lo detecta. |
| Commercial/Finance | PASS | No hay pricing, billing real, customer data ni claims comerciales. La disciplina de coste se mantiene: Python-first, LLM solo para juicio estrecho y `prompt-quality` PASS. | Sin cambios. | Riesgo residual: hipotesis comercial y demos fuera de alcance de esta tarea. |

## Validacion ejecutada

- `python tools/validate_copilot_factory.py`: PASS, 18 copilots, 50 agents, 50 tasks.
- `python tools/validate_prompt_quality.py`: PASS, 18 copilots, 72 runtime prompts.
- `python tools/validate_runtime_equivalence.py`: PASS, 18 copilots checked.
- Smoke LangChain con `python -B`: PASS; `render_prompt()` devuelve 3 mensajes, redacta token GitHub/Bearer sinteticos y el schema exige `phase` y `expected_outputs`.
- Check de release: sin `__pycache__` bajo `dist/copilots/java_generic`.
- Busqueda de patrones sensibles en Java Generic y audits task-033: sin matches.

## Archivos parcheados o actualizados en la tarea

- `dist/copilots/java_generic/shared/spec.json`
- `dist/copilots/java_generic/shared/output_schema.json`
- `dist/copilots/java_generic/codex/AGENT.md`
- `dist/copilots/java_generic/claude/AGENT.md`
- `dist/copilots/java_generic/github-copilot/copilot-agent.md`
- `dist/copilots/java_generic/github-copilot/copilot-profile.json`
- `dist/copilots/java_generic/langchain/agent.py`
- `dist/copilots/java_generic/langchain/agent_contract.json`
- `dist/copilots/java_generic/langchain/agent_profile.json`
- `tools/validate_runtime_equivalence.py`
- Reportes bajo `generated/`
- `.codex-loop/factory/audits/task-033-qa.md`
- `.codex-loop/factory/audits/task-033-safe-coding.md`
- `.codex-loop/factory/audits/task-033-department-council.md`

## Riesgos residuales consolidados

- La equivalencia validada es local y contractual: schema, prompts, digests, adapters y LangChain smoke. No incluye invocacion real de LLM externo.
- GitHub MCP permanece correctamente como placeholder/offline; no se prueba activacion real ni operaciones remotas.
- No hay repositorio Git inicializado en este workspace; la trazabilidad queda en reportes `generated/*` y archivos de auditoria.
