# Task 017 Safe-Coding And Privacy Audit

Fecha: 2026-05-04

## Alcance

Revision defensiva de la tarea 17/50: `Builds Python/LangChain compatible agent specs.`

Superficies revisadas:

- `dist/copilots`
- `dist/copilots/_runtime_safety.py`
- `generated/runtime-injection-map.json`
- `generated/runtime-equivalence-report.json`
- `generated/runtime-equivalence-report.md`
- `generated/prompt-quality-report.json`
- `generated/prompt-quality-report.md`
- `generated/test-strategy-audit-report.json`
- `generated/test-strategy-audit-report.md`
- `generated/validation-report.json`
- `generated/validation-report.md`
- `tools/validate_runtime_equivalence.py`

## Hallazgos

| Severidad | Hallazgo | Evidencia | Estado |
|---|---|---|---|
| Medium | El smoke test de LangChain importaba `dist/copilots/*/langchain/agent.py` y podia dejar efectos laterales de bytecode en artefactos release. | `validate_copilot_factory.py` fallo tras el smoke test por 38 incidencias de `__pycache__` bajo `dist/copilots`. | Corregido |
| Low | La deteccion/redaccion de credenciales no cubria varios formatos comunes de secreto. | El runtime cubria `sk-*`, GitHub PAT y Bearer, pero no GitLab PAT, AWS access key id, Google API key, Slack token, JWT o bloques de private key. | Corregido |
| Info | No se detectaron secretos reales ni rutas absolutas locales en artefactos de distribucion/reportes. | La busqueda sensible posterior solo encontro fixtures sinteticos dentro de `tools/validate_runtime_equivalence.py`. | Aceptado |
| Info | Auth, sesion, CORS, multi-tenant SaaS y billing no aplican directamente a este incremento. | La tarea produce contratos locales, perfiles LangChain y reportes; los conectores siguen como nombres/placeholders sin valores de credencial. | Aceptado |

## Parches Hechos

- `tools/validate_runtime_equivalence.py`: ampliados patrones de secreto, anadida inspeccion estatica previa para agentes LangChain generados, bloqueo de imports/llamadas de efecto lateral obvias, restauracion de `sys.path` y `sys.dont_write_bytecode` durante el smoke test.
- `tools/validate_runtime_equivalence.py`: anadidos negativos verificables para secretos AWS/private key, side effects estaticos y render seguro.
- `dist/copilots/_runtime_safety.py`: ampliada la redaccion runtime para GitLab PAT, AWS access key id, Google API key, Slack token, JWT y private key markers.
- Limpieza de `__pycache__` generados bajo `dist/copilots` despues de verificar que las rutas estaban dentro de ese subarbol.
- Regenerado `generated/runtime-equivalence-report.json` y `generated/runtime-equivalence-report.md` con los nuevos negativos.

## Comandos Ejecutados

```powershell
Get-Command rg -ErrorAction SilentlyContinue | Select-Object -ExpandProperty Source
```

Resultado: `rg` disponible como shim local en `.codex-loop/tool-shims/rg.ps1`.

```powershell
git status --short
```

Resultado: no aplica; el workspace actual no contiene metadatos Git.

```powershell
rg -n "<patrones-sensibles>" generated/runtime-injection-map.json generated/*.json generated/*.md dist/copilots tools/validate_runtime_equivalence.py
```

Resultado: sin secretos reales en artefactos; solo fixtures sinteticos del validador.

```powershell
python tools\validate_runtime_equivalence.py
```

Resultado: `Runtime equivalence PASS: 18 copilots checked.`

```powershell
python tools\validate_copilot_factory.py
```

Resultado inicial: fallo por `__pycache__` en `dist/copilots`, corregido en este parche.

```powershell
[System.IO.Directory]::Delete((Resolve-Path 'dist\copilots\__pycache__').Path, $true)
```

Resultado: cache raiz de `dist/copilots` eliminado.

```powershell
$targetRoot = (Resolve-Path 'dist\copilots').Path
Get-ChildItem -Path $targetRoot -Recurse -Directory -Filter __pycache__
```

Resultado: 18 directorios adicionales localizados bajo `dist/copilots` y eliminados tras comprobar el prefijo de ruta.

```powershell
python tools\validate_copilot_factory.py
python tools\validate_prompt_quality.py
python tools\validate_runtime_equivalence.py
```

Resultados finales:

- `Copilot factory validation PASS: 18 copilots, 50 agents, 50 tasks.`
- `Prompt quality validation PASS: 18 copilots, 72 runtime prompts.`
- `Runtime equivalence PASS: 18 copilots checked.`

```powershell
Get-ChildItem -Path dist\copilots -Recurse -Directory -Filter __pycache__
```

Resultado final: sin salida; no quedan caches Python bajo `dist/copilots`.

```powershell
python tools\validate_copilot_factory.py
```

Resultado post-runtime: `Copilot factory validation PASS: 18 copilots, 50 agents, 50 tasks.`

## Riesgos Residuales

- El smoke test sigue importando codigo Python local generado para validar `render_prompt()`. El riesgo queda reducido por inspeccion estatica, restauracion de entorno y bytecode desactivado, pero no sustituye un sandbox de proceso separado.
- Los patrones de secretos son defensivos y no exhaustivos para todos los proveedores posibles. Mantener busquedas especificas por proveedor si se agregan nuevos conectores.
- Los conectores declarados siguen siendo placeholders; cualquier activacion real debe usar variables de entorno o secreto gestionado, nunca valores en repo ni reportes.
