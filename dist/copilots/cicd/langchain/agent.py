from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any

sys.path.append(str(Path(__file__).resolve().parents[2]))
from _runtime_safety import redact_value, validate_evidence, validate_request


PROFILE = {"connectors": ["github_mcp"], "env_keys": ["GITHUB_TOKEN"], "family": "devops", "function": "Pipeline analysis, build troubleshooting, release automation and rollback diagnostics.", "id": "cicd", "name": "Copiloto CI/CD", "outputs": ["pipeline_triage", "workflow_patch_plan"], "sdlc_phases": ["devops", "release", "operate"], "stacks": ["github_actions", "ci_cd"], "version": "copilot-factory-0.2.0"}
SYSTEM_PROMPT = "Loaded reproducible CI/CD prompt from langchain/agent_profile.json."
DEVELOPER_PROMPT = "Loaded from langchain/agent_profile.json."
OUTPUT_SCHEMA = {'$schema': 'https://json-schema.org/draft/2020-12/schema', 'title': 'Copiloto CI/CD Output Contract', 'type': 'object', 'required': ['copilot_id', 'decision', 'evidence', 'actions', 'validation', 'risks'], 'properties': {'copilot_id': {'const': 'cicd'}, 'decision': {'type': 'string'}, 'confidence': {'type': 'integer', 'minimum': 0, 'maximum': 100}, 'phase': {'enum': ['devops', 'release', 'operate']}, 'expected_outputs': {'type': 'array', 'items': {'enum': ['pipeline_triage', 'workflow_patch_plan']}}, 'evidence': {'type': 'array', 'items': {'type': 'object', 'required': ['kind', 'ref', 'summary'], 'properties': {'kind': {'type': 'string'}, 'ref': {'type': 'string'}, 'summary': {'type': 'string'}}}}, 'actions': {'type': 'array', 'items': {'type': 'object', 'required': ['owner', 'action', 'scope'], 'properties': {'owner': {'type': 'string'}, 'action': {'type': 'string'}, 'scope': {'type': 'string'}}}}, 'validation': {'type': 'array', 'items': {'type': 'string'}}, 'risks': {'type': 'array', 'items': {'type': 'string'}}, 'handoff': {'type': 'object'}, 'implementation': {'type': 'object'}, 'cloud_migration': {'type': 'object'}}}
RUNTIME_EQUIVALENCE_CONTRACT = {"version": "cicd-runtime-contract-1.1", "sourceOfTruth": "dist/copilots/cicd/shared/spec.json", "outputSchemaRef": "dist/copilots/cicd/shared/output_schema.json", "runtimes": ["codex", "claude", "github-copilot", "langchain"], "requiredOutputFields": OUTPUT_SCHEMA["required"], "declaredOutputs": PROFILE["outputs"], "traceabilityRules": ["Every material claim cites evidence.kind, evidence.ref and evidence.summary.", "Every action names owner, action and scope.", "Every handoff includes validation or an explicit stop condition."], "costPolicy": "python_first_llm_sparse_no_repo_dump", "driftPolicy": {"maxUnexplainedDrift": 0, "schemaDrift": "blocker", "promptDrift": "blocker"}}
SDLC_PLAYBOOK = [{"exitEvidence": "devops artifact plus one validation signal for Copiloto CI/CD", "goal": "Inspect pipelines, logs, caches, environments, build reproducibility and release safety.", "phase": "devops", "pythonCheck": "workflow YAML parse, failed job log summarization"}, {"exitEvidence": "release artifact plus one validation signal for Copiloto CI/CD", "goal": "Prepare versioning, changelog, risk signoff, deployment and rollback evidence.", "phase": "release", "pythonCheck": "manifest, changelog and version compatibility check"}, {"exitEvidence": "operate artifact plus one validation signal for Copiloto CI/CD", "goal": "Define monitoring, incidents, runbooks, ownership and continuous improvement loops.", "phase": "operate", "pythonCheck": "runbook and alert coverage check"}]
QUALITY_RUBRIC = [{"criterion": "Evidence first", "failSignal": "Advice appears before evidence or invents repository state.", "passSignal": "Claims cite files, logs, catalog entries, connector outputs or explicit user constraints."}, {"criterion": "Python first", "failSignal": "LLM is asked to count, route, validate keys or scan secrets.", "passSignal": "Deterministic checks are delegated to scripts or structured validation."}, {"criterion": "Output contract", "failSignal": "Returns generic consultancy text with no artifact.", "passSignal": "Produces one of: pipeline_triage, workflow_patch_plan."}, {"criterion": "Scope control", "failSignal": "Expands beyond copilot mission without handoff.", "passSignal": "Names affected phases, files, connectors and owners."}, {"criterion": "Primary gate", "failSignal": "Moves forward without the primary quality gate.", "passSignal": "No release recommendation without logs, command history, rollback and owner impact."}]
ARCHITECTURE_DECISION_AUDIT = None
DESIGN_BOUNDARY_AUDIT = None
BUILD_IMPLEMENTATION_AUDIT = None


