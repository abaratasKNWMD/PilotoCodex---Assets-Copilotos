# Task 005 QA Audit

## Scope

Audited increment for `factory_agent_05_architecture`: Architecture Board routing, ADR/principles decision-audit contract, runtime equivalence across Codex, Claude, GitHub Copilot and LangChain, and generated validation reports.

Reviewed main artifacts:

- `OPERATING_SYSTEM.md`
- `generated/semantic-routing-plan.md`
- `dist/copilots/aida_architecture/shared/architecture_decision_audit.json`
- `dist/copilots/aida_architecture/shared/spec.json`
- `dist/copilots/aida_architecture/{codex,claude,github-copilot,langchain}`
- `tools/semantic_router.py`
- `tools/validate_copilot_factory.py`
- `generated/*report*.json`

## Findings

1. Fixed: LangChain architecture adapter returned `pass: true` while required audit evidence was missing.
   - Impact: architecture decisions could appear accepted despite missing `principles`, `adr`, `technical_decision_quality` or `validation`, weakening traceability and cost discipline.
   - Evidence: `python dist/copilots/aida_architecture/langchain/agent.py "architecture adr principles"` initially reported `audit.pass: true` with populated `evidence_needed`.
   - Patch: `dist/copilots/aida_architecture/langchain/agent.py` now marks incomplete evidence as an issue, returns `pass: false`, and blocks LLM escalation until the evidence pack is complete.

2. Fixed: factory validation only checked LangChain architecture behavior by string markers.
   - Impact: the validator could pass even when the runtime behavior contradicted the shared audit artifact.
   - Patch: `tools/validate_copilot_factory.py` now loads the architecture LangChain adapter and checks both negative and complete evidence cases:
     - missing evidence blocks pass;
     - all required evidence passes;
     - missing evidence prevents LLM escalation.

## Patches Made

- `dist/copilots/aida_architecture/langchain/agent.py`
  - Added missing-evidence issue reporting.
  - Changed pass condition to require no issues and no pending evidence.
  - Guarded LLM escalation behind a passing audit.

- `tools/validate_copilot_factory.py`
  - Added executable behavior checks for the Architecture Board LangChain adapter.
  - Extended the validation report with `langchainMissingEvidenceBlocks`, `langchainCompleteEvidencePasses` and `langchainLlmEscalationGuarded`.

Generated reports were refreshed by validation commands:

- `generated/validation-report.json`
- `generated/validation-report.md`
- `generated/prompt-quality-report.json`
- `generated/prompt-quality-report.md`
- `generated/runtime-equivalence-report.json`
- `generated/runtime-equivalence-report.md`

## Commands Executed

- `Get-Command rg -ErrorAction SilentlyContinue`
- `git status --short` failed because this workspace has no `.git` metadata.
- `Get-ChildItem -Force`
- `python tools/validate_copilot_factory.py`
- `python tools/semantic_router.py python ci routing`
- `python tools/semantic_router.py "architecture adr principles"`
- `python dist/copilots/aida_architecture/langchain/agent.py "architecture adr principles"`
- `python tools/validate_prompt_quality.py`
- `python tools/validate_runtime_equivalence.py`

## Verification Results

- `python tools/validate_copilot_factory.py`: PASS.
- `python tools/semantic_router.py python ci routing`: PASS, returned `python` then `cicd` as the top cheap routes with `llm_assist_used: false`.
- `python tools/semantic_router.py "architecture adr principles"`: PASS, returned `aida_architecture` first with `architecture_decision_audit` evidence.
- `python dist/copilots/aida_architecture/langchain/agent.py "architecture adr principles"`: PASS for negative QA expectation; missing evidence now yields `audit.pass: false` and `llm_escalation: false`.
- `python tools/validate_prompt_quality.py`: PASS; `aida_architecture` LangChain prompt growth remains under the configured 10 percent cap.
- `python tools/validate_runtime_equivalence.py`: PASS.

## Residual Risks

- No Git metadata is present, so changed-file attribution relies on the provided task file list and local inspection rather than `git diff`.
- Cleanup of empty `__pycache__` directories created during Python checks was blocked by local command policy; validators ignore `__pycache__`.
- The generic LangChain template in `tools/elevate_copilot_prompts.py` still treats missing generic evidence as non-fatal for other copilots. This audit did not patch it because the task scope is Architecture Board behavior.
