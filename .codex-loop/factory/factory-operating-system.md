# Factory Operating System

This workspace is a copilot factory, not a frontend product. The source of truth is the shared copilot spec plus the generated runtime adapters under `dist/copilots/`.

Rules:

- Use `factory-prompt.md` for planning mode.
- Use `tasks.json` for queue-only mode.
- Prefer reproducible CLI verification over browser checks.
- Keep Python as the deterministic brain for routing, validation and audits.
- Do not accept runtime drift between Codex, Claude, GitHub Copilot and LangChain.