class AuditResult:
    def __init__(self, pass_: bool, score: int, issues: list[str], evidence_needed: list[str]) -> None:
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


class CicdAgent:
    def __init__(self, profile: dict[str, Any] | None = None):
        self.profile = profile or PROFILE
        profile_doc = self._load_profile_doc()
        self.system_prompt = str(profile_doc.get("systemPrompt") or SYSTEM_PROMPT)
        self.developer_prompt = str(profile_doc.get("developerPrompt") or DEVELOPER_PROMPT)

    def _load_profile_doc(self) -> dict[str, Any]:
        try:
            loaded = json.loads(Path(__file__).with_name("agent_profile.json").read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            return {}
        return loaded if isinstance(loaded, dict) else {}

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

    def validate_candidate_output(self, output: Any | None) -> list[str]:
        if output is None:
            return []
        if not isinstance(output, dict):
            return ["candidate_output must be object."]
        issues: list[str] = []
        missing = [key for key in OUTPUT_SCHEMA["required"] if key not in output]
        if missing:
            issues.append("candidate_output missing: " + ", ".join(missing) + ".")
        if output.get("copilot_id") != self.profile["id"]:
            issues.append("candidate_output copilot_id drift.")
        if "decision" in output and not isinstance(output.get("decision"), str):
            issues.append("candidate_output decision must be string.")
        confidence = output.get("confidence")
        if "confidence" in output and (not isinstance(confidence, int) or not 0 <= confidence <= 100):
            issues.append("candidate_output confidence must be integer between 0 and 100.")
        if "phase" in output and output.get("phase") not in self.profile["sdlc_phases"]:
            issues.append("candidate_output phase drift.")
        expected_outputs = output.get("expected_outputs", [])
        if expected_outputs and (not isinstance(expected_outputs, list) or not set(expected_outputs).issubset(set(self.profile["outputs"]))):
            issues.append("candidate_output expected_outputs drift.")
        for key, fields in {"evidence": ("kind", "ref", "summary"), "actions": ("owner", "action", "scope")}.items():
            if key not in output:
                continue
            items = output.get(key)
            if not isinstance(items, list):
                issues.append(f"candidate_output {key} must be an array.")
                continue
            for index, item in enumerate(items):
                if not isinstance(item, dict):
                    issues.append(f"candidate_output {key}[{index}] must be object.")
                    continue
                item_missing = [field for field in fields if field not in item]
                bad = [field for field in fields if field in item and not isinstance(item.get(field), str)]
                if item_missing:
                    issues.append(f"candidate_output {key}[{index}] missing: {', '.join(item_missing)}.")
                if bad:
                    issues.append(f"candidate_output {key}[{index}] non-string: {', '.join(bad)}.")
        for key in ["validation", "risks"]:
            values = output.get(key)
            if key in output and (not isinstance(values, list) or any(not isinstance(item, str) for item in values)):
                issues.append(f"candidate_output {key} must be an array of strings.")
        return issues

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
        candidate_issues = self.validate_candidate_output(evidence.get("candidate_output"))
        issues.extend(candidate_issues)
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
            "runtime_contract": RUNTIME_EQUIVALENCE_CONTRACT,
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
            {"role": "system", "content": self.system_prompt},
            {"role": "developer", "content": self.developer_prompt},
            {"role": "user", "content": json.dumps(user_payload, indent=2)},
        ]


def build_agent() -> CicdAgent:
    return CicdAgent()


if __name__ == "__main__":
    import sys
    agent = build_agent()
    request = " ".join(sys.argv[1:]) or "route and audit this request"
    print(json.dumps(agent.plan(request, {"source_refs": [], "validation": []}), indent=2))
