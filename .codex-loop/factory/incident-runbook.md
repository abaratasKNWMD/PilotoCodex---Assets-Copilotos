# Incident Runbook

Generated: 2026-05-05T19:40:26.075Z

| Incident | Meaning | Automatic/Human Response |
|---|---|---|
| provider-policy-friction | Prompt o contexto disparó filtro del proveedor. | Abrir .codex-loop/factory/policy-safe-brief.md, dividir tarea, usar safe-coding/privacy y reintentar. |
| provider-or-process-timeout | La tarea fue demasiado larga o se cortó stream/proceso. | Dividir por Files/DoD, subir responseTimeoutMs o bajar microtaskMaxMinutes. |
| remote-access-friction | Web/search/API externa bloqueada, 403 o rate limit. | Usar cache/fuentes alternativas, marcar confianza baja y seguir con caveats. |
| codex-cli-contract-drift | Cambió el contrato de flags de Codex CLI. | Ejecutar preflight, revisar codex exec --help y ajustar runner/codexExtraArgs. |
| codex-json-output-drift | Codex respondió pero el extractor no encontró final message. | Inspeccionar JSONL, actualizar parser extractFinalMessageFromCodexJsonl. |
| browser.no_e2e | Frontend sin prueba real de navegación. | Añadir Playwright/Cypress/test:e2e o smoke de dev/preview. |
| packaging.tauri_config_missing | Packaging Tauri incompleto. | Añadir src-tauri, Cargo.toml, tauri.conf.json y scripts tauri. |
| packaging.rust_toolchain_missing | Rust/Cargo no disponible. | Instalar toolchain o marcar prepared-not-built con riesgo residual. |
| coverage.weak_tests | Coverage alto pero tests pobres. | Añadir pruebas de comportamiento y asserts reales. |
| tasks.bad_shape | Cola de tareas microscópica, enorme o sin contrato. | Regenerar task-synthesizer con Files/DoD/Verify/Risk/Frontier. |
| repair.blast_radius_warning | Repair tocó demasiados archivos. | Revisar diff, revertir snapshot si procede y relanzar repair más acotado. |
