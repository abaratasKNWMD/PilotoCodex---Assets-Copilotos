# Semantic Routing Plan

1. Convert a request into lowercase tokens.
2. Score every copilot by family, stack, SDLC phase, connector and expected output tags.
3. Pick top copilots.
4. Run Python validators and static catalog checks.
5. Escalate only the minimal context to Codex, Claude or LangChain.

Test:

```powershell
python tools/semantic_router.py "java ci sonar remediation"
```
