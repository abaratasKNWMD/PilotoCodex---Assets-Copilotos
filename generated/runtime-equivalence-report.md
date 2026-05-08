# Runtime Equivalence Report

Pass: True

Copilots checked: 18

Metrics:

- `devex`: checked 4 runtimes via `dist/copilots/devex/shared/spec.json`
- `aida_architecture`: checked 4 runtimes via `dist/copilots/aida_architecture/shared/spec.json`
- `as_is_discovery`: checked 4 runtimes via `dist/copilots/as_is_discovery/shared/spec.json`
- `single_registry`: checked 4 runtimes via `dist/copilots/single_registry/shared/spec.json`
- `firefly_v5`: checked 4 runtimes via `dist/copilots/firefly_v5/shared/spec.json`
- `firefly_v6`: checked 4 runtimes via `dist/copilots/firefly_v6/shared/spec.json`
- `moonshine`: checked 4 runtimes via `dist/copilots/moonshine/shared/spec.json`
- `java_generic`: checked 4 runtimes via `dist/copilots/java_generic/shared/spec.json`
- `java_architect`: checked 4 runtimes via `dist/copilots/java_architect/shared/spec.json`
- `angular_18`: checked 4 runtimes via `dist/copilots/angular_18/shared/spec.json`
- `nodejs`: checked 4 runtimes via `dist/copilots/nodejs/shared/spec.json`
- `python`: checked 4 runtimes via `dist/copilots/python/shared/spec.json`
- `qa_general`: checked 4 runtimes via `dist/copilots/qa_general/shared/spec.json`
- `sonarqube_remediation`: checked 4 runtimes via `dist/copilots/sonarqube_remediation/shared/spec.json`
- `cicd`: checked 4 runtimes via `dist/copilots/cicd/shared/spec.json`
- `journey_to_cloud`: checked 4 runtimes via `dist/copilots/journey_to_cloud/shared/spec.json`
- `copilots_manager`: checked 4 runtimes via `dist/copilots/copilots_manager/shared/spec.json`
- `firefly_marketplace`: checked 4 runtimes via `dist/copilots/firefly_marketplace/shared/spec.json`

Codex adapter audit:

- Pass: True
- Owner: factory_agent_14_codex
- Mission: Builds Codex-facing task prompts and local tool protocol.
- Protocols checked: 18
- Issue count: 0

Codex protocol metrics:

- `devex`: protocol `dist/copilots/devex/shared/codex_tool_protocol.json`, pass=True
- `aida_architecture`: protocol `dist/copilots/aida_architecture/shared/codex_tool_protocol.json`, pass=True
- `as_is_discovery`: protocol `dist/copilots/as_is_discovery/shared/codex_tool_protocol.json`, pass=True
- `single_registry`: protocol `dist/copilots/single_registry/shared/codex_tool_protocol.json`, pass=True
- `firefly_v5`: protocol `dist/copilots/firefly_v5/shared/codex_tool_protocol.json`, pass=True
- `firefly_v6`: protocol `dist/copilots/firefly_v6/shared/codex_tool_protocol.json`, pass=True
- `moonshine`: protocol `dist/copilots/moonshine/shared/codex_tool_protocol.json`, pass=True
- `java_generic`: protocol `dist/copilots/java_generic/shared/codex_tool_protocol.json`, pass=True
- `java_architect`: protocol `dist/copilots/java_architect/shared/codex_tool_protocol.json`, pass=True
- `angular_18`: protocol `dist/copilots/angular_18/shared/codex_tool_protocol.json`, pass=True
- `nodejs`: protocol `dist/copilots/nodejs/shared/codex_tool_protocol.json`, pass=True
- `python`: protocol `dist/copilots/python/shared/codex_tool_protocol.json`, pass=True
- `qa_general`: protocol `dist/copilots/qa_general/shared/codex_tool_protocol.json`, pass=True
- `sonarqube_remediation`: protocol `dist/copilots/sonarqube_remediation/shared/codex_tool_protocol.json`, pass=True
- `cicd`: protocol `dist/copilots/cicd/shared/codex_tool_protocol.json`, pass=True
- `journey_to_cloud`: protocol `dist/copilots/journey_to_cloud/shared/codex_tool_protocol.json`, pass=True
- `copilots_manager`: protocol `dist/copilots/copilots_manager/shared/codex_tool_protocol.json`, pass=True
- `firefly_marketplace`: protocol `dist/copilots/firefly_marketplace/shared/codex_tool_protocol.json`, pass=True

