# Copilot Factory Validation

Pass: True

Copilots: 18

Factory agents: 50

Tasks: 50

Control Room:

- Present: True
- Owner: factory_agent_01_director
- Mission: Owns the whole run, keeps gates honest and prevents scope drift.
- Concurrency: serial
- Lock file: .codex-loop/run.lock.json
- Lock file present: True
- Lock file valid: True
- Lock workspace matches: True
- Lock heartbeat age seconds: 17
- Snapshot evidence required: True
- Snapshot evidence present: True
- First task has DirectorGate: True

Semantic Router:

- Agent present: True
- Policy present: True
- Audit present: True
- Sample route checked: True
- Sample top route: python
- Deterministic Python first: True
- LLM assist used: False

Discovery Auditor:

- Agent present: True
- Policy present: True
- Audit present: True
- Catalog profile present: True
- Lookup profile present: True
- Sample route checked: True
- Sample top route: as_is_discovery
- Runtime trace returned: True

Architecture Auditor:

- Agent present: True
- Audit artifact present: True
- Shared spec contract present: True
- LangChain profile contract present: True
- Runtime refs checked: ['codex', 'claude', 'github-copilot', 'runtime-contract', 'readme']
- LangChain behavior checked: True
- LangChain input validation checked: True
- LangChain prompt redaction checked: True
- Sample route checked: True
- Sample top route: aida_architecture
- Route audit evidence: True
- Localized route checked: True
- Localized route cheap path: True
- Localized route audit evidence: True

Design Auditor:

- Agent present: True
- Agent outputs present: True
- Policy present: True
- Target copilots: ['aida_architecture', 'java_generic', 'java_architect', 'angular_18', 'nodejs']
- Artifacts checked: ['aida_architecture', 'java_generic', 'java_architect', 'angular_18', 'nodejs']
- Schemas require handoff: ['aida_architecture', 'java_generic', 'java_architect', 'angular_18', 'nodejs']
- Runtime map checked: ['aida_architecture', 'java_generic', 'java_architect', 'angular_18', 'nodejs']
- Matrix evidence present: True
- LangChain input validation checked: ['aida_architecture', 'java_generic', 'java_architect', 'angular_18', 'nodejs']
- LangChain evidence gate checked: ['aida_architecture', 'java_generic', 'java_architect', 'angular_18', 'nodejs']
- LangChain LLM escalation guarded: ['aida_architecture', 'java_generic', 'java_architect', 'angular_18', 'nodejs']
- LangChain prompt redaction checked: ['aida_architecture', 'java_generic', 'java_architect', 'angular_18', 'nodejs']
- Sample route checked: True
- Sample top route: java_architect
- Localized route checked: True
- Localized top route: aida_architecture
- Localized route cheap path: True

Build Auditor:

- Agent present: True
- Agent outputs present: True
- Policy present: True
- Target copilots: ['devex', 'firefly_v5', 'firefly_v6', 'moonshine', 'java_generic', 'angular_18', 'nodejs', 'python']
- Artifacts checked: ['devex', 'firefly_v5', 'firefly_v6', 'moonshine', 'java_generic', 'angular_18', 'nodejs', 'python']
- Schemas require implementation: ['devex', 'firefly_v5', 'firefly_v6', 'moonshine', 'java_generic', 'angular_18', 'nodejs', 'python']
- Runtime map checked: ['devex', 'firefly_v5', 'firefly_v6', 'moonshine', 'java_generic', 'angular_18', 'nodejs', 'python']
- Factory audit checked: True
- Matrix evidence present: True
- LangChain input validation checked: ['devex', 'firefly_v5', 'firefly_v6', 'moonshine', 'java_generic', 'angular_18', 'nodejs', 'python']
- LangChain evidence gate checked: ['devex', 'firefly_v5', 'firefly_v6', 'moonshine', 'java_generic', 'angular_18', 'nodejs', 'python']
- LangChain LLM escalation guarded: ['devex', 'firefly_v5', 'firefly_v6', 'moonshine', 'java_generic', 'angular_18', 'nodejs', 'python']
- LangChain prompt redaction checked: ['devex', 'firefly_v5', 'firefly_v6', 'moonshine', 'java_generic', 'angular_18', 'nodejs', 'python']
- Sample route checked: True
- Sample top route: devex
- Localized route checked: True
- Localized top route: devex
- Localized route cheap path: True

