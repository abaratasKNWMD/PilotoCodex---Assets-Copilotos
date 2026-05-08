# Cost Routing Policy

Owner: `factory_agent_20_cost`

Mission: Routes cheap deterministic work to Python and expensive judgement to LLMs.

## Decision Contract

- Python owns catalog generation, semantic routing, schema validation, prompt-size budgets, runtime equivalence diffs and documentation marker audits.
- LLM judgement is reserved for architecture tradeoffs, non-trivial code changes and final operator synthesis after Python gates pass.
- LLM assist before deterministic scoring is not allowed. Cheap route evidence must keep `routing_evidence.llm_assist_used=false`.
- Raw logs, credentials, billing data and customer data must not be copied into prompts. Use placeholders and report references.

## Runtime Equivalence

- Codex, Claude, GitHub Copilot and LangChain use the same cost-routing policy.
- `dist/copilots/<copilot_id>/shared/spec.json` remains the canonical copilot source.
- `generated/runtime-injection-map.json` remains the adapter trace map.
- `maxUnexplainedDrift` remains `0`; runtime-specific prompt expansion cannot bypass the cost route.

## Verification

- Contract artifact: `.codex-loop/factory/cost-routing-contract.json`
- Scorecard artifact: `.codex-loop/factory/cost-routing-scorecard.json`
- Validator evidence: `generated/validation-report.json#/costRoutingAuditor`
- Required commands:
  - `python tools/validate_copilot_factory.py`
  - `python tools/validate_prompt_quality.py`
