"""LangChain-compatible Python brain for Copiloto Firefly v6.

No hard langchain dependency; deterministic routing and audit stay in Python.
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


PROFILE = {"connectors": ["github_mcp", "sonarqube_mcp"], "env_keys": ["GITHUB_TOKEN", "SONARQUBE_TOKEN"], "family": "development", "function": "Firefly v5 evolution with stronger knowledge-base separation and QA specialization.", "id": "firefly_v6", "name": "Copiloto Firefly v6", "outputs": ["kb_partition_report", "test_plan", "quality_gate"], "sdlc_phases": ["build", "test", "devops"], "stacks": ["java", "enterprise"], "version": "copilot-factory-0.2.0"}
SYSTEM_PROMPT = "You are Copiloto Firefly v6, a production-grade SDLC copilot.\n\nMission:\nProduce stack-specific implementation plans, patches and verification loops without breaking ownership boundaries.\n\nScope:\n- Primary function: Firefly v5 evolution with stronger knowledge-base separation and QA specialization.\n- Runtime family: development\n- Stacks: java, enterprise\n- SDLC phases: build, test, devops\n- Declared connectors: github_mcp, sonarqube_mcp\n- Declared environment variable names: GITHUB_TOKEN, SONARQUBE_TOKEN\n\nNon-negotiable behavior:\n1. Start from evidence. If a repository, issue, PR, build log, SonarQube issue or catalog is available, inspect that before giving guidance.\n2. Python is the deterministic brain. Use Python tools for routing, catalog checks, schema checks, prompt checks, matrix generation and repetitive audits. Use an LLM only for judgement-heavy synthesis.\n3. Do not store secrets, invent connector access, fake CI results or pretend to have inspected files that were not inspected.\n4. Keep work scoped to the selected copilot mission. If another copilot owns the problem, hand off with an evidence pack instead of expanding silently.\n5. Every recommendation must include a next action, owner, evidence source and validation method.\n6. Prefer product-grade outputs over chatty advice: scorecards, ADR reviews, test matrices, patch plans, routing decisions, remediation backlogs or runbooks.\n\nStack rules:\n- Inspect build files before proposing framework changes: pom.xml, build.gradle, settings.gradle and CI workflows.\n- Respect package boundaries, dependency direction, transaction scope and existing test style.\n- Prefer small refactors with characterization tests before broad modernization.\n- Apply repository evidence before changing enterprise artifacts.\n\nMain risk to prevent:\nFast code that ignores architecture, test contracts, CI health or source-of-truth constraints.\n\nPrimary quality gate:\nNo patch plan is valid until affected files, tests, rollback path and acceptance evidence are named.\n"
DEVELOPER_PROMPT = "Developer operating instructions for Copiloto Firefly v6:\n\nExecution order:\n1. Intake: restate the requested outcome in one precise sentence.\n2. Route: confirm why this copilot is selected and name any secondary copilots that should be consulted.\n3. Evidence: collect the smallest useful set of files, logs, catalog entries or connector outputs.\n4. Deterministic pass: use Python or structured checks for anything countable or schema-like.\n5. Judgement pass: use the LLM only to interpret trade-offs, synthesize risks or design non-trivial patches.\n6. Output: return the expected artifact in the declared schema, then a short human summary.\n7. Verification: include exact commands, checks or acceptance criteria.\n8. Handoff: if blocked, provide the evidence pack and stop condition.\n\nExpected outputs:\n- kb_partition_report: must be concrete, evidence-backed and machine-checkable when possible.\n- test_plan: must be concrete, evidence-backed and machine-checkable when possible.\n- quality_gate: must be concrete, evidence-backed and machine-checkable when possible.\n\nPhase instructions:\n- build: Create scoped implementation plans or patches with affected files and rollback notes.\n- test: Turn requirements and code risks into unit, integration, negative and regression tests.\n- devops: Inspect pipelines, logs, caches, environments, build reproducibility and release safety.\n\nConnector discipline:\n- Connector declarations are not credentials. They are capability contracts.\n- Required connectors for this copilot: github_mcp, sonarqube_mcp\n- Environment variable names only: GITHUB_TOKEN, SONARQUBE_TOKEN\n- If a connector is unavailable, produce an offline audit using local files and mark connector evidence as pending.\n\nCost discipline:\n- Python handles discovery, scoring, diff summaries, schema checks and regression matrices.\n- Codex or Claude handles only the narrow judgement slice that Python cannot decide.\n- Never send an entire repository to an LLM when a file list, symbol graph or targeted excerpt is enough.\n\nFailure discipline:\n- If evidence contradicts the user request, state the contradiction plainly.\n- If a task is too broad, split it into phase-gated batches.\n- If a proposed change touches security, release, credentials or production connectors, require explicit human approval.\n"
OUTPUT_SCHEMA = {"$schema":"https://json-schema.org/draft/2020-12/schema","type":"object","required":["copilot_id","decision","evidence","actions","validation","risks","implementation","kb_partition"],"properties":{"copilot_id":{"const":"firefly_v6"},"decision":{"type":"string"},"evidence":{"type":"array","minItems":8,"items":{"type":"object","required":["kind","ref","summary"],"properties":{"kind":{"enum":["implementation_plan","stack_rules","affected_files","validation","kb_partition_map","source_of_truth_registry","context_window_budget","runtime_trace"]},"ref":{"type":"string"},"summary":{"type":"string"}},"additionalProperties":False},"allOf":[{"contains":{"properties":{"kind":{"const":"implementation_plan"}}}},{"contains":{"properties":{"kind":{"const":"stack_rules"}}}},{"contains":{"properties":{"kind":{"const":"affected_files"}}}},{"contains":{"properties":{"kind":{"const":"validation"}}}},{"contains":{"properties":{"kind":{"const":"kb_partition_map"}}}},{"contains":{"properties":{"kind":{"const":"source_of_truth_registry"}}}},{"contains":{"properties":{"kind":{"const":"context_window_budget"}}}},{"contains":{"properties":{"kind":{"const":"runtime_trace"}}}}]},"actions":{"type":"array"},"validation":{"type":"array"},"risks":{"type":"array"},"implementation":{"type":"object","required":["target_stack","affected_files","plan_steps","stack_rules_checked","validation_commands","rollback_plan","out_of_scope","evidence_pack"],"additionalProperties":False,"properties":{"target_stack":{},"affected_files":{},"plan_steps":{},"stack_rules_checked":{},"validation_commands":{},"rollback_plan":{},"out_of_scope":{},"evidence_pack":{}}},"kb_partition":{"type":"object","required":["kb_partition_map","source_of_truth_registry","context_window_budget","excluded_sources","runtime_trace","validation_commands"],"additionalProperties":False,"properties":{"kb_partition_map":{"type":"array","minItems":1},"source_of_truth_registry":{"type":"array","minItems":1},"context_window_budget":{"type":"object","required":["max_evidence_refs","max_prompt_bytes","summary_first","redaction_required","overflow_action"],"additionalProperties":False,"properties":{"max_evidence_refs":{"maximum":12},"max_prompt_bytes":{"maximum":12000},"summary_first":{"const":True},"redaction_required":{"const":True},"overflow_action":{"const":"emit_gap_register_before_llm_escalation"}}},"excluded_sources":{"type":"array"},"runtime_trace":{"type":"object","required":["source_of_truth","runtime_adapters","runtimes"],"additionalProperties":False,"properties":{"source_of_truth":{"const":"dist/copilots/firefly_v6/shared/spec.json"},"runtime_adapters":{"type":"object"},"runtimes":{"type":"array","minItems":4}}},"validation_commands":{"type":"array"}}}}}
SDLC_PLAYBOOK = [{"exitEvidence": "build artifact plus one validation signal for Copiloto Firefly v6", "goal": "Create scoped implementation plans or patches with affected files and rollback notes.", "phase": "build", "pythonCheck": "affected-file diff summary, lint/test command discovery"}, {"exitEvidence": "test artifact plus one validation signal for Copiloto Firefly v6", "goal": "Turn requirements and code risks into unit, integration, negative and regression tests.", "phase": "test", "pythonCheck": "test matrix expansion, pairwise/negative case generation"}, {"exitEvidence": "devops artifact plus one validation signal for Copiloto Firefly v6", "goal": "Inspect pipelines, logs, caches, environments, build reproducibility and release safety.", "phase": "devops", "pythonCheck": "workflow YAML parse, failed job log summarization"}]
QUALITY_RUBRIC = [{"criterion": "Evidence first", "failSignal": "Advice appears before evidence or invents repository state.", "passSignal": "Claims cite files, logs, catalog entries, connector outputs or explicit user constraints."}, {"criterion": "Python first", "failSignal": "LLM is asked to count, route, validate keys or scan secrets.", "passSignal": "Deterministic checks are delegated to scripts or structured validation."}, {"criterion": "Output contract", "failSignal": "Returns generic consultancy text with no artifact.", "passSignal": "Produces one of: kb_partition_report, test_plan, quality_gate."}, {"criterion": "Scope control", "failSignal": "Expands beyond copilot mission without handoff.", "passSignal": "Names affected phases, files, connectors and owners."}, {"criterion": "Primary gate", "failSignal": "Moves forward without the primary quality gate.", "passSignal": "No patch plan is valid until affected files, tests, rollback path and acceptance evidence are named."}]
RUNTIME_EQUIVALENCE = {"sourceOfTruth": "dist/copilots/firefly_v6/shared/spec.json", "outputSchema": "dist/copilots/firefly_v6/shared/output_schema.json", "runtimes": ["codex", "claude", "github-copilot", "langchain"], "maxUnexplainedDrift": 0}
ARCHITECTURE_DECISION_AUDIT = None
DESIGN_BOUNDARY_AUDIT = None
BUILD_IMPLEMENTATION_AUDIT = {"artifact": "shared/implementation_plan_audit.json", "mission": "Audits implementation plans and stack-specific rules.", "ownerAgent": "factory_agent_07_build", "qualityGates": ["scoped_implementation_plan", "stack_rule_alignment", "test_and_rollback_readiness", "traceability_and_cost"], "requiredEvidence": ["implementation_plan", "stack_rules", "affected_files", "validation"], "requiredImplementationFields": ["target_stack", "affected_files", "plan_steps", "stack_rules_checked", "validation_commands", "rollback_plan", "out_of_scope", "evidence_pack"], "requiredOutputFields": ["copilot_id", "decision", "evidence", "actions", "validation", "risks", "implementation"], "runtimeEquivalence": {"maxUnexplainedDrift": 0, "runtimes": ["codex", "claude", "github-copilot", "langchain"], "sourceOfTruth": "dist/copilots/firefly_v6/shared/implementation_plan_audit.json"}, "version": "implementation-plan-stack-rules-audit-1.0"}
KB_CONTEXT_WINDOW_AUDIT = {"artifact": "shared/kb_context_window_audit.json", "mission": "Audits KB separation, source-of-truth rules and context windows.", "qualityGates": ["kb_separation", "canonical_source_refs", "context_budget", "runtime_equivalence"], "requiredEvidence": ["kb_partition_map", "source_of_truth_registry", "context_window_budget", "runtime_trace"], "requiredKbPartitionFields": ["kb_partition_map", "source_of_truth_registry", "context_window_budget", "excluded_sources", "runtime_trace", "validation_commands"], "sourceOfTruth": "dist/copilots/firefly_v6/shared/kb_context_window_audit.json"}


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


class FireflyV6Agent:
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

    def audit_kb_context_window(self, evidence: dict[str, Any] | None = None) -> dict[str, Any]:
        evidence = validate_evidence(evidence)
        needed = [
            key
            for key in KB_CONTEXT_WINDOW_AUDIT.get("requiredEvidence", [])
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
        kb_words = {"kb", "knowledge", "source", "truth", "context", "window", "windows", "separation", "separacion"}
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
        elif self.normalize(request) & kb_words:
            kb_audit = self.audit_kb_context_window(evidence)
            for key in kb_audit.get("evidence_needed", []):
                if key not in needed:
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
            "runtime_equivalence": RUNTIME_EQUIVALENCE,
            "audit": audit,
        }
        if ARCHITECTURE_DECISION_AUDIT is not None:
            plan["architecture_decision_audit"] = ARCHITECTURE_DECISION_AUDIT
        if DESIGN_BOUNDARY_AUDIT is not None:
            plan["design_boundary_audit"] = DESIGN_BOUNDARY_AUDIT
        if BUILD_IMPLEMENTATION_AUDIT is not None:
            plan["implementation_plan_audit"] = BUILD_IMPLEMENTATION_AUDIT
        plan["kb_context_window_audit"] = KB_CONTEXT_WINDOW_AUDIT
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


def build_agent() -> FireflyV6Agent:
    return FireflyV6Agent()


if __name__ == "__main__":
    import sys
    agent = build_agent()
    request = " ".join(sys.argv[1:]) or "route and audit this request"
    print(json.dumps(agent.plan(request, {"source_refs": [], "validation": []}), indent=2))




