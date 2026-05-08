# QA Audit - Task 001

Scope: `factory_agent_01_director` / Control Room contract.

Date: 2026-05-04.

## Verdict

PASS after fixes.

The director mission is now represented by machine-checkable artifacts:

- `factory.config.json/controlRoom` contains the ownership, serial concurrency, state lock, gate honesty, scope drift, runtime-equivalence, cost-trace and release truth policies.
- `tasks.json` task 1 contains the `DirectorGate` markers and runs structure, prompt quality and runtime-equivalence validation.
- `tools/validate_copilot_factory.py` validates the Control Room contract and includes Control Room evidence in `generated/validation-report.json` and `.md`.
- `tools/generate_copilot_factory.py` and `tools/elevate_copilot_prompts.py` regenerate the same contract instead of erasing it.

## Findings

1. Fixed - Gate drift in task 1.
   `tasks.json` declared `gates=structure+promptDepth+runtimeEquivalence`, but the `Verify` command only ran structure and prompt quality. Patched task 1 and the task generator so runtime equivalence is enforced.

2. Fixed - DoD was not fully machine-verifiable.
   `tools/validate_copilot_factory.py` counted copilots, agents and files, but did not validate the new Control Room contract or first queue gate. Added validation for owner, mission, serial concurrency, lock policy, required reports, runtime adapters, zero unexplained drift, cost trace, release truth gates and task markers.

3. Fixed - Regeneration could erase the Control Room contract.
   `tools/generate_copilot_factory.py` and `tools/elevate_copilot_prompts.py` could rewrite `factory.config.json`, docs and task prompts without the new director controls. Added generator support for `controlRoom`, `DirectorGate` and the three-command verification chain.

## Patches Made

- Updated `tasks.json`.
- Updated `tools/validate_copilot_factory.py`.
- Updated `tools/generate_copilot_factory.py`.
- Updated `tools/elevate_copilot_prompts.py`.
- Regenerated factory artifacts through `python tools/generate_copilot_factory.py`.
- Regenerated validation reports through the validators.

## QA Checklist

- Main flow: generator plus validation flow passes.
- Empty/loading/error states: not applicable; this task has no UI flow.
- UX/copy/accessibility: not applicable for UI; operator copy now names the Control Room gate and evidence sources.
- Code quality: validators compile and the new checks are scoped to the director/control-room contract.
- Tests: deterministic validators cover the new contract.
- Documentation: README, operating system and prompt surfaces keep the director contract after regeneration.

## Commands Executed

- `Get-Command rg -ErrorAction SilentlyContinue`
- `git status --short` - failed because this workspace is not a Git repository.
- `python tools/validate_copilot_factory.py`
- `python tools/validate_prompt_quality.py`
- `python tools/validate_runtime_equivalence.py`
- `python tools/generate_copilot_factory.py`
- `python -m py_compile tools/generate_copilot_factory.py tools/elevate_copilot_prompts.py tools/validate_copilot_factory.py tools/validate_prompt_quality.py tools/validate_runtime_equivalence.py`
- `python tools/validate_copilot_factory.py && python tools/validate_prompt_quality.py`

Final verification output:

- `Copilot factory validation PASS: 18 copilots, 50 agents, 50 tasks.`
- `Prompt quality validation PASS: 18 copilots, 72 runtime prompts.`
- `Runtime equivalence PASS: 18 copilots checked.`

## Residual Risks

- There is no Git metadata in this workspace, so the audit cannot compare against a committed baseline.
- The validator checks the declared state-lock contract and reports whether `.codex-loop/run.lock.json` exists, but it does not prove atomic lock acquisition or process liveness.
- `tasks.json` remains a string-based queue format; the new checks use required markers to avoid broad schema changes in this task.