Claude adapter audit:

- Pass: True
- Owner: factory_agent_15_claude
- Mission: Builds Claude-facing project instructions and agent cards.
- Protocols checked: 18
- Issue count: 0

Claude project instruction metrics:

- `devex`: protocol `dist/copilots/devex/shared/claude_project_instructions.json`, pass=True
- `aida_architecture`: protocol `dist/copilots/aida_architecture/shared/claude_project_instructions.json`, pass=True
- `as_is_discovery`: protocol `dist/copilots/as_is_discovery/shared/claude_project_instructions.json`, pass=True
- `single_registry`: protocol `dist/copilots/single_registry/shared/claude_project_instructions.json`, pass=True
- `firefly_v5`: protocol `dist/copilots/firefly_v5/shared/claude_project_instructions.json`, pass=True
- `firefly_v6`: protocol `dist/copilots/firefly_v6/shared/claude_project_instructions.json`, pass=True
- `moonshine`: protocol `dist/copilots/moonshine/shared/claude_project_instructions.json`, pass=True
- `java_generic`: protocol `dist/copilots/java_generic/shared/claude_project_instructions.json`, pass=True
- `java_architect`: protocol `dist/copilots/java_architect/shared/claude_project_instructions.json`, pass=True
- `angular_18`: protocol `dist/copilots/angular_18/shared/claude_project_instructions.json`, pass=True
- `nodejs`: protocol `dist/copilots/nodejs/shared/claude_project_instructions.json`, pass=True
- `python`: protocol `dist/copilots/python/shared/claude_project_instructions.json`, pass=True
- `qa_general`: protocol `dist/copilots/qa_general/shared/claude_project_instructions.json`, pass=True
- `sonarqube_remediation`: protocol `dist/copilots/sonarqube_remediation/shared/claude_project_instructions.json`, pass=True
- `cicd`: protocol `dist/copilots/cicd/shared/claude_project_instructions.json`, pass=True
- `journey_to_cloud`: protocol `dist/copilots/journey_to_cloud/shared/claude_project_instructions.json`, pass=True
- `copilots_manager`: protocol `dist/copilots/copilots_manager/shared/claude_project_instructions.json`, pass=True
- `firefly_marketplace`: protocol `dist/copilots/firefly_marketplace/shared/claude_project_instructions.json`, pass=True

GitHub Copilot profile audit:

- Pass: True
- Owner: factory_agent_16_github
- Mission: Builds GitHub Copilot profile docs and MCP placeholders.
- Profiles checked: 18
- Issue count: 0

GitHub Copilot profile metrics:

