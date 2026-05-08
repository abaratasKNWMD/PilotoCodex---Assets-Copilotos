# Parallel Scheduler Policy

Use parallel execution only when tasks have disjoint write sets. Queue-only data-factory tasks should prefer serial execution unless explicitly prepared for parallel batches.
