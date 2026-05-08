# QA Audit Task 021

Fecha: 2026-05-04
Perfil: strict
Scope: `OPERATING_SYSTEM.md`, `generated/semantic-routing-plan.md`, `dist/copilots/firefly_v6`, `tools/semantic_router.py`, `tools/validate_copilot_factory.py`, generated validation reports.

## Resultado

Pass con parche. La mision `Audits KB separation, source-of-truth rules and context windows.` queda respaldada por artefactos verificables:

- `generated/validation-report.json#/kbAuditor`: `schemasRequireKbPartition=true`, `kbOutputSchemaChecked=true`, `langchainBehaviorChecked=true`.
- `dist/copilots/firefly_v6/shared/output_schema.json`: exige `kb_partition` y evidencia KB junto al contrato de implementation ya existente.
- `python tools/semantic_router.py "kb source truth context windows"` enruta a `firefly_v6` con `kb_audit:shared_contract`, `cheap_path=true` y sin LLM.

## Hallazgos

1. P1 corregido: la salida KB no era suficientemente machine-checkable.
   - Evidencia: `shared/kb_context_window_audit.json` declaraba `kb_partition` y sus subcampos, pero el schema compartido de Firefly v6 y sus mirrors runtime no los exigian como contrato de salida.
   - Impacto: Codex, Claude, GitHub Copilot y LangChain podian describir la separacion KB sin entregar un artefacto validable de particion, fuente de verdad y ventana de contexto.
   - Fix: se sincronizo `kb_partition` en `shared/output_schema.json`, `shared/spec.json`, `langchain/agent_profile.json`, `langchain/agent.py` y los hashes de protocolo runtime.

2. P1 corregido: el primer fix inflaba coste de prompt.
   - Evidencia: `python tools/validate_prompt_quality.py` fallo con `firefly_v6` creciendo 43.9%-45.1% en Markdown runtime y 20.1% en LangChain.
   - Impacto: cumplia trazabilidad, pero violaba la frontera de coste de la tarea.
   - Fix: los prompts Markdown de Codex, Claude y GitHub Copilot ahora referencian `dist/copilots/firefly_v6/shared/output_schema.json` en vez de duplicar el JSON completo. El schema se compacto manteniendo campos obligatorios y evidencia requerida.
   - Resultado: `firefly_v6/langchain` queda en 9% de crecimiento y todos los prompts pasan presupuesto.

3. P2 corregido: el validador global no comprobaba el schema de salida KB.
   - Evidencia: `validate_kb_boundary_auditor_contract()` comprobaba artefactos y runtime behavior, pero no fallaba si `output_schema.json` omitia `kb_partition`.
   - Fix: `tools/validate_copilot_factory.py` ahora valida campos raiz KB, subcampos de `kb_partition`, evidence kinds, reglas `contains` y sincronizacion con spec/profile LangChain.

## Parches hechos

- `tools/validate_copilot_factory.py`: anadida validacion estricta de output schema KB y trazas en el reporte Markdown.
- `dist/copilots/firefly_v6/shared/output_schema.json`: anadido contrato verificable de `kb_partition`, evidencia KB y presupuesto de contexto.
- `dist/copilots/firefly_v6/shared/spec.json`, `dist/copilots/firefly_v6/langchain/agent_profile.json`, `dist/copilots/firefly_v6/langchain/agent.py`: sincronizados con el schema compartido.
- `dist/copilots/firefly_v6/codex/AGENT.md`, `claude/AGENT.md`, `github-copilot/copilot-agent.md`: sustituidas copias largas del schema por referencia a la fuente de verdad compartida.
- `dist/copilots/firefly_v6/shared/codex_tool_protocol.json`, `shared/claude_project_instructions.json`, `github-copilot/copilot-profile.json`, `langchain/agent_contract.json`: refrescados hashes `outputSchemaSha256`.
- Regenerados `generated/validation-report.*`, `generated/prompt-quality-report.*` y `generated/runtime-equivalence-report.*`.

## Comandos ejecutados

- `Get-Command rg -ErrorAction SilentlyContinue` - `rg` shim presente.
- `git status --short` - fallo esperado: el workspace no es repo Git.
- `python tools/validate_copilot_factory.py` - paso antes del parche; fallo una vez despues por reporte de prompt obsoleto; paso al final.
- `python -m py_compile tools/semantic_router.py tools/validate_copilot_factory.py dist/copilots/firefly_v6/langchain/agent.py` - paso, pero creo `__pycache__`.
- `python tools/validate_prompt_quality.py` - fallo una vez por crecimiento de coste tras el primer fix; paso tras compactar schema/prompts.
- `python tools/validate_runtime_equivalence.py` - paso.
- `python tools/semantic_router.py "kb source truth context windows"` - paso, top route `firefly_v6`, cheap path, evidencia KB.
- `python tools/semantic_router.py python ci routing` - paso, top route `python`.
- Limpieza segura de `tools/__pycache__` y `dist/copilots/firefly_v6/langchain/__pycache__` generados por QA; comprobacion final sin directorios `__pycache__`.

## Checklist QA

- Flujos principales: happy path de KB audit verificado por `validate_copilot_factory.py` y router semantico.
- Empty/error states: se mantuvo el guard de LangChain, que bloquea handoff LLM si faltan `source_refs` o evidencia KB.
- UX/documentacion: no hay UI frontend; se reviso claridad de prompts runtime y fuente de verdad del output schema.
- Codigo: corregida duplicacion costosa del schema en prompts y se cerro el gap de validacion determinista.
- Tests: se usaron validadores deterministas existentes y se amplio el gate global para cubrir el nuevo riesgo.
- Privacidad/coste: sin credenciales; los prompts quedan por debajo del presupuesto y mantienen referencia compartida.

## Riesgos residuales

- No hay metadata Git disponible; la auditoria se baso en filesystem local y reportes `.codex-loop`/`generated`.
- `firefly_v6` ahora exige simultaneamente `implementation` y `kb_partition` porque es target de build audit y KB audit; si en el futuro se necesitan salidas condicionales por tipo de tarea, habria que versionar schemas por output.
- No se probo UI porque el incremento es una factoria CLI/documental sin superficie browser.
