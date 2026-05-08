# QA Audit Task 031 - Copiloto Firefly v6

Fecha: 2026-05-05
Perfil: strict
Scope auditado: `dist/copilots/firefly_v6/shared/spec.json`, adaptadores Codex/Claude/GitHub Copilot/LangChain y reportes generados de validacion.

## Veredicto

PASS con correccion operativa menor.

El contrato compartido de Firefly v6 mantiene equivalencia declarada entre Codex, Claude, GitHub Copilot y LangChain: los adaptadores referencian `shared/spec.json`, `shared/output_schema.json`, los conectores se mantienen como placeholders/env names, y los reportes no almacenan cuerpos de prompt.

## Hallazgos

1. Release readiness: existia `dist/copilots/__pycache__/_runtime_safety.cpython-314.pyc`.
   - Impacto: `python tools/validate_copilot_factory.py` fallaba porque el paquete de runtime no debe incluir caches Python.
   - Estado: corregido eliminando `dist/copilots/__pycache__`.

2. LangChain smoke funcional.
   - Happy path: `audit()` con evidencia de source refs, validacion, KB partition y runtime trace devuelve `pass=true`.
   - Empty state: request vacio devuelve `ValueError: LangChain request cannot be empty.`
   - Privacy/error handling: `render_prompt()` redacta token/customer-like data y no recrea `dist/copilots/__pycache__` al ejecutarse con `python -B`.

3. UX/documentacion de operador.
   - No hay UI de usuario en este incremento. La revision UX se traduce a ergonomia de operador: README, AGENT.md y contratos indican runbook, schema compartido, validadores y politica de placeholders.

## Parches Hechos

- Eliminado artefacto generado no publicable: `dist/copilots/__pycache__/_runtime_safety.cpython-314.pyc`.
- No se tocaron prompts, schema ni adaptadores porque la equivalencia y el presupuesto de coste ya pasan los validadores.

## Comandos Ejecutados

- `python tools\validate_copilot_factory.py`
  - Resultado inicial: FAIL por `dist/copilots/__pycache__/`.
- Limpieza controlada con Python local de `dist/copilots/__pycache__`.
- `python tools\validate_copilot_factory.py; if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }`
- `python tools\validate_prompt_quality.py; if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }`
- `python tools\validate_runtime_equivalence.py; if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }`
  - Resultado final: PASS en los tres validadores.
- `python -B -c "... build_agent(); audit(...); ..."`
  - Resultado: `pass=true`, `score=7`, request vacio rechazado.
- `python -B -c "... render_prompt(...secret/customer data...) ..."`
  - Resultado: secretos/customer-like data redactados; `pycache=False`.
- `Test-Path dist\copilots\__pycache__`
  - Resultado final: `False`.

## Riesgos Residuales

- No hay repositorio Git en el workspace, asi que no pude producir diff formal ni separar cambios previos por commit.
- Los validadores regeneran reportes en `generated/`; si se ejecutan en paralelo pueden pisar timestamps/reportes compartidos. El DoD solicitado se ejecuto en orden y paso.
- El presupuesto LangChain de Firefly v6 esta cerca del limite de crecimiento (`0.0941` con limite `0.10`), por lo que futuras ampliaciones del runtime Python deberian compensar coste o mover detalle a artefactos compartidos.
