# QA Audit Task 015

Fecha: 2026-05-04
Perfil: strict
Tarea auditada: `[P1][factory_agent_15_claude] Builds Claude-facing project instructions and agent cards.`

## Veredicto

Pass con parche aplicado.

La mision Claude-facing esta reflejada en artefactos verificables: `dist/copilots/*/shared/claude_project_instructions.json`, `dist/copilots/*/claude/AGENT.md`, `generated/runtime-injection-map.json` y `generated/runtime-equivalence-report.json`.

## Hallazgos

- P1 corregido: los `AGENT.md` de Codex y Claude tenian el primer bullet de `Runtime Specific Protocol` con cuatro espacios iniciales. En Markdown eso se renderiza como bloque de codigo, degradando instrucciones operativas justo en la seccion runtime-specific. El problema afectaba a 36 adaptadores: 18 Codex y 18 Claude.
- Gap de test corregido: `tools/validate_runtime_equivalence.py` no detectaba este fallo de formato, aunque impactaba directamente la usabilidad de las instrucciones Claude-facing y la equivalencia real entre runtimes.
- Sin hallazgos funcionales adicionales en los gates de estructura, prompt quality o runtime equivalence despues del parche.

## Parches Hechos

- `tools/elevate_copilot_prompts.py`: `runtime_specific_protocol()` ahora genera bullets con `as_bullets()` para evitar indentacion accidental al interpolar secciones multilinea.
- `tools/validate_runtime_equivalence.py`: se anadio validacion de la seccion `Runtime Specific Protocol` para detectar bullets indentados que renderizan como bloque de codigo.
- `tools/validate_runtime_equivalence.py`: se anadio caso negativo `indented_runtime_protocol_markdown` al test strategy audit.
- `dist/copilots/*/codex/AGENT.md` y `dist/copilots/*/claude/AGENT.md`: reescritura mecanica acotada para normalizar `^    - ` a `- ` en los 36 adaptadores afectados.
- Reportes regenerados por validadores: `generated/prompt-quality-report.*`, `generated/runtime-equivalence-report.*` y `generated/validation-report.*`.

## Comandos Ejecutados

- `Get-Command rg -ErrorAction SilentlyContinue`: `rg` disponible como shim local.
- `git status --short`: fallo esperado; el workspace no es un repositorio Git.
- `python tools\validate_copilot_factory.py`: pass inicial antes del parche.
- `python tools\validate_prompt_quality.py`: pass inicial antes del parche.
- `python tools\validate_runtime_equivalence.py`: pass inicial antes del nuevo gate.
- `python tools\validate_runtime_equivalence.py`: fallo esperado tras anadir el nuevo gate; detecto 36 incidencias `*_runtime_specific_protocol_markdown`.
- Reescritura PowerShell mecanica de 36 `AGENT.md` Codex/Claude afectados.
- `Select-String -Path dist\copilots\*\codex\AGENT.md,dist\copilots\*\claude\AGENT.md -Pattern "^    - "`: 0 ocurrencias despues del parche.
- `python tools\validate_prompt_quality.py`: PASS, 18 copilots y 72 runtime prompts.
- `python tools\validate_runtime_equivalence.py`: PASS, 18 copilots checked.
- `python tools\validate_copilot_factory.py`: PASS, 18 copilots, 50 agents, 50 tasks.
- `python tools\validate_copilot_factory.py && python tools\validate_prompt_quality.py && python tools\validate_runtime_equivalence.py`: PASS completo.

## Notas De Limpieza

- `python -m py_compile` se probo para los scripts tocados, pero genero `tools/__pycache__`, que el gate de release bloquea. Se elimino el cache exacto creado durante la auditoria y se verifico que no quedaran directorios `__pycache__` bajo `tools`.

## Riesgos Residuales

- No hay metadata Git local, asi que la trazabilidad de diff depende de esta auditoria, los timestamps de archivos y los reportes generados.
- No se ejecuto una regeneracion completa con `tools/elevate_copilot_prompts.py` para evitar churn amplio en timestamps y artefactos no necesarios. El generador quedo corregido y los artefactos afectados se parchearon de forma mecanica.
- La revision fue de producto/codigo para artefactos CLI/Markdown/JSON; no aplica UX visual responsive ni estados de loading/error de una UI web.
