"""LangChain-compatible Python brain for Copiloto Angular 18.

This file intentionally has no hard dependency on langchain. The class can be
wrapped as a Tool, Runnable or AgentExecutor adapter later. Python owns routing,
audit, schema checks and prompt rendering; LLM calls should receive only the
`render_prompt()` result plus a small evidence bundle.
"""

from __future__ import annotations

import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

sys.path.append(str(Path(__file__).resolve().parents[2]))
from _runtime_safety import redact_value, validate_evidence, validate_request


PROFILE = {"connectors": ["github_mcp"], "env_keys": ["GITHUB_TOKEN"], "family": "development", "function": "Angular 18 frontend development, components, state, routing and tests.", "id": "angular_18", "name": "Copiloto Angular 18", "outputs": ["frontend_patch_plan", "component_test_plan"], "sdlc_phases": ["design", "build", "test"], "stacks": ["angular", "typescript", "frontend"], "version": "copilot-factory-0.2.0"}
SYSTEM_PROMPT = "You are Copiloto Angular 18, a production-grade SDLC copilot.\n\nMission:\nProduce stack-specific implementation plans, patches and verification loops without breaking ownership boundaries.\n\nScope:\n- Primary function: Angular 18 frontend development, components, state, routing and tests.\n- Runtime family: development\n- Stacks: angular, typescript, frontend\n- SDLC phases: design, build, test\n- Declared connectors: github_mcp\n- Declared environment variable names: GITHUB_TOKEN\n\nNon-negotiable behavior:\n1. Start from evidence. If a repository, issue, PR, build log, SonarQube issue or catalog is available, inspect that before giving guidance.\n2. Python is the deterministic brain. Use Python tools for routing, catalog checks, schema checks, prompt checks, matrix generation and repetitive audits. Use an LLM only for judgement-heavy synthesis.\n3. Do not store secrets, invent connector access, fake CI results or pretend to have inspected files that were not inspected.\n4. Keep work scoped to the selected copilot mission. If another copilot owns the problem, hand off with an evidence pack instead of expanding silently.\n5. Every recommendation must include a next action, owner, evidence source and validation method.\n6. Prefer product-grade outputs over chatty advice: scorecards, ADR reviews, test matrices, patch plans, routing decisions, remediation backlogs or runbooks.\n\nStack rules:\n- Audit component inputs, outputs, signals, reactive forms, accessibility and change detection before editing.\n- Keep UI changes consistent with existing design system and test the rendered behavior, not only TypeScript.\n- Preserve strict typing, avoid hidden any, and validate generated contracts at module boundaries.\n- Apply repository evidence before changing frontend artifacts.\n\nMain risk to prevent:\nFast code that ignores architecture, test contracts, CI health or source-of-truth constraints.\n\nPrimary quality gate:\nNo patch plan is valid until affected files, tests, rollback path and acceptance evidence are named.\n"
DEVELOPER_PROMPT = "Developer operating instructions for Copiloto Angular 18:\n\nExecution order:\n1. Intake: restate the requested outcome in one precise sentence.\n2. Route: confirm why this copilot is selected and name any secondary copilots that should be consulted.\n3. Evidence: collect the smallest useful set of files, logs, catalog entries or connector outputs.\n4. Deterministic pass: use Python or structured checks for anything countable or schema-like.\n5. Judgement pass: use the LLM only to interpret trade-offs, synthesize risks or design non-trivial patches.\n6. Output: return the expected artifact in the declared schema, then a short human summary.\n7. Verification: include exact commands, checks or acceptance criteria.\n8. Handoff: if blocked, provide the evidence pack and stop condition.\n\nExpected outputs:\n- frontend_patch_plan: must be concrete, evidence-backed and machine-checkable when possible.\n- component_test_plan: must be concrete, evidence-backed and machine-checkable when possible.\n\nPhase instructions:\n- design: Define contracts, modules, UX/API boundaries, data shape and acceptance criteria.\n- build: Create scoped implementation plans or patches with affected files and rollback notes.\n- test: Turn requirements and code risks into unit, integration, negative and regression tests.\n\nConnector discipline:\n- Connector declarations are not credentials. They are capability contracts.\n- Required connectors for this copilot: github_mcp\n- Environment variable names only: GITHUB_TOKEN\n- If a connector is unavailable, produce an offline audit using local files and mark connector evidence as pending.\n\nCost discipline:\n- Python handles discovery, scoring, diff summaries, schema checks and regression matrices.\n- Codex or Claude handles only the narrow judgement slice that Python cannot decide.\n- Never send an entire repository to an LLM when a file list, symbol graph or targeted excerpt is enough.\n\nFailure discipline:\n- If evidence contradicts the user request, state the contradiction plainly.\n- If a task is too broad, split it into phase-gated batches.\n- If a proposed change touches security, release, credentials or production connectors, require explicit human approval.\n"
OUTPUT_SCHEMA = {'$schema': 'https://json-schema.org/draft/2020-12/schema', 'title': 'Copiloto Angular 18 Output Contract', 'type': 'object', 'additionalProperties': False, 'required': ['copilot_id', 'decision', 'phase', 'expected_outputs', 'evidence', 'actions', 'validation', 'risks', 'handoff', 'implementation'], 'properties': {'copilot_id': {'const': 'angular_18'}, 'decision': {'type': 'string'}, 'confidence': {'type': 'integer', 'minimum': 0, 'maximum': 100}, 'phase': {'enum': ['design', 'build', 'test']}, 'expected_outputs': {'type': 'array', 'minItems': 1, 'items': {'enum': ['frontend_patch_plan', 'component_test_plan']}}, 'evidence': {'type': 'array', 'items': {'type': 'object', 'required': ['kind', 'ref', 'summary'], 'properties': {'kind': {'enum': ['domain_boundaries', 'contracts', 'handoff_clarity', 'validation', 'implementation_plan', 'stack_rules', 'affected_files']}, 'ref': {'type': 'string'}, 'summary': {'type': 'string'}}, 'additionalProperties': False}, 'minItems': 7, 'allOf': [{'contains': {'type': 'object', 'required': ['kind'], 'properties': {'kind': {'const': 'domain_boundaries'}}}}, {'contains': {'type': 'object', 'required': ['kind'], 'properties': {'kind': {'const': 'contracts'}}}}, {'contains': {'type': 'object', 'required': ['kind'], 'properties': {'kind': {'const': 'handoff_clarity'}}}}, {'contains': {'type': 'object', 'required': ['kind'], 'properties': {'kind': {'const': 'validation'}}}}, {'contains': {'type': 'object', 'required': ['kind'], 'properties': {'kind': {'const': 'implementation_plan'}}}}, {'contains': {'type': 'object', 'required': ['kind'], 'properties': {'kind': {'const': 'stack_rules'}}}}, {'contains': {'type': 'object', 'required': ['kind'], 'properties': {'kind': {'const': 'affected_files'}}}}, {'contains': {'type': 'object', 'required': ['kind'], 'properties': {'kind': {'const': 'validation'}}}}]}, 'actions': {'type': 'array', 'items': {'type': 'object', 'required': ['owner', 'action', 'scope'], 'properties': {'owner': {'type': 'string'}, 'action': {'type': 'string'}, 'scope': {'type': 'string'}}, 'additionalProperties': False}}, 'validation': {'type': 'array', 'items': {'type': 'string'}}, 'risks': {'type': 'array', 'items': {'type': 'string'}}, 'handoff': {'type': 'object', 'required': ['next_owner', 'next_runtime', 'next_action', 'excluded_scope', 'dependency_direction', 'evidence_pack', 'validation_command', 'stop_condition'], 'additionalProperties': False, 'properties': {'next_owner': {'type': 'string', 'minLength': 1}, 'next_runtime': {'enum': ['codex', 'claude', 'github-copilot', 'langchain']}, 'next_action': {'type': 'string', 'minLength': 1}, 'excluded_scope': {'type': 'array', 'minItems': 1, 'items': {'type': 'string', 'minLength': 1}}, 'dependency_direction': {'type': 'string', 'minLength': 1}, 'evidence_pack': {'type': 'array', 'minItems': 1, 'items': {'type': 'string', 'minLength': 1}}, 'validation_command': {'type': 'string', 'minLength': 1}, 'stop_condition': {'type': 'string', 'minLength': 1}}}, 'implementation': {'type': 'object', 'required': ['target_stack', 'affected_files', 'plan_steps', 'stack_rules_checked', 'validation_commands', 'rollback_plan', 'out_of_scope', 'evidence_pack'], 'additionalProperties': False, 'properties': {'target_stack': {'type': 'string', 'minLength': 1}, 'affected_files': {'type': 'array', 'minItems': 1, 'items': {'type': 'string', 'minLength': 1}}, 'plan_steps': {'type': 'array', 'minItems': 1, 'items': {'type': 'string', 'minLength': 1}}, 'stack_rules_checked': {'type': 'array', 'minItems': 1, 'items': {'type': 'string', 'minLength': 1}}, 'validation_commands': {'type': 'array', 'minItems': 1, 'items': {'type': 'string', 'minLength': 1}}, 'rollback_plan': {'type': 'string', 'minLength': 1}, 'out_of_scope': {'type': 'array', 'minItems': 1, 'items': {'type': 'string', 'minLength': 1}}, 'evidence_pack': {'type': 'array', 'minItems': 1, 'items': {'type': 'string', 'minLength': 1}}}}, 'cloud_migration': {'type': 'object'}}}
SDLC_PLAYBOOK = [{"exitEvidence": "design artifact plus one validation signal for Copiloto Angular 18", "goal": "Define contracts, modules, UX/API boundaries, data shape and acceptance criteria.", "phase": "design", "pythonCheck": "contract schema check, acceptance criteria completeness"}, {"exitEvidence": "build artifact plus one validation signal for Copiloto Angular 18", "goal": "Create scoped implementation plans or patches with affected files and rollback notes.", "phase": "build", "pythonCheck": "affected-file diff summary, lint/test command discovery"}, {"exitEvidence": "test artifact plus one validation signal for Copiloto Angular 18", "goal": "Turn requirements and code risks into unit, integration, negative and regression tests.", "phase": "test", "pythonCheck": "test matrix expansion, pairwise/negative case generation"}]
QUALITY_RUBRIC = [{"criterion": "Evidence first", "failSignal": "Advice appears before evidence or invents repository state.", "passSignal": "Claims cite files, logs, catalog entries, connector outputs or explicit user constraints."}, {"criterion": "Python first", "failSignal": "LLM is asked to count, route, validate keys or scan secrets.", "passSignal": "Deterministic checks are delegated to scripts or structured validation."}, {"criterion": "Output contract", "failSignal": "Returns generic consultancy text with no artifact.", "passSignal": "Produces one of: frontend_patch_plan, component_test_plan."}, {"criterion": "Scope control", "failSignal": "Expands beyond copilot mission without handoff.", "passSignal": "Names affected phases, files, connectors and owners."}, {"criterion": "Primary gate", "failSignal": "Moves forward without the primary quality gate.", "passSignal": "No patch plan is valid until affected files, tests, rollback path and acceptance evidence are named."}]
ARCHITECTURE_DECISION_AUDIT = None
DESIGN_BOUNDARY_AUDIT = {"artifact": "shared/design_boundary_audit.json", "mission": "Audits domain boundaries, contracts and handoff clarity.", "ownerAgent": "factory_agent_06_design", "qualityGates": ["boundary_ownership", "contract_completeness", "handoff_readiness", "traceability_and_cost"], "requiredEvidence": ["domain_boundaries", "contracts", "handoff_clarity", "validation"], "requiredHandoffFields": ["next_owner", "next_runtime", "next_action", "excluded_scope", "dependency_direction", "evidence_pack", "validation_command", "stop_condition"], "requiredOutputFields": ["copilot_id", "decision", "evidence", "actions", "validation", "risks", "handoff"], "runtimeEquivalence": {"maxUnexplainedDrift": 0, "runtimes": ["codex", "claude", "github-copilot", "langchain"], "sourceOfTruth": "dist/copilots/angular_18/shared/design_boundary_audit.json"}, "version": "domain-boundary-handoff-audit-1.0"}
BUILD_IMPLEMENTATION_AUDIT = {"artifact": "shared/implementation_plan_audit.json", "mission": "Audits implementation plans and stack-specific rules.", "ownerAgent": "factory_agent_07_build", "qualityGates": ["scoped_implementation_plan", "stack_rule_alignment", "test_and_rollback_readiness", "traceability_and_cost"], "requiredEvidence": ["implementation_plan", "stack_rules", "affected_files", "validation"], "requiredImplementationFields": ["target_stack", "affected_files", "plan_steps", "stack_rules_checked", "validation_commands", "rollback_plan", "out_of_scope", "evidence_pack"], "requiredOutputFields": ["copilot_id", "decision", "evidence", "actions", "validation", "risks", "implementation"], "runtimeEquivalence": {"maxUnexplainedDrift": 0, "runtimes": ["codex", "claude", "github-copilot", "langchain"], "sourceOfTruth": "dist/copilots/angular_18/shared/implementation_plan_audit.json"}, "version": "implementation-plan-stack-rules-audit-1.0"}
RUNTIME_CONTRACT={"version":"angular-18-runtime-contract-1.0","sourceOfTruth":"dist/copilots/angular_18/shared/spec.json","outputSchema":"dist/copilots/angular_18/shared/output_schema.json","runtimes":["codex","claude","github-copilot","langchain"],"adapterFiles":{"codex":"dist/copilots/angular_18/codex/AGENT.md","claude":"dist/copilots/angular_18/claude/AGENT.md","github-copilot":"dist/copilots/angular_18/github-copilot/copilot-agent.md","langchain":"dist/copilots/angular_18/langchain/agent.py"},"promptInvariants":["All runtimes embed systemPrompt and developerPrompt from shared spec verbatim.","Runtime-specific protocol may add adapter guidance but must not weaken shared behavior.","LLM prompts receive targeted evidence bundles, not repository dumps."],"outputInvariants":["Outputs must satisfy shared/output_schema.json.","Every output includes copilot_id, phase, expected_outputs, evidence, actions, validation, risks, handoff and implementation when required.","Evidence must cite local files, connector outputs or explicit user constraints before judgement."],"requiredTraceFields":["phase","expected_outputs"],"costTraceability":{"deterministicFirst":True,"llmEscalation":"only_for_judgement_after_python_checks","traceRequired":["sourceOfTruth","outputSchema","evidence_pack","validation_commands"]},"safety":{"secretHandling":"env_names_only_placeholders_only","connectorActivation":"declared_capability_not_credentials","writeBoundary":"current_workspace_only"},"validationCommands":["python tools/validate_copilot_factory.py","python tools/validate_prompt_quality.py","python tools/validate_runtime_equivalence.py"]}


