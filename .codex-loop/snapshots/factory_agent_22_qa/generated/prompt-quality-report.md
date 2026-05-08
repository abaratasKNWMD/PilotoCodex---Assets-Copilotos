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

- `devex` / `codex`: 14694 chars
- `devex` / `claude`: 14601 chars
- `devex` / `github-copilot`: 14982 chars
- `devex` / `langchain`: 17572 chars
- `aida_architecture` / `codex`: 14804 chars
- `aida_architecture` / `claude`: 14711 chars
- `aida_architecture` / `github-copilot`: 15144 chars
- `aida_architecture` / `langchain`: 18040 chars
- `as_is_discovery` / `codex`: 11288 chars
- `as_is_discovery` / `claude`: 11195 chars
- `as_is_discovery` / `github-copilot`: 11576 chars
- `as_is_discovery` / `langchain`: 14608 chars
- `single_registry` / `codex`: 11160 chars
- `single_registry` / `claude`: 11067 chars
- `single_registry` / `github-copilot`: 11448 chars
- `single_registry` / `langchain`: 14479 chars
- `firefly_v5` / `codex`: 14873 chars
- `firefly_v5` / `claude`: 14780 chars
- `firefly_v5` / `github-copilot`: 15193 chars
- `firefly_v5` / `langchain`: 17722 chars

Sample cost metrics:

- `devex` / `systemPrompt`: 1729 chars (baseline 1729, delta 0, growth 0.0)
- `devex` / `developerPrompt`: 2265 chars (baseline 2265, delta 0, growth 0.0)
- `devex` / `codex`: 14694 chars (baseline 14694, delta 0, growth 0.0)
- `devex` / `claude`: 14601 chars (baseline 14601, delta 0, growth 0.0)
- `devex` / `github-copilot`: 14982 chars (baseline 14982, delta 0, growth 0.0)
- `devex` / `langchain`: 17572 chars (baseline 17572, delta 0, growth 0.0)
- `aida_architecture` / `systemPrompt`: 1756 chars (baseline 1756, delta 0, growth 0.0)
- `aida_architecture` / `developerPrompt`: 2262 chars (baseline 2262, delta 0, growth 0.0)
- `aida_architecture` / `codex`: 14804 chars (baseline 14804, delta 0, growth 0.0)
- `aida_architecture` / `claude`: 14711 chars (baseline 14711, delta 0, growth 0.0)
- `aida_architecture` / `github-copilot`: 15144 chars (baseline 15144, delta 0, growth 0.0)
- `aida_architecture` / `langchain`: 18040 chars (baseline 18040, delta 0, growth 0.0)
- `as_is_discovery` / `systemPrompt`: 1809 chars (baseline 1809, delta 0, growth 0.0)
- `as_is_discovery` / `developerPrompt`: 2092 chars (baseline 2092, delta 0, growth 0.0)
- `as_is_discovery` / `codex`: 11288 chars (baseline 11288, delta 0, growth 0.0)
- `as_is_discovery` / `claude`: 11195 chars (baseline 11195, delta 0, growth 0.0)
- `as_is_discovery` / `github-copilot`: 11576 chars (baseline 11576, delta 0, growth 0.0)
- `as_is_discovery` / `langchain`: 14608 chars (baseline 14608, delta 0, growth 0.0)
- `single_registry` / `systemPrompt`: 1706 chars (baseline 1706, delta 0, growth 0.0)
- `single_registry` / `developerPrompt`: 2091 chars (baseline 2091, delta 0, growth 0.0)

Test strategy audit:

- Pass: True
- Pairwise case count: 6
- Negative cases detected: True
- QA runtime metrics present: ['claude', 'codex', 'github-copilot', 'langchain']
- Runtime markers checked: ['codex', 'claude', 'github-copilot', 'langchain']

Negative case results:

- `valid_control`: passedExpectation=True, expectedFailure=False, failureDetected=False
- `secret_pattern`: passedExpectation=True, expectedFailure=True, failureDetected=True
- `local_path`: passedExpectation=True, expectedFailure=True, failureDetected=True
- `cost_growth`: passedExpectation=True, expectedFailure=True, failureDetected=True

Issues:

- none
