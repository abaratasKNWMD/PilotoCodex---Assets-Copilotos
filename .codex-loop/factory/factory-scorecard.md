# Factory Scorecard

Generated: 2026-05-05T19:37:33.728Z
Workspace: c:\Users\abaratas\Desktop\CARPETA PROYECTOS\TEST CODEX\NuevoProyecto
Score: 901/1000
Grade: A
Autonomous ready: yes
Critical failures: 0

| # | ID | Category | Severity | Status | Score | Evidence |
|---:|---|---|---|---|---:|---|
| 1 | runtime.workspace.writable | Runtime | critical | pass | 10/10 | Write probe succeeded. |
| 2 | runtime.workspace.path | Runtime | critical | pass | 10/10 | c:\Users\abaratas\Desktop\CARPETA PROYECTOS\TEST CODEX\NuevoProyecto |
| 3 | runtime.transport.codex_cli | Runtime | critical | pass | 10/10 | transport=codexCli |
| 4 | runtime.codex.version | Runtime | critical | pass | 10/10 | display=c:\Users\abaratas\.vscode\extensions\openai.chatgpt-26.429.30905-win32-x64\bin\windows-x86_64\codex.exe; exit=0; stdout=codex-cli 0.128.0-alpha.1; stderr= |
| 5 | runtime.codex.exec_help | Runtime | critical | pass | 10/10 | exit=0; stdout=Run Codex non-interactively Usage: codex exec [OPTIONS] [PROMPT] codex exec [OPTIONS] <COMMAND> [ARGS] Commands: resume Resume a previous session by id or pick ; stderr= |
| 6 | runtime.codex.approval | Runtime | critical | pass | 10/10 | approval_policy=never |
| 7 | runtime.codex.sandbox | Runtime | critical | pass | 10/10 | sandbox=workspace-write |
| 8 | runtime.timeout | Runtime | major | pass | 10/10 | 900000ms |
| 9 | runtime.retries | Runtime | major | pass | 10/10 | 3 |
| 10 | runtime.web_search | Runtime | major | pass | 10/10 | web_search=cached |
| 11 | runtime.git_folder | Runtime | minor | pass | 8/10 | No .git folder; codex exec uses --skip-git-repo-check. |
| 12 | factory.enabled | Factory Config | major | warn | 6/10 | factoryEnabled=false |
| 13 | factory.preset | Factory Config | major | pass | 10/10 | preset=freePrompt |
| 14 | factory.task_count | Factory Config | minor | pass | 10/10 | 50 |
| 15 | factory.quality_profile | Factory Config | major | pass | 10/10 | strict |
| 16 | factory.verify_each_task | Factory Config | critical | pass | 10/10 | true |
| 17 | factory.repair_enabled | Factory Config | major | pass | 10/10 | true |
| 18 | factory.review_at_end | Factory Config | major | pass | 10/10 | true |
| 19 | factory.decision_guard | Factory Config | major | pass | 10/10 | true |
| 20 | factory.adaptive_planning | Factory Config | major | pass | 10/10 | true |
| 21 | factory.autonomy_budget | Factory Config | minor | pass | 10/10 | forever=false; hours=4 |
| 22 | factory.github_scout | Factory Config | major | pass | 10/10 | true |
| 23 | factory.creative_studio | Factory Config | minor | pass | 10/10 | true |
| 24 | factory.browser_qa | Factory Config | major | warn | 4/10 | false |
| 25 | factory.safe_coding_review | Factory Config | major | pass | 10/10 | true |
| 26 | factory.release_readiness | Factory Config | major | pass | 10/10 | true |
| 27 | runtime.policy_safe_mode | Runtime Policy | critical | pass | 10/10 | true |
| 28 | runtime.pause_on_failed_verification | Runtime Policy | critical | pass | 10/10 | true |
| 29 | runtime.repair_depth | Runtime Policy | major | pass | 10/10 | 2 |
| 30 | runtime.policy_friction_scan | Runtime Policy | major | fail | 0/10 | 3 hit groups; files=agent-state.json, agent.log, README.md, .codex-loop/factory/preflight-report.md, .codex-loop/factory/runtime-risk-report.md, .codex-loop/factory/snapshots/firefly_v5-owner30-20260505-110705/dist/copilots/firefly_v5/shared/spec.json, .codex-loop/factory/snapshots/firefly_v5-owner30-20260505-110705/dist/copilots/firefly_v5/github-copilot/copilot-agent.md, .codex-loop/factory/snapshots/firefly_v5-owner30-20260505-110705/dist/copilots/firefly_v5/codex/AGENT.md, .codex-loop/factory/snapshots/firefly_v5-owner30-20260505-110705/dist/copilots/firefly_v5/claude/AGENT.md, .codex-loop/factory/snapshots/factory_agent_16_github-20260504-194311/dist/copilots/sonarqube_remediation/shared/spec.json, .codex-loop/factory/snapshots/factory_agent_16_github-20260504-194311/dist/copilots/sonarqube_remediation/shared/runtime_contract.md, .codex-loop/factory/snapshots/factory_agent_16_github-20260504-194311/dist/copilots/sonarqube_remediation/langchain/agent_profile.json, .codex-loop/factory/snapshots/factory_agent_16_github-20260504-194311/dist/copilots/sonarqube_remediation/github-copilot/copilot-agent.md, .codex-loop/factory/snapshots/factory_agent_16_github-20260504-194311/dist/copilots/sonarqube_remediation/codex/AGENT.md, .codex-loop/factory/snapshots/factory_agent_16_github-20260504-194311/dist/copilots/sonarqube_remediation/claude/AGENT.md, .codex-loop/factory/snapshots/factory_agent_16_github-20260504-194311/dist/copilots/single_registry/shared/spec.json, .codex-loop/factory/snapshots/factory_agent_16_github-20260504-194311/dist/copilots/single_registry/shared/runtime_contract.md, .codex-loop/factory/snapshots/factory_agent_16_github-20260504-194311/dist/copilots/single_registry/langchain/agent_profile.json, .codex-loop/factory/snapshots/factory_agent_16_github-20260504-194311/dist/copilots/single_registry/github-copilot/copilot-agent.md, .codex-loop/factory/snapshots/factory_agent_16_github-20260504-194311/dist/copilots/single_registry/codex/AGENT.md, .codex-loop/factory/snapshots/factory_agent_16_github-20260504-194311/dist/copilots/single_registry/claude/AGENT.md, .codex-loop/factory/snapshots/factory_agent_16_github-20260504-194311/dist/copilots/qa_general/shared/spec.json, .codex-loop/factory/snapshots/factory_agent_16_github-20260504-194311/dist/copilots/qa_general/shared/runtime_contract.md, .codex-loop/factory/snapshots/factory_agent_16_github-20260504-194311/dist/copilots/qa_general/langchain/agent_profile.json, .codex-loop/factory/snapshots/factory_agent_16_github-20260504-194311/dist/copilots/qa_general/github-copilot/copilot-agent.md |
| 31 | output.root_safe | Output Topology | critical | pass | 10/10 | products |
| 32 | output.registry | Output Topology | major | pass | 10/10 | exists=false; parseable=true; path=.codex-loop/factory/project-registry.json |
| 33 | output.registry_count | Output Topology | major | pass | 10/10 | 0/5 |
| 34 | output.slug_collisions | Output Topology | critical | pass | 10/10 | duplicates=(none); unsafe=(none) |
| 35 | output.root_pollution | Output Topology | major | pass | 10/10 | (none) |
| 36 | frontier.output-topology | Frontier Governance | minor | pass | 10/10 | root=products; registry=0; unsafe=0; duplicates=0 |
| 37 | frontier.runtime-toolchain | Frontier Governance | minor | pass | 10/10 | codex=true; execHelp=0; node=true; npm=true; rg=false; rgShim=true; timeout=900000; retries=3 |
| 38 | frontier.state-locks | Frontier Governance | minor | pass | 10/10 | lock pid=20472; stale=true; alive=true; unfinished=false |
| 39 | frontier.quality-real | Frontier Governance | major | warn | 4/10 | build=false; test=false; coverageScript=false; coverage=missing%; verifyEach=true |
| 40 | frontier.render-browser | Frontier Governance | major | warn | 5/10 | browserQa=false; e2eScript=false; playwrightConfig=false |
| 41 | frontier.packaging | Frontier Governance | minor | pass | 10/10 | enabled=false; tauriConfig=false; tauriScript=false; buildScript=false |
| 42 | frontier.sensitive-data | Frontier Governance | minor | pass | 10/10 | 0 hit groups; files=(none) |
| 43 | frontier.license-github-scout | Frontier Governance | minor | pass | 10/10 | githubScout=true; ledger=true; notices=false; policy=permissiveOnly |
| 44 | frontier.research-trust | Frontier Governance | minor | pass | 10/10 | preset=freePrompt; researchEvidence=true; policySafeBrief=true |
| 45 | frontier.cost-time | Frontier Governance | minor | pass | 10/10 | forever=false; guard=true; hours=4; maxTasks=0 |
| 46 | frontier.naming | Frontier Governance | minor | pass | 10/10 | duplicates=(none); unsafe=(none) |
| 47 | frontier.rollback | Frontier Governance | minor | pass | 10/10 | createBackups=true; git=false; rollbackFolder=true |
| 48 | frontier.final-truth-gate | Frontier Governance | major | warn | 6/10 | frontierReview=true; finalReview=false; releaseReport=false |
| 49 | tool.node | Tools | major | pass | 10/10 | Found on PATH. |
| 50 | tool.npm | Tools | major | pass | 10/10 | Found on PATH. |
| 51 | tool.npx | Tools | major | pass | 10/10 | Found on PATH. |
| 52 | tool.git | Tools | major | pass | 10/10 | Found on PATH. |
| 53 | tool.rg | Tools | minor | pass | 10/10 | Local shim ready in .codex-loop/tool-shims. |
| 54 | tool.gh | Tools | minor | warn | 5/10 | Not found on PATH. |
| 55 | tool.python | Tools | minor | pass | 10/10 | Found on PATH. |
| 56 | tool.py | Tools | minor | pass | 10/10 | Found on PATH. |
| 57 | tool.pnpm | Tools | minor | warn | 5/10 | Not found on PATH. |
| 58 | tool.yarn | Tools | minor | warn | 5/10 | Not found on PATH. |
| 59 | tool.bun | Tools | minor | warn | 5/10 | Not found on PATH. |
| 60 | tool.cargo | Tools | minor | pass | 10/10 | Found on PATH. |
| 61 | tool.rustc | Tools | minor | pass | 10/10 | Found on PATH. |
| 62 | tool.tauri | Tools | minor | warn | 5/10 | Not found on PATH. |
| 63 | tool.code | Tools | minor | pass | 10/10 | Found on PATH. |
| 64 | tool.codex | Tools | minor | pass | 10/10 | Found on PATH. |
| 65 | package.exists | Workspace Package | minor | warn | 5/10 | No package.json yet. |
| 66 | package.parseable | Workspace Package | major | pass | 10/10 | OK |
| 67 | package.script.dev | Workspace Package | minor | warn | 5/10 | (none) |
| 68 | package.script.build | Workspace Package | major | warn | 5/10 | (none) |
| 69 | package.script.test | Workspace Package | major | warn | 4/10 | (none) |
| 70 | package.script.coverage | Workspace Package | major | warn | 4/10 | (none) |
| 71 | package.script.lint | Workspace Package | minor | warn | 5/10 | (none) |
| 72 | package.script.e2e | Workspace Package | minor | warn | 5/10 | (none) |
| 73 | protocol.codex.loop.factory.factory.operating.system.md | Factory Protocol | major | pass | 10/10 | present |
| 74 | protocol.codex.loop.factory.microtask.contract.md | Factory Protocol | major | pass | 10/10 | present |
| 75 | protocol.codex.loop.factory.quality.gates.json | Factory Protocol | major | pass | 10/10 | present |
| 76 | protocol.codex.loop.factory.acceptance.frontiers.json | Factory Protocol | major | pass | 10/10 | present |
| 77 | protocol.codex.loop.factory.departments.md | Factory Protocol | major | pass | 10/10 | present |
| 78 | protocol.codex.loop.factory.department.raci.md | Factory Protocol | major | pass | 10/10 | present |
| 79 | protocol.codex.loop.factory.browser.render.security.gates.md | Factory Protocol | major | pass | 10/10 | present |
| 80 | protocol.codex.loop.factory.packaging.gates.md | Factory Protocol | major | pass | 10/10 | present |
| 81 | protocol.codex.loop.factory.github.scout.policy.md | Factory Protocol | major | pass | 10/10 | present |
| 82 | protocol.codex.loop.factory.github.reuse.ledger.md | Factory Protocol | major | pass | 10/10 | present |
| 83 | protocol.codex.loop.factory.capability.autodiscovery.policy.md | Factory Protocol | major | pass | 10/10 | present |
| 84 | protocol.codex.loop.factory.creative.studio.md | Factory Protocol | major | pass | 10/10 | present |
| 85 | protocol.codex.loop.factory.image.generation.policy.md | Factory Protocol | major | pass | 10/10 | present |
| 86 | protocol.codex.loop.factory.presentation.policy.md | Factory Protocol | major | pass | 10/10 | present |
| 87 | protocol.codex.loop.factory.scroll.storytelling.policy.md | Factory Protocol | major | pass | 10/10 | present |
| 88 | protocol.codex.loop.factory.pixel.ops.policy.md | Factory Protocol | major | pass | 10/10 | present |
| 89 | protocol.codex.loop.factory.rooms.map.json | Factory Protocol | major | pass | 10/10 | present |
| 90 | protocol.codex.loop.factory.parallelization.policy.md | Factory Protocol | major | pass | 10/10 | present |
| 91 | protocol.codex.loop.factory.parallel.scheduler.policy.md | Factory Protocol | major | pass | 10/10 | present |
| 92 | protocol.codex.loop.factory.worker.isolation.policy.md | Factory Protocol | major | pass | 10/10 | present |
| 93 | protocol.codex.loop.factory.adaptive.planning.policy.md | Factory Protocol | major | pass | 10/10 | present |
| 94 | protocol.codex.loop.factory.completion.decision.schema.json | Factory Protocol | major | pass | 10/10 | present |
| 95 | protocol.codex.loop.factory.supervisor.guard.policy.md | Factory Protocol | major | pass | 10/10 | present |
| 96 | protocol.codex.loop.factory.supervisor.decision.schema.json | Factory Protocol | major | pass | 10/10 | present |
| 97 | protocol.codex.loop.factory.backlog.mutation.log.md | Factory Protocol | major | pass | 10/10 | present |
| 98 | protocol.codex.loop.factory.org.graph.json | Factory Protocol | major | pass | 10/10 | present |
| 99 | protocol.codex.loop.factory.org.graph.md | Factory Protocol | major | pass | 10/10 | present |
| 100 | protocol.codex.loop.factory.agent.roster.md | Factory Protocol | major | pass | 10/10 | present |
