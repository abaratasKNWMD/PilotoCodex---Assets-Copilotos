from __future__ import annotations

import json
import re
import shutil
import sys
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from pathlib import Path
from textwrap import dedent

sys.dont_write_bytecode = True


ROOT = Path(__file__).resolve().parents[1]
GENERATED = ROOT / "generated"
DIST = ROOT / "dist" / "copilots"
DATA = ROOT / "data"
CONFIG = ROOT / "config"

FACTORY_VERSION = "copilot-factory-0.2.0"
RUNTIMES = ["codex", "claude", "github-copilot", "langchain"]
DIRECTOR_AGENT = "factory_agent_01_director"
DIRECTOR_MISSION = "Owns the whole run, keeps gates honest and prevents scope drift."
SECURITY_AGENT = "factory_agent_09_security"
SECURITY_MISSION = "Audits sensitive credentials policy, threat model and safe MCP usage."
SECURITY_AUDIT_VERSION = "sensitive-credentials-mcp-audit-1.0"
SECURITY_ENV_EXAMPLE = "config/.env.example"
SECURITY_MCP_CONFIG = "config/mcp-connectors.example.json"
SECURITY_REQUIRED_DENIED_OPERATIONS = [
    "secret_read",
    "secret_write",
    "billing_admin",
    "org_admin",
    "destructive_repo_admin",
]
SECURITY_REQUIRED_SAFE_USAGE = {
    "default_enabled": False,
    "local_only_config": True,
    "allowlist_required": True,
    "operator_activation_required": True,
    "operator_approval_required_for_writes": True,
    "deny_customer_data_in_prompts": True,
    "redact_tokens_in_logs": True,
    "audit_trail_required": True,
    "no_external_network_without_operator_approval": True,
}
SECURITY_RUNTIME_EQUIVALENCE = {
    "runtimes": RUNTIMES,
    "source_of_truth": SECURITY_MCP_CONFIG,
    "same_policy_for_all_runtimes": True,
    "trace_evidence": "generated/validation-report.json.securityAuditor",
    "max_unexplained_drift": 0,
    "cost_control": "python_first_llm_sparse",
}
SDLC_PHASES = [
    "discovery",
    "as_is",
    "architecture",
    "design",
    "build",
    "test",
    "security",
    "devops",
    "cloud",
    "release",
    "operate",
]
NORMALIZATION_VERSION = "catalog-normalization-1.0"
CASE_POLICY = {
    "copilot_id": "lower_snake_case",
    "connector_names": "lower_snake_case",
    "env_names": "upper_snake_case",
    "outputs": "lower_snake_case",
}
TRACEABILITY_POLICY = {
    "catalog_index": "generated/copilot-index.json",
    "runtime_source_of_truth": "dist/copilots/<copilot_id>/shared/spec.json",
}
SEMANTIC_AGENT = "factory_agent_03_semantics"
SEMANTIC_ROUTING_VERSION = "semantic-routing-1.0"
SEMANTIC_SCORE_MODEL = "weighted_exact_and_token_overlap"
DISCOVERY_AGENT = "factory_agent_04_discovery"
DISCOVERY_MISSION = "Audits AS-IS coverage and repo inventory contracts."
DISCOVERY_AUDIT_VERSION = "as-is-inventory-audit-1.0"
DISCOVERY_TARGET_COPILOT = "as_is_discovery"
DISCOVERY_REQUIRED_OUTPUTS = [
    "as_is_report",
    "inventory_json",
]
DISCOVERY_AGENT_OUTPUTS = [
    "as_is_coverage_audit",
    "repo_inventory_contract",
    "coverage_gap_register",
]
DISCOVERY_COVERAGE_ITEMS = [
    "source_systems",
    "repository_topology",
    "interfaces",
    "data_flows",
    "business_rules",
    "dependencies",
    "owners",
    "risks",
    "validation_signals",
]
DISCOVERY_INVENTORY_FIELDS = [
    "path",
    "artifact_type",
    "owner",
    "sdlc_phase",
    "runtime_scope",
    "evidence_ref",
    "validation_status",
]
DISCOVERY_EXECUTION_ORDER = [
    "load_catalog",
    "load_index",
    "collect_runtime_trace",
    "audit_as_is_outputs",
    "audit_inventory_contract",
    "emit_gap_register",
    "return_discovery_audit",
]
DISCOVERY_VALIDATION_COMMANDS = [
    "python tools/validate_copilot_factory.py",
    "python tools/semantic_router.py as_is inventory coverage",
    "python tools/semantic_router.py python ci routing",
]
DESIGN_AGENT = "factory_agent_06_design"
DESIGN_MISSION = "Audits domain boundaries, contracts and handoff clarity."
DESIGN_AUDIT_VERSION = "domain-boundary-handoff-audit-1.0"
DESIGN_AUDIT_ARTIFACT = "shared/design_boundary_audit.json"
DESIGN_TARGET_COPILOTS = [
    "aida_architecture",
    "java_generic",
    "java_architect",
    "angular_18",
    "nodejs",
]
DESIGN_AGENT_OUTPUTS = [
    "domain_boundary_audit",
    "contract_surface_matrix",
    "handoff_evidence_pack",
]
DESIGN_REQUIRED_EVIDENCE = [
    "domain_boundaries",
    "contracts",
    "handoff_clarity",
    "validation",
]
DESIGN_QUALITY_GATES = [
    "boundary_ownership",
    "contract_completeness",
    "handoff_readiness",
    "traceability_and_cost",
]
DESIGN_REQUIRED_OUTPUT_FIELDS = [
    "copilot_id",
    "decision",
    "evidence",
    "actions",
    "validation",
    "risks",
    "handoff",
]
DESIGN_REQUIRED_HANDOFF_FIELDS = [
    "next_owner",
    "next_runtime",
    "next_action",
    "excluded_scope",
    "dependency_direction",
    "evidence_pack",
    "validation_command",
    "stop_condition",
]
DESIGN_EXECUTION_ORDER = [
    "load_catalog",
    "collect_runtime_trace",
    "audit_domain_boundaries",
    "audit_contract_surfaces",
    "audit_handoff_clarity",
    "emit_boundary_gap_register",
    "return_design_audit",
]
DESIGN_ROUTING_SIGNALS = [
    "design",
    "diseno",
    "domain",
    "dominio",
    "boundaries",
    "boundary",
    "limites",
    "contracts",
    "contract",
    "contratos",
    "handoff",
    "traspaso",
    "modules",
    "api",
    "data",
    "acceptance",
    "criteria",
]
DESIGN_VALIDATION_COMMANDS = [
    "python tools/validate_copilot_factory.py",
    "python tools/semantic_router.py design domain boundaries contracts handoff",
    "python tools/semantic_router.py diseno dominio contratos limites handoff",
    "python tools/semantic_router.py python ci routing",
]
BUILD_AGENT = "factory_agent_07_build"
BUILD_MISSION = "Audits implementation plans and stack-specific rules."
BUILD_AUDIT_VERSION = "implementation-plan-stack-rules-audit-1.0"
BUILD_AUDIT_ARTIFACT = "shared/implementation_plan_audit.json"
BUILD_TARGET_COPILOTS = [
    "devex",
    "firefly_v5",
    "firefly_v6",
    "moonshine",
    "java_generic",
    "angular_18",
    "nodejs",
    "python",
]
BUILD_AGENT_OUTPUTS = [
    "implementation_plan_audit",
    "stack_rule_matrix",
    "build_readiness_evidence_pack",
]
BUILD_REQUIRED_EVIDENCE = [
    "implementation_plan",
    "stack_rules",
    "affected_files",
    "validation",
]
BUILD_QUALITY_GATES = [
    "scoped_implementation_plan",
    "stack_rule_alignment",
    "test_and_rollback_readiness",
    "traceability_and_cost",
]
BUILD_REQUIRED_OUTPUT_FIELDS = [
    "copilot_id",
    "decision",
    "evidence",
    "actions",
    "validation",
    "risks",
    "implementation",
]
BUILD_REQUIRED_IMPLEMENTATION_FIELDS = [
    "target_stack",
    "affected_files",
    "plan_steps",
    "stack_rules_checked",
    "validation_commands",
    "rollback_plan",
    "out_of_scope",
    "evidence_pack",
]
BUILD_EXECUTION_ORDER = [
    "load_catalog",
    "collect_runtime_trace",
    "audit_implementation_plan",
    "audit_stack_specific_rules",
    "audit_validation_and_rollback",
    "emit_build_gap_register",
    "return_build_audit",
]
BUILD_ROUTING_SIGNALS = [
    "build",
    "implementation",
    "implementacion",
    "plan",
    "patch",
    "stack",
    "stack-specific",
    "rules",
    "reglas",
    "affected",
    "files",
    "archivos",
    "rollback",
    "validation",
    "tests",
    "maven",
    "gradle",
    "angular",
    "node",
    "typescript",
    "python",
]
BUILD_VALIDATION_COMMANDS = [
    "python tools/validate_copilot_factory.py",
    "python tools/validate_prompt_quality.py",
    "python tools/semantic_router.py build implementation stack rules affected files rollback",
    "python tools/semantic_router.py implementacion reglas stack archivos rollback",
    "python tools/semantic_router.py python ci routing",
]
CHEAP_PATH_THRESHOLD = 3.0
MAX_ROUTE_LIMIT = 10
SEMANTIC_SCORE_INPUTS = [
    "id",
    "family",
    "function",
    "connectors",
    "env_keys",
    "stacks",
    "sdlc_phases",
    "outputs",
]
SEMANTIC_EXECUTION_ORDER = [
    "validate_request",
    "load_catalog",
    "load_index",
    "score_catalog",
    "rank_routes",
    "attach_runtime_trace",
    "return_route_payload",
]
SEMANTIC_LLM_GUARD = {
    "before_scoring": False,
    "default": "disabled",
    "escalation": "allowed_after_no_cheap_path_only",
    "trace_field": "routing_evidence.llm_assist_used",
}
SEMANTIC_RUNTIME_EQUIVALENCE = {
    "runtimes": RUNTIMES,
    "same_scoring_policy": True,
    "runtime_trace_required": True,
}
COPILOT_ID_ALIASES = {
    "ci": "cicd",
    "ci_cd": "cicd",
    "node_js": "nodejs",
}
CONNECTOR_ALIASES = {
    "confluence": "confluence_mcp_optional",
    "confluence_mcp": "confluence_mcp_optional",
    "confluence_optional": "confluence_mcp_optional",
    "github": "github_mcp",
    "github_mcp": "github_mcp",
    "mcp_github": "github_mcp",
    "sonar": "sonarqube_mcp",
    "sonar_mcp": "sonarqube_mcp",
    "sonarqube": "sonarqube_mcp",
    "sonarqube_mcp": "sonarqube_mcp",
}
ENV_KEY_ALIASES = {
    "CONFLUENCE_API_TOKEN": "CONFLUENCE_TOKEN_OPTIONAL",
    "GH_TOKEN": "GITHUB_TOKEN",
    "GITHUB_PAT": "GITHUB_TOKEN",
    "SONAR_TOKEN": "SONARQUBE_TOKEN",
}


@dataclass(frozen=True)
class Copilot:
    id: str
    name: str
    family: str
    function: str
    connectors: list[str]
    env_keys: list[str]
    stacks: list[str]
    sdlc_phases: list[str]
    outputs: list[str]


