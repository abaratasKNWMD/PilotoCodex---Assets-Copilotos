# Worker Isolation Policy

- Do not overwrite validated dataset artifacts without cause.
- Keep state under `state/` and derived data under `output/`.
- Preserve queue semantics for `pending`, `completed`, and `failed`.