Test Strategy Audit:

- Pass: True
- Agent present: True
- QA copilot present: True
- QA spec playbook checked: True
- Runtime refs checked: ['codex', 'claude', 'github-copilot', 'langchain']
- Pairwise case count: 6
- Negative cases detected: True
- Sample route checked: True
- Sample top route: qa_general
- Sample route cheap path: True
- Runtime trace returned: True

Security Auditor:

- Pass: True
- Agent present: True
- Policy version: sensitive-credentials-mcp-audit-1.0
- Mission: Audits sensitive credentials policy, threat model and safe MCP usage.
- Env example checked: True
- MCP config checked: True
- Sensitive credentials policy checked: True
- Threat model checked: True
- Safe MCP usage checked: True
- Runtime equivalence checked: True
- Connectors checked: github_mcp, sonarqube_mcp, confluence_mcp_optional
- Negative cases detected: True

MCP Connector Auditor:

- Pass: True
- Agent present: True
- Policy version: mcp-connector-placeholder-audit-1.0
- Env example checked: True
- MCP config checked: True
- Audit contract checked: True
- Declaration requirements checked: True
- Env placeholder requirements checked: True
- Runtime equivalence checked: True
- Quality gates checked: True
- Connectors checked: confluence_mcp_optional, github_mcp, sonarqube_mcp
- Env placeholders checked: CONFLUENCE_TOKEN_OPTIONAL, GITHUB_TOKEN, SONARQUBE_TOKEN
- Orphan sensitive placeholders: none
- Negative cases detected: True

DevOps Auditor:

- Pass: True
- Agent present: True
- Policy version: devops-ci-logs-reproducibility-rollback-audit-1.0
- Target copilot: cicd
- Run factory checked: True
- Factory audit checked: True
- Log evidence report: generated/devops-log-evidence.json
- Runtime trace checked: True
- Runtime refs checked: ['codex', 'claude', 'github-copilot', 'langchain']
- Sample route checked: True
- Sample top route: cicd
- Sample route cheap path: True
- Negative cases detected: True

Cloud Auditor:

- Pass: True
- Agent present: True
- Policy version: cloud-migration-target-modernization-audit-1.0
- Target copilot: journey_to_cloud
- Audit artifact checked: True
- Factory audit checked: True
- Runtime trace checked: True
- Runtime refs checked: ['codex', 'claude', 'github-copilot', 'langchain']
- Schemas require cloud_migration: True
- Cloud migration schema checked: True
- Sample route checked: True
- Sample top route: journey_to_cloud
- Sample route cheap path: True
- Negative cases detected: True

Release Auditor:

- Pass: True
- Agent present: True
- Policy version: release-readiness-scorecard-exit-criteria-audit-1.0
- Target copilots checked: ['devex', 'aida_architecture', 'java_architect', 'qa_general', 'sonarqube_remediation', 'cicd', 'journey_to_cloud', 'firefly_marketplace']
- Config gate checked: True
- Factory audit checked: True
- Runtime trace checked: True
- Runtime refs checked: ['devex', 'aida_architecture', 'java_architect', 'qa_general', 'sonarqube_remediation', 'cicd', 'journey_to_cloud', 'firefly_marketplace']
- Scorecards checked: ['devex', 'aida_architecture', 'java_architect', 'qa_general', 'sonarqube_remediation', 'cicd', 'journey_to_cloud', 'firefly_marketplace']
- Exit criteria checked: ['product-market-fit', 'implementation', 'test-coverage', 'browser-navigation-render', 'safe-coding-privacy', 'seo-content', 'packaging-artifact', 'release-handoff']
- Sample route checked: True
- Sample top route: firefly_marketplace
- Sample route cheap path: True
- Negative cases detected: True