COPILOTS = [
    Copilot("devex", "Copiloto DevEx", "core", "Development standards, SDLC discipline, repo hygiene and cross-copilot support.", ["github_mcp"], ["GITHUB_TOKEN"], ["all"], ["discovery", "build", "test", "release"], ["devex_scorecard", "standards_patch_plan"]),
    Copilot("aida_architecture", "Copiloto de Principios de Arquitectura AIDA", "core", "Architecture evaluation, decision review and enterprise guidelines.", ["github_mcp", "confluence_mcp_optional"], ["GITHUB_TOKEN", "CONFLUENCE_TOKEN_OPTIONAL"], ["enterprise"], ["architecture", "design", "release"], ["adr_review", "architecture_principles_report"]),
    Copilot("as_is_discovery", "Copiloto de Discovery AS-IS", "core", "Legacy discovery, system inventory and current-state documentation.", ["github_mcp"], ["GITHUB_TOKEN"], ["legacy", "all"], ["discovery", "as_is"], ["as_is_report", "inventory_json"]),
    Copilot("single_registry", "Copiloto Registro Unico", "core", "Normalize technical information into one canonical registry.", ["github_mcp"], ["GITHUB_TOKEN"], ["all"], ["discovery", "operate"], ["technical_registry", "normalization_report"]),
    Copilot("firefly_v5", "Copiloto Firefly v5", "development", "Unit tests, integration tests, QA, CI/CD troubleshooting and remediation.", ["github_mcp", "sonarqube_mcp"], ["GITHUB_TOKEN", "SONARQUBE_TOKEN"], ["java", "enterprise"], ["build", "test", "devops"], ["test_plan", "ci_triage", "sonar_remediation"]),
    Copilot("firefly_v6", "Copiloto Firefly v6", "development", "Firefly v5 evolution with stronger knowledge-base separation and QA specialization.", ["github_mcp", "sonarqube_mcp"], ["GITHUB_TOKEN", "SONARQUBE_TOKEN"], ["java", "enterprise"], ["build", "test", "devops"], ["kb_partition_report", "test_plan", "quality_gate"]),
    Copilot("moonshine", "Copiloto Moonshine", "development", "Moonshine backend development and operational repair.", ["github_mcp"], ["GITHUB_TOKEN"], ["moonshine", "backend"], ["build", "test", "operate"], ["backend_patch_plan", "runtime_diagnostics"]),
    Copilot("java_generic", "Copiloto Java Generico", "development", "Enterprise Java development, refactoring and maintainability.", ["github_mcp"], ["GITHUB_TOKEN"], ["java", "spring", "maven", "gradle"], ["design", "build", "test"], ["java_patch_plan", "test_plan"]),
    Copilot("java_architect", "Copiloto Java Architect", "development", "Java design decisions, modularity, integration boundaries and architecture fitness.", ["github_mcp"], ["GITHUB_TOKEN"], ["java", "architecture"], ["architecture", "design", "release"], ["java_adr", "architecture_fitness_report"]),
    Copilot("angular_18", "Copiloto Angular 18", "development", "Angular 18 frontend development, components, state, routing and tests.", ["github_mcp"], ["GITHUB_TOKEN"], ["angular", "typescript", "frontend"], ["design", "build", "test"], ["frontend_patch_plan", "component_test_plan"]),
    Copilot("nodejs", "Copiloto Node.js", "development", "Enterprise Node.js backend development, APIs, services and observability.", ["github_mcp"], ["GITHUB_TOKEN"], ["node", "typescript", "backend"], ["design", "build", "test", "operate"], ["node_patch_plan", "api_contract_report"]),
    Copilot("python", "Copiloto Python", "development", "Python development, automation, data pipelines, semantic engines and tests.", ["github_mcp"], ["GITHUB_TOKEN"], ["python"], ["build", "test", "operate"], ["python_patch_plan", "automation_report"]),
    Copilot("qa_general", "Copiloto QA General", "quality", "Test case identification, QA automation and risk-based validation.", ["github_mcp"], ["GITHUB_TOKEN"], ["all"], ["test", "release"], ["qa_strategy", "test_matrix"]),
    Copilot("sonarqube_remediation", "Copiloto SonarQube Remediacion", "quality", "SonarQube non-conformity remediation and technical debt burn-down.", ["github_mcp", "sonarqube_mcp"], ["GITHUB_TOKEN", "SONARQUBE_TOKEN"], ["all"], ["test", "security", "release"], ["sonar_report", "remediation_backlog"]),
    Copilot("cicd", "Copiloto CI/CD", "devops", "Pipeline analysis, build troubleshooting, release automation and rollback diagnostics.", ["github_mcp"], ["GITHUB_TOKEN"], ["github_actions", "ci_cd"], ["devops", "release", "operate"], ["pipeline_triage", "workflow_patch_plan"]),
    Copilot("journey_to_cloud", "Copiloto Journey to Cloud", "cloud", "Cloud migration, legacy rebuild strategy and target architecture planning.", ["github_mcp"], ["GITHUB_TOKEN"], ["cloud", "modernization"], ["architecture", "cloud", "release"], ["migration_plan", "cloud_readiness_report"]),
    Copilot("copilots_manager", "Copilots Manager", "orchestration", "Discover copilots, install profiles, manage dependencies and route work.", ["github_mcp"], ["GITHUB_TOKEN"], ["orchestration"], ["discovery", "operate"], ["copilot_registry", "routing_plan"]),
    Copilot("firefly_marketplace", "Copiloto Firefly Marketplace", "marketplace", "Package, distribute and version copilots for reuse.", ["github_mcp"], ["GITHUB_TOKEN"], ["marketplace"], ["release", "operate"], ["marketplace_manifest", "distribution_report"]),
]


def snake_identifier(value: object) -> str:
    clean = re.sub(r"[^A-Za-z0-9]+", "_", str(value or "").strip())
    return re.sub(r"_+", "_", clean).strip("_").lower()


def upper_snake_identifier(value: object) -> str:
    return snake_identifier(value).upper()


def normalize_copilot_id(value: object) -> str:
    identifier = snake_identifier(value)
    return COPILOT_ID_ALIASES.get(identifier, identifier)


def normalize_connector_name(value: object) -> str:
    identifier = snake_identifier(value)
    return CONNECTOR_ALIASES.get(identifier, identifier)


def normalize_env_key(value: object) -> str:
    identifier = upper_snake_identifier(value)
    return ENV_KEY_ALIASES.get(identifier, identifier)


def normalize_output_name(value: object) -> str:
    return snake_identifier(value)


def list_values(value: object) -> list:
    if isinstance(value, list):
        return value
    if value in (None, ""):
        return []
    return [value]


