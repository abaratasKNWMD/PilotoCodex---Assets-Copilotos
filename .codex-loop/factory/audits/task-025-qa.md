# QA Audit Task 025 - Validator Smoke Runner

Fecha: 2026-05-05
Perfil: strict
Tarea auditada: `[P1][factory_agent_25_smoke] Runs generated validators and reports blockers.`

## Veredicto

PASS con parches aplicados.

La mision queda reflejada en artefactos verificables y no solo en texto descriptivo:

- `generated/validator-smoke/copilot-factory.json`: recibo del validador factory con comando, digest del reporte, estado y blockers.
- `generated/validator-smoke/prompt-quality.json`: recibo del validador de calidad de prompts.
- `generated/validator-smoke/runtime-equivalence.json`: recibo del validador de equivalencia runtime.
- `generated/validator-smoke-report.json`: agregado de los 3 recibos con `completedValidators=3`, `expectedValidators=3`, `blockerCount=0`, `pass=true`, `promptBodiesStored=false` y modo `receipts_from_actual_validator_processes_no_recursive_subprocess`.
- `generated/validation-report.json`, `generated/prompt-quality-report.json` y `generated/runtime-equivalence-report.json`: los tres reportes fuente pasan con 0 issues.

## Hallazgos

1. Medium corregido - la validacion de shape de recibos smoke no era equivalente entre los tres validadores.
   - Impacto: el agregado final dependia del ultimo validador ejecutado; un recibo con drift en `runtimeEquivalence` o claves de cuerpo de prompt podia no ser detectado por todas las rutas.
   - Estado: corregido en `tools/validate_copilot_factory.py`, `tools/validate_prompt_quality.py` y `tools/validate_runtime_equivalence.py`.

2. Medium corregido - `tools/validate_runtime_equivalence.py` podia lanzar una excepcion si `runtimeEquivalence` en un recibo smoke no era un objeto.
   - Impacto: un recibo corrupto podia romper la auditoria en vez de quedar reportado como shape issue/blocker.
   - Estado: corregido; los tres validadores ahora reportan `runtimeEquivalence must be an object`.

3. Low corregido - `README.md` no documentaba la nueva superficie `generated/validator-smoke-report.*` ni los recibos `generated/validator-smoke/*.json`.
   - Impacto: la evidencia operativa quedaba solo en artefactos generados, no en la documentacion principal.
   - Estado: corregido.

## Parches Hechos

- `tools/validate_copilot_factory.py`
  - Agregado contrato comun `SMOKE_RUNTIME_EQUIVALENCE_ASSERTIONS`.
  - Agregada deteccion de claves prohibidas de cuerpo de prompt en recibos smoke.
  - Endurecida la validacion de `runtimeEquivalence` para tipo, source of truth, max drift, prompt bodies y assertions.

- `tools/validate_prompt_quality.py`
  - Alineada la validacion smoke con los mismos checks de equivalencia runtime.
  - Reutilizada la deteccion existente de claves prohibidas de prompt.

- `tools/validate_runtime_equivalence.py`
  - Corregido el acceso inseguro a `.get()` cuando `runtimeEquivalence` no es dict.
  - Agregada deteccion de claves prohibidas de cuerpo de prompt en recibos smoke.

- `README.md`
  - Documentados `generated/validator-smoke-report.*`, `generated/validator-smoke/<validator>.json` y el contrato operativo de `factory_agent_25_smoke`.

## Checklist QA

- Flujos principales: PASS. El comando DoD ejecuta los 3 validadores y actualiza recibos y agregado smoke.
- Empty/error states: PASS con parche. Recibos malformados por tipo incorrecto en `runtimeEquivalence` se reportan como issue en vez de romper el proceso.
- Loading/error UX: No aplica UI frontend. La UX operativa queda en Markdown/JSON generados y README.
- Accesibilidad/formularios/responsive: No aplica; no hay interfaz visual ni formularios.
- Codigo: PASS con parche. Se redujo drift funcional entre validadores smoke y se mantuvo el scope en archivos de la tarea.
- Tests/validacion: PASS. Se ejecuto una prueba negativa local de shape de recibos y la verificacion completa.
- Documentacion: PASS con parche en README.
- Privacidad/coste/trazabilidad: PASS. Los recibos guardan rutas relativas, SHA-256, estado y blockers; no guardan cuerpos de prompt.

## Comandos Ejecutados

- `Get-Command rg -ErrorAction SilentlyContinue`
- `git status --short` - fallo esperado: esta carpeta no es repositorio Git.
- `Get-ChildItem -Path . -Force`
- `Get-Content -Raw -Path tools/validate_copilot_factory.py`
- `Get-Content -Raw -Path tools/validate_prompt_quality.py`
- `Get-Content -Raw -Path tools/validate_runtime_equivalence.py`
- `Get-ChildItem -Path generated -File`
- `python tools/validate_copilot_factory.py; if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }; python tools/validate_prompt_quality.py; if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }; python tools/validate_runtime_equivalence.py; if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }` - PASS antes y despues del parche.
- `rg -n "def (build_current_validator_smoke|write_validator_smoke_artifacts|build_validator_smoke_report|smoke_receipt_shape_issues|smoke_runtime_equivalence_contract|normalize_validator_blockers|sha256_path|write_json_atomic|write_text_atomic|render_validator_smoke_report_md)" tools/validate_copilot_factory.py tools/validate_prompt_quality.py tools/validate_runtime_equivalence.py`
- `rg -n "TODO|FIXME|pass #|except Exception|except:|subprocess|os\.system|eval\(|exec\(" tools/validate_copilot_factory.py tools/validate_prompt_quality.py tools/validate_runtime_equivalence.py`
- `Get-Content -Raw -Path generated/validator-smoke-report.json`
- `Get-Content -Raw -Path generated/validator-smoke/copilot-factory.json`
- `Get-Content -Raw -Path generated/validator-smoke/prompt-quality.json`
- `Get-Content -Raw -Path generated/validator-smoke/runtime-equivalence.json`
- `rg -n "factory_agent_25_smoke|Runs generated validators" data tools generated README.md tasks.json factory.config.json`
- `rg -n "validator-smoke|Validator Smoke|smoke report|validate_copilot_factory|validate_prompt_quality|validate_runtime_equivalence" README.md OPERATING_SYSTEM.md factory-prompt.md`
- `python -` con imports locales y negativos sinteticos para `smoke_receipt_shape_issues` - PASS.
- `rg -n "SMOKE_RUNTIME_EQUIVALENCE_ASSERTIONS|SMOKE_FORBIDDEN_PROMPT_KEYS|runtimeEquivalence must be an object|prompt body key detected|Validator Smoke Evidence|validator-smoke-report" tools/validate_copilot_factory.py tools/validate_prompt_quality.py tools/validate_runtime_equivalence.py README.md`
- `python tools/validate_copilot_factory.py && python tools/validate_prompt_quality.py && python tools/validate_runtime_equivalence.py` - PASS final.

## Riesgos Residuales

- No hay repositorio Git local, asi que la auditoria no puede apoyarse en diff historico ni commits.
- Los validadores regeneran `checkedAt` y digests de reportes, por lo que cada ejecucion produce churn temporal en los artefactos generados.
- La logica smoke sigue duplicada en tres scripts por compatibilidad con el incremento existente; queda alineada por este parche, pero un refactor futuro a helper compartido reduciria riesgo de drift.
