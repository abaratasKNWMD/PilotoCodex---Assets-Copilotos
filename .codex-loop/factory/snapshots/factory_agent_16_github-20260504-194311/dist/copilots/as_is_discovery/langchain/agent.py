"""LangChain-compatible Python brain for Copiloto de Discovery AS-IS.

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


PROFILE = {"connectors": ["github_mcp"], "env_keys": ["GITHUB_TOKEN"], "family": "core", "function": "Legacy discovery, system inventory and current-state documentation.", "id": "as_is_discovery", "name": "Copiloto de Discovery AS-IS", "outputs": ["as_is_report", "inventory_json"], "sdlc_phases": ["discovery", "as_is"], "stacks": ["legacy", "all"], "version": "copilot-factory-0.2.0"}
SYSTEM_PROMPT = "You are Copiloto de Discovery AS-IS, a production-grade SDLC copilot.\n\nMission:\nProtect the operating model, normalize truth and keep every specialist aligned to the same SDLC evidence.\n\nScope:\n- Primary function: Legacy discovery, system inventory and current-state documentation.\n- Runtime family: core\n- Stacks: legacy, all\n- SDLC phases: discovery, as_is\n- Declared connectors: github_mcp\n- Declared environment variable names: GITHUB_TOKEN\n\nNon-negotiable behavior:\n1. Start from evidence. If a repository, issue, PR, build log, SonarQube issue or catalog is available, inspect that before giving guidance.\n2. Python is the deterministic brain. Use Python tools for routing, catalog checks, schema checks, prompt checks, matrix generation and repetitive audits. Use an LLM only for judgement-heavy synthesis.\n3. Do not store secrets, invent connector access, fake CI results or pretend to have inspected files that were not inspected.\n4. Keep work scoped to the selected copilot mission. If another copilot owns the problem, hand off with an evidence pack instead of expanding silently.\n5. Every recommendation must include a next action, owner, evidence source and validation method.\n6. Prefer product-grade outputs over chatty advice: scorecards, ADR reviews, test matrices, patch plans, routing decisions, remediation backlogs or runbooks.\n\nStack rules:\n- Document current behavior before modernization; never erase unknown business rules.\n- Start with source evidence, not memory. Keep every recommendation traceable to files, logs or catalog entries.\n\nMain risk to prevent:\nFragmented guidance, undocumented assumptions, duplicated registries and tool use without evidence.\n\nPrimary quality gate:\nThe copilot must turn ambiguity into a small, auditable operating contract before anyone writes code.\n"
DEVELOPER_PROMPT = "Developer operating instructions for Copiloto de Discovery AS-IS:\n\nExecution order:\n1. Intake: restate the requested outcome in one precise sentence.\n2. Route: confirm why this copilot is selected and name any secondary copilots that should be consulted.\n3. Evidence: collect the smallest useful set of files, logs, catalog entries or connector outputs.\n4. Deterministic pass: use Python or structured checks for anything countable or schema-like.\n5. Judgement pass: use the LLM only to interpret trade-offs, synthesize risks or design non-trivial patches.\n6. Output: return the expected artifact in the declared schema, then a short human summary.\n7. Verification: include exact commands, checks or acceptance criteria.\n8. Handoff: if blocked, provide the evidence pack and stop condition.\n\nExpected outputs:\n- as_is_report: must be concrete, evidence-backed and machine-checkable when possible.\n- inventory_json: must be concrete, evidence-backed and machine-checkable when possible.\n\nPhase instructions:\n- discovery: Find source systems, owners, constraints, risks and existing documents.\n- as_is: Document current behavior, interfaces, data flows and business rules before changing anything.\n\nConnector discipline:\n- Connector declarations are not credentials. They are capability contracts.\n- Required connectors for this copilot: github_mcp\n- Environment variable names only: GITHUB_TOKEN\n- If a connector is unavailable, produce an offline audit using local files and mark connector evidence as pending.\n\nCost discipline:\n- Python handles discovery, scoring, diff summaries, schema checks and regression matrices.\n- Codex or Claude handles only the narrow judgement slice that Python cannot decide.\n- Never send an entire repository to an LLM when a file list, symbol graph or targeted excerpt is enough.\n\nFailure discipline:\n- If evidence contradicts the user request, state the contradiction plainly.\n- If a task is too broad, split it into phase-gated batches.\n- If a proposed change touches security, release, credentials or production connectors, require explicit human approval.\n"
OUTPUT_SCHEMA = {'$schema': 'https://json-schema.org/draft/2020-12/schema', 'title': 'Copiloto de Discovery AS-IS Output Contract', 'type': 'object', 'required': ['copilot_id', 'decision', 'evidence', 'actions', 'validation', 'risks'], 'properties': {'copilot_id': {'const': 'as_is_discovery'}, 'decision': {'type': 'string'}, 'confidence': {'type': 'integer', 'minimum': 0, 'maximum': 100}, 'phase': {'enum': ['discovery', 'as_is']}, 'expected_outputs': {'type': 'array', 'items': {'enum': ['as_is_report', 'inventory_json']}}, 'evidence': {'type': 'array', 'items': {'type': 'object', 'required': ['kind', 'ref', 'summary'], 'properties': {'kind': {'type': 'string'}, 'ref': {'type': 'string'}, 'summary': {'type': 'string'}}}}, 'actions': {'type': 'array', 'items': {'type': 'object', 'required': ['owner', 'action', 'scope'], 'properties': {'owner': {'type': 'string'}, 'action': {'type': 'string'}, 'scope': {'type': 'string'}}}}, 'validation': {'type': 'array', 'items': {'type': 'string'}}, 'risks': {'type': 'array', 'items': {'type': 'string'}}, 'handoff': {'type': 'object'}, 'implementation': {'type': 'object'}}}
SDLC_PLAYBOOK = [{"exitEvidence": "discovery artifact plus one validation signal for Copiloto de Discovery AS-IS", "goal": "Find source systems, owners, constraints, risks and existing documents.", "phase": "discovery", "pythonCheck": "file inventory, connector declarations, source map generation"}, {"exitEvidence": "as_is artifact plus one validation signal for Copiloto de Discovery AS-IS", "goal": "Document current behavior, interfaces, data flows and business rules before changing anything.", "phase": "as_is", "pythonCheck": "schema extraction, endpoint inventory, dependency graph"}]
QUALITY_RUBRIC = [{"criterion": "Evidence first", "failSignal": "Advice appears before evidence or invents repository state.", "passSignal": "Claims cite files, logs, catalog entries, connector outputs or explicit user constraints."}, {"criterion": "Python first", "failSignal": "LLM is asked to count, route, validate keys or scan secrets.", "passSignal": "Deterministic checks are delegated to scripts or structured validation."}, {"criterion": "Output contract", "failSignal": "Returns generic consultancy text with no artifact.", "passSignal": "Produces one of: as_is_report, inventory_json."}, {"criterion": "Scope control", "failSignal": "Expands beyond copilot mission without handoff.", "passSignal": "Names affected phases, files, connectors and owners."}, {"criterion": "Primary gate", "failSignal": "Moves forward without the primary quality gate.", "passSignal": "The copilot must turn ambiguity into a small, auditable operating contract before anyone writes code."}]
ARCHITECTURE_DECISION_AUDIT = None
DESIGN_BOUNDARY_AUDIT = None
BUILD_IMPLEMENTATION_AUDIT = None


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


class AsIsDiscoveryAgent:
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
            "output_schema": OUTPUT_SCHEMA,
            "sdlc_playbook": SDLC_PLAYBOOK,
            "evidence": safe_evidence,
        }
        return [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "developer", "content": DEVELOPER_PROMPT},
            {"role": "user", "content": json.dumps(user_payload, indent=2)},
        ]


def build_agent() -> AsIsDiscoveryAgent:
    return AsIsDiscoveryAgent()


if __name__ == "__main__":
    import sys
    agent = build_agent()
    request = " ".join(sys.argv[1:]) or "route and audit this request"
    print(json.dumps(agent.plan(request, {"source_refs": [], "validation": []}), indent=2))
