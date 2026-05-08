"""LangChain-compatible Python brain for Copiloto Journey to Cloud."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any

sys.path.append(str(Path(__file__).resolve().parents[2]))
from _runtime_safety import redact_value, validate_evidence, validate_request


PROFILE = {"connectors": ["github_mcp"], "env_keys": ["GITHUB_TOKEN"], "family": "cloud", "function": "Cloud migration, legacy rebuild strategy and target architecture planning.", "id": "journey_to_cloud", "name": "Copiloto Journey to Cloud", "outputs": ["migration_plan", "cloud_readiness_report"], "sdlc_phases": ["architecture", "cloud", "release"], "stacks": ["cloud", "modernization"], "version": "copilot-factory-0.2.0"}
SYSTEM_PROMPT = "You are Copiloto Journey to Cloud, a production-grade SDLC copilot.\n\nMission:\nMove legacy systems to safer cloud increments with explicit target architecture and risk burn-down.\n\nScope:\n- Primary function: Cloud migration, legacy rebuild strategy and target architecture planning.\n- Runtime family: cloud\n- Stacks: cloud, modernization\n- SDLC phases: architecture, cloud, release\n- Declared connectors: github_mcp\n- Declared environment variable names: GITHUB_TOKEN\n\nNon-negotiable behavior:\n1. Start from evidence. If a repository, issue, PR, build log, SonarQube issue or catalog is available, inspect that before giving guidance.\n2. Python is the deterministic brain. Use Python tools for routing, catalog checks, schema checks, prompt checks, matrix generation and repetitive audits. Use an LLM only for judgement-heavy synthesis.\n3. Do not store secrets, invent connector access, fake CI results or pretend to have inspected files that were not inspected.\n4. Keep work scoped to the selected copilot mission. If another copilot owns the problem, hand off with an evidence pack instead of expanding silently.\n5. Every recommendation must include a next action, owner, evidence source and validation method.\n6. Prefer product-grade outputs over chatty advice: scorecards, ADR reviews, test matrices, patch plans, routing decisions, remediation backlogs or runbooks.\n\nStack rules:\n- Separate application, data, identity, network, deployment and observability decisions.\n- Apply repository evidence before changing modernization artifacts.\n\nMain risk to prevent:\nBig-bang migration, hidden coupling, unpriced platform assumptions and missing operational ownership.\n\nPrimary quality gate:\nEvery migration step must preserve a working system and name data, network, security and observability impacts.\n"
DEVELOPER_PROMPT = "Developer operating instructions for Copiloto Journey to Cloud:\n\nExecution order:\n1. Intake: restate the requested outcome in one precise sentence.\n2. Route: confirm why this copilot is selected and name any secondary copilots that should be consulted.\n3. Evidence: collect the smallest useful set of files, logs, catalog entries or connector outputs.\n4. Deterministic pass: use Python or structured checks for anything countable or schema-like.\n5. Judgement pass: use the LLM only to interpret trade-offs, synthesize risks or design non-trivial patches.\n6. Output: return the expected artifact in the declared schema, then a short human summary.\n7. Verification: include exact commands, checks or acceptance criteria.\n8. Handoff: if blocked, provide the evidence pack and stop condition.\n\nExpected outputs:\n- migration_plan: must be concrete, evidence-backed and machine-checkable when possible.\n- cloud_readiness_report: must be concrete, evidence-backed and machine-checkable when possible.\n\nPhase instructions:\n- architecture: Evaluate decisions, boundaries, trade-offs, ADRs, risks and target principles.\n- cloud: Plan migration increments, platform target, data movement, networking and operations.\n- release: Prepare versioning, changelog, risk signoff, deployment and rollback evidence.\n\nConnector discipline:\n- Connector declarations are not credentials. They are capability contracts.\n- Required connectors for this copilot: github_mcp\n- Environment variable names only: GITHUB_TOKEN\n- If a connector is unavailable, produce an offline audit using local files and mark connector evidence as pending.\n\nCost discipline:\n- Python handles discovery, scoring, diff summaries, schema checks and regression matrices.\n- Codex or Claude handles only the narrow judgement slice that Python cannot decide.\n- Never send an entire repository to an LLM when a file list, symbol graph or targeted excerpt is enough.\n\nFailure discipline:\n- If evidence contradicts the user request, state the contradiction plainly.\n- If a task is too broad, split it into phase-gated batches.\n- If a proposed change touches security, release, credentials or production connectors, require explicit human approval.\n"
OUTPUT_SCHEMA = {'$schema': 'https://json-schema.org/draft/2020-12/schema', 'title': 'Copiloto Journey to Cloud Output Contract', 'type': 'object', 'required': ['copilot_id', 'decision', 'evidence', 'actions', 'validation', 'risks', 'cloud_migration'], 'properties': {'copilot_id': {'const': 'journey_to_cloud'}, 'decision': {'type': 'string'}, 'confidence': {'type': 'integer', 'minimum': 0, 'maximum': 100}, 'phase': {'enum': ['architecture', 'cloud', 'release']}, 'expected_outputs': {'type': 'array', 'items': {'enum': ['migration_plan', 'cloud_readiness_report']}}, 'evidence': {'type': 'array', 'items': {'type': 'object', 'required': ['kind', 'ref', 'summary'], 'properties': {'kind': {'enum': ['migration_inventory', 'target_platform', 'modernization_increments', 'validation']}, 'ref': {'type': 'string'}, 'summary': {'type': 'string'}}, 'additionalProperties': False}, 'minItems': 4, 'allOf': [{'contains': {'type': 'object', 'required': ['kind'], 'properties': {'kind': {'const': 'migration_inventory'}}}}, {'contains': {'type': 'object', 'required': ['kind'], 'properties': {'kind': {'const': 'target_platform'}}}}, {'contains': {'type': 'object', 'required': ['kind'], 'properties': {'kind': {'const': 'modernization_increments'}}}}, {'contains': {'type': 'object', 'required': ['kind'], 'properties': {'kind': {'const': 'validation'}}}}]}, 'actions': {'type': 'array', 'items': {'type': 'object', 'required': ['owner', 'action', 'scope'], 'properties': {'owner': {'type': 'string'}, 'action': {'type': 'string'}, 'scope': {'type': 'string'}}, 'additionalProperties': False}}, 'validation': {'type': 'array', 'items': {'type': 'string'}}, 'risks': {'type': 'array', 'items': {'type': 'string'}}, 'handoff': {'type': 'object'}, 'implementation': {'type': 'object'}, 'cloud_migration': {'type': 'object', 'required': ['current_state_refs', 'target_platform', 'migration_increments', 'modernization_actions', 'data_network_security_impacts', 'rollback_and_parallel_run', 'validation_commands', 'evidence_pack', 'out_of_scope'], 'additionalProperties': False, 'properties': {'current_state_refs': {'type': 'array'}, 'target_platform': {'type': 'object'}, 'migration_increments': {'type': 'array', 'minItems': 3, 'items': {'type': 'object', 'required': ['increment_id', 'source_evidence', 'target_capability', 'modernization_action', 'validation_command', 'rollback_path'], 'additionalProperties': False}}, 'modernization_actions': {'type': 'array'}, 'data_network_security_impacts': {'type': 'array'}, 'rollback_and_parallel_run': {'type': 'string'}, 'validation_commands': {'type': 'array'}, 'evidence_pack': {'type': 'array'}, 'out_of_scope': {'type': 'array'}}}}, 'additionalProperties': False}
SDLC_PLAYBOOK = [{"exitEvidence": "architecture artifact plus one validation signal for Copiloto Journey to Cloud", "goal": "Evaluate decisions, boundaries, trade-offs, ADRs, risks and target principles.", "phase": "architecture", "pythonCheck": "ADR presence, dependency direction, module boundary matrix"}, {"exitEvidence": "cloud artifact plus one validation signal for Copiloto Journey to Cloud", "goal": "Plan migration increments, platform target, data movement, networking and operations.", "phase": "cloud", "pythonCheck": "migration inventory, platform capability matrix"}, {"exitEvidence": "release artifact plus one validation signal for Copiloto Journey to Cloud", "goal": "Prepare versioning, changelog, risk signoff, deployment and rollback evidence.", "phase": "release", "pythonCheck": "manifest, changelog and version compatibility check"}]
QUALITY_RUBRIC = [{"criterion": "Evidence first", "failSignal": "Advice appears before evidence or invents repository state.", "passSignal": "Claims cite files, logs, catalog entries, connector outputs or explicit user constraints."}, {"criterion": "Python first", "failSignal": "LLM is asked to count, route, validate keys or scan secrets.", "passSignal": "Deterministic checks are delegated to scripts or structured validation."}, {"criterion": "Output contract", "failSignal": "Returns generic consultancy text with no artifact.", "passSignal": "Produces one of: migration_plan, cloud_readiness_report."}, {"criterion": "Scope control", "failSignal": "Expands beyond copilot mission without handoff.", "passSignal": "Names affected phases, files, connectors and owners."}, {"criterion": "Primary gate", "failSignal": "Moves forward without the primary quality gate.", "passSignal": "Every migration step must preserve a working system and name data, network, security and observability impacts."}]
CLOUD_MIGRATION_AUDIT = {"artifact": "shared/cloud_migration_audit.json", "requiredEvidence": ["migration_inventory", "target_platform", "modernization_increments", "validation"]}
RUNTIME_EQUIVALENCE_CONTRACT = {"version": "journey-to-cloud-runtime-equivalence-1.0", "sourceOfTruth": "shared/spec.json", "schemaSource": "shared/output_schema.json", "runtimes": ["codex", "claude", "github-copilot", "langchain"], "assertions": ["same_prompts", "same_schema", "same_evidence", "python_first", "max_drift_zero"], "validationCommands": ["python tools/validate_copilot_factory.py", "python tools/validate_prompt_quality.py", "python tools/validate_runtime_equivalence.py"]}
ARCHITECTURE_DECISION_AUDIT = None
DESIGN_BOUNDARY_AUDIT = None
BUILD_IMPLEMENTATION_AUDIT = None


class AuditResult:
    def __init__(self, pass_: bool, score: int, issues: list[str], evidence_needed: list[str]):
        self.pass_ = pass_
        self.score = score
        self.issues = issues
        self.evidence_needed = evidence_needed

    def to_dict(self) -> dict[str, Any]:
        return {
            "pass": self.pass_,
            "score": self.score,
            "issues": self.issues,
            "evidence_needed": self.evidence_needed,
        }


class JourneyToCloudAgent:
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
        spec = json.loads((Path(__file__).resolve().parents[1] / "shared/spec.json").read_text(encoding="utf-8"))
        return {
            "runtime_equivalence": spec.get("runtimeEquivalenceContract", RUNTIME_EQUIVALENCE_CONTRACT),
            "cloud_migration_audit": spec.get("cloudMigrationAudit", CLOUD_MIGRATION_AUDIT),
        }

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
        request_words = self.normalize(request)
        if score == 0:
            issues.append("Request does not match this copilot strongly enough.")
        if not evidence.get("source_refs"):
            needed.append("source_refs")
        cloud_words = {"cloud", "migration", "migracion", "modernization", "modernizacion", "platform", "plataforma", "legacy", "target", "rollback", "network", "security", "observability"}
        architecture_words = {"architecture", "arquitectura", "principles", "principios", "adr", "decision", "quality", "calidad", "technical", "tecnica", "tecnico"}
        design_words = {"design", "diseno", "domain", "dominio", "boundary", "boundaries", "limites", "contract", "contracts", "contratos", "handoff", "traspaso"}
        build_words = {"build", "implementation", "implementacion", "plan", "patch", "stack", "rules", "reglas", "affected", "files", "archivos", "rollback", "validation", "tests"}
        if request_words & cloud_words:
            for key in CLOUD_MIGRATION_AUDIT["requiredEvidence"]:
                if not evidence.get(key) and key not in needed:
                    needed.append(key)
        if ARCHITECTURE_DECISION_AUDIT is not None and request_words & architecture_words:
            architecture_audit = self.audit_architecture_decision(evidence)
            for key in architecture_audit.get("evidence_needed", []):
                if key not in needed:
                    needed.append(key)
        elif DESIGN_BOUNDARY_AUDIT is not None and request_words & design_words:
            for key in DESIGN_BOUNDARY_AUDIT.get("requiredEvidence", []):
                if not evidence.get(key):
                    needed.append(key)
        elif BUILD_IMPLEMENTATION_AUDIT is not None and request_words & build_words:
            for key in BUILD_IMPLEMENTATION_AUDIT.get("requiredEvidence", []):
                if not evidence.get(key):
                    needed.append(key)
        elif not evidence.get("validation") and "validation" not in needed:
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
            "audit": audit,
            "runtime_contract": self.runtime_contract(),
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
            "output_schema": OUTPUT_SCHEMA,
            "sdlc_playbook": SDLC_PLAYBOOK,
            "evidence": safe_evidence,
        }
        return [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "developer", "content": DEVELOPER_PROMPT},
            {"role": "user", "content": json.dumps(user_payload, indent=2)},
        ]


def build_agent() -> JourneyToCloudAgent:
    return JourneyToCloudAgent()


if __name__ == "__main__":
    import sys
    agent = build_agent()
    request = " ".join(sys.argv[1:]) or "route and audit this request"
    print(json.dumps(agent.plan(request, {"source_refs": [], "validation": []}), indent=2))
