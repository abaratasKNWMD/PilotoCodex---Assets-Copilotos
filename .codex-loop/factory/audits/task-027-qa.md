# Task 027 QA Audit - AIDA Architecture Copilot

Resultado: PASS con parche aplicado.

## Alcance

- Copiloto auditado: `aida_architecture`.
- Archivos principales revisados: `shared/spec.json`, `codex/AGENT.md`, `claude/AGENT.md`, `github-copilot/copilot-agent.md`, `langchain/agent.py`.
- Superficie QA: equivalencia entre runtimes, contrato de salida, disciplina Python-first, redaccion de secretos, placeholders MCP y trazabilidad por matriz SDLC.

## Hallazgos

1. P1 corregido: `dist/copilots/aida_architecture/langchain/agent.py` no reconocia solicitudes localizadas como `revisa principios de arquitectura AIDA` ni `validar contratos y handoff de diseno`; ambas daban `score=0` y bloqueaban indebidamente el runtime LangChain, aunque Codex/Claude/GitHub Copilot exponen el copiloto con nombre y uso en castellano.
2. Durante la verificacion, un `py_compile` genero `__pycache__` dentro de `dist/`; se elimino porque el validador lo considera contaminacion del artefacto de release.
3. Tras tocar `agent.py`, la matriz SDLC tenia hashes obsoletos para AIDA/LangChain en `architecture`, `design` y `release`; se regenero con el validador de factory.

## Parches Hechos

- `dist/copilots/aida_architecture/langchain/agent.py`
  - `score()` ahora considera `id` y `name` del perfil, no solo tags tecnicos en ingles.
  - Se anadieron alias minimos de routing local para AIDA: `arquitectura`, `principios`, `diseno`, `contratos`.
  - `normalize()` convierte `ñ/N` a `n/N` sin imports nuevos, preservando el contrato de imports permitidos de LangChain.
- Artefactos generados refrescados por validadores:
  - `generated/sdlc-runtime-matrix.json`
  - `generated/sdlc-runtime-matrix.md`
  - `generated/sdlc-runtime-matrix-maintenance.json`
  - `generated/sdlc-runtime-matrix-maintenance.md`
  - reportes `generated/*report*.json|md` actualizados por las ejecuciones de validacion.

## Checks Practicos

- Happy path LangChain:
  - `review architecture decision ADR and principles` -> `score=10`, `pass=true`.
  - `revisa principios de arquitectura AIDA` -> `score=8`, `pass=true`.
  - `validar contratos y handoff de diseno` -> `score=4`, `pass=true`.
- Empty state:
  - Solicitud AIDA sin evidencias -> `pass=false` y `evidence_needed=["source_refs","principles","adr","technical_decision_quality","validation"]`.
- Error/release-sensitive state:
  - Solicitud con `token`/`production`/`release` -> `pass=false` con gate de aprobacion humana.
- Seguridad:
  - `render_prompt()` mantiene redaccion: el placeholder `[REDACTED_GITHUB_TOKEN]` no aparece en el prompt renderizado como valor sensible.
- UX/documentacion:
  - No hay UI aplicable; README del copiloto ya declara runtime files, source of truth, validadores y politica de no pegar logs/tokens/customer data.

## Comandos Ejecutados

- `Get-Command rg -ErrorAction SilentlyContinue`
- `git status --short` -> no aplicable: el workspace no es un repositorio Git.
- `python tools\validate_copilot_factory.py` -> PASS final: 18 copilots, 50 agents, 50 tasks.
- `python tools\validate_prompt_quality.py` -> PASS final: 18 copilots, 72 runtime prompts.
- `python tools\validate_runtime_equivalence.py` -> PASS final: 18 copilots checked.
- Test focal LangChain con `PYTHONDONTWRITEBYTECODE=1`: import, `plan()`, `render_prompt()`, redaccion y schema required.
- Limpieza controlada de `__pycache__` generados durante QA; verificado sin caches bajo `dist/copilots`.

## Riesgos Residuales

- No hay metadatos Git locales para comprobar diff exacto o autoreship.
- El parche es manual sobre artefacto generado; si se regenera desde plantillas antiguas, el fix debe trasladarse al generador o a la fuente canonica del runtime.
- La cobertura automatica existente no detectaba el caso localizado de LangChain; queda cubierto por esta auditoria, pero no por un test persistente dedicado.