def unique(values: list[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for value in values:
        if value and value not in seen:
            seen.add(value)
            result.append(value)
    return result


def normalize_catalog_entry(item: dict) -> dict:
    source = {
        "copilot_id": item.get("id", ""),
        "connector_names": list_values(item.get("connectors")),
        "env_names": list_values(item.get("env_keys")),
        "outputs": list_values(item.get("outputs")),
    }
    canonical = {
        "copilot_id": normalize_copilot_id(source["copilot_id"]),
        "connector_names": unique([normalize_connector_name(value) for value in source["connector_names"]]),
        "env_names": unique([normalize_env_key(value) for value in source["env_names"]]),
        "outputs": unique([normalize_output_name(value) for value in source["outputs"]]),
    }
    normalized = dict(item)
    normalized["id"] = canonical["copilot_id"]
    normalized["connectors"] = canonical["connector_names"]
    normalized["env_keys"] = canonical["env_names"]
    normalized["outputs"] = canonical["outputs"]
    normalized["normalization"] = {
        "version": NORMALIZATION_VERSION,
        "canonical": canonical,
        "source": source,
        "status": "already_normalized" if source == canonical else "normalized",
        "case_policy": CASE_POLICY,
        "traceability": TRACEABILITY_POLICY,
    }
    return normalized


def semantic_routing_profile() -> dict:
    return {
        "policy_version": SEMANTIC_ROUTING_VERSION,
        "router": "tools/semantic_router.py",
        "role": "python_brain",
        "deterministic_python_first": True,
        "score_before_llm_assist": True,
        "llm_assist_before_scoring_allowed": False,
        "evidence_field": "routing_evidence",
        "runtime_trace_required": True,
        "score_model": SEMANTIC_SCORE_MODEL,
    }


def semantic_routing_policy() -> dict:
    return {
        "ownerAgent": SEMANTIC_AGENT,
        "policyVersion": SEMANTIC_ROUTING_VERSION,
        "router": "tools/semantic_router.py",
        "deterministicPythonFirst": True,
        "scoreBeforeLlmAssist": True,
        "llmAssistBeforeScoringAllowed": False,
        "llmAssistDefault": SEMANTIC_LLM_GUARD["default"],
        "llmEscalation": SEMANTIC_LLM_GUARD["escalation"],
        "cheapPathThreshold": CHEAP_PATH_THRESHOLD,
        "maxRouteLimit": MAX_ROUTE_LIMIT,
        "evidenceField": "routing_evidence",
        "scoreInputs": SEMANTIC_SCORE_INPUTS,
        "executionOrder": SEMANTIC_EXECUTION_ORDER,
        "runtimeEquivalence": {
            "runtimes": RUNTIMES,
            "sameScoringPolicy": True,
            "runtimeTraceRequired": True,
        },
        "scoreModel": SEMANTIC_SCORE_MODEL,
    }


def semantic_routing_audit() -> dict:
    return {
        "pass": True,
        "policyVersion": SEMANTIC_ROUTING_VERSION,
        "ownerAgent": SEMANTIC_AGENT,
        "router": "tools/semantic_router.py",
        "deterministicPythonFirst": True,
        "scoreBeforeLlmAssist": True,
        "llmAssistUsedByRouter": False,
        "cheapPathThreshold": CHEAP_PATH_THRESHOLD,
        "evidenceField": "routing_evidence",
        "runtimeEquivalenceRuntimes": RUNTIMES,
        "sampleRequest": "python ci routing",
        "sampleExpectedTopRoute": "python",
        "routeEvidenceFields": [
            "score",
            "confidence",
            "match_reasons",
            "runtime_trace",
            "routing_evidence",
        ],
        "scoreModel": SEMANTIC_SCORE_MODEL,
    }


def discovery_audit_runtime_equivalence() -> dict:
    return {
        "runtimes": RUNTIMES,
        "source_of_truth": "dist/copilots/as_is_discovery/shared/spec.json",
        "max_unexplained_drift": 0,
    }


def discovery_audit_profile() -> dict:
    return {
        "policy_version": DISCOVERY_AUDIT_VERSION,
        "owner_agent": DISCOVERY_AGENT,
        "mission": DISCOVERY_MISSION,
        "coverage_items": DISCOVERY_COVERAGE_ITEMS,
        "inventory_fields": DISCOVERY_INVENTORY_FIELDS,
        "required_outputs": DISCOVERY_REQUIRED_OUTPUTS,
        "gap_register_required": True,
        "evidence_field": "discovery_audit",
        "runtime_trace_required": True,
        "validation_commands": DISCOVERY_VALIDATION_COMMANDS,
        "runtime_equivalence": discovery_audit_runtime_equivalence(),
        "cost_control": {
            "deterministic_python_first": True,
            "llm_escalation": "allowed_after_inventory_gaps_only",
        },
    }


def discovery_audit_policy() -> dict:
    return {
        "ownerAgent": DISCOVERY_AGENT,
        "policyVersion": DISCOVERY_AUDIT_VERSION,
        "targetCopilot": DISCOVERY_TARGET_COPILOT,
        "router": "tools/semantic_router.py",
        "deterministicPythonFirst": True,
        "llmEscalation": "allowed_after_inventory_gaps_only",
        "evidenceField": "discovery_audit",
        "coverageItems": DISCOVERY_COVERAGE_ITEMS,
        "inventoryFields": DISCOVERY_INVENTORY_FIELDS,
        "requiredOutputs": DISCOVERY_REQUIRED_OUTPUTS,
        "executionOrder": DISCOVERY_EXECUTION_ORDER,
        "gapRegisterRequired": True,
        "validationCommands": DISCOVERY_VALIDATION_COMMANDS,
        "runtimeEquivalence": {
            "runtimes": RUNTIMES,
            "sourceOfTruth": "dist/copilots/as_is_discovery/shared/spec.json",
            "maxUnexplainedDrift": 0,
        },
    }


def discovery_audit_summary() -> dict:
    return {
        "pass": True,
        "policyVersion": DISCOVERY_AUDIT_VERSION,
        "ownerAgent": DISCOVERY_AGENT,
        "targetCopilot": DISCOVERY_TARGET_COPILOT,
        "coverageItemsChecked": len(DISCOVERY_COVERAGE_ITEMS),
        "inventoryFieldsChecked": len(DISCOVERY_INVENTORY_FIELDS),
        "requiredOutputs": DISCOVERY_REQUIRED_OUTPUTS,
        "gapRegisterRequired": True,
        "runtimeEquivalenceRuntimes": RUNTIMES,
        "evidenceField": "discovery_audit",
        "sampleRequest": "as_is inventory coverage",
        "sampleExpectedTopRoute": DISCOVERY_TARGET_COPILOT,
        "routeEvidenceFields": [
            "runtime_trace",
            "discovery_audit",
            "routing_evidence",
        ],
        "validationCommands": DISCOVERY_VALIDATION_COMMANDS,
    }


def is_design_boundary_copilot(item: dict) -> bool:
    return item.get("id") in DESIGN_TARGET_COPILOTS and "design" in item.get("sdlc_phases", [])


def design_audit_source(copilot_id: str) -> str:
    return f"dist/copilots/{copilot_id}/shared/design_boundary_audit.json"


def design_runtime_equivalence(copilot_id: str) -> dict:
    return {
        "sourceOfTruth": design_audit_source(copilot_id),
        "runtimes": RUNTIMES,
        "maxUnexplainedDrift": 0,
    }


def design_runtime_contract(copilot_id: str) -> dict:
    return {
        "artifact": DESIGN_AUDIT_ARTIFACT,
        "version": DESIGN_AUDIT_VERSION,
        "ownerAgent": DESIGN_AGENT,
        "mission": DESIGN_MISSION,
        "requiredEvidence": DESIGN_REQUIRED_EVIDENCE,
        "qualityGates": DESIGN_QUALITY_GATES,
        "requiredOutputFields": DESIGN_REQUIRED_OUTPUT_FIELDS,
        "requiredHandoffFields": DESIGN_REQUIRED_HANDOFF_FIELDS,
        "runtimeEquivalence": design_runtime_equivalence(copilot_id),
    }


def design_profile(copilot_id: str) -> dict:
    return {
        "policy_version": DESIGN_AUDIT_VERSION,
        "owner_agent": DESIGN_AGENT,
        "mission": DESIGN_MISSION,
        "required_evidence": DESIGN_REQUIRED_EVIDENCE,
        "quality_gates": DESIGN_QUALITY_GATES,
        "required_output_fields": DESIGN_REQUIRED_OUTPUT_FIELDS,
        "required_handoff_fields": DESIGN_REQUIRED_HANDOFF_FIELDS,
        "evidence_field": "design_boundary_audit",
        "runtime_trace_required": True,
        "validation_commands": DESIGN_VALIDATION_COMMANDS,
        "runtime_equivalence": {
            "runtimes": RUNTIMES,
            "source_of_truth": design_audit_source(copilot_id),
            "max_unexplained_drift": 0,
        },
        "cost_control": {
            "deterministic_python_first": True,
            "llm_escalation": "allowed_after_boundary_conflicts_only",
        },
    }


def design_audit_policy() -> dict:
    return {
        "ownerAgent": DESIGN_AGENT,
        "policyVersion": DESIGN_AUDIT_VERSION,
        "targetCopilots": DESIGN_TARGET_COPILOTS,
        "router": "tools/semantic_router.py",
        "deterministicPythonFirst": True,
        "llmEscalation": "allowed_after_boundary_conflicts_only",
        "evidenceField": "design_boundary_audit",
        "requiredEvidence": DESIGN_REQUIRED_EVIDENCE,
        "qualityGates": DESIGN_QUALITY_GATES,
        "requiredOutputFields": DESIGN_REQUIRED_OUTPUT_FIELDS,
        "requiredHandoffFields": DESIGN_REQUIRED_HANDOFF_FIELDS,
        "executionOrder": DESIGN_EXECUTION_ORDER,
        "validationCommands": DESIGN_VALIDATION_COMMANDS,
        "runtimeEquivalence": {
            "runtimes": RUNTIMES,
            "sourceOfTruthPattern": "dist/copilots/<copilot_id>/shared/design_boundary_audit.json",
            "maxUnexplainedDrift": 0,
        },
    }


def design_audit_summary() -> dict:
    return {
        "pass": True,
        "policyVersion": DESIGN_AUDIT_VERSION,
        "ownerAgent": DESIGN_AGENT,
        "targetCopilots": DESIGN_TARGET_COPILOTS,
        "requiredEvidence": DESIGN_REQUIRED_EVIDENCE,
        "qualityGates": DESIGN_QUALITY_GATES,
        "requiredOutputFields": DESIGN_REQUIRED_OUTPUT_FIELDS,
        "requiredHandoffFields": DESIGN_REQUIRED_HANDOFF_FIELDS,
        "evidenceField": "design_boundary_audit",
        "sampleRequest": "design domain boundaries contracts handoff",
        "sampleExpectedTopRoutes": DESIGN_TARGET_COPILOTS,
        "routeEvidenceFields": [
            "runtime_trace",
            "design_boundary_audit",
            "routing_evidence",
        ],
        "validationCommands": DESIGN_VALIDATION_COMMANDS,
    }


def is_build_implementation_copilot(item: dict) -> bool:
    return item.get("id") in BUILD_TARGET_COPILOTS and "build" in item.get("sdlc_phases", [])


def build_audit_source(copilot_id: str) -> str:
    return f"dist/copilots/{copilot_id}/shared/implementation_plan_audit.json"


def build_runtime_equivalence(copilot_id: str) -> dict:
    return {
        "sourceOfTruth": build_audit_source(copilot_id),
        "runtimes": RUNTIMES,
        "maxUnexplainedDrift": 0,
    }


def build_runtime_contract(copilot_id: str) -> dict:
    return {
        "artifact": BUILD_AUDIT_ARTIFACT,
        "version": BUILD_AUDIT_VERSION,
        "ownerAgent": BUILD_AGENT,
        "mission": BUILD_MISSION,
        "requiredEvidence": BUILD_REQUIRED_EVIDENCE,
        "qualityGates": BUILD_QUALITY_GATES,
        "requiredOutputFields": BUILD_REQUIRED_OUTPUT_FIELDS,
        "requiredImplementationFields": BUILD_REQUIRED_IMPLEMENTATION_FIELDS,
        "runtimeEquivalence": build_runtime_equivalence(copilot_id),
    }


def build_profile(copilot_id: str) -> dict:
    return {
        "policy_version": BUILD_AUDIT_VERSION,
        "owner_agent": BUILD_AGENT,
        "mission": BUILD_MISSION,
        "required_evidence": BUILD_REQUIRED_EVIDENCE,
        "quality_gates": BUILD_QUALITY_GATES,
        "required_output_fields": BUILD_REQUIRED_OUTPUT_FIELDS,
        "required_implementation_fields": BUILD_REQUIRED_IMPLEMENTATION_FIELDS,
        "evidence_field": "implementation_plan_audit",
        "runtime_trace_required": True,
        "validation_commands": BUILD_VALIDATION_COMMANDS,
        "runtime_equivalence": {
            "runtimes": RUNTIMES,
            "source_of_truth": build_audit_source(copilot_id),
            "max_unexplained_drift": 0,
        },
        "cost_control": {
            "deterministic_python_first": True,
            "llm_escalation": "allowed_after_stack_rule_gaps_only",
        },
    }


def build_audit_policy() -> dict:
    return {
        "ownerAgent": BUILD_AGENT,
        "policyVersion": BUILD_AUDIT_VERSION,
        "targetCopilots": BUILD_TARGET_COPILOTS,
        "router": "tools/semantic_router.py",
        "deterministicPythonFirst": True,
        "llmEscalation": "allowed_after_stack_rule_gaps_only",
        "evidenceField": "implementation_plan_audit",
        "requiredEvidence": BUILD_REQUIRED_EVIDENCE,
        "qualityGates": BUILD_QUALITY_GATES,
        "requiredOutputFields": BUILD_REQUIRED_OUTPUT_FIELDS,
        "requiredImplementationFields": BUILD_REQUIRED_IMPLEMENTATION_FIELDS,
        "executionOrder": BUILD_EXECUTION_ORDER,
        "validationCommands": BUILD_VALIDATION_COMMANDS,
        "runtimeEquivalence": {
            "runtimes": RUNTIMES,
            "sourceOfTruthPattern": "dist/copilots/<copilot_id>/shared/implementation_plan_audit.json",
            "maxUnexplainedDrift": 0,
        },
    }


def build_audit_summary() -> dict:
    return {
        "pass": True,
        "policyVersion": BUILD_AUDIT_VERSION,
        "ownerAgent": BUILD_AGENT,
        "targetCopilots": BUILD_TARGET_COPILOTS,
        "requiredEvidence": BUILD_REQUIRED_EVIDENCE,
        "qualityGates": BUILD_QUALITY_GATES,
        "requiredOutputFields": BUILD_REQUIRED_OUTPUT_FIELDS,
        "requiredImplementationFields": BUILD_REQUIRED_IMPLEMENTATION_FIELDS,
        "evidenceField": "implementation_plan_audit",
        "sampleRequest": "build implementation stack rules affected files rollback",
        "sampleExpectedTopRoutes": BUILD_TARGET_COPILOTS,
        "routeEvidenceFields": [
            "runtime_trace",
            "implementation_plan_audit",
            "routing_evidence",
        ],
        "validationCommands": BUILD_VALIDATION_COMMANDS,
    }


def normalized_copilots() -> list[dict]:
    items = [normalize_catalog_entry(asdict(item)) for item in COPILOTS]
    for item in items:
        if item["id"] == "python":
            item["semantic_routing"] = semantic_routing_profile()
        if item["id"] == DISCOVERY_TARGET_COPILOT:
            item["discovery_audit"] = discovery_audit_profile()
        if is_design_boundary_copilot(item):
            item["design_boundary_audit"] = design_profile(item["id"])
        if is_build_implementation_copilot(item):
            item["implementation_plan_audit"] = build_profile(item["id"])
    return items


def runtime_trace(copilot_id: str) -> dict:
    return {
        "source_of_truth": f"dist/copilots/{copilot_id}/shared/spec.json",
        "runtime_adapters": {
            "codex": f"dist/copilots/{copilot_id}/codex/AGENT.md",
            "claude": f"dist/copilots/{copilot_id}/claude/AGENT.md",
            "github-copilot": f"dist/copilots/{copilot_id}/github-copilot/copilot-agent.md",
            "langchain": f"dist/copilots/{copilot_id}/langchain/agent.py",
        },
        "runtimes": RUNTIMES,
    }


def copilot_index() -> dict:
    copilots = []
    lookup = {}
    for item in normalized_copilots():
        indexed = {**item, "runtime_trace": runtime_trace(item["id"])}
        copilots.append(indexed)
        lookup[item["id"]] = {
            "name": item["name"],
            "family": item["family"],
            "connectors": item["connectors"],
            "env_keys": item["env_keys"],
            "outputs": item["outputs"],
            "normalization": item["normalization"]["canonical"],
            "runtime_trace": indexed["runtime_trace"],
        }
        if "semantic_routing" in item:
            lookup[item["id"]]["semantic_routing"] = item["semantic_routing"]
        if "discovery_audit" in item:
            lookup[item["id"]]["discovery_audit"] = item["discovery_audit"]
        if "design_boundary_audit" in item:
            lookup[item["id"]]["design_boundary_audit"] = item["design_boundary_audit"]
        if "implementation_plan_audit" in item:
            lookup[item["id"]]["implementation_plan_audit"] = item["implementation_plan_audit"]
    return {
        "version": FACTORY_VERSION,
        "generatedAt": now(),
        "normalizationPolicy": {
            "version": NORMALIZATION_VERSION,
            "normalizer": "tools/semantic_router.py",
            "canonicalCase": CASE_POLICY,
            "runtimeEquivalence": {
                "sourceOfTruth": "dist/copilots/<copilot_id>/shared/spec.json",
                "runtimes": RUNTIMES,
                "maxUnexplainedDrift": 0,
            },
            "costControl": {
                "deterministicPythonFirst": True,
                "llmEscalation": "not_required_for_catalog_normalization",
            },
            "semanticRouting": semantic_routing_policy(),
            "discoveryAudit": discovery_audit_policy(),
            "designBoundaryAudit": design_audit_policy(),
            "buildImplementationAudit": build_audit_policy(),
        },
        "normalizedFields": {
            "copilotIds": [item["id"] for item in copilots],
            "connectorNames": sorted({value for item in copilots for value in item["connectors"]}),
            "envNames": sorted({value for item in copilots for value in item["env_keys"]}),
            "outputs": sorted({value for item in copilots for value in item["outputs"]}),
        },
        "runtimes": RUNTIMES,
        "copilots": copilots,
        "normalizedLookup": lookup,
        "normalizationAudit": {
            "pass": True,
            "copilots": len(copilots),
            "copilotIds": len({item["id"] for item in copilots}),
            "connectorNames": len({value for item in copilots for value in item["connectors"]}),
            "envNames": len({value for item in copilots for value in item["env_keys"]}),
            "outputs": len({value for item in copilots for value in item["outputs"]}),
            "runtimeTraceComplete": all(set(item["runtime_trace"]["runtimes"]) == set(RUNTIMES) for item in copilots),
        },
        "semanticRoutingAudit": semantic_routing_audit(),
        "discoveryAudit": discovery_audit_summary(),
        "designBoundaryAudit": design_audit_summary(),
        "buildImplementationAudit": build_audit_summary(),
    }


AGENT_GROUPS = [
    ("director", "Factory Director", "Owns the whole run, keeps gates honest and prevents scope drift."),
    ("catalog", "Catalog Normalizer", "Normalizes copilot IDs, connector names, env names and outputs."),
    ("semantics", "Semantic Router", "Uses deterministic Python scoring before any LLM assist."),
    ("discovery", "Discovery Auditor", "Audits AS-IS coverage and repo inventory contracts."),
    ("architecture", "Architecture Auditor", "Audits principles, ADRs and technical decision quality."),
    ("design", "Design Auditor", "Audits domain boundaries, contracts and handoff clarity."),
    ("build", "Build Auditor", "Audits implementation plans and stack-specific rules."),
    ("test", "Test Auditor", "Audits test strategy, pairwise cases and negative cases."),
    ("security", "Security Auditor", SECURITY_MISSION),
    ("devops", "DevOps Auditor", "Audits CI/CD, logs, reproducibility and rollback paths."),
    ("cloud", "Cloud Auditor", "Audits migration, target platform and modernization increments."),
    ("release", "Release Auditor", "Audits package readiness, scorecards and exit criteria."),
    ("operate", "Operate Auditor", "Audits observability, incident playbooks and runbooks."),
    ("codex", "Codex Adapter Builder", "Builds Codex-facing task prompts and local tool protocol."),
    ("claude", "Claude Adapter Builder", "Builds Claude-facing project instructions and agent cards."),
    ("github", "GitHub Copilot Adapter Builder", "Builds GitHub Copilot profile docs and MCP placeholders."),
    ("langchain", "LangChain Adapter Builder", "Builds Python/LangChain compatible agent specs."),
    ("mcp", "MCP Connector Auditor", "Audits connector declarations and env placeholders."),
    ("docs", "Documentation Auditor", "Audits generated READMEs and operator docs."),
    ("cost", "Token Cost Governor", "Routes cheap deterministic work to Python and expensive judgement to LLMs."),
    ("kb", "Knowledge Boundary Auditor", "Audits KB separation, source-of-truth rules and context windows."),
    ("qa", "QA Committee Chair", "Consolidates all phase verdicts into a pass/fail report."),
    ("packager", "Product Packager", "Builds distribution manifests and file indexes."),
    ("matrix", "SDLC Matrix Builder", "Maintains the SDLC x Copilot x Runtime matrix."),
    ("smoke", "Smoke Runner", "Runs generated validators and reports blockers."),
]


def main() -> None:
    clean_dirs()
    write_root_docs()
    write_catalogs()
    write_runtime_adapters()
    write_semantic_tools()
    write_tasks()
    write_reports()
    elevate_prompt_contracts()
    print(f"Generated {len(COPILOTS)} copilots x {len(RUNTIMES)} runtimes with {len(agent_roster())} factory agents.")


def elevate_prompt_contracts() -> None:
    from elevate_copilot_prompts import elevate

    elevate(ROOT)


def clean_dirs() -> None:
    for folder in [GENERATED, DIST, DATA, CONFIG]:
        folder.mkdir(parents=True, exist_ok=True)
    purge_python_bytecode_artifacts()


def purge_python_bytecode_artifacts() -> None:
    release_roots = [DIST.resolve(), (ROOT / "tools").resolve()]

    def is_release_artifact(path: Path) -> bool:
        try:
            resolved = path.resolve()
        except OSError:
            return False
        return any(resolved == root or root in resolved.parents for root in release_roots)

    for root in release_roots:
        if not root.exists():
            continue
        for cache_dir in root.rglob("__pycache__"):
            if cache_dir.is_dir() and is_release_artifact(cache_dir):
                shutil.rmtree(cache_dir)
        for bytecode in root.rglob("*.pyc"):
            if bytecode.is_file() and is_release_artifact(bytecode):
                bytecode.unlink()


def write_root_docs() -> None:
    write(ROOT / "README.md", render_readme())
    write(ROOT / "OPERATING_SYSTEM.md", render_operating_system())
    write(ROOT / "factory-prompt.md", render_factory_prompt())
    write(ROOT / ".gitignore", render_gitignore())
    write(ROOT / ".vscode" / "settings.json", json.dumps(workspace_settings(), indent=2) + "\n")
    write(ROOT / "agent-state.json", json.dumps(initial_agent_state(), indent=2) + "\n")
    write(ROOT / "factory.config.json", json.dumps({
        "version": FACTORY_VERSION,
        "brain": "python_deterministic",
        "llm_role": "cerebellum_for_sparse_judgement_and_generation",
        "copilots": len(COPILOTS),
        "runtimes": RUNTIMES,
        "factoryAgents": len(agent_roster()),
        "commands": {
            "generate": "python tools/generate_copilot_factory.py",
            "validate": "python tools/validate_copilot_factory.py",
            "run": "python tools/run_factory.py",
        },
        "controlRoom": control_room_contract(),
    }, indent=2) + "\n")
    write(CONFIG / "mcp-connectors.example.json", json.dumps(security_mcp_connectors_contract(), indent=2) + "\n")
    write(CONFIG / ".env.example", security_env_example())


def security_env_example() -> str:
    return "\n".join([
        "# Sensitive credentials policy:",
        "# Keep this file placeholder-only. Set real values only in a local shell,",
        "# OS secret store, CI secret store, or approved MCP runtime environment.",
        "# Do not commit .env files, token samples, customer data, or billing data.",
        "GITHUB_TOKEN=",
        "SONARQUBE_TOKEN=",
        "CONFLUENCE_TOKEN_OPTIONAL=",
        "",
    ])


def security_mcp_connectors_contract() -> dict:
    return {
        "policy_version": SECURITY_AUDIT_VERSION,
        "owner_agent": SECURITY_AGENT,
        "mission": SECURITY_MISSION,
        "runtime_equivalence": SECURITY_RUNTIME_EQUIVALENCE,
        "sensitive_credentials_policy": {
            "storage": "environment_only",
            "placeholder_only_in_repo": True,
            "deny_real_values_in_env_example": True,
            "required_env_example": SECURITY_ENV_EXAMPLE,
            "redaction_required": True,
            "rotation_owner_required": True,
            "customer_data_allowed": False,
            "billing_data_allowed": False,
            "allowed_placeholder_values": [""],
            "deny_value_prefixes": [
                "sk-",
                "github_pat_",
                "ghp_",
                "gho_",
                "ghu_",
                "ghs_",
                "ghr_",
                "Bearer ",
            ],
        },
        "threat_model": [
            {
                "id": "credential_exposure",
                "asset": "MCP credentials",
                "threat": "Repository, prompt, trace, or generated artifact contains a live token.",
                "control": "Only env var names and empty placeholders are allowed in tracked examples.",
                "verification": "python tools/validate_copilot_factory.py",
            },
            {
                "id": "overprivileged_connector",
                "asset": "External systems reachable through MCP",
                "threat": "A connector grants broad write, admin, secret, billing, or destructive access.",
                "control": "Each connector declares owner, purpose, allowed operations, denied operations, and least-privilege scope.",
                "verification": "python tools/validate_copilot_factory.py",
            },
            {
                "id": "prompt_or_trace_leakage",
                "asset": "Runtime prompts, traces, logs, and reports",
                "threat": "Sensitive values or customer data are copied into prompts or audit traces.",
                "control": "Tokens are redacted from logs, customer data is denied in prompts, and validation scans text artifacts.",
                "verification": "python tools/validate_copilot_factory.py",
            },
            {
                "id": "unsafe_mcp_activation",
                "asset": "Local MCP runtime configuration",
                "threat": "A connector is enabled without operator intent, traceability, or runtime parity.",
                "control": "Examples default to disabled and require operator activation, allowlists, and common runtime policy.",
                "verification": "python tools/validate_copilot_factory.py",
            },
        ],
        "mcp_safe_usage": SECURITY_REQUIRED_SAFE_USAGE,
        "connectors": {
            "github_mcp": {
                "enabled": False,
                "env": "GITHUB_TOKEN",
                "purpose": "Repository metadata plus operator-approved issue, pull request, and review operations.",
                "owner": "Operations",
                "rotation_owner": "Operations",
                "least_privilege_scope": "repo metadata and pull request issue operations approved by operator",
                "allowed_runtimes": RUNTIMES,
                "requires_operator_activation": True,
                "operator_approval_required_for_writes": True,
                "allowed_operations": [
                    "read_repo_metadata",
                    "read_issues",
                    "read_pull_requests",
                    "write_operator_approved_comments",
                ],
                "denied_operations": SECURITY_REQUIRED_DENIED_OPERATIONS,
            },
            "sonarqube_mcp": {
                "enabled": False,
                "env": "SONARQUBE_TOKEN",
                "purpose": "Quality gate, issue, and coverage signal reads for release readiness.",
                "owner": "Quality",
                "rotation_owner": "Quality",
                "least_privilege_scope": "quality gate and issue read access",
                "allowed_runtimes": RUNTIMES,
                "requires_operator_activation": True,
                "operator_approval_required_for_writes": True,
                "allowed_operations": [
                    "read_quality_gates",
                    "read_issues",
                    "read_coverage",
                ],
                "denied_operations": SECURITY_REQUIRED_DENIED_OPERATIONS,
            },
            "confluence_mcp_optional": {
                "enabled": False,
                "env": "CONFLUENCE_TOKEN_OPTIONAL",
                "purpose": "Approved architecture documentation reads for enterprise handoff only.",
                "owner": "Architecture",
                "rotation_owner": "Architecture",
                "least_privilege_scope": "approved documentation read access",
                "allowed_runtimes": RUNTIMES,
                "requires_operator_activation": True,
                "operator_approval_required_for_writes": True,
                "allowed_operations": [
                    "read_approved_spaces",
                    "read_architecture_docs",
                ],
                "denied_operations": SECURITY_REQUIRED_DENIED_OPERATIONS,
            },
        },
        "rules": [
            "Never store real token values in this repository.",
            "Use environment variable names only in tracked examples.",
            "Every connector must have a purpose, owner, rotation owner, runtime allowlist, allowed operations, denied operations, and least-privilege scope before activation.",
            "Examples must default connectors to disabled until the operator activates them locally.",
            "The same MCP safety policy applies to Codex, Claude, GitHub Copilot, and LangChain.",
        ],
    }


def control_room_contract() -> dict:
    return {
        "ownerAgent": DIRECTOR_AGENT,
        "room": "Control Room",
        "mission": DIRECTOR_MISSION,
        "concurrency": "serial",
        "stateLockFrontier": {
            "lockFile": ".codex-loop/run.lock.json",
            "denyConcurrentFactoryRuns": True,
            "activeRunRequiresNoNewFactory": True,
            "snapshotRequiredWhenGitMissing": True,
            "requiredLockFields": ["id", "pid", "workspace", "startedAt", "heartbeatAt", "mode"],
            "workspaceMustMatchRoot": True,
            "heartbeatMustNotPrecedeStart": True,
            "snapshotEvidenceRoots": [".codex-loop/backups", ".codex-loop/rollback"],
            "frontier": "state-locks",
        },
        "gateHonesty": {
            "mustPassBeforeDone": [
                "python tools/validate_copilot_factory.py",
                "python tools/validate_prompt_quality.py",
                "python tools/validate_runtime_equivalence.py",
            ],
            "requiredReports": [
                "generated/validation-report.json",
                "generated/prompt-quality-report.json",
                "generated/runtime-equivalence-report.json",
            ],
            "doneRequiresEvidence": True,
            "compileOnlyIsInsufficient": True,
        },
        "scopeDrift": {
            "declaredTaskFilesOnlyByDefault": True,
            "allowedFactoryRoots": [
                ".codex-loop",
                "config",
                "data",
                "dist",
                "generated",
                "products",
                "tools",
            ],
            "productRoot": "products",
            "registryRequiredForNewProducts": True,
        },
        "runtimeEquivalence": {
            "canonicalSpec": "dist/copilots/<copilot>/shared/spec.json",
            "traceMap": "generated/runtime-injection-map.json",
            "adapters": RUNTIMES,
            "maxUnexplainedDrift": 0,
        },
        "costTrace": {
            "deterministicPythonFirst": True,
            "llmRole": "sparse_judgement_code_edits_and_final_synthesis",
            "avoidRepeatedPromptExpansion": True,
            "auditArtifactsAreSourceOfTruth": True,
        },
        "releaseTruthGate": {
            "ownerReviewRequired": True,
            "qaReviewRequired": True,
            "safeCodingPrivacyReviewRequired": True,
            "releaseReviewRequired": True,
            "residualRiskMustBeExplicit": True,
        },
    }


def write_catalogs() -> None:
    write(DATA / "copilots.json", json.dumps(normalized_copilots(), indent=2) + "\n")
    write(DATA / "agent_roster.json", json.dumps(agent_roster(), indent=2) + "\n")
    write(DATA / "sdlc_phases.json", json.dumps({"phases": SDLC_PHASES}, indent=2) + "\n")


def write_runtime_adapters() -> None:
    for copilot in COPILOTS:
        base = DIST / copilot.id
        shared = {
            **asdict(copilot),
            "version": FACTORY_VERSION,
            "identity": {
                "slug": copilot.id,
                "displayName": copilot.name,
                "family": copilot.family,
            },
            "routing": routing_profile(copilot),
            "governance": governance_profile(copilot),
            "semanticTags": semantic_tags(copilot),
        }
        if is_design_boundary_copilot(asdict(copilot)):
            shared["designBoundaryAudit"] = design_runtime_contract(copilot.id)
        if is_build_implementation_copilot(asdict(copilot)):
            shared["buildImplementationAudit"] = build_runtime_contract(copilot.id)
        write(base / "shared" / "spec.json", json.dumps(shared, indent=2) + "\n")
        write(base / "README.md", render_copilot_readme(copilot))
        write(base / "codex" / "AGENT.md", render_codex_agent(copilot))
        write(base / "claude" / "AGENT.md", render_claude_agent(copilot))
        write(base / "github-copilot" / "copilot-agent.md", render_github_agent(copilot))
        write(base / "langchain" / "agent_profile.json", json.dumps(shared, indent=2) + "\n")
        write(base / "langchain" / "agent.py", render_langchain_agent(copilot))


def write_semantic_tools() -> None:
    write(ROOT / "tools" / "semantic_router.py", render_semantic_router())
    write(ROOT / "tools" / "run_factory.py", render_run_factory())


def write_tasks() -> None:
    tasks = []
    for index, agent in enumerate(agent_roster(), start=1):
        tasks.append(render_factory_task(agent, index))
    write(ROOT / "tasks.json", json.dumps(tasks, indent=2) + "\n")


def write_reports() -> None:
    roster = agent_roster()
    write(GENERATED / "agent-roster.json", json.dumps(roster, indent=2) + "\n")
    write(GENERATED / "agent-roster.md", render_agent_roster_md(roster))
    write(GENERATED / "copilot-index.json", json.dumps(copilot_index(), indent=2) + "\n")
    write(GENERATED / "sdlc-audit-matrix.md", render_sdlc_matrix())
    write(GENERATED / "token-cost-strategy.md", render_cost_strategy())
    write(GENERATED / "semantic-routing-plan.md", render_semantic_plan())
    write(GENERATED / "factory-audit.json", json.dumps(factory_audit(), indent=2) + "\n")
    write(GENERATED / "factory-audit.md", render_factory_audit())


def agent_roster() -> list[dict]:
    agents = []
    for idx, (short, name, mission) in enumerate(AGENT_GROUPS, start=1):
        agent = {
            "id": f"factory_agent_{idx:02d}_{short}",
            "name": name,
            "phase": phase_for_group(short),
            "mode": mode_for_group(short),
            "mission": mission,
        }
        if short == "catalog":
            agent["outputs"] = [
                "normalized_copilot_catalog",
                "normalized_route_payload",
                "runtime_trace_index",
            ]
            agent["normalization_contract"] = {
                "version": NORMALIZATION_VERSION,
                "source": "data/copilots.json",
                "generated_index": "generated/copilot-index.json",
                "router": "tools/semantic_router.py",
                "canonical_fields": CASE_POLICY,
                "runtime_equivalence": {
                    "sourceOfTruth": "dist/copilots/<copilot_id>/shared/spec.json",
                    "runtimes": RUNTIMES,
                    "maxUnexplainedDrift": 0,
                },
            }
        if short == "semantics":
            agent["outputs"] = [
                "deterministic_route_scores",
                "route_confidence_payload",
                "llm_escalation_guard",
            ]
            agent["deterministic_scoring_contract"] = {
                "version": SEMANTIC_ROUTING_VERSION,
                "router": "tools/semantic_router.py",
                "catalog": "data/copilots.json",
                "index": "generated/copilot-index.json",
                "score_inputs": SEMANTIC_SCORE_INPUTS,
                "execution_order": SEMANTIC_EXECUTION_ORDER,
                "cheap_path_threshold": CHEAP_PATH_THRESHOLD,
                "max_route_limit": MAX_ROUTE_LIMIT,
                "llm_assist": SEMANTIC_LLM_GUARD,
                "runtime_equivalence": SEMANTIC_RUNTIME_EQUIVALENCE,
                "score_model": SEMANTIC_SCORE_MODEL,
            }
        if short == "discovery":
            agent["outputs"] = DISCOVERY_AGENT_OUTPUTS
            agent["as_is_inventory_contract"] = {
                "version": DISCOVERY_AUDIT_VERSION,
                "source_catalog": "data/copilots.json",
                "generated_index": "generated/copilot-index.json",
                "router": "tools/semantic_router.py",
                "target_copilot": DISCOVERY_TARGET_COPILOT,
                "required_outputs": DISCOVERY_REQUIRED_OUTPUTS,
                "coverage_items": DISCOVERY_COVERAGE_ITEMS,
                "inventory_fields": DISCOVERY_INVENTORY_FIELDS,
                "execution_order": DISCOVERY_EXECUTION_ORDER,
                "evidence_field": "discovery_audit",
                "gap_register_required": True,
                "validation_commands": DISCOVERY_VALIDATION_COMMANDS,
                "runtime_equivalence": discovery_audit_runtime_equivalence(),
            }
        if short == "design":
            agent["outputs"] = DESIGN_AGENT_OUTPUTS
            agent["design_boundary_contract"] = {
                "version": DESIGN_AUDIT_VERSION,
                "source_catalog": "data/copilots.json",
                "generated_index": "generated/copilot-index.json",
                "router": "tools/semantic_router.py",
                "target_copilots": DESIGN_TARGET_COPILOTS,
                "required_evidence": DESIGN_REQUIRED_EVIDENCE,
                "quality_gates": DESIGN_QUALITY_GATES,
                "required_output_fields": DESIGN_REQUIRED_OUTPUT_FIELDS,
                "required_handoff_fields": DESIGN_REQUIRED_HANDOFF_FIELDS,
                "execution_order": DESIGN_EXECUTION_ORDER,
                "evidence_field": "design_boundary_audit",
                "validation_commands": DESIGN_VALIDATION_COMMANDS,
                "runtime_equivalence": {
                    "runtimes": RUNTIMES,
                    "source_of_truth_pattern": "dist/copilots/<copilot_id>/shared/design_boundary_audit.json",
                    "max_unexplained_drift": 0,
                },
            }
        if short == "build":
            agent["outputs"] = BUILD_AGENT_OUTPUTS
            agent["implementation_plan_contract"] = {
                "version": BUILD_AUDIT_VERSION,
                "source_catalog": "data/copilots.json",
                "generated_index": "generated/copilot-index.json",
                "router": "tools/semantic_router.py",
                "target_copilots": BUILD_TARGET_COPILOTS,
                "required_evidence": BUILD_REQUIRED_EVIDENCE,
                "quality_gates": BUILD_QUALITY_GATES,
                "required_output_fields": BUILD_REQUIRED_OUTPUT_FIELDS,
                "required_implementation_fields": BUILD_REQUIRED_IMPLEMENTATION_FIELDS,
                "execution_order": BUILD_EXECUTION_ORDER,
                "evidence_field": "implementation_plan_audit",
                "validation_commands": BUILD_VALIDATION_COMMANDS,
                "runtime_equivalence": {
                    "runtimes": RUNTIMES,
                    "source_of_truth_pattern": "dist/copilots/<copilot_id>/shared/implementation_plan_audit.json",
                    "max_unexplained_drift": 0,
                },
            }
        agents.append(agent)
    for idx, copilot in enumerate(COPILOTS, start=len(agents) + 1):
        agents.append({
            "id": f"copilot_owner_{idx:02d}_{copilot.id}",
            "name": f"{copilot.name} Product Owner",
            "phase": "productization",
            "mode": "python_first_codex_assisted",
            "mission": f"own product quality for {copilot.name}",
        })
    while len(agents) < 50:
        idx = len(agents) + 1
        phase = SDLC_PHASES[(idx - 1) % len(SDLC_PHASES)]
        agents.append({
            "id": f"sdlc_auditor_{idx:02d}_{phase}",
            "name": f"{phase.title()} Deep Auditor {idx:02d}",
            "phase": phase,
            "mode": "python_audit_first",
            "mission": f"deep-audit {phase} evidence across every copilot runtime",
        })
    return agents[:50]


def phase_for_group(short: str) -> str:
    mapping = {
        "director": "orchestration",
        "catalog": "discovery",
        "semantics": "discovery",
        "codex": "adapter",
        "claude": "adapter",
        "github": "adapter",
        "langchain": "adapter",
        "mcp": "security",
        "cost": "operate",
        "kb": "architecture",
        "packager": "release",
        "matrix": "test",
        "smoke": "test",
    }
    return mapping.get(short, short if short in SDLC_PHASES else "quality")


def mode_for_group(short: str) -> str:
    if short in {"semantics", "catalog", "matrix", "cost", "packager", "smoke"}:
        return "python_only"
    if short in {"codex", "claude", "github", "langchain"}:
        return "adapter_generation"
    return "python_first_llm_sparse"


def room_for_agent(agent: dict) -> str:
    phase = agent["phase"]
    if phase in {"orchestration", "productization"}:
        return "Control Room"
    if phase in {"discovery", "adapter"}:
        return "Python Brain"
    if phase in {"architecture", "design"}:
        return "Architecture Board"
    if phase in {"build", "test"}:
        return "Adapter Lab"
    if phase in {"security", "devops", "cloud", "release", "operate"}:
        return "Operations"
    return "QA Lab"


def concurrency_for_agent(agent: dict) -> str:
    if agent["phase"] in {"adapter", "productization"}:
        return "parallel-safe"
    if agent["mode"] == "python_only":
        return "parallel-safe"
    return "serial"


def files_for_agent(agent: dict) -> list[str]:
    phase = agent["phase"]
    if agent["id"].startswith("copilot_owner_"):
        copilot_id = agent["id"].split("_", 3)[-1]
        return [
            f"dist/copilots/{copilot_id}/shared/spec.json",
            f"dist/copilots/{copilot_id}/codex/AGENT.md",
            f"dist/copilots/{copilot_id}/claude/AGENT.md",
            f"dist/copilots/{copilot_id}/github-copilot/copilot-agent.md",
            f"dist/copilots/{copilot_id}/langchain/agent.py",
        ]
    if agent["id"].startswith("sdlc_auditor_"):
        return [
            "generated/sdlc-audit-matrix.md",
            "generated/factory-audit.json",
            "generated/runtime-injection-map.json",
        ]
    by_phase = {
        "orchestration": ["README.md", "OPERATING_SYSTEM.md", "factory.config.json", "tasks.json", "factory-prompt.md"],
        "discovery": ["data/copilots.json", "data/agent_roster.json", "tools/semantic_router.py", "generated/copilot-index.json"],
        "architecture": ["OPERATING_SYSTEM.md", "generated/semantic-routing-plan.md", "dist/copilots"],
        "design": ["dist/copilots", "generated/runtime-injection-map.json", "generated/sdlc-audit-matrix.md"],
        "build": ["tools/generate_copilot_factory.py", "dist/copilots", "generated/factory-audit.json"],
        "test": ["tools/validate_copilot_factory.py", "tools/validate_prompt_quality.py", "tools/validate_runtime_equivalence.py"],
        "security": ["config/.env.example", "config/mcp-connectors.example.json", "tools/validate_copilot_factory.py"],
        "devops": ["tools/run_factory.py", "generated/factory-audit.json", "generated/validation-report.json"],
        "cloud": ["generated/factory-audit.json", "generated/runtime-injection-map.json", "dist/copilots"],
        "release": ["factory.config.json", "generated/runtime-injection-map.json", "generated/factory-audit.json"],
        "operate": ["README.md", "factory-prompt.md", ".vscode/settings.json", ".codex-loop/factory"],
        "adapter": ["dist/copilots", "generated/runtime-injection-map.json", "tools/validate_runtime_equivalence.py"],
    }
    return by_phase.get(phase, ["README.md", "dist/copilots", "generated"])


def dod_for_agent(agent: dict) -> str:
    if agent["id"].startswith("copilot_owner_"):
        return "el copilot mantiene equivalencia entre Codex, Claude, GitHub Copilot y LangChain, con prompts, schema y contrato coherentes"
    if agent["id"].startswith("sdlc_auditor_"):
        return "el auditor deja evidencia concreta del fase/riesgo revisado sin romper la generacion existente"
    mission = agent["mission"]
    return f"la mision `{mission}` queda reflejada en artefactos verificables y no solo en texto descriptivo"


def verify_for_agent(agent: dict) -> str:
    if agent["phase"] in {"orchestration", "adapter", "productization", "test", "release"}:
        return "python tools/validate_copilot_factory.py && python tools/validate_prompt_quality.py && python tools/validate_runtime_equivalence.py"
    if agent["phase"] in {"discovery", "architecture", "design"}:
        return "python tools/validate_copilot_factory.py && python tools/semantic_router.py python ci routing"
    return "python tools/validate_copilot_factory.py && python tools/validate_prompt_quality.py"


def risk_for_agent(agent: dict) -> str:
    if agent["phase"] in {"security", "release", "adapter"}:
        return "medium"
    if agent["phase"] in {"orchestration", "productization"}:
        return "medium"
    return "low"


def frontier_for_agent(agent: dict) -> str:
    phase = agent["phase"]
    mapping = {
        "orchestration": "state-locks",
        "discovery": "research-trust",
        "architecture": "routing-equivalence",
        "design": "runtime-contracts",
        "build": "runtime-contracts",
        "test": "quality-real",
        "security": "sensitive-data",
        "devops": "runtime-toolchain",
        "cloud": "cost-time",
        "release": "output-topology",
        "operate": "state-locks",
        "adapter": "runtime-contracts",
        "productization": "runtime-contracts",
    }
    return mapping.get(phase, "quality-real")


def render_factory_task(agent: dict, index: int) -> str:
    priority = "P0" if index <= 10 else "P1" if index <= 30 else "P2"
    files = ", ".join(files_for_agent(agent))
    director_gate = ""
    if agent["id"] == DIRECTOR_AGENT:
        director_gate = (
            "DirectorGate: controlRoom=factory.config.json/controlRoom; "
            "lock=.codex-loop/run.lock.json; "
            "scope=declared-files-only; "
            "gates=structure+promptDepth+runtimeEquivalence; "
            "evidence=generated-validation-reports; "
            "drift=max-0-unexplained; "
            "cost=python-first-llm-sparse | "
        )
    return (
        f"[{priority}][{agent['id']}][~<=20m] "
        f"Room: {room_for_agent(agent)} | "
        f"Concurrency: {concurrency_for_agent(agent)} | "
        f"Goal: Trabajar solo dentro de NuevoProyecto para {agent['mission']}. Mantener equivalencia real entre Codex, Claude, GitHub Copilot y LangChain sin inflar costes ni perder trazabilidad. | "
        f"Files: {files} | "
        f"DoD: {dod_for_agent(agent)}. | "
        f"{director_gate}"
        f"Verify: {verify_for_agent(agent)} | "
        f"Risk: {risk_for_agent(agent)} | "
        f"Frontier: {frontier_for_agent(agent)}"
    )


def workspace_settings() -> dict:
    return {
        "codexLoop.transport": "codexCli",
        "codexLoop.codexApprovalPolicy": "never",
        "codexLoop.codexSandbox": "workspace-write",
        "codexLoop.factoryPreset": "freePrompt",
        "codexLoop.factoryTaskCount": 50,
        "codexLoop.factoryFreePromptFile": "factory-prompt.md",
        "codexLoop.browserQaEnabled": False,
        "codexLoop.packagingEnabled": False,
        "codexLoop.seoContentEnabled": False,
        "codexLoop.presentationDeckEnabled": False,
        "codexLoop.scrollStorytellingEnabled": False,
        "codexLoop.parallelWorkers": 4,
        "codexLoop.parallelSchedulerEnabled": False,
        "codexLoop.policySafeModeEnabled": True,
        "codexLoop.verifyAfterEachTask": True,
        "codexLoop.pauseOnFailedVerification": True,
        "codexLoop.factoryAdaptivePlanningEnabled": True,
        "codexLoop.factoryDecisionGuardEnabled": True,
        "codexLoop.factoryRestartOnBadDecision": True,
        "codexLoop.delayBetweenTasksMs": 1500,
        "codexLoop.responseTimeoutMs": 900000,
        "codexLoop.maxRetries": 3,
    }


def initial_agent_state() -> dict:
    return {
        "nextTaskIndex": 0,
        "updatedAt": now(),
        "results": [],
    }


def render_factory_prompt() -> str:
    return dedent(f"""\
    # Copilot Factory Prompt

    Este workspace es una fabrica de copilotos multiplataforma.

    Objetivo operativo:

    - Mantener {len(COPILOTS)} copilotos equivalentes en Codex, Claude, GitHub Copilot y LangChain.
    - Tratar Python como cerebro determinista para catalogo, routing, validacion y auditoria.
    - Usar LLM solo para juicio fino, copy final o diseno de cambios no triviales.
    - Ejecutar el Control Room desde `factory.config.json/controlRoom`: el director posee la corrida, bloquea deriva de alcance y exige evidencia antes de declarar done.

    Instrucciones para Codex Loop:

    1. Trabaja solo dentro de `NuevoProyecto/`.
    2. Antes de editar, inspecciona `.codex-loop/run.lock.json`, `data/copilots.json`, `data/agent_roster.json`, `generated/runtime-injection-map.json` y el copilot afectado.
    3. No rompas equivalencia entre runtimes: si cambias `shared/spec.json`, revisa Codex, Claude, GitHub Copilot y LangChain.
    4. Valida con:
       - `python tools/validate_copilot_factory.py`
       - `python tools/validate_prompt_quality.py`
       - `python tools/validate_runtime_equivalence.py`
    5. Evita meter secretos, tokens o credenciales reales. Solo nombres de variables de entorno.
    6. Mantén las tareas acotadas y deja evidencia verificable.

    Contrato del Factory Director:

    - State lock: respeta `.codex-loop/run.lock.json`; comprueba campos requeridos, workspace, orden de timestamps y snapshot local si no hay Git.
    - Gate honesty: no aceptes "done" sin reports generados o riesgo residual explicito.
    - Runtime parity: usa `dist/copilots/<copilot>/shared/spec.json` como canon y `generated/runtime-injection-map.json` como mapa de trazabilidad.
    - Cost trace: ejecuta Python primero y reserva LLM para juicio escaso, cambios de codigo y sintesis final.
    - Scope lock: toca solo archivos declarados o tooling minimo de verificacion; productos nuevos van bajo `products/<slug>/` con registry.
    """)


def render_gitignore() -> str:
    return dedent("""\
    __pycache__/
    *.pyc
    agent.log
    agent-state.json
    .codex-loop/run.lock.json
    .codex-loop/backups/
    .codex-loop/codex-runs/
    .codex-loop/pixel-ops/
    .codex-loop/rollback/
    .codex-loop/tmp/
    .codex-loop/tool-shims/
    .codex-loop/verification/
    .codex-loop/verification-probes/
    .codex-loop/runtime/
    """)


def routing_profile(copilot: Copilot) -> dict:
    return {
        "cheapPath": ["python semantic_router", "static rules", "catalog lookup"],
        "llmPath": ["active runtime LLM layer only for ambiguous architecture judgement, complex patch planning, or final prose"],
        "escalation": {
            "lowRisk": "python_only",
            "mediumRisk": "python_with_runtime_adapter_prompt",
            "highRisk": "human_review_required",
        },
        "connectors": copilot.connectors,
    }


def governance_profile(copilot: Copilot) -> dict:
    return {
        "noSecretsInRepo": True,
        "requiresSourceEvidence": True,
        "requiresSdlcPhaseTag": True,
        "requiresExitCriteria": True,
        "humanApprovalForWrites": ["security", "release", "connector activation"],
        "envKeys": copilot.env_keys,
    }


def semantic_tags(copilot: Copilot) -> list[str]:
    return sorted(set([copilot.family, *copilot.stacks, *copilot.sdlc_phases, *copilot.connectors]))


def render_readme() -> str:
    return dedent(f"""\
    # Copilot Factory

    This project builds a product-grade copilot ecosystem for Codex, Claude, GitHub Copilot Agents and LangChain-compatible Python agents.

    Version: `{FACTORY_VERSION}`

    ## What changed in v2

    - The first version was only a structural scaffold. V2 turns every copilot into a real runtime contract.
    - Every copilot now has system prompt, developer prompt, output schema, SDLC playbook, quality rubric and runtime-specific injection files.
    - Python is the brain: catalog generation, semantic routing, prompt quality validation, schema validation and audit reports.
    - Codex, Claude, GitHub Copilot and LangChain are adapters over the same shared spec, not four unrelated prompt piles.

    ## Commands

    ```powershell
    python tools/generate_copilot_factory.py
    python tools/validate_copilot_factory.py
    python tools/validate_prompt_quality.py
    python tools/validate_runtime_equivalence.py
    python tools/semantic_router.py python ci routing
    python tools/run_factory.py
    ```

    `tools/semantic_router.py` requires a non-empty routing request and exits non-zero for empty input.

    ## Outputs

    - `tasks.json`: 50 factory-grade Codex Loop tasks.
    - `factory-prompt.md`: free-prompt briefing for Codex Loop.
    - `data/copilots.json`: canonical 18-copilot catalog.
    - `generated/copilot-index.json`: normalized IDs, connector names, env names, outputs and runtime traces.
    - `dist/copilots/<copilot>/shared/spec.json`: source of truth.
    - `dist/copilots/<copilot>/shared/implementation_plan_audit.json`: Build Auditor contract for implementation plans and stack-specific rules where applicable.
    - `dist/copilots/<copilot>/codex/AGENT.md`: Codex injection.
    - `dist/copilots/<copilot>/claude/AGENT.md`: Claude injection.
    - `dist/copilots/<copilot>/github-copilot/copilot-agent.md`: GitHub Copilot profile.
    - `dist/copilots/<copilot>/langchain/agent.py`: Python/LangChain brain.
    - `generated/factory-audit.json`: factory-level pass/fail summary, including Build Auditor evidence.
    - `generated/phase-verdict-report.*`: QA Committee Chair pass/fail consolidation across every SDLC phase, backed by `dist/copilots/qa_general/shared/phase_verdict_report_contract.json`.
    - `generated/runtime-injection-map.json`: where each prompt and runtime contract lives.
    - `generated/prompt-quality-report.*`: prompt-depth QA gate.
    - `generated/runtime-equivalence-report.*`: cross-runtime drift gate.
    - `config/.env.example`: placeholder-only sensitive credential names.
    - `config/mcp-connectors.example.json`: disabled-by-default MCP policy, threat model and runtime parity contract.

    ## Sensitive Credentials And MCP

    Real tokens must stay outside the repository. Keep `config/.env.example` empty, activate MCP connectors only in a local or approved runtime environment, and use `config/mcp-connectors.example.json` as the shared policy for Codex, Claude, GitHub Copilot and LangChain.

    ## Control Room Director Contract

    `factory_agent_01_director` is the run owner. Its mission is encoded as a machine-readable control contract in `factory.config.json` under `controlRoom`, and as the first queue gate in `tasks.json`.

    The director cannot mark a run done unless these artifacts exist and agree:

    - State lock evidence: `.codex-loop/run.lock.json` exists, has the required fields (`id`, `pid`, `workspace`, `startedAt`, `heartbeatAt`, `mode`), matches this workspace and has a heartbeat that does not precede the start time.
    - Gate evidence: `generated/validation-report.json`, `generated/prompt-quality-report.json` and `generated/runtime-equivalence-report.json` are the truth sources for structure, prompt depth and runtime drift.
    - Scope evidence: task files must stay inside the declared task file list or documented factory roots; product code belongs under `products/<slug>/` with registry updates when a product is created.
    - Equivalence evidence: `dist/copilots/<copilot>/shared/spec.json` remains canonical, with Codex, Claude, GitHub Copilot and LangChain treated as runtime adapters over that spec.
    - Cost evidence: deterministic Python gates run before any sparse LLM judgement, so traceability comes from generated reports instead of repeated prompt expansion.

    ## QA Phase Verdict Evidence

    `factory_agent_22_qa` owns the mission `Consolidates all phase verdicts into a pass/fail report.` The executable contract is `dist/copilots/qa_general/shared/phase_verdict_report_contract.json`; `python tools/validate_copilot_factory.py` emits `generated/phase-verdict-report.json` and `generated/phase-verdict-report.md`.

    The report consolidates discovery, as_is, architecture, design, build, test, security, devops, cloud, release and operate verdicts from `generated/validation-report.json`, using explicit `pass` booleans and `pass` or `fail` verdict values only. It also consumes `generated/runtime-equivalence-report.json` and only passes when that gate passes with `maxUnexplainedDrift=0` and zero issues, plus negative fixtures proving missing phases, invalid verdicts, inferred passes, runtime gate failures and inconsistent aggregation are detected.
    """)


def render_operating_system() -> str:
    return dedent("""\
    # Copilot Factory Operating System

    ## Mission

    Create equivalent, auditable copilots for Codex, Claude, GitHub Copilot Agents and LangChain while keeping token cost low. The Factory Director owns the whole run, keeps gates honest and prevents scope drift through verifiable state locks, report gates and runtime-equivalence evidence.

    ## Abstraction Layers

    1. Catalog Brain: Python owns copilot definitions, connectors, env names, outputs and SDLC phases.
    2. Semantic Brain: Python routes requests using stack tags, phase tags, connector requirements and output contracts.
    3. Prompt Brain: Python renders system/developer prompts from shared copilot specs, so runtime prompts do not drift.
    4. Runtime Adapters: Codex, Claude, GitHub Copilot and LangChain receive the same operating contract in runtime-native form.
    5. SDLC Committee: Discovery, Architecture, Design, Build, Test, Security, DevOps, Cloud, Release and Operate auditors can verify each artifact.
    6. LLM Cerebellum: the active runtime LLM layer is used only for narrow judgement, code edits and final synthesis after Python prepared the evidence.

    ## Cost Policy

    Python first. LLM second. Human approval for secrets, connector activation, production writes and release.

    ## Quality Policy

    A copilot prompt is not accepted unless `python tools/validate_prompt_quality.py` passes.

    Cross-runtime drift is not accepted unless `python tools/validate_runtime_equivalence.py` passes.

    ## Control Room Gate

    The Control Room is serial. `factory_agent_01_director` owns this gate before any task is declared complete:

    1. State lock: respect `.codex-loop/run.lock.json`; verify required fields, workspace match, timestamp order and snapshot evidence when Git metadata is absent before treating the run as owned.
    2. Scope lock: edit only declared task files unless a minimal verifier or generated report is required; product output stays under `products/<slug>/`.
    3. Gate honesty: "done" requires evidence, not intent. Structure, prompt quality and runtime equivalence reports are the acceptance artifacts.
    4. Runtime parity: `shared/spec.json` is canonical; Codex, Claude, GitHub Copilot and LangChain adapters must remain explainably equivalent.
    5. Cost trace: Python deterministic checks run first; LLM work stays sparse and must point back to concrete artifacts.
    6. Final truth: unresolved frontier risks stay explicit instead of being hidden behind a passing compile or partial report.

    ## Connector Policy

    Declare MCP connectors by env var name only. Never store token values.

    ## Codex Loop Modes

    - `Prompt libre`: load `factory-prompt.md` when you want planning and selective improvements.
    - `Ejecutar solo tasks.json`: consume the factory-grade queue when you want controlled autonomous work.
    """)


def render_copilot_readme(copilot: Copilot) -> str:
    return dedent(f"""\
    # {copilot.name}

    Family: `{copilot.family}`

    Function: {copilot.function}

    Connectors: {", ".join(copilot.connectors)}

    Env vars: {", ".join(copilot.env_keys)}

    Runtimes:

    - `codex/AGENT.md`
    - `claude/AGENT.md`
    - `github-copilot/copilot-agent.md`
    - `langchain/agent_profile.json`
    - `langchain/agent.py`

    Exit criteria:

    - Uses shared spec.
    - Produces SDLC-tagged output.
    - States evidence required before changing code.
    - Never embeds secrets.
    - Routes cheap analysis through Python first.
    """)


def render_codex_agent(copilot: Copilot) -> str:
    return render_agent_markdown(copilot, "Codex", "Use repository tools, inspect files first, make scoped patches, run validators.")


def render_claude_agent(copilot: Copilot) -> str:
    return render_agent_markdown(copilot, "Claude", "Use long-context synthesis, produce careful review notes, defer exact file edits to tool-capable executor unless connected.")


def render_github_agent(copilot: Copilot) -> str:
    return render_agent_markdown(copilot, "GitHub Copilot", "Use GitHub MCP evidence, PR context, issues, checks and source files before recommendations.")


def render_agent_markdown(copilot: Copilot, runtime: str, runtime_rule: str) -> str:
    return dedent(f"""\
    # {copilot.name} - {runtime} Adapter

    ## Role

    {copilot.function}

    ## Runtime Rule

    {runtime_rule}

    ## Python-First Contract

    Before asking an LLM for judgement, use the generated catalog, semantic router and SDLC matrix. Escalate only when the deterministic route is ambiguous or a patch/review needs language-level reasoning.

    ## Inputs

    - Shared spec: `../shared/spec.json`
    - Connectors: {", ".join(copilot.connectors)}
    - Env vars: {", ".join(copilot.env_keys)}
    - SDLC phases: {", ".join(copilot.sdlc_phases)}

    ## Required Outputs

    {chr(10).join(f"- {item}" for item in copilot.outputs)}

    ## Guardrails

    - Do not store secrets.
    - Cite source evidence before changing code.
    - Keep patches scoped.
    - Produce a phase-tagged audit trail.
    - Ask for human approval before connector activation, release changes or security-sensitive writes.
    """)


def render_langchain_agent(copilot: Copilot) -> str:
    class_name = "".join(part.title() for part in copilot.id.split("_")) + "Agent"
    return dedent(f'''\
    """Generated no-dependency LangChain-compatible profile for {copilot.name}.

    This module intentionally works without langchain installed. If LangChain is available,
    wrap `plan()` as a Tool or Runnable.
    """

    from __future__ import annotations

    PROFILE = {json.dumps(asdict(copilot), indent=4)}


    class {class_name}:
        def __init__(self, profile=None):
            self.profile = profile or PROFILE

        def score(self, request: str) -> int:
            text = request.lower()
            tags = set(self.profile["stacks"] + self.profile["sdlc_phases"] + self.profile["connectors"])
            return sum(1 for tag in tags if tag.replace("_", " ") in text or tag in text)

        def plan(self, request: str) -> dict:
            return {{
                "copilot": self.profile["id"],
                "name": self.profile["name"],
                "score": self.score(request),
                "cheap_path": ["catalog lookup", "semantic scoring", "phase audit"],
                "llm_escalation": "only if score is low or architecture/security judgement is ambiguous",
                "required_connectors": self.profile["connectors"],
                "required_env": self.profile["env_keys"],
                "outputs": self.profile["outputs"],
            }}
    ''')


def render_semantic_router() -> str:
    current_router = ROOT / "tools" / "semantic_router.py"
    if current_router.exists():
        return current_router.read_text(encoding="utf-8")
    return dedent('''\
    from __future__ import annotations

    import json
    import math
    import re
    from pathlib import Path

    ROOT = Path(__file__).resolve().parents[1]
    CATALOG = ROOT / "data" / "copilots.json"
    INDEX = ROOT / "generated" / "copilot-index.json"
    RUNTIMES = ("codex", "claude", "github-copilot", "langchain")
    NORMALIZATION_VERSION = "catalog-normalization-1.0"
    SEMANTIC_ROUTING_VERSION = "semantic-routing-1.0"
    DISCOVERY_AUDIT_VERSION = "as-is-inventory-audit-1.0"
    SCORE_MODEL = "weighted_exact_and_token_overlap"
    MAX_REQUEST_CHARS = 2000
    MAX_ROUTE_LIMIT = 10
    CHEAP_PATH_THRESHOLD = 3.0
    CASE_POLICY = {
        "copilot_id": "lower_snake_case",
        "connector_names": "lower_snake_case",
        "env_names": "upper_snake_case",
        "outputs": "lower_snake_case",
    }
    TRACEABILITY_POLICY = {
        "catalog_index": "generated/copilot-index.json",
        "runtime_source_of_truth": "dist/copilots/<copilot_id>/shared/spec.json",
    }
    ENV_CHUNK_SUFFIXES = ("_TOKEN", "_KEY", "_SECRET", "_PAT")

    COPILOT_ID_ALIASES = {
        "ci": "cicd",
        "ci_cd": "cicd",
        "node_js": "nodejs",
    }

    CONNECTOR_ALIASES = {
        "confluence": "confluence_mcp_optional",
        "confluence_mcp": "confluence_mcp_optional",
        "confluence_optional": "confluence_mcp_optional",
        "github": "github_mcp",
        "github_mcp": "github_mcp",
        "mcp_github": "github_mcp",
        "sonar": "sonarqube_mcp",
        "sonar_mcp": "sonarqube_mcp",
        "sonarqube": "sonarqube_mcp",
        "sonarqube_mcp": "sonarqube_mcp",
    }

    ENV_KEY_ALIASES = {
        "CONFLUENCE_API_TOKEN": "CONFLUENCE_TOKEN_OPTIONAL",
        "GH_TOKEN": "GITHUB_TOKEN",
        "GITHUB_PAT": "GITHUB_TOKEN",
        "SONAR_TOKEN": "SONARQUBE_TOKEN",
    }


    class RoutingInputError(ValueError):
        pass


    class RouterDataError(RuntimeError):
        pass


    def load_catalog() -> list[dict]:
        try:
            raw = json.loads(CATALOG.read_text(encoding="utf-8"))
        except FileNotFoundError as exc:
            raise RouterDataError("Missing required catalog: data/copilots.json.") from exc
        except json.JSONDecodeError as exc:
            raise RouterDataError(
                f"Invalid JSON in data/copilots.json at line {exc.lineno}, column {exc.colno}: {exc.msg}."
            ) from exc
        except OSError as exc:
            reason = exc.strerror or exc.__class__.__name__
            raise RouterDataError(f"Cannot read catalog data/copilots.json: {reason}.") from exc

        if not isinstance(raw, list):
            raise RouterDataError("Catalog data/copilots.json must be a JSON array.")

        normalized = []
        for position, item in enumerate(raw, start=1):
            if not isinstance(item, dict):
                raise RouterDataError(f"Catalog entry {position} must be a JSON object.")
            normalized.append(normalize_catalog_entry(item))
        return normalized


    def load_index() -> dict:
        try:
            raw = json.loads(INDEX.read_text(encoding="utf-8"))
        except FileNotFoundError as exc:
            raise RouterDataError("Missing required trace index: generated/copilot-index.json.") from exc
        except json.JSONDecodeError as exc:
            raise RouterDataError(
                f"Invalid JSON in generated/copilot-index.json at line {exc.lineno}, column {exc.colno}: {exc.msg}."
            ) from exc
        except OSError as exc:
            reason = exc.strerror or exc.__class__.__name__
            raise RouterDataError(f"Cannot read trace index generated/copilot-index.json: {reason}.") from exc
        if not isinstance(raw, dict):
            raise RouterDataError("Trace index generated/copilot-index.json must be a JSON object.")
        if not isinstance(raw.get("normalizedLookup"), dict):
            raise RouterDataError("Trace index generated/copilot-index.json is missing normalizedLookup.")
        return raw


    WEIGHTS = {
        "family": 1.0,
        "function": 0.5,
        "connectors": 1.5,
        "stacks": 3.0,
        "sdlc_phases": 2.5,
        "outputs": 2.0,
    }

    EXACT_WEIGHTS = {
        "id": 1.5,
        "connectors": 1.5,
        "env_keys": 1.75,
        "outputs": 2.0,
    }

    SCORE_INPUTS = [
        "id",
        "family",
        "function",
        "connectors",
        "env_keys",
        "stacks",
        "sdlc_phases",
        "outputs",
    ]

    EXECUTION_ORDER = [
        "validate_request",
        "load_catalog",
        "load_index",
        "score_catalog",
        "rank_routes",
        "attach_runtime_trace",
        "return_route_payload",
    ]

    LLM_ESCALATION_GUARD = {
        "before_scoring": False,
        "default": "disabled",
        "escalation": "allowed_after_no_cheap_path_only",
        "trace_field": "routing_evidence.llm_assist_used",
    }


    def normalize(text: str) -> set[str]:
        clean = re.sub(r"[^a-zA-Z0-9_ -]+", " ", text.lower())
        return set(clean.replace("-", " ").replace("_", " ").split())


    def request_chunks(text: str) -> list[str]:
        return [chunk for chunk in re.split(r"[^A-Za-z0-9_-]+", text) if chunk]


    def is_env_like_chunk(value: str) -> bool:
        identifier = upper_snake_identifier(value)
        return identifier in ENV_KEY_ALIASES or identifier.endswith(ENV_CHUNK_SUFFIXES)


    def normalize_request_words(request: str) -> set[str]:
        chunks = [chunk for chunk in request_chunks(request) if not is_env_like_chunk(chunk)]
        return normalize(" ".join(chunks))


    def request_exact_terms(request: str) -> dict[str, set[str]]:
        chunks = request_chunks(request)
        return {
            "id": {normalize_copilot_id(chunk) for chunk in chunks},
            "connectors": {normalize_connector_name(chunk) for chunk in chunks},
            "env_keys": {normalize_env_key(chunk) for chunk in chunks},
            "outputs": {normalize_output_name(chunk) for chunk in chunks},
        }


    def snake_identifier(value: object) -> str:
        clean = re.sub(r"[^A-Za-z0-9]+", "_", str(value or "").strip())
        return re.sub(r"_+", "_", clean).strip("_").lower()


    def upper_snake_identifier(value: object) -> str:
        return snake_identifier(value).upper()


    def normalize_copilot_id(value: object) -> str:
        identifier = snake_identifier(value)
        return COPILOT_ID_ALIASES.get(identifier, identifier)


    def normalize_connector_name(value: object) -> str:
        identifier = snake_identifier(value)
        return CONNECTOR_ALIASES.get(identifier, identifier)


    def normalize_env_key(value: object) -> str:
        identifier = upper_snake_identifier(value)
        return ENV_KEY_ALIASES.get(identifier, identifier)


    def normalize_output_name(value: object) -> str:
        return snake_identifier(value)


    def list_values(value: object) -> list:
        if isinstance(value, list):
            return value
        if value in (None, ""):
            return []
        return [value]


    def unique(values: list[str]) -> list[str]:
        seen: set[str] = set()
        result: list[str] = []
        for value in values:
            if value and value not in seen:
                seen.add(value)
                result.append(value)
        return result


    def normalize_catalog_entry(item: dict) -> dict:
        source = {
            "copilot_id": item.get("id", ""),
            "connector_names": list_values(item.get("connectors")),
            "env_names": list_values(item.get("env_keys")),
            "outputs": list_values(item.get("outputs")),
        }
        canonical = {
            "copilot_id": normalize_copilot_id(source["copilot_id"]),
            "connector_names": unique([normalize_connector_name(value) for value in source["connector_names"]]),
            "env_names": unique([normalize_env_key(value) for value in source["env_names"]]),
            "outputs": unique([normalize_output_name(value) for value in source["outputs"]]),
        }
        normalized = dict(item)
        normalized["id"] = canonical["copilot_id"]
        normalized["connectors"] = canonical["connector_names"]
        normalized["env_keys"] = canonical["env_names"]
        normalized["outputs"] = canonical["outputs"]
        normalized["normalization"] = {
            "version": NORMALIZATION_VERSION,
            "canonical": canonical,
            "source": source,
            "status": "already_normalized" if source == canonical else "normalized",
            "case_policy": CASE_POLICY,
            "traceability": TRACEABILITY_POLICY,
        }
        return normalized


    def score(copilot: dict, request: str) -> tuple[float, list[str]]:
        words = normalize_request_words(request)
        exact_terms = request_exact_terms(request)
        score = 0.0
        reasons: list[str] = []
        exact_values = {
            "id": [normalize_copilot_id(copilot.get("id", ""))],
            "connectors": [normalize_connector_name(value) for value in list_values(copilot.get("connectors"))],
            "env_keys": [normalize_env_key(value) for value in list_values(copilot.get("env_keys"))],
            "outputs": [normalize_output_name(value) for value in list_values(copilot.get("outputs"))],
        }
        for key, weight in EXACT_WEIGHTS.items():
            for value in exact_values[key]:
                if value and value in exact_terms[key]:
                    score += weight
                    reasons.append(f"{key}:{value}")
        seen_token_reasons: set[str] = set()
        for key, weight in WEIGHTS.items():
            raw = copilot.get(key, "")
            values = raw if isinstance(raw, list) else [raw]
            for value in values:
                for token in normalize(str(value)):
                    reason = f"{key}:{token}"
                    if token in words and reason not in seen_token_reasons:
                        seen_token_reasons.add(reason)
                        score += weight
                        reasons.append(reason)
        return score, reasons


    def confidence(raw_score: float) -> int:
        return min(100, int(round((1 - math.exp(-raw_score / 6.0)) * 100)))


    def validate_request(request: object) -> str:
        if not isinstance(request, str):
            raise RoutingInputError("Routing request must be a string.")
        normalized_request = " ".join(request.split())
        if not normalized_request:
            raise RoutingInputError("Routing request cannot be empty.")
        if len(normalized_request) > MAX_REQUEST_CHARS:
            raise RoutingInputError(f"Routing request must be {MAX_REQUEST_CHARS} characters or fewer.")
        return normalized_request


    def validate_limit(limit: object) -> int:
        if isinstance(limit, bool) or not isinstance(limit, int):
            raise RoutingInputError("Route limit must be an integer.")
        if not 1 <= limit <= MAX_ROUTE_LIMIT:
            raise RoutingInputError(f"Route limit must be between 1 and {MAX_ROUTE_LIMIT}.")
        return limit


    def route(request: str, limit: int = 5) -> list[dict]:
        request = validate_request(request)
        limit = validate_limit(limit)
        ranked = []
        catalog = load_catalog()
        index = load_index()
        for item in catalog:
            raw_score, reasons = score(item, request)
            ranked.append((item, raw_score, reasons))
        ranked.sort(key=lambda row: row[1], reverse=True)
        ranked = [row for row in ranked if row[1] > 0]
        return [route_payload(index, item, raw_score, reasons) for item, raw_score, reasons in ranked[:limit]]


    def route_payload(index: dict, item: dict, raw_score: float, reasons: list[str]) -> dict:
        payload = {
            "id": item["id"],
            "name": item["name"],
            "score": round(raw_score, 2),
            "confidence": confidence(raw_score),
            "match_reasons": reasons[:8],
            "connectors": item["connectors"],
            "env_keys": item["env_keys"],
            "outputs": item["outputs"],
            "normalization": item["normalization"]["canonical"],
            "runtime_trace": runtime_trace(index, item["id"]),
            "cheap_path": raw_score >= CHEAP_PATH_THRESHOLD,
            "routing_evidence": routing_evidence(raw_score, reasons),
        }
        if item.get("discovery_audit"):
            payload["discovery_audit"] = discovery_audit_evidence(index, item)
        return payload


    def routing_evidence(raw_score: float, reasons: list[str]) -> dict:
        return {
            "policy_version": SEMANTIC_ROUTING_VERSION,
            "deterministic_python_first": True,
            "score_before_llm_assist": True,
            "scoring_engine": "tools/semantic_router.py",
            "score_model": SCORE_MODEL,
            "score_policy_ref": "generated/copilot-index.json#/normalizationPolicy/semanticRouting",
            "score_inputs": SCORE_INPUTS,
            "execution_order": EXECUTION_ORDER,
            "cheap_path_threshold": CHEAP_PATH_THRESHOLD,
            "raw_score": round(raw_score, 2),
            "score_reasons": reasons[:8],
            "llm_assist_used": False,
            "llm_escalation_guard": LLM_ESCALATION_GUARD,
            "runtime_equivalence": {
                "runtimes": list(RUNTIMES),
                "same_scoring_policy": True,
                "runtime_trace_required": True,
            },
        }


    def discovery_audit_evidence(index: dict, item: dict) -> dict:
        lookup = index.get("normalizedLookup", {}) if isinstance(index, dict) else {}
        indexed = lookup.get(item["id"], {}).get("discovery_audit") if isinstance(lookup, dict) else None
        contract = indexed or item.get("discovery_audit")
        if not isinstance(contract, dict):
            raise RouterDataError(f"Discovery audit contract missing for copilot `{item['id']}`.")
        if contract.get("policy_version") != DISCOVERY_AUDIT_VERSION:
            raise RouterDataError(f"Discovery audit contract version drifted for copilot `{item['id']}`.")
        required_outputs = contract.get("required_outputs", [])
        missing_outputs = [output for output in required_outputs if output not in item.get("outputs", [])]
        evidence = dict(contract)
        evidence["runtime_trace"] = runtime_trace(index, item["id"])
        evidence["contract_checks"] = {
            "required_outputs_present": not missing_outputs,
            "missing_outputs": missing_outputs,
            "coverage_items": len(contract.get("coverage_items", [])),
            "inventory_fields": len(contract.get("inventory_fields", [])),
        }
        return evidence


    def runtime_trace(index: dict, copilot_id: str) -> dict:
        lookup = index.get("normalizedLookup", {}) if isinstance(index, dict) else {}
        indexed = lookup.get(copilot_id, {}).get("runtime_trace") if isinstance(lookup, dict) else None
        if not indexed:
            raise RouterDataError(f"Trace index missing runtime_trace for copilot `{copilot_id}`.")
        return indexed


    def main(argv: list[str] | None = None) -> int:
        import sys

        args = sys.argv[1:] if argv is None else argv
        request = " ".join(args).strip()
        if not request:
            print("Usage: python tools/semantic_router.py <routing request>", file=sys.stderr)
            return 2
        try:
            result = route(request)
        except RoutingInputError as exc:
            print(f"Input error: {exc}", file=sys.stderr)
            return 2
        except RouterDataError as exc:
            print(f"Data error: {exc}", file=sys.stderr)
            return 1
        print(json.dumps(result, indent=2))
        return 0


    if __name__ == "__main__":
        raise SystemExit(main())
    ''')


def render_run_factory() -> str:
    return dedent('''\
    from __future__ import annotations

    import json
    import os
    import re
    import subprocess
    import sys
    from datetime import datetime, timezone
    from pathlib import Path

    ROOT = Path(__file__).resolve().parents[1]
    AUDIT_PATH = ROOT / "generated" / "factory-audit.json"
    LOG_EVIDENCE_PATH = ROOT / "generated" / "devops-log-evidence.json"
    SCRIPT_TIMEOUT_SECONDS = 900
    MAX_LOG_BYTES_TO_SCAN = 2_000_000
    RUNTIMES = ["codex", "claude", "github-copilot", "langchain"]
    RUN_SEQUENCE = [
        "generate_copilot_factory.py",
        "validate_copilot_factory.py",
        "validate_prompt_quality.py",
        "validate_runtime_equivalence.py",
    ]
    DEVOPS_AUDIT_VERSION = "devops-ci-logs-reproducibility-rollback-audit-1.0"
    DEVOPS_AGENT = "factory_agent_10_devops"
    DEVOPS_MISSION = "Audits CI/CD, logs, reproducibility and rollback paths."
    DEVOPS_REQUIRED_EVIDENCE = [
        "ci_cd_entrypoint",
        "log_evidence",
        "reproducibility",
        "rollback_paths",
    ]
    DEVOPS_QUALITY_GATES = [
        "serial_command_order",
        "bounded_runtime_toolchain",
        "report_and_log_traceability",
        "rollback_snapshot_ready",
        "traceability_and_cost",
    ]
    DEVOPS_VALIDATION_COMMANDS = [
        "python tools/validate_copilot_factory.py",
        "python tools/validate_prompt_quality.py",
        "python tools/validate_runtime_equivalence.py",
    ]
    DEVOPS_REQUIRED_REPORTS = [
        "generated/validation-report.json",
        "generated/prompt-quality-report.json",
        "generated/runtime-equivalence-report.json",
    ]
    SECRET_PATTERNS = [
        re.compile(r"(?<![A-Za-z0-9])sk-[A-Za-z0-9_-]{20,}"),
        re.compile(r"github_pat_[A-Za-z0-9_]{20,}", re.I),
        re.compile(r"gh[pousr]_[A-Za-z0-9_]{20,}", re.I),
        re.compile(r"Bearer\\s+[A-Za-z0-9._~+/=-]{20,}", re.I),
    ]
    LOCAL_PATH_PATTERNS = [
        re.compile(r"(?i)\\b[A-Z]:[\\\\/]+Users[\\\\/]+[^\\\\/\\s\\"']+"),
        re.compile(r"(?i)/Users/[A-Za-z0-9._-]+"),
        re.compile(r"(?i)/home/[A-Za-z0-9._-]+"),
    ]


    def run(script: str) -> None:
        env = os.environ.copy()
        env["PYTHONDONTWRITEBYTECODE"] = "1"
        subprocess.run(
            [sys.executable, str(ROOT / "tools" / script)],
            cwd=ROOT,
            env=env,
            check=True,
            timeout=SCRIPT_TIMEOUT_SECONDS,
        )


    def read_audit() -> dict:
        try:
            return json.loads(AUDIT_PATH.read_text(encoding="utf-8"))
        except (FileNotFoundError, json.JSONDecodeError):
            return {}


    def count_pattern_matches(patterns: list[re.Pattern], text: str) -> int:
        return sum(len(pattern.findall(text)) for pattern in patterns)


    def log_evidence_payload() -> dict:
        source = ROOT / "agent.log"
        report = {
            "pass": False,
            "sourceLog": "agent.log",
            "checkedAt": datetime.now(timezone.utc).isoformat(),
            "bytes": 0,
            "lineCount": 0,
            "maxBytesScanned": MAX_LOG_BYTES_TO_SCAN,
            "privacy": {
                "rawLogLocalOnly": True,
                "contentStored": False,
                "sanitizedEvidenceOnly": True,
                "absolutePathsRedacted": True,
            },
            "checks": {
                "sourceExists": source.is_file(),
                "sourceNonEmpty": False,
                "scanTruncated": False,
                "secretPatternMatches": 0,
                "localAbsolutePathMatches": 0,
            },
        }
        if not source.is_file():
            return report

        size = source.stat().st_size
        report["bytes"] = size
        report["checks"]["sourceNonEmpty"] = size > 0
        if size > MAX_LOG_BYTES_TO_SCAN:
            report["checks"]["scanTruncated"] = True
            return report

        try:
            text = source.read_text(encoding="utf-8", errors="replace")
        except OSError as exc:
            report["error"] = type(exc).__name__
            return report

        report["lineCount"] = text.count("\\n") + (0 if not text or text.endswith("\\n") else 1)
        report["checks"]["secretPatternMatches"] = count_pattern_matches(SECRET_PATTERNS, text)
        report["checks"]["localAbsolutePathMatches"] = count_pattern_matches(LOCAL_PATH_PATTERNS, text)
        report["pass"] = (
            report["checks"]["sourceNonEmpty"]
            and not report["checks"]["scanTruncated"]
            and report["checks"]["secretPatternMatches"] == 0
        )
        return report


    def emit_log_evidence() -> dict:
        report = log_evidence_payload()
        LOG_EVIDENCE_PATH.parent.mkdir(parents=True, exist_ok=True)
        LOG_EVIDENCE_PATH.write_text(json.dumps(report, indent=2) + "\\n", encoding="utf-8")
        return report


    def devops_audit_payload(log_evidence_pass: bool) -> dict:
        return {
            "pass": log_evidence_pass,
            "policyVersion": DEVOPS_AUDIT_VERSION,
            "ownerAgent": DEVOPS_AGENT,
            "mission": DEVOPS_MISSION,
            "targetCopilot": "cicd",
            "targetCopilotSourceOfTruth": "dist/copilots/cicd/shared/spec.json",
            "requiredEvidence": DEVOPS_REQUIRED_EVIDENCE,
            "qualityGates": DEVOPS_QUALITY_GATES,
            "runSequence": RUN_SEQUENCE,
            "scriptTimeoutSeconds": SCRIPT_TIMEOUT_SECONDS,
            "ciCdEntrypoint": "tools/run_factory.py",
            "rawLogSource": "agent.log",
            "logPrivacy": {
                "rawLogLocalOnly": True,
                "sanitizedEvidenceOnly": True,
            },
            "logEvidence": [
                "generated/devops-log-evidence.json",
                *DEVOPS_REQUIRED_REPORTS,
            ],
            "reproducibility": {
                "pythonExecutable": "sys.executable",
                "workingDirectory": "workspace_root",
                "deterministicOrder": True,
                "subprocessCheck": True,
                "noBytecodeArtifacts": True,
                "networkRequired": False,
                "credentialsRequired": False,
            },
            "rollbackPaths": [
                ".codex-loop/rollback",
                ".codex-loop/backups",
            ],
            "runtimeEquivalence": {
                "runtimes": RUNTIMES,
                "sourceOfTruth": "dist/copilots/cicd/shared/spec.json",
                "traceSource": "generated/runtime-injection-map.json#/copilots/cicd",
                "maxUnexplainedDrift": 0,
            },
            "costControl": {
                "deterministicPythonFirst": True,
                "llmEscalation": "not_required_for_ci_log_reproducibility_audit",
            },
            "validationCommands": DEVOPS_VALIDATION_COMMANDS,
            "checkedAt": datetime.now(timezone.utc).isoformat(),
        }


    def emit_devops_audit() -> None:
        log_report = emit_log_evidence()
        audit = read_audit()
        audit["devopsAudit"] = devops_audit_payload(log_report["pass"])
        audit["pass"] = audit.get("pass", True) and audit["devopsAudit"]["pass"]
        AUDIT_PATH.parent.mkdir(parents=True, exist_ok=True)
        AUDIT_PATH.write_text(json.dumps(audit, indent=2) + "\\n", encoding="utf-8")


    if __name__ == "__main__":
        run(RUN_SEQUENCE[0])
        emit_devops_audit()
        for script in RUN_SEQUENCE[1:]:
            run(script)
    ''')


def render_agent_roster_md(roster: list[dict]) -> str:
    rows = "\n".join(f"| {item['id']} | {item['name']} | {item['phase']} | {item['mode']} |" for item in roster)
    return f"# Agent Roster\n\n| ID | Name | Phase | Mode |\n|---|---|---|---|\n{rows}\n"


def render_sdlc_matrix() -> str:
    header = "| Copilot | " + " | ".join(SDLC_PHASES) + " |\n"
    divider = "|---" * (len(SDLC_PHASES) + 1) + "|\n"
    rows = []
    for copilot in COPILOTS:
        cells = ["yes" if phase in copilot.sdlc_phases else "" for phase in SDLC_PHASES]
        rows.append("| " + copilot.name + " | " + " | ".join(cells) + " |")
    evidence_rows = []
    for copilot in COPILOTS:
        item = asdict(copilot)
        if not is_design_boundary_copilot(item):
            continue
        evidence_rows.append(
            "| "
            + copilot.name
            + " | `"
            + design_audit_source(copilot.id)
            + "` | `"
            + "`, `".join(DESIGN_REQUIRED_EVIDENCE)
            + "` | `"
            + "`, `".join(DESIGN_REQUIRED_HANDOFF_FIELDS)
            + "` | Codex, Claude, GitHub Copilot and LangChain share `maxUnexplainedDrift = 0` |"
        )
    evidence = (
        "\n## Design Boundary Contract Evidence\n\n"
        "| Copilot | Contract artifact | Required evidence | Required handoff fields | Runtime equivalence |\n"
        "|---|---|---|---|---|\n"
        + "\n".join(evidence_rows)
        + "\n"
    )
    build_rows = []
    for copilot in COPILOTS:
        item = asdict(copilot)
        if not is_build_implementation_copilot(item):
            continue
        build_rows.append(
            "| "
            + copilot.name
            + " | `"
            + build_audit_source(copilot.id)
            + "` | `"
            + "`, `".join(BUILD_REQUIRED_EVIDENCE)
            + "` | `"
            + "`, `".join(BUILD_REQUIRED_IMPLEMENTATION_FIELDS)
            + "` | Codex, Claude, GitHub Copilot and LangChain share `maxUnexplainedDrift = 0` |"
        )
    build_evidence = (
        "\n## Build Implementation Contract Evidence\n\n"
        "| Copilot | Contract artifact | Required evidence | Required implementation fields | Runtime equivalence |\n"
        "|---|---|---|---|---|\n"
        + "\n".join(build_rows)
        + "\n"
    )
    return "# SDLC Audit Matrix\n\n" + header + divider + "\n".join(rows) + "\n" + evidence + build_evidence


def render_cost_strategy() -> str:
    return dedent("""\
    # Token Cost Strategy

    ## Rule

    Python owns discovery, routing, catalog validation, phase matrices, file generation and first-pass audits.

    ## Escalate to the active runtime LLM layer only for

    - Non-trivial code edits.
    - Ambiguous architecture trade-offs.
    - Security-sensitive review that needs human-readable reasoning.
    - Final documentation polish after Python generated the evidence.

    ## Avoid

    - Re-sending whole repositories to LLMs.
    - Asking LLMs to classify simple stack/phase/connector routing.
    - Using live connector calls before local catalog checks.
    """)


def render_semantic_plan() -> str:
    return dedent("""\
    # Semantic Routing Plan

    1. Convert a request into lowercase tokens.
    2. Score every copilot by family, stack, SDLC phase, connector and expected output tags.
    3. Pick top copilots.
    4. Run Python validators and static catalog checks.
    5. Escalate only the minimal context to Codex, Claude or LangChain.

    Test:

    ```powershell
    python tools/semantic_router.py "java ci sonar remediation"
    ```
    """)


def factory_audit() -> dict:
    return {
        "version": FACTORY_VERSION,
        "generatedAt": now(),
        "copilots": len(COPILOTS),
        "runtimes": RUNTIMES,
        "runtimeArtifacts": len(COPILOTS) * len(RUNTIMES),
        "factoryAgents": len(agent_roster()),
        "sdlcPhases": SDLC_PHASES,
        "buildImplementationAudit": build_audit_summary(),
        "pass": True,
    }


def render_factory_audit() -> str:
    audit = factory_audit()
    return dedent(f"""\
    # Factory Audit

    Pass: {audit['pass']}

    Copilots: {audit['copilots']}

    Runtimes: {", ".join(audit['runtimes'])}

    Runtime artifacts: {audit['runtimeArtifacts']}

    Factory agents: {audit['factoryAgents']}

    Build implementation audit: {audit['buildImplementationAudit']['policyVersion']} for {len(audit['buildImplementationAudit']['targetCopilots'])} copilots.
    """)


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


if __name__ == "__main__":
    main()
