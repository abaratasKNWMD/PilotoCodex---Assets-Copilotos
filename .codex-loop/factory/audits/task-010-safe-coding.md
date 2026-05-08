# Task 010 Safe-Coding / Privacy Review

Fecha: 2026-05-04

Scope revisado: `tools/run_factory.py`, `tools/generate_copilot_factory.py`, `tools/validate_copilot_factory.py`, `generated/factory-audit.json`, `generated/validation-report.*`, `generated/prompt-quality-report.*`, `generated/runtime-equivalence-report.*`, `generated/test-strategy-audit-report.*` y evidencia DevOps generada.

Resultado: aprobado con parche defensivo.

## Hallazgos

- Severidad media: `generated/factory-audit.json` usaba `agent.log` como evidencia directa. El log operativo local no contenia credenciales reales detectadas, pero si contiene rutas absolutas locales. Esto no era adecuado como artefacto publicable de release.
- Severidad baja: no hay repositorio Git disponible en el workspace; la trazabilidad de rollback depende de snapshots bajo `.codex-loop/rollback` y `.codex-loop/backups`. El validador ya lo comprueba y los artefactos existen.
- Sin hallazgos: no se detectaron tokens, claves API, valores bearer, passwords reales ni datos de billing en los artefactos de release revisados.

## Parches hechos

- `tools/run_factory.py`: ahora genera `generated/devops-log-evidence.json` como evidencia saneada del log. El JSON contiene solo metadatos, conteos y checks; no almacena contenido de `agent.log`.
- `tools/generate_copilot_factory.py`: se actualizo la plantilla de `run_factory` para que el cambio no se pierda al regenerar la fabrica.
- `tools/validate_copilot_factory.py`: el contrato DevOps ahora exige `generated/devops-log-evidence.json`, rechaza publicar `agent.log` como `logEvidence`, valida la privacidad del resumen saneado y anade un caso negativo `raw_log_evidence`.
- `generated/factory-audit.json` y `generated/validation-report.*`: regenerados con `logEvidence` apuntando al reporte saneado.
- `generated/devops-log-evidence.json`: nuevo artefacto verificable. Resultado: `pass=true`, `secretPatternMatches=0`, `contentStored=false`, `localAbsolutePathMatches=222` solo como conteo.

## Comandos ejecutados

- `Get-Command rg -ErrorAction SilentlyContinue`
- `git status --short` -> no es repositorio Git.
- Busquedas defensivas con `rg`/`Select-String` para tokens, bearer values y rutas absolutas.
- `python -m py_compile tools/run_factory.py tools/validate_copilot_factory.py tools/generate_copilot_factory.py`
- `python tools/run_factory.py` -> PASS en factory, prompt quality y runtime equivalence.
- `python tools/validate_copilot_factory.py && python tools/validate_prompt_quality.py` -> PASS.

## Riesgos residuales

- `agent.log` sigue existiendo como log operativo local y contiene rutas absolutas locales. Queda tratado como fuente local-only, no como evidencia publicable; el artefacto de release almacena solo el resumen saneado.
- Al no existir `.git`, la restauracion sigue dependiendo de snapshots locales. Esta condicion esta reflejada y validada por el Control Room.
