# Task 021 Safe-Coding / Privacy Review

Scope: `OPERATING_SYSTEM.md`, `generated/semantic-routing-plan.md`, `tools/semantic_router.py`, `tools/validate_copilot_factory.py`, generated audit reports and `dist/copilots` artifacts related to `factory_agent_21_kb`.

Mission reviewed: Audits KB separation, source-of-truth rules and context windows.

## Findings

| Severity | Finding | Evidence | Status |
| --- | --- | --- | --- |
| Critical | No live credentials, access tokens, private keys, billing secrets, customer data or absolute local user paths found in scoped artifacts. | Secret/path scans over `OPERATING_SYSTEM.md`, `generated`, `tools`, `dist/copilots`, `config` and `.codex-loop` returned no matches. | Pass |
| High | Runtime KB policy has a canonical source of truth and runtime adapters cite shared artifacts instead of creating independent policy. | `dist/copilots/firefly_v6/shared/kb_context_window_audit.json`, `dist/copilots/firefly_v6/shared/spec.json`, `dist/copilots/firefly_v6/langchain/agent.py`, `tools/semantic_router.py`. | Pass |
| High | User-facing routing inputs are bounded and normalized with understandable errors. | `tools/semantic_router.py` validates string type, non-empty requests, maximum request length and bounded route limit; CLI maps input errors to exit code 2. | Pass |
| High | LangChain runtime evidence is bounded and redacted before prompt rendering. | `dist/copilots/_runtime_safety.py` enforces request length, evidence item/depth/key/string limits, secret-like key redaction and value redaction for token/path/customer/tenant/billing patterns. | Pass |
| Medium | Connector declarations remain capability contracts, not credential storage. | Artifacts expose env var names such as `GITHUB_TOKEN` and `SONARQUBE_TOKEN` only; validator security and MCP connector auditors pass. | Pass |
| Medium | KB route keeps deterministic, low-cost routing before LLM escalation. | `python tools/semantic_router.py "kb source truth context windows"` routes to `firefly_v6` with `cheap_path: true`, `llm_assist_used: false` and `kb_audit:shared_contract`. | Pass |

## Patches Made

- Added this audit artifact: `.codex-loop/factory/audits/task-021-safe-coding.md`.
- Redacted the documented local-path scan command so the audit artifact itself does not contain local absolute path patterns.
- No product code or generated contract patch was needed. The scoped review found no obvious safe-coding/privacy defect requiring remediation.

## Commands Executed

- `Get-Command rg -ErrorAction SilentlyContinue | Select-Object -ExpandProperty Source`
- `git status --short` (reported that this workspace is not a Git repository)
- `Get-ChildItem -Force`
- `Get-ChildItem -Recurse -Force dist\copilots | Select-Object FullName,Length,LastWriteTime`
- `Get-Content -Raw OPERATING_SYSTEM.md`
- `Get-Content -Raw generated\semantic-routing-plan.md`
- `Get-Content -Raw tools\semantic_router.py`
- `Get-Content -Raw tools\validate_copilot_factory.py`
- `rg -n --hidden --glob '!agent.log' --glob '!agent-state.json' --glob '!*.pyc' "(AKIA[0-9A-Z]{16}|ghp_[A-Za-z0-9_]{20,}|github_pat_[A-Za-z0-9_]+|sk-[A-Za-z0-9]{20,}|xox[baprs]-[A-Za-z0-9-]+|-----BEGIN (RSA|OPENSSH|EC|PRIVATE) KEY-----|password\s*[:=]\s*[^\s]+|secret\s*[:=]\s*[^\s]+|token\s*[:=]\s*[^\s]+|api[_-]?key\s*[:=]\s*[^\s]+)" OPERATING_SYSTEM.md generated tools dist\copilots config .codex-loop`
- Local absolute path exposure scan over `OPERATING_SYSTEM.md`, `generated`, `tools`, `dist\copilots`, `config` and `.codex-loop` with known user-home path patterns redacted from this report.
- `rg -n "factory_agent_21_kb|kb_context_window_audit|KB_|Knowledge Boundary|context_window" tools\validate_copilot_factory.py tools\semantic_router.py OPERATING_SYSTEM.md generated\semantic-routing-plan.md dist\copilots\firefly_v6`
- `Get-Content -Raw dist\copilots\firefly_v6\shared\kb_context_window_audit.json`
- `Get-Content -Raw dist\copilots\firefly_v6\langchain\agent.py`
- `Get-Content -Raw dist\copilots\_runtime_safety.py`
- `Get-Content -Raw dist\copilots\firefly_v6\shared\spec.json`
- `Get-Content -Raw dist\copilots\firefly_v6\langchain\agent_profile.json`
- `Get-Content -Raw dist\copilots\firefly_v6\shared\output_schema.json`
- `python tools/validate_copilot_factory.py`
- `python tools/semantic_router.py python ci routing`
- `python tools/semantic_router.py "kb source truth context windows"`
- `Get-ChildItem -Force .codex-loop\factory`
- `Get-ChildItem -Force .codex-loop\factory\audits -ErrorAction SilentlyContinue`
- `Get-Content -Raw generated\validation-report.json`
- `Get-Content -Raw .codex-loop\factory\audits\task-021-safe-coding.md`
- `rg -n --hidden "<redacted local absolute path patterns>" .codex-loop\factory\audits\task-021-safe-coding.md`

## Verification Results

- `python tools/validate_copilot_factory.py`: pass, 18 copilots, 50 agents, 50 tasks.
- `python tools/semantic_router.py python ci routing`: pass, top route `python`, deterministic evidence returned, no LLM assist.
- `python tools/semantic_router.py "kb source truth context windows"`: pass, top route `firefly_v6`, `cheap_path: true`, `kb_context_window_audit` payload present.
- `generated/validation-report.json`: `pass: true`, `securityAuditor.pass: true`, `mcpConnectorAuditor.pass: true`, `runtimeSafety.pass: true`, `kbAuditor.routeAuditEvidence: true`.
- Post-report validation initially caught a local absolute path pattern inside this audit file's command log. The command log was redacted and the final `python tools/validate_copilot_factory.py` run passed.

## Residual Risks

- This was a static/local defensive review. It did not execute real MCP connectors, external auth flows, SaaS tenant isolation flows, CORS policy checks or billing integrations because they are outside this task scope.
- `dist/copilots` is generated output; future generator changes must keep `_runtime_safety.py` redaction and KB contract validation in sync to avoid drift.
- The workspace has no Git metadata, so review traceability depends on local snapshot/report artifacts rather than a commit diff.