@dataclass
class AuditResult:
    pass_: bool
    score: int
    issues: list[str]
    evidence_needed: list[str]

    def to_dict(self) -> dict[str, Any]:
        return {
            "pass": self.pass_,
            "score": self.score,
            "issues": self.issues,
            "evidence_needed": self.evidence_needed,
        }


class Angular18Agent:
    def __init__(self, profile: dict[str, Any] | None = None):
        self.profile = profile or PROFILE

    def normalize(self, text: str) -> set[str]:
        return set(re.sub(r"[^a-zA-Z0-9_ -]+", " ", text.lower()).replace("-", " ").replace("_", " ").split())

    def score(self, request: str) -> int:
        request = validate_request(request)
        words = self.normalize(request)
        tags: list[str] = []
        for key in ["family", "function"]:
            tags.extend(str(self.profile.get(key, "")).lower().replace("_", " ").split())
        for key in ["stacks", "sdlc_phases", "connectors", "outputs"]:
            tags.extend(" ".join(self.profile.get(key, [])).lower().replace("_", " ").split())
        return sum(1 for tag in tags if tag in words)

    def output_schema(self) -> dict[str, Any]:
        return OUTPUT_SCHEMA

    def runtime_contract(self) -> dict[str, Any]:
        return RUNTIME_CONTRACT

    def audit_architecture_decision(self, evidence: dict[str, Any] | None = None) -> dict[str, Any]:
        evidence = validate_evidence(evidence)
        if ARCHITECTURE_DECISION_AUDIT is None:
            return AuditResult(pass_=True, score=0, issues=[], evidence_needed=[]).to_dict()
        needed = [
            key
            for key in ARCHITECTURE_DECISION_AUDIT.get("requiredEvidence", [])
            if not evidence.get(key)
        ]
        return AuditResult(pass_=not needed, score=100 if not needed else 50, issues=[], evidence_needed=needed).to_dict()

    def audit(self, request: str, evidence: dict[str, Any] | None = None) -> dict[str, Any]:
        request = validate_request(request)
        evidence = validate_evidence(evidence)
        issues: list[str] = []
        needed: list[str] = []
        score = self.score(request)
        if score == 0:
            issues.append("Request does not match this copilot strongly enough.")
        if not evidence.get("source_refs"):
            needed.append("source_refs")
        architecture_words = {"architecture", "arquitectura", "principles", "principios", "adr", "decision", "quality", "calidad", "technical", "tecnica", "tecnico"}
        design_words = {"design", "diseno", "domain", "dominio", "boundary", "boundaries", "limites", "contract", "contracts", "contratos", "handoff", "traspaso"}
        build_words = {"build", "implementation", "implementacion", "plan", "patch", "stack", "rules", "reglas", "affected", "files", "archivos", "rollback", "validation", "tests"}
        if ARCHITECTURE_DECISION_AUDIT is not None and self.normalize(request) & architecture_words:
            architecture_audit = self.audit_architecture_decision(evidence)
            for key in architecture_audit.get("evidence_needed", []):
                if key not in needed:
                    needed.append(key)
        elif DESIGN_BOUNDARY_AUDIT is not None and self.normalize(request) & design_words:
            for key in DESIGN_BOUNDARY_AUDIT.get("requiredEvidence", []):
                if not evidence.get(key):
                    needed.append(key)
        elif BUILD_IMPLEMENTATION_AUDIT is not None and self.normalize(request) & build_words:
            for key in BUILD_IMPLEMENTATION_AUDIT.get("requiredEvidence", []):
                if not evidence.get(key):
                    needed.append(key)
        elif not evidence.get("validation"):
            needed.append("validation")
        if any(word in request.lower() for word in ["secret", "token", "production", "release"]):
            issues.append("Human approval gate required for security or release-sensitive work.")
        return AuditResult(pass_=not issues and not needed, score=score, issues=issues, evidence_needed=needed).to_dict()

    def plan(self, request: str, evidence: dict[str, Any] | None = None) -> dict[str, Any]:
        request = validate_request(request)
        audit = self.audit(request, evidence)
        plan = {
            "copilot": self.profile["id"],
            "name": self.profile["name"],
            "score": audit["score"],
            "python_first": [
                "catalog lookup",
                "semantic scoring",
                "phase audit",
                "connector declaration check",
                "output schema check",
            ],
            "llm_escalation": self.should_escalate_to_llm(request, audit),
            "connectors": self.profile["connectors"],
            "env_keys": self.profile["env_keys"],
            "outputs": self.profile["outputs"],
            "runtime_contract": RUNTIME_CONTRACT,
            "audit": audit,
        }
        if ARCHITECTURE_DECISION_AUDIT is not None:
            plan["architecture_decision_audit"] = ARCHITECTURE_DECISION_AUDIT
        if DESIGN_BOUNDARY_AUDIT is not None:
            plan["design_boundary_audit"] = DESIGN_BOUNDARY_AUDIT
        if BUILD_IMPLEMENTATION_AUDIT is not None:
            plan["implementation_plan_audit"] = BUILD_IMPLEMENTATION_AUDIT
        return plan

    def should_escalate_to_llm(self, request: str, audit: dict[str, Any]) -> bool:
        text = validate_request(request).lower()
        judgement_words = ["architecture", "tradeoff", "design", "refactor", "write", "fix", "review", "explain"]
        return audit.get("pass") is True and audit["score"] > 0 and any(word in text for word in judgement_words)

    def render_prompt(self, request: str, evidence: dict[str, Any] | None = None) -> list[dict[str, str]]:
        request = validate_request(request)
        evidence = validate_evidence(evidence)
        safe_request = redact_value(request)
        safe_evidence = redact_value(evidence)
        plan = redact_value(self.plan(request, safe_evidence))
        user_payload = {
            "request": safe_request,
            "profile": self.profile,
            "plan": plan,
            "runtime_contract": RUNTIME_CONTRACT,
            "output_schema": OUTPUT_SCHEMA,
            "sdlc_playbook": SDLC_PLAYBOOK,
            "evidence": safe_evidence,
        }
        return [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "developer", "content": DEVELOPER_PROMPT},
            {"role": "user", "content": json.dumps(user_payload, indent=2)},
        ]


def build_agent() -> Angular18Agent:
    return Angular18Agent()


if __name__ == "__main__":
    import sys
    agent = build_agent()
    request = " ".join(sys.argv[1:]) or "route and audit this request"
    print(json.dumps(agent.plan(request, {"source_refs": [], "validation": []}), indent=2))