- `devex`: profile `dist/copilots/devex/github-copilot/copilot-profile.json`, mcp `dist/copilots/devex/github-copilot/mcp-placeholders.json`, pass=True
- `aida_architecture`: profile `dist/copilots/aida_architecture/github-copilot/copilot-profile.json`, mcp `dist/copilots/aida_architecture/github-copilot/mcp-placeholders.json`, pass=True
- `as_is_discovery`: profile `dist/copilots/as_is_discovery/github-copilot/copilot-profile.json`, mcp `dist/copilots/as_is_discovery/github-copilot/mcp-placeholders.json`, pass=True
- `single_registry`: profile `dist/copilots/single_registry/github-copilot/copilot-profile.json`, mcp `dist/copilots/single_registry/github-copilot/mcp-placeholders.json`, pass=True
- `firefly_v5`: profile `dist/copilots/firefly_v5/github-copilot/copilot-profile.json`, mcp `dist/copilots/firefly_v5/github-copilot/mcp-placeholders.json`, pass=True
- `firefly_v6`: profile `dist/copilots/firefly_v6/github-copilot/copilot-profile.json`, mcp `dist/copilots/firefly_v6/github-copilot/mcp-placeholders.json`, pass=True
- `moonshine`: profile `dist/copilots/moonshine/github-copilot/copilot-profile.json`, mcp `dist/copilots/moonshine/github-copilot/mcp-placeholders.json`, pass=True
- `java_generic`: profile `dist/copilots/java_generic/github-copilot/copilot-profile.json`, mcp `dist/copilots/java_generic/github-copilot/mcp-placeholders.json`, pass=True
- `java_architect`: profile `dist/copilots/java_architect/github-copilot/copilot-profile.json`, mcp `dist/copilots/java_architect/github-copilot/mcp-placeholders.json`, pass=True
- `angular_18`: profile `dist/copilots/angular_18/github-copilot/copilot-profile.json`, mcp `dist/copilots/angular_18/github-copilot/mcp-placeholders.json`, pass=True
- `nodejs`: profile `dist/copilots/nodejs/github-copilot/copilot-profile.json`, mcp `dist/copilots/nodejs/github-copilot/mcp-placeholders.json`, pass=True
- `python`: profile `dist/copilots/python/github-copilot/copilot-profile.json`, mcp `dist/copilots/python/github-copilot/mcp-placeholders.json`, pass=True
- `qa_general`: profile `dist/copilots/qa_general/github-copilot/copilot-profile.json`, mcp `dist/copilots/qa_general/github-copilot/mcp-placeholders.json`, pass=True
- `sonarqube_remediation`: profile `dist/copilots/sonarqube_remediation/github-copilot/copilot-profile.json`, mcp `dist/copilots/sonarqube_remediation/github-copilot/mcp-placeholders.json`, pass=True
- `cicd`: profile `dist/copilots/cicd/github-copilot/copilot-profile.json`, mcp `dist/copilots/cicd/github-copilot/mcp-placeholders.json`, pass=True
- `journey_to_cloud`: profile `dist/copilots/journey_to_cloud/github-copilot/copilot-profile.json`, mcp `dist/copilots/journey_to_cloud/github-copilot/mcp-placeholders.json`, pass=True
- `copilots_manager`: profile `dist/copilots/copilots_manager/github-copilot/copilot-profile.json`, mcp `dist/copilots/copilots_manager/github-copilot/mcp-placeholders.json`, pass=True
- `firefly_marketplace`: profile `dist/copilots/firefly_marketplace/github-copilot/copilot-profile.json`, mcp `dist/copilots/firefly_marketplace/github-copilot/mcp-placeholders.json`, pass=True

LangChain agent audit:

- Pass: True
- Owner: factory_agent_17_langchain
- Mission: Builds Python/LangChain compatible agent specs.
- Contracts checked: 18
- Issue count: 0

LangChain agent contract metrics:

- `devex`: contract `dist/copilots/devex/langchain/agent_contract.json`, runtime `dist/copilots/devex/langchain/agent.py`, pass=True
- `aida_architecture`: contract `dist/copilots/aida_architecture/langchain/agent_contract.json`, runtime `dist/copilots/aida_architecture/langchain/agent.py`, pass=True
- `as_is_discovery`: contract `dist/copilots/as_is_discovery/langchain/agent_contract.json`, runtime `dist/copilots/as_is_discovery/langchain/agent.py`, pass=True
- `single_registry`: contract `dist/copilots/single_registry/langchain/agent_contract.json`, runtime `dist/copilots/single_registry/langchain/agent.py`, pass=True
- `firefly_v5`: contract `dist/copilots/firefly_v5/langchain/agent_contract.json`, runtime `dist/copilots/firefly_v5/langchain/agent.py`, pass=True
- `firefly_v6`: contract `dist/copilots/firefly_v6/langchain/agent_contract.json`, runtime `dist/copilots/firefly_v6/langchain/agent.py`, pass=True
- `moonshine`: contract `dist/copilots/moonshine/langchain/agent_contract.json`, runtime `dist/copilots/moonshine/langchain/agent.py`, pass=True
- `java_generic`: contract `dist/copilots/java_generic/langchain/agent_contract.json`, runtime `dist/copilots/java_generic/langchain/agent.py`, pass=True
- `java_architect`: contract `dist/copilots/java_architect/langchain/agent_contract.json`, runtime `dist/copilots/java_architect/langchain/agent.py`, pass=True
- `angular_18`: contract `dist/copilots/angular_18/langchain/agent_contract.json`, runtime `dist/copilots/angular_18/langchain/agent.py`, pass=True
- `nodejs`: contract `dist/copilots/nodejs/langchain/agent_contract.json`, runtime `dist/copilots/nodejs/langchain/agent.py`, pass=True
- `python`: contract `dist/copilots/python/langchain/agent_contract.json`, runtime `dist/copilots/python/langchain/agent.py`, pass=True
- `qa_general`: contract `dist/copilots/qa_general/langchain/agent_contract.json`, runtime `dist/copilots/qa_general/langchain/agent.py`, pass=True
- `sonarqube_remediation`: contract `dist/copilots/sonarqube_remediation/langchain/agent_contract.json`, runtime `dist/copilots/sonarqube_remediation/langchain/agent.py`, pass=True
- `cicd`: contract `dist/copilots/cicd/langchain/agent_contract.json`, runtime `dist/copilots/cicd/langchain/agent.py`, pass=True
- `journey_to_cloud`: contract `dist/copilots/journey_to_cloud/langchain/agent_contract.json`, runtime `dist/copilots/journey_to_cloud/langchain/agent.py`, pass=True
- `copilots_manager`: contract `dist/copilots/copilots_manager/langchain/agent_contract.json`, runtime `dist/copilots/copilots_manager/langchain/agent.py`, pass=True
- `firefly_marketplace`: contract `dist/copilots/firefly_marketplace/langchain/agent_contract.json`, runtime `dist/copilots/firefly_marketplace/langchain/agent.py`, pass=True

