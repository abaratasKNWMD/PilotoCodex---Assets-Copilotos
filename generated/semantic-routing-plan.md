# Semantic Routing Plan

1. Convert a request into lowercase tokens.
2. Score every copilot by family, stack, SDLC phase, connector and expected output tags.
3. Apply deterministic audit boosts for shared Architecture, Design, Build and KB contracts when request terms match their scoped evidence requirements.
4. Pick top copilots.
5. Attach runtime trace plus audit evidence payloads from shared artifacts.
6. Run Python validators and static catalog checks.
7. Escalate only the minimal context to Codex, Claude or LangChain.

## KB Routing Contract

- Trigger terms: `kb`, `knowledge`, `source`, `truth`, `context`, `window`, `windows`, `separation`.
- Target copilot: `firefly_v6`.
- Source of truth: `dist/copilots/firefly_v6/shared/kb_context_window_audit.json`.
- Route evidence field: `kb_context_window_audit`.
- Required evidence: `kb_partition_map`, `source_of_truth_registry`, `context_window_budget`, `runtime_trace`.
- Cost rule: deterministic Python scoring and shared-artifact checks run before any LLM assist.

Test:

```powershell
python tools/semantic_router.py "java ci sonar remediation"
python tools/semantic_router.py "kb source truth context windows"
```
