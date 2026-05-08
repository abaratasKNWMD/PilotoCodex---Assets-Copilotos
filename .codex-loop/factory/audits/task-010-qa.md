# Task 010 QA Audit

## Alcance

- Tarea auditada: `[P0][factory_agent_10_devops] Audits CI/CD, logs, reproducibility and rollback paths.`
- Superficie revisada: `tools/run_factory.py`, `tools/generate_copilot_factory.py`, `tools/validate_copilot_factory.py` y artefactos `generated/*report*`.
- UI/UX: no aplica. El incremento es CLI/runtime-toolchain, sin pantallas, formularios, estados visuales ni navegacion de usuario.

## Hallazgos

1. **Fail real de reproducibilidad tras regenerar. Corregido.**
   - `tools/run_factory.py` habia sido mejorado por la tarea, pero `tools/generate_copilot_factory.py` seguia emitiendo una version antigua.
   - Al ejecutar `python tools/run_factory.py`, el generador sobrescribio `tools/run_factory.py` y la validacion fallo porque desaparecieron `RUN_SEQUENCE`, `SCRIPT_TIMEOUT_SECONDS`, `emit_devops_audit`, `devops_audit_payload` y el timeout.
   - Riesgo: el DoD podia pasar una vez, pero romperse en la siguiente regeneracion.

2. **Evidencia DevOps demasiado declarativa. Corregido.**
   - La validacion comprobaba que `agent.log`, reportes y rutas rollback estuvieran listados, pero no que existieran como evidencia local usable.
   - Riesgo: falso positivo de release readiness si el JSON contenia strings correctos pero faltaban archivos, reportes validos o snapshots.

3. **Bytecode accidental detectado por la propia validacion. Corregido.**
   - `python -m py_compile ...` genero `tools/__pycache__`, y `python tools/validate_copilot_factory.py` fallo con 5 issues de artefactos `.pyc`.
   - Se elimino el bytecode creado durante QA y `run_factory.py` ahora fuerza `PYTHONDONTWRITEBYTECODE=1` para sus subprocess.

## Parches hechos

- `tools/generate_copilot_factory.py`
  - `render_run_factory()` ahora emite la version DevOps completa y reproducible de `tools/run_factory.py`.
  - El template generado conserva `RUN_SEQUENCE`, timeout por script, `emit_devops_audit()`, `devops_audit_payload()` y `PYTHONDONTWRITEBYTECODE`.

- `tools/run_factory.py`
  - Regenerado desde la plantilla corregida.
  - Ejecuta subprocess con `env["PYTHONDONTWRITEBYTECODE"] = "1"`.
  - Publica `devopsAudit.reproducibility.noBytecodeArtifacts = true`.

- `tools/validate_copilot_factory.py`
  - Valida que la plantilla generadora de `run_factory.py` no vuelva a perder el contrato DevOps.
  - Endurece `devopsAudit` con comprobaciones ejecutables:
    - `agent.log` existe y no esta vacio.
    - Reportes externos requeridos existen, son JSON y tienen `pass=true`.
    - `.codex-loop/rollback` y `.codex-loop/backups` existen y contienen evidencia.
    - `logEvidence` no admite rutas absolutas ni `..`.
    - Casos negativos cubren `unsafe_log_path` y `noBytecodeArtifacts`.

- Artefactos regenerados:
  - `generated/factory-audit.json`
  - `generated/validation-report.json`
  - `generated/validation-report.md`
  - `generated/prompt-quality-report.json`
  - `generated/prompt-quality-report.md`
  - `generated/runtime-equivalence-report.json`
  - `generated/runtime-equivalence-report.md`
  - `generated/test-strategy-audit-report.json`
  - `generated/test-strategy-audit-report.md`

## Comandos ejecutados

- `Get-Command rg -ErrorAction SilentlyContinue`
  - Resultado: `rg` disponible via `.codex-loop/tool-shims/rg.ps1`.

- `git status --short`
  - Resultado: no hay repositorio Git en esta carpeta.

- `python -m py_compile tools/run_factory.py tools/validate_copilot_factory.py tools/validate_prompt_quality.py tools/validate_runtime_equivalence.py`
  - Resultado: compilo, pero genero `tools/__pycache__`.

- `python tools/validate_copilot_factory.py`
  - Resultado inicial: fallo por bytecode `.pyc` en `tools/__pycache__`.

- `python tools/validate_prompt_quality.py`
  - Resultado: PASS.

- Limpieza controlada de `tools/__pycache__`
  - Resultado: bytecode creado durante QA eliminado.

- `python tools/run_factory.py`
  - Resultado inicial: fallo porque el generador sobrescribia `tools/run_factory.py` con una version antigua. Hallazgo convertido en parche.

- `python tools/generate_copilot_factory.py`
  - Resultado: `Generated 18 copilots x 4 runtimes with 50 factory agents.`

- `python tools/run_factory.py`
  - Resultado final: PASS en generacion, validacion de factory, prompt quality y runtime equivalence.

- `python tools/validate_copilot_factory.py && python tools/validate_prompt_quality.py`
  - Resultado final: PASS.

- `python tools/validate_runtime_equivalence.py`
  - Resultado final: PASS.

- `Test-Path 'tools\\__pycache__'`
  - Resultado final: `False`.

## Riesgos residuales

- No hay metadata Git local, asi que la trazabilidad de diffs/rollback depende de los artefactos `.codex-loop/backups` y `.codex-loop/rollback`.
- `generated/validation-report.json` es producido por el propio `validate_copilot_factory.py`; la validacion evita bloquear el bootstrap por su propio reporte en curso, pero el artefacto final queda regenerado y en PASS.
- No se realizo prueba visual porque no hay frontend en este incremento.
