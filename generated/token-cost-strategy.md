# Token Cost Strategy

## Rule

Python owns discovery, routing, catalog validation, phase matrices, file generation and first-pass audits.

## Escalate to Codex or Claude only for

- Non-trivial code edits.
- Ambiguous architecture trade-offs.
- Security-sensitive review that needs human-readable reasoning.
- Final documentation polish after Python generated the evidence.

## Avoid

- Re-sending whole repositories to LLMs.
- Asking LLMs to classify simple stack/phase/connector routing.
- Using live connector calls before local catalog checks.
