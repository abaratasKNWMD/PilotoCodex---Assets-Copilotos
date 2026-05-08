# Codex Factory Preflight

Generated: 2026-05-05T19:37:33.728Z
Workspace: c:\Users\abaratas\Desktop\CARPETA PROYECTOS\TEST CODEX\NuevoProyecto
Mode: start
Autonomous ready: yes
Score: 901/1000 (A)
Critical failures: 0
Major failures: 1
Warnings: 18

## Critical Blockers

- None.

## Top Warnings

- factory.enabled: Factory mode enabled (6/10, major)
- factory.browser_qa: Browser QA frontier enabled (4/10, major)
- runtime.policy_friction_scan: Workspace prompt-risk wording scan (0/10, major)
- frontier.quality-real: Calidad real (4/10, major)
- frontier.render-browser: Render/browser (5/10, major)
- frontier.final-truth-gate: Final truth gate (6/10, major)
- tool.gh: gh available (5/10, minor)
- tool.pnpm: pnpm available (5/10, minor)
- tool.yarn: yarn available (5/10, minor)
- tool.bun: bun available (5/10, minor)
- tool.tauri: tauri available (5/10, minor)
- package.exists: package.json exists (5/10, minor)
- package.script.dev: dev script (5/10, minor)
- package.script.build: build script (5/10, major)
- package.script.test: test script (4/10, major)
- package.script.coverage: coverage script (4/10, major)
- package.script.lint: lint script (5/10, minor)
- package.script.e2e: e2e/browser script (5/10, minor)

## Artifacts

- .codex-loop/factory/factory-scorecard.md
- .codex-loop/factory/factory-scorecard.json
- .codex-loop/factory/runtime-risk-report.md
- .codex-loop/factory/runtime-risk-report.json
- .codex-loop/factory/output-frontier-report.md
- .codex-loop/factory/output-frontier-report.json
- .codex-loop/factory/frontier-governance-report.md
- .codex-loop/factory/frontier-governance-report.json
- .codex-loop/factory/policy-safe-brief.md
- .codex-loop/factory/verification-frontier-probe.md
- .codex-loop/factory/verification-frontier-probe.json
- .codex-loop/factory/codex-runtime-incidents.md
- .codex-loop/factory/codex-runtime-incidents.jsonl
- .codex-loop/factory/artifact-passport.md
- .codex-loop/factory/artifact-passport.json
- .codex-loop/factory/incident-runbook.md
- .codex-loop/factory/preflight-report.json

## Context

