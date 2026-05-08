# QA Audit Task 034 - Copiloto Java Architect

Fecha: 2026-05-05
Perfil: strict
Alcance auditado: `dist/copilots/java_architect/shared/spec.json`, runtimes Codex/Claude/GitHub Copilot/LangChain y la plantilla relacionada `tools/elevate_copilot_prompts.py`.

## Hallazgos

- Corregido: los adaptadores Markdown de Java Architect apuntaban a rutas de herramientas que resolvían a `dist/tools/...` en vez de al directorio raíz `tools/...`. Impacto: el operador podía seguir un contrato runtime no ejecutable aunque los validadores de equivalencia pasaran.
- Corregido: el runtime GitHub Copilot apuntaba la política MCP a `dist/config/...` en vez de `config/mcp-connectors.example.json`.
- Corregido: el artefacto de design boundary aparecía como `shared/design_boundary_audit.json` dentro de adaptadores runtime; desde esos directorios era ambiguo/no resolvía. Ahora usa `../shared/design_boundary_audit.json`.
- Verificado sin parche: `spec.json`, `shared/output_schema.json` y la constante `OUTPUT_SCHEMA` de LangChain están sincronizados.
- Verificado sin parche: el agente LangChain rechaza request vacío, bloquea evidencia incompleta, acepta evidencia completa de diseño y redacta un token falso con forma de credencial.

## Parches Hechos

- `dist/copilots/java_architect/codex/AGENT.md`: rutas `../../../../tools/...` y artefacto `../shared/design_boundary_audit.json`.
- `dist/copilots/java_architect/claude/AGENT.md`: mismas correcciones de rutas y artefacto compartido.
- `dist/copilots/java_architect/github-copilot/copilot-agent.md`: mismas correcciones, más `../../../../config/mcp-connectors.example.json`.
- `tools/elevate_copilot_prompts.py`: añadida normalización de referencias runtime `shared/...` a `../shared/...` y corregida la ruta de política MCP de GitHub Copilot para futuras elevaciones.

## Comandos Ejecutados

- `Get-Command rg -ErrorAction SilentlyContinue`: `rg` disponible como shim local.
- `git status --short`: falló porque el workspace no es repositorio Git.
- `python tools/validate_copilot_factory.py`: PASS inicial.
- `python tools/validate_prompt_quality.py`: PASS inicial.
- `python tools/validate_runtime_equivalence.py`: PASS inicial.
- Checks Python puntuales de rutas runtime, sincronía schema/spec y comportamiento LangChain.
- `python -m py_compile tools/elevate_copilot_prompts.py dist/copilots/java_architect/langchain/agent.py`: sintaxis OK, pero generó `__pycache__`.
- `python tools/validate_copilot_factory.py`: FAIL temporal por `__pycache__` generado.
- Limpieza exacta de los `.pyc` creados y directorios vacíos usando APIs .NET con rutas verificadas dentro del workspace.
- Revalidación final:
  - `python tools/validate_copilot_factory.py`: PASS.
  - `python tools/validate_prompt_quality.py`: PASS.
  - `python tools/validate_runtime_equivalence.py`: PASS.

## Riesgos Residuales

- No hay metadata Git local, así que la auditoría no puede separar cambios previos de usuario frente al incremento salvo por inspección directa.
- No reejecuté la elevación completa de prompts para evitar churn fuera del copilot auditado; la plantilla queda corregida para futuras generaciones.
- La suite actual no detectaba rutas Markdown no resolubles; el fallo quedó cubierto por checks QA puntuales y por el parche de plantilla.
