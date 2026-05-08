# Prompt Quality Report

Pass: True

Copilots: 18

Minimum depth thresholds:

- Markdown runtime prompt chars: 6500
- LangChain/Python adapter chars: 4500
- System prompt chars: 1300
- Developer prompt chars: 1500

Cost budget:

- Baseline: `generated/prompt-size-baseline.json`
- Max growth ratio: 0.1

Sample metrics:

- `devex` / `codex`: 15294 chars
- `devex` / `claude`: 15201 chars
- `devex` / `github-copilot`: 15582 chars
- `devex` / `langchain`: 18796 chars
- `aida_architecture` / `codex`: 15364 chars
- `aida_architecture` / `claude`: 15271 chars
- `aida_architecture` / `github-copilot`: 15704 chars
- `aida_architecture` / `langchain`: 19488 chars
- `as_is_discovery` / `codex`: 12033 chars
- `as_is_discovery` / `claude`: 11940 chars
- `as_is_discovery` / `github-copilot`: 12321 chars
- `as_is_discovery` / `langchain`: 15833 chars
- `single_registry` / `codex`: 11681 chars
- `single_registry` / `claude`: 11588 chars
- `single_registry` / `github-copilot`: 11969 chars
- `single_registry` / `langchain`: 15451 chars
- `firefly_v5` / `codex`: 15602 chars
- `firefly_v5` / `claude`: 15509 chars
- `firefly_v5` / `github-copilot`: 15922 chars
- `firefly_v5` / `langchain`: 19410 chars

Sample cost metrics:

- `devex` / `systemPrompt`: 1729 chars (baseline 1729, delta 0, growth 0.0)
- `devex` / `developerPrompt`: 2278 chars (baseline 2265, delta 13, growth 0.0057)
- `devex` / `codex`: 15294 chars (baseline 14694, delta 600, growth 0.0408)
- `devex` / `claude`: 15201 chars (baseline 14601, delta 600, growth 0.0411)
- `devex` / `github-copilot`: 15582 chars (baseline 14982, delta 600, growth 0.04)
- `devex` / `langchain`: 18796 chars (baseline 17572, delta 1224, growth 0.0697)
- `aida_architecture` / `systemPrompt`: 1756 chars (baseline 1756, delta 0, growth 0.0)
- `aida_architecture` / `developerPrompt`: 2262 chars (baseline 2262, delta 0, growth 0.0)
- `aida_architecture` / `codex`: 15364 chars (baseline 14804, delta 560, growth 0.0378)
- `aida_architecture` / `claude`: 15271 chars (baseline 14711, delta 560, growth 0.0381)
- `aida_architecture` / `github-copilot`: 15704 chars (baseline 15144, delta 560, growth 0.037)
- `aida_architecture` / `langchain`: 19488 chars (baseline 18040, delta 1448, growth 0.0803)
- `as_is_discovery` / `systemPrompt`: 1809 chars (baseline 1809, delta 0, growth 0.0)
- `as_is_discovery` / `developerPrompt`: 2263 chars (baseline 2092, delta 171, growth 0.0817)
- `as_is_discovery` / `codex`: 12033 chars (baseline 11288, delta 745, growth 0.066)
- `as_is_discovery` / `claude`: 11940 chars (baseline 11195, delta 745, growth 0.0665)
- `as_is_discovery` / `github-copilot`: 12321 chars (baseline 11576, delta 745, growth 0.0644)
- `as_is_discovery` / `langchain`: 15833 chars (baseline 14608, delta 1225, growth 0.0839)
- `single_registry` / `systemPrompt`: 1706 chars (baseline 1706, delta 0, growth 0.0)
- `single_registry` / `developerPrompt`: 2091 chars (baseline 2091, delta 0, growth 0.0)

Test strategy audit:

- Pass: True
- Pairwise case count: 6
- Negative cases detected: True
- QA runtime metrics present: ['claude', 'codex', 'github-copilot', 'langchain']
- Runtime markers checked: ['codex', 'claude', 'github-copilot', 'langchain']

SDLC runtime matrix audit:

- Pass: True
- Artifact: `generated/sdlc-runtime-matrix.json`
- Policy version: sdlc-copilot-runtime-matrix-1.0
- Expected cells: 204
- Actual cells: 204
- Runtime prompt pairs covered: 72
- Prompt content stored: False
- Prompt budget detections: []
- Negative prompt storage detected: True
- Trace ledger entries: 51 / 51
- Trace ledger digest matches: True
- Trace ledger runtime coverage checked: 51
- Trace ledger pairwise cases checked: 306
- Cell equivalence pass: True
- Cell equivalence cells passing: 204 / 204
- Maintenance artifact: `generated/sdlc-runtime-matrix-maintenance.json`
- Maintenance receipt pass: True
- Maintenance prompt budget detections: []
- Maintenance cell digest matches: True
- Maintenance cell equivalence gate: True

Negative case results:

- `valid_control`: passedExpectation=True, expectedFailure=False, failureDetected=False
- `secret_pattern`: passedExpectation=True, expectedFailure=True, failureDetected=True
- `expanded_secret_patterns`: passedExpectation=True, expectedFailure=True, failureDetected=True
- `local_path`: passedExpectation=True, expectedFailure=True, failureDetected=True
- `cost_growth`: passedExpectation=True, expectedFailure=True, failureDetected=True

Validator Smoke:

- Owner: factory_agent_25_smoke
- Mission: Runs generated validators and reports blockers.
- Validator: prompt_quality
- Command: `python tools/validate_prompt_quality.py`
- Report artifact: `generated/prompt-quality-report.json`
- Report pass: True
- Blocker count: 0
- Prompt bodies stored: False

Issues:

- none
