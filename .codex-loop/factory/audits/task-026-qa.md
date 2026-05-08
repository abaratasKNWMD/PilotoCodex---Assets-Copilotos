# QA Audit Task 026 - Copiloto DevEx Runtime Equivalence

Fecha: 2026-05-05
Perfil: strict
Tarea auditada: `[P1][copilot_owner_26_devex] Room: Control Room | Concurrency: parallel-safe | Goal: mantener equivalencia real entre Codex, Claude, GitHub Copilot y LangChain sin inflar costes ni perder trazabilidad.`

## Veredicto

PASS con parche menor aplicado.

El contrato DevEx queda coherente entre los cuatro runtimes:

- `dist/copilots/devex/shared/spec.json`: define `runtimeParityContract` con Codex, Claude, GitHub Copilot y LangChain, `maxUnexplainedDrift=0`, schema compartido y reglas de coste/trazabilidad.
- `dist/copilots/devex/codex/AGENT.md`, `dist/copilots/devex/claude/AGENT.md` y `dist/copilots/devex/github-copilot/copilot-agent.md`: incluyen runtime injection, prompts compartidos, Python Brain Contract y Runtime Parity Contract.
- `dist/copilots/devex/langchain/agent.py`: expone `build_agent`, `score`, `audit`, `plan`, `render_prompt`, `output_schema` y redaccion de inputs antes de renderizar prompts.
- `generated/runtime-equivalence-report.json`: `pass=true`, 18 copilots revisados, `devex` con 4 runtimes e `issues=0`.

## Hallazgos

1. Low corregido - el README operativo de DevEx omitia `python tools/validate_runtime_equivalence.py` en los checks pre-handoff.
   - Impacto: el paquete documentaba factory y prompt quality, pero no el validador que prueba el DoD principal de esta tarea.
   - Estado: corregido en `dist/copilots/devex/README.md`.

2. Informativo - `python -m py_compile` creo caches `__pycache__` bajo `dist/copilots`, que el validador bloquea como artefactos de release.
   - Impacto: fallo temporal de `validate_copilot_factory.py` con 4 issues de bytecode cache.
   - Estado: caches eliminados, validador vuelve a PASS, y se verifico que no quedan carpetas `__pycache__` bajo `dist/copilots`.

## Parches Hechos

- `dist/copilots/devex/README.md`
  - Agregado `python tools/validate_runtime_equivalence.py` al runbook de handoff para alinear documentacion con el contrato de equivalencia runtime.

- `.codex-loop/factory/audits/task-026-qa.md`
  - Creada esta evidencia QA obligatoria.

## Checklist QA

- Flujos principales: PASS. Los tres validadores requeridos pasan y el smoke runtime de LangChain pasa con evidencia completa.
- Empty/error states: PASS. `agent.plan('', {})` rechaza request vacia con `ValueError`; la ausencia de evidencia se reporta como `evidence_needed` en vez de inventar datos.
- Loading/error states: No aplica UI frontend. La UX operativa es CLI/Markdown/JSON.
- UX/copy/accesibilidad: PASS para documentacion operativa; se corrigio el runbook incompleto. No hay formularios ni interfaz responsive.
- Codigo: PASS. No se detectaron errores Python evidentes en el adaptador; imports, API publica, sanitizacion y contrato de salida funcionan.
- Tests/validacion: PASS. Se ejecutaron validadores oficiales y smoke directo del adaptador LangChain con redaccion de token placeholder.
- Documentacion: PASS con parche en README.
- Privacidad/coste/trazabilidad: PASS. El contrato mantiene Python-first, LLM solo para juicio, referencias compartidas y redaccion de credenciales.

## Comandos Ejecutados

- `Get-Command rg -ErrorAction SilentlyContinue`
- `git status --short` - fallo esperado: esta carpeta no es repositorio Git.
- `Get-ChildItem -LiteralPath dist\copilots\devex -Recurse`
- `Get-Content -Raw -LiteralPath dist\copilots\devex\shared\spec.json`
- `Get-Content -Raw -LiteralPath dist\copilots\devex\codex\AGENT.md`
- `Get-Content -Raw -LiteralPath dist\copilots\devex\claude\AGENT.md`
- `Get-Content -Raw -LiteralPath dist\copilots\devex\github-copilot\copilot-agent.md`
- `Get-Content -Raw -LiteralPath dist\copilots\devex\langchain\agent.py`
- `Get-Content -Raw -LiteralPath dist\copilots\devex\shared\output_schema.json`
- `Get-Content -Raw -LiteralPath dist\copilots\devex\langchain\agent_contract.json`
- `Get-Content -Raw -LiteralPath dist\copilots\devex\README.md`
- `python tools\validate_copilot_factory.py` - PASS inicial.
- `python tools\validate_prompt_quality.py` - PASS inicial.
- `python tools\validate_runtime_equivalence.py` - PASS inicial.
- `python dist\copilots\devex\langchain\agent.py "build implementation stack rules affected files rollback"` - PASS; devuelve plan con evidencia requerida cuando no se aporta evidence pack.
- `python -m py_compile dist\copilots\devex\langchain\agent.py dist\copilots\_runtime_safety.py` - compila, pero genero caches de bytecode bloqueados por release hygiene.
- `rg -n "TODO|FIXME|placeholder-token|credentialValue|rawPrompt|systemPrompt|developerPrompt|C:\\Users|/home/|/Users/" dist\copilots\devex generated\runtime-equivalence-report.json generated\validation-report.json generated\prompt-quality-report.json`
- `python tools\validate_copilot_factory.py` - fallo temporal por `__pycache__` generado por el smoke.
- Borrado no recursivo via Python de los dos `.pyc` conocidos y sus carpetas vacias, con verificacion de rutas dentro del workspace.
- `python tools\validate_copilot_factory.py` - PASS final.
- `python tools\validate_prompt_quality.py` - PASS final.
- `python tools\validate_runtime_equivalence.py` - PASS final.
- Smoke LangChain con `PYTHONDONTWRITEBYTECODE=1`: happy path con evidencia completa, rechazo de request vacia y redaccion de token placeholder - PASS.
- `Get-ChildItem -LiteralPath dist\copilots -Directory -Recurse -Force -Filter __pycache__` - sin resultados.
- Consultas JSON sobre `generated/validation-report.json`, `generated/prompt-quality-report.json` y `generated/runtime-equivalence-report.json` - todos PASS, `issues=0`.
- `rg -n "validate_runtime_equivalence|Operator Runbook" dist\copilots\devex\README.md`
- `rg -n "Runtime Parity Contract|maxUnexplainedDrift|Runtime Injection|Python Brain Contract" dist\copilots\devex\codex\AGENT.md dist\copilots\devex\claude\AGENT.md dist\copilots\devex\github-copilot\copilot-agent.md dist\copilots\devex\langchain\agent.py dist\copilots\devex\shared\spec.json`

## Riesgos Residuales

- No hay repositorio Git local, asi que no se pudo comparar contra un diff historico ni confirmar autoria por commit.
- Los validadores regeneran `checkedAt` y digests en `generated/*`; se espera churn temporal en reportes aunque el contrato funcional no cambie.
- `py_compile` no debe usarse como smoke de release sin `PYTHONDONTWRITEBYTECODE=1`, porque crea caches que la propia factory bloquea.