```json
{
  "mode": "start",
  "resolvedCodex": {
    "command": "c:\\Users\\abaratas\\.vscode\\extensions\\openai.chatgpt-26.429.30905-win32-x64\\bin\\windows-x86_64\\codex.exe",
    "argsPrefix": [],
    "display": "c:\\Users\\abaratas\\.vscode\\extensions\\openai.chatgpt-26.429.30905-win32-x64\\bin\\windows-x86_64\\codex.exe"
  },
  "codexVersion": {
    "exitCode": 0,
    "stdout": "codex-cli 0.128.0-alpha.1\n",
    "stderr": ""
  },
  "codexExecHelp": {
    "exitCode": 0,
    "stdout": "Run Codex non-interactively\n\nUsage: codex exec [OPTIONS] [PROMPT]\n       codex exec [OPTIONS] <COMMAND> [ARGS]\n\nCommands:\n  resume  Resume a previous session by id or pick the most recent with --last\n  review  Run a code review against the current repository\n  help    Print this message or the help of the given subcommand(s)\n\nArguments:\n  [PROMPT]\n          Initial instructions for the agent. If not provided as an argument (or if `-` is used),\n          instructions are read from stdin. If stdin is piped and a prompt is also provided, stdin\n          is appended as a `<stdin>` block\n\nOptions:\n  -c, --config <key=value>\n          Override a configuration value that would otherwise be loaded from `~/.codex/config.toml`.\n          Use a dotted path (`foo.bar.baz`) to override nested values. The `value` portion is parsed\n          as TOML. If it fails to parse as TOML, the raw string is used as a literal.\n          \n          Examples: - `-c model=\"o3\"` - `-c 'sandbox_permissions=[\"disk-full-read-access\"]'` - `-c\n          shell_environment_policy.inherit=all`\n\n      --enable <FEATURE>\n          Enable a feature (repeatable). Equivalent to `-c features.<name>=true`\n\n      --disable <FEATURE>\n          Disable a feature (repeatable). Equivalent to `-c features.<name>=false`\n\n  -i, --image <FILE>...\n          Optional image(s) to attach to the initial prompt\n\n  -m, --model <MODEL>\n          Model the agent should use\n\n      --oss\n          Use open-source provider\n\n      --local-provider <OSS_PROVIDER>\n          Specify which local provider to use (lmstudio or ollama). If not specified with --oss,\n          will use config default or show selection\n\n  -p, --profile <CONFIG_PROFILE>\n          Configuration profile from config.toml to specify default options\n\n  -s, --sandbox <SANDBOX_MODE>\n          Select the sandbox policy to use when executing model-generated shell commands\n          \n          [possible values: read-only, workspace-write, danger-full-access]\n\n      --da",
    "stderr": ""
  },
  "commands": {
    "node": true,
    "npm": true,
    "npx": true,
    "git": true,
    "rg": false,
    "gh": false,
    "python": true,
    "py": true,
    "pnpm": false,
    "yarn": false,
    "bun": false,
    "cargo": true,
    "rustc": true,
    "tauri": false,
    "code": true,
    "codex": true
  },
  "toolShims": {
    "pathEntries": [
      "c:\\Users\\abaratas\\Desktop\\CARPETA PROYECTOS\\TEST CODEX\\NuevoProyecto\\.codex-loop\\tool-shims"
    ],
    "rg": true,
    "files": [
      ".codex-loop/tool-shims/rg.cmd",
      ".codex-loop/tool-shims/rg.ps1"
    ]
  },
  "workspaceWritable": true,
  "hasGitFolder": false,
  "runLock": {
    "id": "20472-1777965982151-myfbun7ymza",
    "pid": 20472,
    "workspace": "c:\\Users\\abaratas\\Desktop\\CARPETA PROYECTOS\\TEST CODEX\\NuevoProyecto",
    "startedAt": "2026-05-05T07:26:22.151Z",
    "heartbeatAt": "2026-05-05T12:56:59.082Z",
    "mode": "task-queue"
  },
  "runLockStale": true,
  "runLockPidAlive": true,
  "tasks": {
    "exists": true,
    "count": 50,
    "factoryGradeCount": 50,
    "parseable": true
  },
  "state": {
    "exists": true,
    "parseable": true,
    "nextTaskIndex": 41,
    "resultCount": 41
  },
  "packageJson": {
    "exists": false,
    "parseable": true,
    "scripts": [],
    "dependencies": [],
    "devDependencies": []
  },
  "protocolMissing": [],
  "protocolInvalidJson": [],
  "coverage": {
    "exists": false
  },
  "policyRisk": {
    "score": 0,
    "maxScore": 10,
    "hits": [
      {
        "term": "bypass wording",
        "count": 19,
        "severity": "medium"
      },
      {
        "term": "secrets wording",
        "count": 283,
        "severity": "low"
      },
      {
        "term": "credential-shaped wording",
        "count": 25,
        "severity": "low"
      }
    ],
    "sampleFiles": [
      "agent-state.json",
      "agent.log",
      "README.md",
      ".codex-loop/factory/preflight-report.md",
      ".codex-loop/factory/runtime-risk-report.md",
      ".codex-loop/factory/snapshots/firefly_v5-owner30-20260505-110705/dist/copilots/firefly_v5/shared/spec.json",
      ".codex-loop/factory/snapshots/firefly_v5-owner30-20260505-110705/dist/copilots/firefly_v5/github-copilot/copilot-agent.md",
      ".codex-loop/factory/snapshots/firefly_v5-owner30-20260505-110705/dist/copilots/firefly_v5/codex/AGENT.md",
      ".codex-loop/factory/snapshots/firefly_v5-owner30-20260505-110705/dist/copilots/firefly_v5/claude/AGENT.md",
      ".codex-loop/factory/snapshots/factory_agent_16_github-20260504-194311/dist/copilots/sonarqube_remediation/shared/spec.json",
      ".codex-loop/factory/snapshots/factory_agent_16_github-20260504-194311/dist/copilots/sonarqube_remediation/shared/runtime_contract.md",
      ".codex-loop/factory/snapshots/factory_agent_16_github-20260504-194311/dist/copilots/sonarqube_remediation/langchain/agent_profile.json",
      ".codex-loop/factory/snapshots/factory_agent_16_github-20260504-194311/dist/copilots/sonarqube_remediation/github-copilot/copilot-agent.md",
      ".codex-loop/factory/snapshots/factory_agent_16_github-20260504-194311/dist/copilots/sonarqube_remediation/codex/AGENT.md",
      ".codex-loop/factory/snapshots/factory_agent_16_github-20260504-194311/dist/copilots/sonarqube_remediation/claude/AGENT.md",
      ".codex-loop/factory/snapshots/factory_agent_16_github-20260504-194311/dist/copilots/single_registry/shared/spec.json",
      ".codex-loop/factory/snapshots/factory_agent_16_github-20260504-194311/dist/copilots/single_registry/shared/runtime_contract.md",
      ".codex-loop/factory/snapshots/factory_agent_16_github-20260504-194311/dist/copilots/single_registry/langchain/agent_profile.json",
      ".codex-loop/factory/snapshots/factory_agent_16_github-20260504-194311/dist/copilots/single_registry/github-copilot/copilot-agent.md",
      ".codex-loop/factory/snapshots/factory_agent_16_github-20260504-194311/dist/copilots/single_registry/codex/AGENT.md",
      ".codex-loop/factory/snapshots/factory_agent_16_github-20260504-194311/dist/copilots/single_registry/claude/AGENT.md",
      ".codex-loop/factory/snapshots/factory_agent_16_github-20260504-194311/dist/copilots/qa_general/shared/spec.json",
      ".codex-loop/factory/snapshots/factory_agent_16_github-20260504-194311/dist/copilots/qa_general/shared/runtime_contract.md",
      ".codex-loop/factory/snapshots/factory_agent_16_github-20260504-194311/dist/copilots/qa_general/langchain/agent_profile.json",
      ".codex-loop/factory/snapshots/factory_agent_16_github-20260504-194311/dist/copilots/qa_general/github-copilot/copilot-agent.md"
    ]
  },
  "outputTopology": {
    "score": 10,
    "maxScore": 10,
    "outputRoot": "products",
    "outputRootSafe": true,
    "registryPath": ".codex-loop/factory/project-registry.json",
    "registryExists": false,
    "registryParseable": true,
    "registryProductCount": 0,
    "registryPaths": [],
    "productFolders": [],
    "duplicateSlugs": [],
    "unsafeRegistryPaths": [],
    "rootLevelProjectFiles": [],
    "warnings": []
  },
  "frontierGovernance": {
    "score": 115,
    "maxScore": 130,
    "frontiers": [
      {
        "id": "output-topology",
        "label": "Output/topologia",
        "status": "controlled",
        "score": 10,
        "evidence": "root=products; registry=0; unsafe=0; duplicates=0",
        "mitigation": "Keep product apps under products/<slug>/ and maintain .codex-loop/factory/project-registry.json."
      },
      {
        "id": "runtime-toolchain",
        "label": "Runtime/toolchain",
        "status": "controlled",
        "score": 10,
        "evidence": "codex=true; execHelp=0; node=true; npm=true; rg=false; rgShim=true; timeout=900000; retries=3",
        "mitigation": "Expose Codex/Node/npm on PATH, verify codex exec --help, keep local tool shims ready, and use long timeouts plus at least 3 retries."
      },
      {
        "id": "state-locks",
        "label": "Estado/locks",
        "status": "controlled",
        "score": 10,
        "evidence": "lock pid=20472; stale=true; alive=true; unfinished=false",
        "mitigation": "Use run.lock, stale detection and unfinished-run detection before starting another factory."
      },
      {
        "id": "quality-real",
        "label": "Calidad real",
        "status": "watch",
        "score": 4,
        "evidence": "build=false; test=false; coverageScript=false; coverage=missing%; verifyEach=true",
        "mitigation": "Add build/test/coverage scripts and repair until coverage evidence approaches 80%."
      },
      {
        "id": "render-browser",
        "label": "Render/browser",
        "status": "watch",
        "score": 5,
        "evidence": "browserQa=false; e2eScript=false; playwrightConfig=false",
        "mitigation": "Frontend products need a real navigation/render smoke path, not only build."
      },
      {
        "id": "packaging",
        "label": "Packaging",
        "status": "controlled",
        "score": 10,
        "evidence": "enabled=false; tauriConfig=false; tauriScript=false; buildScript=false",
        "mitigation": "Only claim a desktop/binary artifact when the packaging config/script or actual artifact exists."
      },
      {
        "id": "sensitive-data",
        "label": "Secretos/datos",
        "status": "controlled",
        "score": 10,
        "evidence": "0 hit groups; files=(none)",
        "mitigation": "Use placeholders/env.example only; block generated credential-shaped values in changed files."
      },
      {
        "id": "license-github-scout",
        "label": "Licencias/GitHub Scout",
        "status": "controlled",
        "score": 10,
        "evidence": "githubScout=true; ledger=true; notices=false; policy=permissiveOnly",
        "mitigation": "Use GitHub for patterns first; adapt only permissive compatible code and record attribution."
      },
      {
        "id": "research-trust",
        "label": "Research trust",
        "status": "controlled",
        "score": 10,
        "evidence": "preset=freePrompt; researchEvidence=true; policySafeBrief=true",
        "mitigation": "Treat market/web findings as noisy; store source signals, confidence and caveats."
      },
      {
        "id": "cost-time",
        "label": "Coste/tiempo",
        "status": "controlled",
        "score": 10,
        "evidence": "forever=false; guard=true; hours=4; maxTasks=0",
        "mitigation": "Forever mode needs a supervisor guard; finite mode needs an explicit budget or task cap."
      },
      {
        "id": "naming",
        "label": "Naming",
        "status": "controlled",
        "score": 10,
        "evidence": "duplicates=(none); unsafe=(none)",
        "mitigation": "Use stable kebab-case product slugs and avoid third-party brands in product identity."
      },
      {
        "id": "rollback",
        "label": "Rollback",
        "status": "controlled",
        "score": 10,
        "evidence": "createBackups=true; git=false; rollbackFolder=true",
        "mitigation": "Keep snapshots or Git available before autonomous workers edit product files."
      },
      {
        "id": "final-truth-gate",
        "label": "Final truth gate",
        "status": "watch",
        "score": 6,
        "evidence": "frontierReview=true; finalReview=false; releaseReport=false",
        "mitigation": "Do not declare done until build/test/render/packaging/data/license evidence is present or residual risk is explicit."
      }
    ],
    "secretRisk": {
      "score": 10,
      "maxScore": 10,
      "hits": [],
      "sampleFiles": []
    },
    "finalTruth": {
      "ready": false,
      "missingEvidence": [
        "No build script yet.",
        "No test script yet.",
        "Coverage evidence missing or below 80%.",
        "Policy-safe wording scan found risky phrasing in planning files."
      ]
    }
  },
  "factoryBootstrap": false,
  "traceLatestError": "9541-department-council-task-41-attempt-1-2026-05-05T12-47-58-333Z: 2026-05-05T12:55:16.802177Z ERROR codex_core::tools::router: error=Exit code: 1"
}
```
