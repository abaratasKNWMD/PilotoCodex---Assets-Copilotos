# Parallelization Policy

- Treat 107 agents as logical roles, not real concurrent sessions.
- Run 4 to 8 real workers at most.
- Prefer queue throughput over uncontrolled concurrency.