Operate Auditor:

- Pass: True
- Agent present: True
- Policy version: operate-observability-incident-runbook-audit-1.0
- Target copilots checked: ['single_registry', 'moonshine', 'nodejs', 'python', 'cicd', 'copilots_manager', 'firefly_marketplace']
- Contract checked: True
- Scorecard checked: True
- Runbook checked: True
- Incident runbook checked: True
- Settings checked: True
- Documentation checked: True
- Telemetry signals checked: ['state_lock_heartbeat', 'validation_gate_reports', 'prompt_quality_gate', 'runtime_equivalence_gate', 'runtime_incident_summary']
- Incident playbooks checked: ['state-lock-stale', 'validation-report-regression', 'runtime-equivalence-drift', 'observability-signal-gap', 'privacy-log-exposure']
- Sample route checked: True
- Sample top route: nodejs
- Sample route cheap path: True
- Negative cases detected: True

Cost Routing Auditor:

- Pass: True
- Agent present: True
- Policy version: cost-routing-1.0
- Contract checked: True
- Scorecard checked: True
- Policy doc checked: True
- Settings checked: True
- Runtime equivalence checked: True
- Traceability checked: True
- Cheap deterministic work checked: ['catalog_generation', 'semantic_routing', 'schema_validation', 'prompt_quality_budget', 'runtime_equivalence_diff', 'documentation_marker_audit']
- Judgement work checked: ['architecture_tradeoff', 'non_trivial_code_change', 'final_operator_synthesis']
- Sample route checked: True
- Sample top route: python
- Sample route cheap path: True
- Negative cases detected: True

Knowledge Boundary Auditor:

- Agent present: True
- Audit artifact present: True
- Shared spec contract present: True
- LangChain profile contract present: True
- Schemas require KB partition: True
- KB output schema checked: True
- Runtime refs checked: ['codex', 'claude', 'github-copilot', 'langchain', 'runtime-contract', 'readme']
- LangChain behavior checked: True
- Sample route checked: True
- Sample top route: firefly_v6
- Sample route cheap path: True
- Route audit evidence: True

Documentation Auditor:

- Pass: True
- Agent present: True
- Policy version: generated-readme-operator-docs-audit-1.0
- Report artifact: generated/documentation-audit-report.json
- Report written: True
- Copilot READMEs checked: ['devex', 'aida_architecture', 'as_is_discovery', 'single_registry', 'firefly_v5', 'firefly_v6', 'moonshine', 'java_generic', 'java_architect', 'angular_18', 'nodejs', 'python', 'qa_general', 'sonarqube_remediation', 'cicd', 'journey_to_cloud', 'copilots_manager', 'firefly_marketplace']
- Operator docs checked: ['README.md', 'OPERATING_SYSTEM.md', 'factory-prompt.md', '.codex-loop/factory/operate-observability-runbook.md', '.codex-loop/factory/incident-runbook.md', '.codex-loop/factory/cost-routing-policy.md']
- Runtime equivalence trace: generated/documentation-audit-report.json#/readmeChecks
- Negative cases detected: True

Runtime Safety:

- Pass: True
- Helper present: True
- Evidence limits checked: True
- Prompt redaction checked: True
- Negative cases detected: True

Generator:

- Present: True
- Semantic router template checked: True
- Generated index checked: True
- Generated agent checked: True
- Generated Python profile checked: True
- Generated discovery policy checked: True
- Generated discovery agent checked: True
- Generated discovery profile checked: True
- Generated design policy checked: True
- Generated design agent checked: True
- Generated design profiles checked: True
- Generated build policy checked: True
- Generated build agent checked: True
- Generated build profiles checked: True
- Generated run_factory checked: True
- Generated security policy checked: True
- Generated security env checked: True

Issues:

- none