Data hygiene audit:

- Pass: True
- Artifacts checked: 91 / 91
- Local path leaks: 0
- Secret pattern leaks: 0
- Issue count: 0

SDLC runtime matrix audit:

- Pass: True
- Artifact: `generated/sdlc-runtime-matrix.json`
- Policy version: sdlc-copilot-runtime-matrix-1.0
- Expected cells: 204
- Actual cells: 204
- Pairwise runtime cases: 306
- Digest drift count: 0
- Runtime file mismatches: 0
- Trace ledger entries: 51
- Trace ledger digest matches: True
- Trace ledger mismatches: 0
- Cell equivalence pass: True
- Cell equivalence cells passing: 204 / 204
- Prompt content stored: False
- Maintenance artifact: `generated/sdlc-runtime-matrix-maintenance.json`
- Maintenance receipt pass: True
- Maintenance runtime count matches: True
- Maintenance cell digest matches: True
- Maintenance cell equivalence gate: True

Test strategy audit:

- Pass: True
- Pairwise case count: 6
- Pairwise coverage cases: 108
- Negative cases detected: True
- QA traceability checked: True
- QA runtime markers checked: ['codex', 'claude', 'github-copilot', 'langchain']

Negative case results:

- `local_path_leak`: passedExpectation=True, expectedFailure=True, failureDetected=True
- `secret_pattern_leak`: passedExpectation=True, expectedFailure=True, failureDetected=True
- `missing_langchain_output_schema`: passedExpectation=True, expectedFailure=True, failureDetected=True
- `invalid_langchain_syntax`: passedExpectation=True, expectedFailure=True, failureDetected=True
- `schema_drift`: passedExpectation=True, expectedFailure=True, failureDetected=True
- `runtime_trace_fields_schema`: passedExpectation=True, expectedFailure=True, failureDetected=True
- `unsafe_copilot_id`: passedExpectation=True, expectedFailure=True, failureDetected=True
- `empty_runtime_injection_map`: passedExpectation=True, expectedFailure=True, failureDetected=True
- `indented_runtime_protocol_markdown`: passedExpectation=True, expectedFailure=True, failureDetected=True
- `github_mcp_non_empty_placeholder`: passedExpectation=True, expectedFailure=True, failureDetected=True
- `github_mcp_env_reference_drift`: passedExpectation=True, expectedFailure=True, failureDetected=True
- `github_profile_cost_control_drift`: passedExpectation=True, expectedFailure=True, failureDetected=True
- `incomplete_langchain_agent_api`: passedExpectation=True, expectedFailure=True, failureDetected=True
- `unsafe_langchain_static_side_effect`: passedExpectation=True, expectedFailure=True, failureDetected=True
- `unsafe_langchain_render_prompt`: passedExpectation=True, expectedFailure=True, failureDetected=True

Validator Smoke:

- Owner: factory_agent_25_smoke
- Mission: Runs generated validators and reports blockers.
- Validator: runtime_equivalence
- Command: `python tools/validate_runtime_equivalence.py`
- Report artifact: `generated/runtime-equivalence-report.json`
- Report pass: True
- Blocker count: 0
- Prompt bodies stored: False

Issues:

- none
