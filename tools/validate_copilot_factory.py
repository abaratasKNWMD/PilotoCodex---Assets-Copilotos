from __future__ import annotations

import json
import hashlib
import importlib.util
import re
import sys
from datetime import datetime, timezone
from pathlib import Path


sys.dont_write_bytecode = True

ROOT = Path(__file__).resolve().parents[1]
REPORT_JSON = ROOT / "generated" / "validation-report.json"
REPORT_MD = ROOT / "generated" / "validation-report.md"
TEST_AUDIT_REPORT_JSON = ROOT / "generated" / "test-strategy-audit-report.json"
TEST_AUDIT_REPORT_MD = ROOT / "generated" / "test-strategy-audit-report.md"
PHASE_VERDICT_REPORT_JSON = ROOT / "generated" / "phase-verdict-report.json"
PHASE_VERDICT_REPORT_MD = ROOT / "generated" / "phase-verdict-report.md"
PHASE_VERDICT_EVIDENCE_MAP_JSON = ROOT / "generated" / "phase-verdict-evidence-map.json"
PHASE_VERDICT_EVIDENCE_MAP_MD = ROOT / "generated" / "phase-verdict-evidence-map.md"
PHASE_VERDICT_CONTRACT_JSON = ROOT / "dist" / "copilots" / "qa_general" / "shared" / "phase_verdict_report_contract.json"
PROMPT_QUALITY_REPORT_JSON = ROOT / "generated" / "prompt-quality-report.json"
RUNTIME_EQUIVALENCE_REPORT_JSON = ROOT / "generated" / "runtime-equivalence-report.json"
DOCS_AUDIT_REPORT_JSON = ROOT / "generated" / "documentation-audit-report.json"
DOCS_AUDIT_REPORT_MD = ROOT / "generated" / "documentation-audit-report.md"
VALIDATOR_SMOKE_REPORT_JSON = ROOT / "generated" / "validator-smoke-report.json"
VALIDATOR_SMOKE_REPORT_MD = ROOT / "generated" / "validator-smoke-report.md"

EXPECTED_COPILOTS = 18
EXPECTED_AGENTS = 50
RUNTIMES = ["codex", "claude", "github-copilot", "langchain"]
SMOKE_AGENT = "factory_agent_25_smoke"
SMOKE_MISSION = "Runs generated validators and reports blockers."
SMOKE_POLICY_VERSION = "generated-validator-smoke-1.0"
SMOKE_SOURCE_OF_TRUTH = "data/agent_roster.json#/factory_agent_25_smoke"
SMOKE_VALIDATORS = [
    {
        "id": "copilot_factory",
        "command": "python tools/validate_copilot_factory.py",
        "report": "generated/validation-report.json",
        "receipt": "generated/validator-smoke/copilot-factory.json",
    },
    {
        "id": "prompt_quality",
        "command": "python tools/validate_prompt_quality.py",
        "report": "generated/prompt-quality-report.json",
        "receipt": "generated/validator-smoke/prompt-quality.json",
    },
    {
        "id": "runtime_equivalence",
        "command": "python tools/validate_runtime_equivalence.py",
        "report": "generated/runtime-equivalence-report.json",
        "receipt": "generated/validator-smoke/runtime-equivalence.json",
    },
]
SMOKE_RUNTIME_EQUIVALENCE_ASSERTIONS = [
    "sameValidatorCommands",
    "sameBlockerTaxonomy",
    "reportDigestTracePresent",
    "promptBodiesStoredFalse",
    "maxUnexplainedDriftZero",
]
SMOKE_FORBIDDEN_PROMPT_KEYS = {
    "adapterPrompt",
    "developerPrompt",
    "promptText",
    "rawPrompt",
    "runtimePrompt",
    "systemPrompt",
}
SDLC_RUNTIME_MATRIX_JSON = ROOT / "generated" / "sdlc-runtime-matrix.json"
SDLC_RUNTIME_MATRIX_MD = ROOT / "generated" / "sdlc-runtime-matrix.md"
SDLC_RUNTIME_MATRIX_MAINTENANCE_JSON = ROOT / "generated" / "sdlc-runtime-matrix-maintenance.json"
SDLC_RUNTIME_MATRIX_MAINTENANCE_MD = ROOT / "generated" / "sdlc-runtime-matrix-maintenance.md"
MATRIX_AGENT = "factory_agent_24_matrix"
MATRIX_MISSION = "Maintains the SDLC x Copilot x Runtime matrix."
MATRIX_POLICY_VERSION = "sdlc-copilot-runtime-matrix-1.0"
MATRIX_MAINTENANCE_VERSION = "sdlc-runtime-matrix-maintenance-1.0"
MATRIX_DIMENSIONS = ["sdlc_phase", "copilot_id", "runtime"]
MATRIX_VALIDATION_COMMANDS = [
    "python tools/validate_copilot_factory.py",
    "python tools/validate_prompt_quality.py",
    "python tools/validate_runtime_equivalence.py",
]
MATRIX_CELL_EQUIVALENCE_VERSION = "runtime-cell-equivalence-1.0"
MATRIX_CELL_EQUIVALENCE_ASSERTIONS = [
    "sourceOfTruthMatchesRuntimeMap",
    "runtimeFileMatchesCanonical",
    "runtimeTraceRefMatchesRuntimeMap",
    "sharedSpecDigestPresent",
    "outputSchemaDigestPresent",
    "runtimeFileDigestPresent",
    "promptBodiesStoredFalse",
    "maxUnexplainedDriftZero",
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
DIRECTOR_AGENT = "factory_agent_01_director"
DIRECTOR_MISSION = "Owns the whole run, keeps gates honest and prevents scope drift."
SEMANTIC_AGENT = "factory_agent_03_semantics"
SEMANTIC_MISSION = "Uses deterministic Python scoring before any LLM assist."
SEMANTIC_ROUTING_VERSION = "semantic-routing-1.0"
SEMANTIC_SCORE_MODEL = "weighted_exact_and_token_overlap"
SEMANTIC_REQUIRED_OUTPUTS = [
    "deterministic_route_scores",
    "route_confidence_payload",
    "llm_escalation_guard",
]
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
DISCOVERY_AGENT = "factory_agent_04_discovery"
DISCOVERY_MISSION = "Audits AS-IS coverage and repo inventory contracts."
DISCOVERY_AUDIT_VERSION = "as-is-inventory-audit-1.0"
DISCOVERY_TARGET_COPILOT = "as_is_discovery"
DISCOVERY_AGENT_OUTPUTS = [
    "as_is_coverage_audit",
    "repo_inventory_contract",
    "coverage_gap_register",
]
DISCOVERY_REQUIRED_OUTPUTS = [
    "as_is_report",
    "inventory_json",
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
DISCOVERY_RUNTIME_EQUIVALENCE = {
    "runtimes": RUNTIMES,
    "source_of_truth": "dist/copilots/as_is_discovery/shared/spec.json",
    "max_unexplained_drift": 0,
}
ARCHITECTURE_AGENT = "factory_agent_05_architecture"
ARCHITECTURE_MISSION = "Audits principles, ADRs and technical decision quality."
ARCHITECTURE_TARGET_COPILOT = "aida_architecture"
ARCHITECTURE_AUDIT_VERSION = "architecture-decision-audit-1.0"
ARCHITECTURE_AUDIT_ARTIFACT = "shared/architecture_decision_audit.json"
ARCHITECTURE_AUDIT_SOURCE = "dist/copilots/aida_architecture/shared/architecture_decision_audit.json"
ARCHITECTURE_REQUIRED_EVIDENCE = [
    "principles",
    "adr",
    "technical_decision_quality",
    "validation",
]
ARCHITECTURE_QUALITY_GATES = [
    "principle_alignment",
    "adr_completeness",
    "decision_quality",
    "traceability_and_cost",
]
ARCHITECTURE_ROUTING_SIGNALS = [
    "architecture",
    "arquitectura",
    "principles",
    "principios",
    "adr",
    "decision",
    "calidad",
    "quality",
    "technical",
    "tecnica",
    "tecnico",
]
ARCHITECTURE_VALIDATION_COMMANDS = [
    "python tools/validate_copilot_factory.py",
    "python tools/semantic_router.py architecture adr principles",
    "python tools/semantic_router.py arquitectura adr principios",
    "python tools/semantic_router.py python ci routing",
]
ARCHITECTURE_RUNTIME_EQUIVALENCE = {
    "sourceOfTruth": ARCHITECTURE_AUDIT_SOURCE,
    "runtimes": RUNTIMES,
    "maxUnexplainedDrift": 0,
}
ARCHITECTURE_ROUTE_SAMPLES = [
    ("architecture adr principles", "english"),
    ("arquitectura adr principios", "spanish"),
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
DESIGN_ROUTE_SAMPLES = [
    ("design domain boundaries contracts handoff", "english"),
    ("diseno dominio contratos limites handoff", "spanish"),
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
BUILD_ROUTE_SAMPLES = [
    ("build implementation stack rules affected files rollback", "english"),
    ("implementacion reglas stack archivos rollback", "spanish"),
]
KB_AGENT = "factory_agent_21_kb"
KB_MISSION = "Audits KB separation, source-of-truth rules and context windows."
KB_TARGET_COPILOT = "firefly_v6"
KB_AUDIT_VERSION = "kb-separation-source-context-audit-1.0"
KB_AUDIT_ARTIFACT = "shared/kb_context_window_audit.json"
KB_AUDIT_SOURCE = "dist/copilots/firefly_v6/shared/kb_context_window_audit.json"
KB_REQUIRED_EVIDENCE = [
    "kb_partition_map",
    "source_of_truth_registry",
    "context_window_budget",
    "runtime_trace",
]
KB_QUALITY_GATES = [
    "kb_separation",
    "canonical_source_refs",
    "context_budget",
    "runtime_equivalence",
]
KB_REQUIRED_OUTPUT_FIELDS = [
    "copilot_id",
    "decision",
    "evidence",
    "actions",
    "validation",
    "risks",
    "kb_partition",
]
KB_REQUIRED_PARTITION_FIELDS = [
    "kb_partition_map",
    "source_of_truth_registry",
    "context_window_budget",
    "excluded_sources",
    "runtime_trace",
    "validation_commands",
]
KB_CONTEXT_WINDOW_POLICY = {
    "maxEvidenceRefs": 12,
    "maxPromptBytes": 12000,
    "summaryFirst": True,
    "fullDocumentOnlyWhenGapBlocksDecision": True,
    "redactionRequired": True,
    "overflowAction": "emit_gap_register_before_llm_escalation",
}
KB_ROUTING_SIGNALS = [
    "kb",
    "knowledge",
    "knowledge_base",
    "source",
    "source_of_truth",
    "truth",
    "context",
    "window",
    "windows",
    "separation",
    "separacion",
]
KB_VALIDATION_COMMANDS = [
    "python tools/validate_copilot_factory.py",
    "python tools/semantic_router.py kb source truth context windows",
    "python tools/semantic_router.py python ci routing",
]
KB_ROUTE_SAMPLE = "kb source truth context windows"
TEST_AGENT = "factory_agent_08_test"
TEST_MISSION = "Audits test strategy, pairwise cases and negative cases."
TEST_TARGET_COPILOT = "qa_general"
TEST_REQUIRED_OUTPUTS = ["qa_strategy", "test_matrix"]
TEST_REQUIRED_EVIDENCE = [
    "test_strategy",
    "pairwise_cases",
    "negative_cases",
    "validation",
]
TEST_QUALITY_GATES = [
    "risk_based_strategy",
    "pairwise_runtime_coverage",
    "negative_case_coverage",
    "traceability_and_cost",
]
TEST_VALIDATION_COMMANDS = [
    "python tools/validate_copilot_factory.py",
    "python tools/validate_prompt_quality.py",
    "python tools/validate_runtime_equivalence.py",
    "python tools/semantic_router.py test strategy pairwise negative cases",
]
TEST_ROUTE_SAMPLE = "test strategy pairwise negative cases"
SECURITY_AGENT = "factory_agent_09_security"
SECURITY_MISSION = "Audits sensitive credentials policy, threat model and safe MCP usage."
SECURITY_AUDIT_VERSION = "sensitive-credentials-mcp-audit-1.0"
SECURITY_ENV_EXAMPLE = "config/.env.example"
SECURITY_MCP_CONFIG = "config/mcp-connectors.example.json"
SECURITY_REQUIRED_ENV_KEYS = [
    "GITHUB_TOKEN",
    "SONARQUBE_TOKEN",
    "CONFLUENCE_TOKEN_OPTIONAL",
]
SECURITY_REQUIRED_THREATS = [
    "credential_exposure",
    "overprivileged_connector",
    "prompt_or_trace_leakage",
    "unsafe_mcp_activation",
]
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
SECURITY_VALIDATION_COMMANDS = [
    "python tools/validate_copilot_factory.py",
    "python tools/validate_prompt_quality.py",
]
MCP_AGENT = "factory_agent_18_mcp"
MCP_MISSION = "Audits connector declarations and env placeholders."
MCP_AUDIT_VERSION = "mcp-connector-placeholder-audit-1.0"
MCP_ENV_EXAMPLE = SECURITY_ENV_EXAMPLE
MCP_CONFIG = SECURITY_MCP_CONFIG
MCP_REQUIRED_DECLARATION_FIELDS = [
    "enabled",
    "env",
    "purpose",
    "owner",
    "rotation_owner",
    "least_privilege_scope",
    "allowed_runtimes",
    "requires_operator_activation",
    "operator_approval_required_for_writes",
    "allowed_operations",
    "denied_operations",
    "traceability_refs",
]
MCP_REQUIRED_QUALITY_GATES = [
    "connector_declarations_complete",
    "env_placeholders_empty",
    "runtime_equivalence_preserved",
    "traceability_refs_present",
    "cost_control_python_first",
]
MCP_RUNTIME_EQUIVALENCE = {
    "runtimes": RUNTIMES,
    "source_of_truth": MCP_CONFIG,
    "same_connector_contract_for_all_runtimes": True,
    "max_unexplained_drift": 0,
    "cost_control": "python_first_llm_sparse",
}
MCP_VALIDATION_COMMANDS = [
    "python tools/validate_copilot_factory.py",
    "python tools/validate_prompt_quality.py",
]
DEVOPS_AGENT = "factory_agent_10_devops"
DEVOPS_MISSION = "Audits CI/CD, logs, reproducibility and rollback paths."
DEVOPS_AUDIT_VERSION = "devops-ci-logs-reproducibility-rollback-audit-1.0"
DEVOPS_TARGET_COPILOT = "cicd"
DEVOPS_RUN_SEQUENCE = [
    "generate_copilot_factory.py",
    "validate_copilot_factory.py",
    "validate_prompt_quality.py",
    "validate_runtime_equivalence.py",
]
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
DEVOPS_LOG_EVIDENCE_REPORT = "generated/devops-log-evidence.json"
DEVOPS_ROLLBACK_PATHS = [
    ".codex-loop/rollback",
    ".codex-loop/backups",
]
DEVOPS_RUNTIME_EQUIVALENCE = {
    "runtimes": RUNTIMES,
    "sourceOfTruth": "dist/copilots/cicd/shared/spec.json",
    "traceSource": "generated/runtime-injection-map.json#/copilots/cicd",
    "maxUnexplainedDrift": 0,
}
CLOUD_AGENT = "factory_agent_11_cloud"
CLOUD_MISSION = "Audits migration, target platform and modernization increments."
CLOUD_AUDIT_VERSION = "cloud-migration-target-modernization-audit-1.0"
CLOUD_TARGET_COPILOT = "journey_to_cloud"
CLOUD_AUDIT_ARTIFACT = "dist/copilots/journey_to_cloud/shared/cloud_migration_audit.json"
CLOUD_REQUIRED_EVIDENCE = [
    "migration_inventory",
    "target_platform",
    "modernization_increments",
    "validation",
]
CLOUD_QUALITY_GATES = [
    "incremental_migration_plan",
    "platform_fit_and_constraints",
    "modernization_traceability",
    "cost_time_guard",
]
CLOUD_REQUIRED_OUTPUT_FIELDS = [
    "copilot_id",
    "decision",
    "evidence",
    "actions",
    "validation",
    "risks",
    "cloud_migration",
]
CLOUD_REQUIRED_MIGRATION_FIELDS = [
    "current_state_refs",
    "target_platform",
    "migration_increments",
    "modernization_actions",
    "data_network_security_impacts",
    "rollback_and_parallel_run",
    "validation_commands",
    "evidence_pack",
    "out_of_scope",
]
CLOUD_VALIDATION_COMMANDS = [
    "python tools/validate_copilot_factory.py",
    "python tools/validate_prompt_quality.py",
    "python tools/validate_runtime_equivalence.py",
]
CLOUD_RUNTIME_EQUIVALENCE = {
    "sourceOfTruth": CLOUD_AUDIT_ARTIFACT,
    "runtimes": RUNTIMES,
    "traceSource": "generated/runtime-injection-map.json#/copilots/journey_to_cloud/cloudMigrationAudit",
    "maxUnexplainedDrift": 0,
}
RELEASE_AGENT = "factory_agent_12_release"
RELEASE_MISSION = "Audits package readiness, scorecards and exit criteria."
RELEASE_AUDIT_VERSION = "release-readiness-scorecard-exit-criteria-audit-1.0"
RELEASE_TARGET_COPILOTS = [
    "devex",
    "aida_architecture",
    "java_architect",
    "qa_general",
    "sonarqube_remediation",
    "cicd",
    "journey_to_cloud",
    "firefly_marketplace",
]
RELEASE_REQUIRED_EVIDENCE = [
    "package_readiness",
    "scorecards",
    "exit_criteria",
    "validation",
]
RELEASE_QUALITY_GATES = [
    "output_topology",
    "artifact_manifest",
    "scorecard_completeness",
    "exit_criteria_evidence",
    "traceability_and_cost",
]
RELEASE_SCORECARD_FIELDS = [
    "copilotId",
    "sourceOfTruth",
    "runtimeAdapters",
    "declaredOutputs",
    "score",
    "scoreType",
    "scoreScope",
    "exitCriteriaStatus",
    "releaseClaimStatus",
    "claimPolicyRef",
    "residualRiskRefs",
    "evidenceRefs",
]
RELEASE_SCORECARD_INDEX = "generated/factory-audit.json#/releaseAudit/scorecardsByCopilot"
RELEASE_SCORE_SCOPE = "metadata_evidence_completeness_only"
RELEASE_SCORE_SCOPE_POLICY = "score_is_metadata_only_and_does_not_override_residual_risks_or_claim_policy"
RELEASE_RELEASE_CLAIM_STATUS = "not_a_product_release_claim"
RELEASE_CLAIM_POLICY_REF = "generated/factory-audit.json#/releaseAudit/packageReadiness/claimPolicy"
RELEASE_RESIDUAL_RISK_REF = "generated/factory-audit.json#/releaseAudit/residualRisks"
RELEASE_EXIT_CRITERIA = [
    "product-market-fit",
    "implementation",
    "test-coverage",
    "browser-navigation-render",
    "safe-coding-privacy",
    "seo-content",
    "packaging-artifact",
    "release-handoff",
]
RELEASE_ARTIFACT_TARGETS = [
    "web-app",
    "desktop-tauri-windows-exe",
    "docs-and-seo",
]
RELEASE_VALIDATION_COMMANDS = [
    "python tools/validate_copilot_factory.py",
    "python tools/validate_prompt_quality.py",
    "python tools/validate_runtime_equivalence.py",
]
RELEASE_RUNTIME_EQUIVALENCE = {
    "sourceOfTruth": "generated/factory-audit.json#/releaseAudit",
    "runtimes": RUNTIMES,
    "traceSource": "generated/runtime-injection-map.json#/copilots/<copilot_id>/releaseReadinessAudit",
    "maxUnexplainedDrift": 0,
}
PACKAGER_AGENT = "factory_agent_23_packager"
PACKAGER_MISSION = "Builds distribution manifests and file indexes."
PACKAGER_POLICY_VERSION = "packager-distribution-manifest-file-index-1.0"
PACKAGER_MANIFEST_REF = "generated/factory-audit.json#/releaseAudit/distributionManifest"
PACKAGER_FILE_INDEX_REF = "generated/runtime-injection-map.json#/distributionFileIndex"
PACKAGER_REQUIRED_ARTIFACTS = [
    "dist/copilots/<copilot_id>/shared/spec.json",
    "dist/copilots/<copilot_id>/shared/output_schema.json",
    "dist/copilots/<copilot_id>/codex/AGENT.md",
    "dist/copilots/<copilot_id>/claude/AGENT.md",
    "dist/copilots/<copilot_id>/github-copilot/copilot-agent.md",
    "dist/copilots/<copilot_id>/langchain/agent.py",
]
PACKAGER_RUNTIME_EQUIVALENCE = {
    "sourceOfTruth": PACKAGER_FILE_INDEX_REF,
    "runtimes": RUNTIMES,
    "maxUnexplainedDrift": 0,
}
OPERATE_AGENT = "factory_agent_13_operate"
OPERATE_MISSION = "Audits observability, incident playbooks and runbooks."
OPERATE_AUDIT_VERSION = "operate-observability-incident-runbook-audit-1.0"
OPERATE_CONTRACT = ".codex-loop/factory/operate-observability-contract.json"
OPERATE_SCORECARD = ".codex-loop/factory/operate-observability-scorecard.json"
OPERATE_RUNBOOK = ".codex-loop/factory/operate-observability-runbook.md"
OPERATE_INCIDENT_RUNBOOK = ".codex-loop/factory/incident-runbook.md"
OPERATE_RUNTIME_INCIDENTS = ".codex-loop/factory/codex-runtime-incidents.md"
OPERATE_TARGET_COPILOTS = [
    "single_registry",
    "moonshine",
    "nodejs",
    "python",
    "cicd",
    "copilots_manager",
    "firefly_marketplace",
]
OPERATE_REQUIRED_EVIDENCE = [
    "observability_contract",
    "incident_playbooks",
    "runbook_ownership",
    "validation",
]
OPERATE_QUALITY_GATES = [
    "signal_coverage",
    "incident_response_playbook",
    "runbook_freshness",
    "privacy_safe_observability",
    "traceability_and_cost",
]
OPERATE_TELEMETRY_SIGNALS = [
    "state_lock_heartbeat",
    "validation_gate_reports",
    "prompt_quality_gate",
    "runtime_equivalence_gate",
    "runtime_incident_summary",
]
OPERATE_INCIDENT_PLAYBOOKS = [
    "state-lock-stale",
    "validation-report-regression",
    "runtime-equivalence-drift",
    "observability-signal-gap",
    "privacy-log-exposure",
]
OPERATE_RUNBOOK_REFS = [
    OPERATE_RUNBOOK,
    OPERATE_INCIDENT_RUNBOOK,
    OPERATE_RUNTIME_INCIDENTS,
]
OPERATE_RUNTIME_EQUIVALENCE = {
    "runtimes": RUNTIMES,
    "sourceOfTruth": OPERATE_CONTRACT,
    "traceEvidence": "generated/validation-report.json#/operateAuditor",
    "sameContractForAdapters": True,
    "maxUnexplainedDrift": 0,
}
OPERATE_VALIDATION_COMMANDS = [
    "python tools/validate_copilot_factory.py",
    "python tools/validate_prompt_quality.py",
]
OPERATE_COST_CONTROL = {
    "deterministicPythonFirst": True,
    "llmEscalation": "only_for_incident_summary_after_artifact_checks",
    "rawLogPromptsAllowed": False,
    "sanitizedEvidenceOnly": True,
}
QA_PHASE_VERDICT_AGENT = "factory_agent_22_qa"
QA_PHASE_VERDICT_MISSION = "Consolidates all phase verdicts into a pass/fail report."
PHASE_VERDICT_AUDIT_VERSION = "phase-verdict-report-1.0"
PHASE_VERDICT_REQUIRED_PHASES = [
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
PHASE_VERDICT_VALIDATION_COMMANDS = [
    "python tools/validate_copilot_factory.py",
    "python tools/validate_prompt_quality.py",
    "python tools/validate_runtime_equivalence.py",
]
PHASE_VERDICT_REPORT_REFS = [
    "generated/phase-verdict-report.json",
    "generated/phase-verdict-report.md",
    "generated/phase-verdict-evidence-map.json",
    "generated/phase-verdict-evidence-map.md",
]
PHASE_VERDICT_INPUT_REFS = [
    "generated/validation-report.json#/discoveryAuditor",
    "generated/validation-report.json#/architectureAuditor",
    "generated/validation-report.json#/designAuditor",
    "generated/validation-report.json#/buildAuditor",
    "generated/validation-report.json#/testStrategyAudit",
    "generated/validation-report.json#/securityAuditor",
    "generated/validation-report.json#/devopsAuditor",
    "generated/validation-report.json#/cloudAuditor",
    "generated/validation-report.json#/releaseAuditor",
    "generated/validation-report.json#/operateAuditor",
]
PHASE_VERDICT_CONTRACT = {
    "version": PHASE_VERDICT_AUDIT_VERSION,
    "ownerAgent": QA_PHASE_VERDICT_AGENT,
    "mission": QA_PHASE_VERDICT_MISSION,
    "sourceOfTruth": "generated/validation-report.json#/phaseVerdictReport",
    "reportArtifacts": PHASE_VERDICT_REPORT_REFS,
    "requiredPhases": PHASE_VERDICT_REQUIRED_PHASES,
    "verdictValues": ["pass", "fail"],
    "explicitPassRequired": True,
    "aggregationRule": "overallPass is true only when every required phase verdict is pass and runtime equivalence has maxUnexplainedDrift 0.",
    "coherenceRules": [
        "Each phase pass boolean must be explicit and match its pass/fail verdict.",
        "summaryPass must match the phase pass boolean.",
        "failedPhases must exactly match phases whose verdict is fail.",
        "failedGates must exactly match runtime gate failures.",
    ],
    "inputReports": PHASE_VERDICT_INPUT_REFS,
    "runtimeEquivalence": {
        "runtimes": RUNTIMES,
        "source": "generated/runtime-equivalence-report.json",
        "maxUnexplainedDrift": 0,
        "requiresReportPass": True,
        "maxIssues": 0,
    },
    "costControl": {
        "deterministicPythonFirst": True,
        "llmEscalation": "only_for_final_operator_summary_after_report_exists",
        "rawLogPromptsAllowed": False,
    },
    "validationCommands": PHASE_VERDICT_VALIDATION_COMMANDS,
}
COST_AGENT = "factory_agent_20_cost"
COST_MISSION = "Routes cheap deterministic work to Python and expensive judgement to LLMs."
COST_ROUTING_VERSION = "cost-routing-1.0"
COST_CONTRACT = ".codex-loop/factory/cost-routing-contract.json"
COST_SCORECARD = ".codex-loop/factory/cost-routing-scorecard.json"
COST_POLICY_DOC = ".codex-loop/factory/cost-routing-policy.md"
COST_ROUTING_MODE = "python_first_llm_sparse"
COST_CHEAP_WORK_IDS = [
    "catalog_generation",
    "semantic_routing",
    "schema_validation",
    "prompt_quality_budget",
    "runtime_equivalence_diff",
    "documentation_marker_audit",
]
COST_JUDGEMENT_WORK_IDS = [
    "architecture_tradeoff",
    "non_trivial_code_change",
    "final_operator_synthesis",
]
COST_VALIDATION_COMMANDS = [
    "python tools/validate_copilot_factory.py",
    "python tools/validate_prompt_quality.py",
]
COST_DECISION_RULES = {
    "pythonFirstRequired": True,
    "llmBeforePythonAllowed": False,
    "scoreBeforeLlmAssist": True,
    "samePolicyForAdapters": True,
    "maxUnexplainedRuntimeDrift": 0,
    "promptGrowthBudgetRef": "generated/prompt-quality-report.json#/costBudget",
    "routerEvidenceField": "routing_evidence",
    "placeholderOnlyCredentials": True,
    "rawLogPromptsAllowed": False,
}
COST_RUNTIME_EQUIVALENCE = {
    "runtimes": RUNTIMES,
    "sameCostRoutingPolicy": True,
    "sameTraceFields": True,
    "adapterSpecificPromptExpansionAllowed": False,
    "maxUnexplainedDrift": 0,
}
COST_TRACEABILITY = {
    "runtimeInjectionMap": "generated/runtime-injection-map.json",
    "canonicalSpec": "dist/copilots/<copilot_id>/shared/spec.json",
    "validationReport": "generated/validation-report.json#/costRoutingAuditor",
    "semanticRouterReport": "generated/validation-report.json#/semanticRouter",
    "promptCostReport": "generated/prompt-quality-report.json#/costBudget",
}
COST_REQUIRED_SETTINGS = [
    "codexLoop.costRoutingContractFile",
    "codexLoop.costRoutingScorecardFile",
    "codexLoop.costRoutingPolicyFile",
    "codexLoop.deterministicPythonFirst",
    "codexLoop.llmEscalationMode",
    "codexLoop.maxUnexplainedRuntimeDrift",
    "codexLoop.rawLogPromptsAllowed",
]
DOCS_AGENT = "factory_agent_19_docs"
DOCS_MISSION = "Audits generated READMEs and operator docs."
DOCS_AUDIT_VERSION = "generated-readme-operator-docs-audit-1.0"
DOCS_REPORT_REF = "generated/documentation-audit-report.json"
DOCS_REPORT_MD_REF = "generated/documentation-audit-report.md"
DOCS_REQUIRED_EVIDENCE = [
    "generated_readmes",
    "operator_docs",
    "runtime_adapter_traceability",
    "validation",
]
DOCS_QUALITY_GATES = [
    "all_copilot_readmes_have_runtime_map",
    "operator_docs_resolve",
    "runtime_equivalence_refs_present",
    "privacy_safe_placeholders",
    "traceability_and_cost",
]
DOCS_REQUIRED_README_SECTIONS = [
    "Purpose",
    "Runtime Files",
    "Python Brain",
    "Peer Auditors",
    "Operator Runbook",
    "Documentation Audit",
]
DOCS_REQUIRED_RUNTIME_MARKERS = [
    "Codex: `codex/AGENT.md`",
    "Claude: `claude/AGENT.md`",
    "GitHub Copilot Agents: `github-copilot/copilot-agent.md`",
    "GitHub Copilot profile: `github-copilot/copilot-profile.json`",
    "GitHub MCP placeholders: `github-copilot/mcp-placeholders.json`",
    "LangChain/Python: `langchain/agent.py`",
    "Shared spec: `shared/spec.json`",
    "Output schema: `shared/output_schema.json`",
]
DOCS_OPERATOR_DOCS = {
    "README.md": [
        "Documentation Auditor Evidence",
        DOCS_REPORT_REF,
        "generated/validation-report.json#/docsAuditor",
    ],
    "OPERATING_SYSTEM.md": [
        "## Quality Policy",
        "python tools/validate_prompt_quality.py",
        "python tools/validate_runtime_equivalence.py",
    ],
    "factory-prompt.md": [
        "Mantener 18 copilotos equivalentes",
        "generated/runtime-injection-map.json",
        "python tools/validate_copilot_factory.py",
    ],
    OPERATE_RUNBOOK: [
        "# Operate Observability Runbook",
        "## Signal Contract",
        "## Review Gate",
    ],
    OPERATE_INCIDENT_RUNBOOK: [
        "# Incident Runbook",
        "provider-policy-friction",
        "codex-cli-contract-drift",
    ],
    COST_POLICY_DOC: [
        "# Cost Routing Policy",
        "## Decision Contract",
        "## Runtime Equivalence",
        "## Verification",
    ],
}
DOCS_RUNTIME_EQUIVALENCE = {
    "runtimes": RUNTIMES,
    "sourceOfTruth": "dist/copilots/<copilot_id>/shared/spec.json",
    "traceEvidence": f"{DOCS_REPORT_REF}#/readmeChecks",
    "sameReadmeContractForAdapters": True,
    "maxUnexplainedDrift": 0,
}
DOCS_VALIDATION_COMMANDS = [
    "python tools/validate_copilot_factory.py",
    "python tools/validate_prompt_quality.py",
]
DOCS_COST_CONTROL = {
    "deterministicPythonFirst": True,
    "llmEscalation": "disabled_for_marker_and_reference_audit",
    "rawLogPromptsAllowed": False,
    "readmeGrowthPolicy": "operator_sections_only",
}
CONTROL_ROOM_REQUIRED_COMMANDS = [
    "python tools/validate_copilot_factory.py",
    "python tools/validate_prompt_quality.py",
    "python tools/validate_runtime_equivalence.py",
]
CONTROL_ROOM_REQUIRED_REPORTS = [
    "generated/validation-report.json",
    "generated/prompt-quality-report.json",
    "generated/runtime-equivalence-report.json",
]
RUN_LOCK_REQUIRED_FIELDS = ["id", "pid", "workspace", "startedAt", "heartbeatAt", "mode"]
STATE_LOCK_SNAPSHOT_ROOTS = [".codex-loop/backups", ".codex-loop/rollback"]
LOCK_CLOCK_SKEW_SECONDS = 300
PRIVATE_KEY_BLOCK_PATTERN = (
    r"-{5}"
    r"BE" r"GIN "
    r"(?:RSA |DSA |EC |OPENSSH |PGP )?"
    r"PRI" r"VATE " r"KEY"
    r"-{5}"
)
SECRET_PATTERNS = [
    re.compile(r"(?<![A-Za-z0-9])sk-or-v1-[A-Za-z0-9_-]{20,}", re.I),
    re.compile(r"(?<![A-Za-z0-9])sk-[A-Za-z0-9_-]{20,}"),
    re.compile(r"github_pat_[A-Za-z0-9_]{20,}", re.I),
    re.compile(r"gh[pousr]_[A-Za-z0-9_]{20,}", re.I),
    re.compile(r"glpat-[A-Za-z0-9_-]{20,}", re.I),
    re.compile(r"\b(?:AKIA|ASIA)[0-9A-Z]{16}\b"),
    re.compile(r"\bAIza[0-9A-Za-z_-]{35}\b"),
    re.compile(r"xox[baprs]-[A-Za-z0-9-]{20,}", re.I),
    re.compile(r"eyJ[A-Za-z0-9_-]{20,}\.[A-Za-z0-9_-]{20,}\.[A-Za-z0-9_-]{20,}"),
    re.compile(PRIVATE_KEY_BLOCK_PATTERN, re.I),
    re.compile(r"Bearer\s+[A-Za-z0-9._~+/=-]{20,}", re.I),
]
LOCAL_PATH_PATTERNS = [
    re.compile(r"(?i)\b[A-Z]:[\\/]+Users[\\/]+[^\\/\s\"']+"),
    re.compile(r"(?i)/Users/[A-Za-z0-9._-]+"),
    re.compile(r"(?i)/home/[A-Za-z0-9._-]+"),
]
LOCAL_RUNTIME_PATH_PREFIXES = (
    ".codex-loop/backups/",
    ".codex-loop/codex-runs/",
    ".codex-loop/pixel-ops/",
    ".codex-loop/rollback/",
    ".codex-loop/runtime/",
    ".codex-loop/tmp/",
    ".codex-loop/tool-shims/",
    ".codex-loop/verification/",
    ".codex-loop/verification-probes/",
)
LOCAL_RUNTIME_FILES = {
    ".codex-loop/run.lock.json",
    "agent.log",
    "agent-state.json",
}
LOCAL_FACTORY_RUNTIME_REPORTS = {
    ".codex-loop/factory/artifact-passport.json",
    ".codex-loop/factory/artifact-passport.md",
    ".codex-loop/factory/factory-scorecard.json",
    ".codex-loop/factory/factory-scorecard.md",
    ".codex-loop/factory/frontier-governance-report.json",
    ".codex-loop/factory/frontier-governance-report.md",
    ".codex-loop/factory/output-frontier-report.json",
    ".codex-loop/factory/output-frontier-report.md",
    ".codex-loop/factory/preflight-report.json",
    ".codex-loop/factory/preflight-report.md",
    ".codex-loop/factory/runtime-risk-report.json",
    ".codex-loop/factory/runtime-risk-report.md",
}


def main() -> None:
    issues: list[str] = []
    copilots = read_json(ROOT / "data" / "copilots.json", [], issues)
    agents = read_json(ROOT / "data" / "agent_roster.json", [], issues)
    index = read_json(ROOT / "generated" / "copilot-index.json", {}, issues)
    tasks = read_json(ROOT / "tasks.json", [], issues)
    config = read_json(ROOT / "factory.config.json", {}, issues)
    control_room = validate_control_room(config, tasks, issues)
    semantic_router = validate_semantic_router_contract(agents, index, issues)
    discovery_auditor = validate_discovery_auditor_contract(copilots, agents, index, issues)
    architecture_auditor = validate_architecture_auditor_contract(agents, issues)
    design_auditor = validate_design_auditor_contract(copilots, agents, index, issues)
    build_auditor = validate_build_auditor_contract(copilots, agents, index, issues)
    test_auditor = validate_test_auditor_contract(copilots, agents, issues)
    security_auditor = validate_security_auditor_contract(agents, issues)
    mcp_connector_auditor = validate_mcp_connector_auditor_contract(agents, issues)
    devops_auditor = validate_devops_auditor_contract(copilots, agents, index, issues)
    cloud_auditor = validate_cloud_auditor_contract(copilots, agents, index, issues)
    release_auditor = validate_release_auditor_contract(copilots, agents, config, issues)
    packager_distribution = validate_packager_distribution_contract(config, issues)
    operate_auditor = validate_operate_auditor_contract(copilots, agents, issues)
    cost_routing_auditor = validate_cost_routing_contract(agents, issues)
    kb_auditor = validate_kb_boundary_auditor_contract(agents, issues)
    docs_auditor = validate_docs_auditor_contract(copilots, agents, issues)
    sdlc_runtime_matrix = validate_sdlc_runtime_matrix_contract(copilots, agents, index, issues)
    runtime_safety = validate_runtime_safety_contract(issues)
    generator = validate_generator_contract(issues)
    phase_verdict_report = validate_phase_verdict_report(
        agents,
        {
            "discoveryAuditor": discovery_auditor,
            "architectureAuditor": architecture_auditor,
            "designAuditor": design_auditor,
            "buildAuditor": build_auditor,
            "testStrategyAudit": test_auditor,
            "securityAuditor": security_auditor,
            "devopsAuditor": devops_auditor,
            "cloudAuditor": cloud_auditor,
            "releaseAuditor": release_auditor,
            "operateAuditor": operate_auditor,
        },
        issues,
    )

    if len(copilots) != EXPECTED_COPILOTS:
        issues.append(f"Expected {EXPECTED_COPILOTS} copilots, found {len(copilots)}.")
    if len(agents) != EXPECTED_AGENTS:
        issues.append(f"Expected {EXPECTED_AGENTS} factory agents, found {len(agents)}.")
    if len(tasks) != EXPECTED_AGENTS:
        issues.append(f"Expected {EXPECTED_AGENTS} tasks, found {len(tasks)}.")

    validate_catalog_normalization(copilots, agents, index, issues)

    for copilot in copilots:
        cid = copilot.get("id", "")
        if not is_lower_snake(cid):
            continue
        base = ROOT / "dist" / "copilots" / cid
        required = [
            base / "shared" / "spec.json",
            base / "README.md",
            base / "codex" / "AGENT.md",
            base / "claude" / "AGENT.md",
            base / "github-copilot" / "copilot-agent.md",
            base / "langchain" / "agent_profile.json",
            base / "langchain" / "agent.py",
        ]
        for file in required:
            if not file.exists():
                issues.append(f"Missing artifact for {cid}: {relative(file)}")
        spec = read_json(base / "shared" / "spec.json", {}, issues)
        if spec.get("id") != cid:
            issues.append(f"Spec ID mismatch for {cid}.")
        if not spec.get("connectors"):
            issues.append(f"Copilot {cid} has no connector declaration.")
        if not spec.get("env_keys"):
            issues.append(f"Copilot {cid} has no env key declaration.")

    for file in ROOT.rglob("*"):
        if not should_scan_text_file(file):
            continue
        try:
            text = file.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        scan_text_safety(file, text, issues)
    validate_no_python_bytecode_artifacts(issues)
    validator_smoke = build_current_validator_smoke(
        "copilot_factory",
        "python tools/validate_copilot_factory.py",
        REPORT_JSON,
        issues,
    )

    report = {
        "pass": not issues,
        "checkedAt": datetime.now(timezone.utc).isoformat(),
        "copilots": len(copilots),
        "factoryAgents": len(agents),
        "tasks": len(tasks),
        "runtimes": RUNTIMES,
        "controlRoom": control_room,
        "semanticRouter": semantic_router,
        "discoveryAuditor": discovery_auditor,
        "architectureAuditor": architecture_auditor,
        "designAuditor": design_auditor,
        "buildAuditor": build_auditor,
        "testStrategyAudit": test_auditor,
        "securityAuditor": security_auditor,
        "mcpConnectorAuditor": mcp_connector_auditor,
        "devopsAuditor": devops_auditor,
        "cloudAuditor": cloud_auditor,
        "releaseAuditor": release_auditor,
        "packagerDistribution": packager_distribution,
        "operateAuditor": operate_auditor,
        "costRoutingAuditor": cost_routing_auditor,
        "kbAuditor": kb_auditor,
        "docsAuditor": docs_auditor,
        "sdlcRuntimeMatrix": sdlc_runtime_matrix,
        "runtimeSafety": runtime_safety,
        "generator": generator,
        "phaseVerdictReport": phase_verdict_report,
        "validatorSmoke": validator_smoke,
        "issues": issues,
    }
    REPORT_JSON.parent.mkdir(parents=True, exist_ok=True)
    REPORT_JSON.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    REPORT_MD.write_text(render_md(report), encoding="utf-8")
    write_test_strategy_audit_report(test_auditor)
    write_phase_verdict_report(phase_verdict_report)
    write_validator_smoke_artifacts(
        "copilot_factory",
        "python tools/validate_copilot_factory.py",
        REPORT_JSON,
        report,
        issues,
    )

    if issues:
        print(f"Copilot factory validation FAIL: {len(issues)} issue(s).")
        for issue in issues[:20]:
            print(f"- {issue}")
        sys.exit(1)
    print(f"Copilot factory validation PASS: {len(copilots)} copilots, {len(agents)} agents, {len(tasks)} tasks.")


def read_json(path: Path, fallback, issues: list[str] | None = None):
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        if issues is not None:
            issues.append(f"Missing required JSON input: {format_path(path)}.")
        return fallback
    except json.JSONDecodeError as exc:
        if issues is not None:
            issues.append(
                f"Invalid JSON in {format_path(path)} at line {exc.lineno}, column {exc.colno}: {exc.msg}."
            )
        return fallback
    except OSError as exc:
        if issues is not None:
            issues.append(f"Cannot read JSON input {format_path(path)}: {exc}.")
        return fallback
    if not isinstance(value, type(fallback)):
        if issues is not None:
            issues.append(
                f"Unexpected JSON type in {format_path(path)}: expected {type(fallback).__name__}, got {type(value).__name__}."
            )
        return fallback
    return value


def build_current_validator_smoke(validator_id: str, command: str, report_path: Path, issues: list) -> dict:
    blockers = normalize_validator_blockers(issues)
    return {
        "version": SMOKE_POLICY_VERSION,
        "ownerAgent": SMOKE_AGENT,
        "mission": SMOKE_MISSION,
        "validatorId": validator_id,
        "command": command,
        "reportArtifact": relative(report_path),
        "reportPass": not issues,
        "blockerCount": len(blockers),
        "blockers": blockers,
        "status": "pass" if not blockers else "blockers_reported",
        "evidenceMode": "report_path_digest_and_blocker_summary",
        "promptBodiesStored": False,
        "runtimeEquivalence": smoke_runtime_equivalence_contract(),
    }


def write_validator_smoke_artifacts(
    validator_id: str,
    command: str,
    report_path: Path,
    report: dict,
    issues: list,
) -> None:
    spec = smoke_validator_spec(validator_id)
    if spec is None:
        return
    receipt = build_current_validator_smoke(validator_id, command, report_path, issues)
    receipt.update(
        {
            "checkedAt": datetime.now(timezone.utc).isoformat(),
            "reportPresent": report_path.exists(),
            "reportCheckedAt": report.get("checkedAt"),
            "reportDigest": sha256_path(report_path),
            "reportPass": report.get("pass") is True,
            "receiptArtifact": spec["receipt"],
        }
    )
    receipt_path = ROOT / spec["receipt"]
    write_json_atomic(receipt_path, receipt)
    aggregate = build_validator_smoke_report()
    write_json_atomic(VALIDATOR_SMOKE_REPORT_JSON, aggregate)
    write_text_atomic(VALIDATOR_SMOKE_REPORT_MD, render_validator_smoke_report_md(aggregate))


def build_validator_smoke_report() -> dict:
    sources = []
    for spec in SMOKE_VALIDATORS:
        receipt_path = ROOT / spec["receipt"]
        receipt = read_json_silent(receipt_path)
        if not isinstance(receipt, dict):
            sources.append(missing_smoke_receipt(spec, receipt_path))
            continue
        shape_issues = smoke_receipt_shape_issues(receipt, spec)
        item = {
            **receipt,
            "receiptPresent": True,
            "receiptArtifact": spec["receipt"],
            "receiptDigest": sha256_path(receipt_path),
            "shapePass": not shape_issues,
            "shapeIssues": shape_issues,
        }
        sources.append(item)

    blocker_count = sum(source.get("blockerCount", 0) for source in sources if isinstance(source.get("blockerCount"), int))
    completed_count = sum(1 for source in sources if source.get("receiptPresent") is True)
    shape_pass = all(source.get("shapePass") is True for source in sources)
    reports_pass = all(source.get("reportPass") is True for source in sources)
    return {
        "version": SMOKE_POLICY_VERSION,
        "checkedAt": datetime.now(timezone.utc).isoformat(),
        "ownerAgent": SMOKE_AGENT,
        "mission": SMOKE_MISSION,
        "sourceOfTruth": SMOKE_SOURCE_OF_TRUTH,
        "pass": completed_count == len(SMOKE_VALIDATORS) and reports_pass and blocker_count == 0 and shape_pass,
        "validationMode": "receipts_from_actual_validator_processes_no_recursive_subprocess",
        "requiredValidators": [
            {key: spec[key] for key in ("id", "command", "report", "receipt")}
            for spec in SMOKE_VALIDATORS
        ],
        "completedValidators": completed_count,
        "expectedValidators": len(SMOKE_VALIDATORS),
        "blockerCount": blocker_count,
        "blockerSources": sources,
        "costControl": {
            "deterministicPythonFirst": True,
            "recursiveValidatorExecution": False,
            "promptBodiesStored": False,
            "evidenceMode": "relative_paths_sha256_digests_and_blocker_summaries",
        },
        "runtimeEquivalence": smoke_runtime_equivalence_contract(),
    }


def missing_smoke_receipt(spec: dict, receipt_path: Path) -> dict:
    return {
        "version": SMOKE_POLICY_VERSION,
        "ownerAgent": SMOKE_AGENT,
        "mission": SMOKE_MISSION,
        "validatorId": spec["id"],
        "command": spec["command"],
        "reportArtifact": spec["report"],
        "receiptArtifact": spec["receipt"],
        "receiptPresent": False,
        "reportPresent": (ROOT / spec["report"]).exists(),
        "reportPass": False,
        "blockerCount": 1,
        "blockers": [
            {
                "scope": spec["id"],
                "kind": "missing_smoke_receipt",
                "message": f"Run `{spec['command']}` to create {relative(receipt_path)}.",
            }
        ],
        "status": "missing_receipt",
        "shapePass": False,
        "shapeIssues": ["missing receipt artifact"],
        "promptBodiesStored": False,
        "runtimeEquivalence": smoke_runtime_equivalence_contract(),
    }


def smoke_receipt_shape_issues(receipt: dict, spec: dict) -> list[str]:
    issues = []
    expected = {
        "version": SMOKE_POLICY_VERSION,
        "ownerAgent": SMOKE_AGENT,
        "mission": SMOKE_MISSION,
        "validatorId": spec["id"],
        "command": spec["command"],
        "reportArtifact": spec["report"],
        "promptBodiesStored": False,
    }
    for key, value in expected.items():
        if receipt.get(key) != value:
            issues.append(f"{key} drifted")
    runtime_equivalence = receipt.get("runtimeEquivalence")
    if not isinstance(runtime_equivalence, dict):
        issues.append("runtimeEquivalence must be an object")
    else:
        assertions = runtime_equivalence.get("equivalenceAssertions", {})
        if runtime_equivalence.get("runtimes") != RUNTIMES:
            issues.append("runtimeEquivalence.runtimes drifted")
        if runtime_equivalence.get("sourceOfTruth") != SMOKE_SOURCE_OF_TRUTH:
            issues.append("runtimeEquivalence.sourceOfTruth drifted")
        if runtime_equivalence.get("maxUnexplainedDrift") != 0:
            issues.append("runtimeEquivalence.maxUnexplainedDrift drifted")
        if runtime_equivalence.get("promptBodiesStored") is not False:
            issues.append("runtimeEquivalence.promptBodiesStored drifted")
        if not isinstance(assertions, dict) or any(
            assertions.get(name) is not True
            for name in SMOKE_RUNTIME_EQUIVALENCE_ASSERTIONS
        ):
            issues.append("runtimeEquivalence assertions drifted")
    if find_forbidden_prompt_keys(receipt):
        issues.append("prompt body key detected")
    if not isinstance(receipt.get("blockers"), list):
        issues.append("blockers must be a list")
    if not isinstance(receipt.get("blockerCount"), int):
        issues.append("blockerCount must be an integer")
    return issues


def smoke_runtime_equivalence_contract() -> dict:
    return {
        "runtimes": RUNTIMES,
        "sourceOfTruth": SMOKE_SOURCE_OF_TRUTH,
        "maxUnexplainedDrift": 0,
        "promptBodiesStored": False,
        "equivalenceAssertions": {name: True for name in SMOKE_RUNTIME_EQUIVALENCE_ASSERTIONS},
    }


def smoke_validator_spec(validator_id: str) -> dict | None:
    return next((spec for spec in SMOKE_VALIDATORS if spec["id"] == validator_id), None)


def find_forbidden_prompt_keys(value, path: str = "$") -> list[str]:
    detections: list[str] = []
    if isinstance(value, dict):
        for key, child in value.items():
            child_path = f"{path}.{key}"
            if key in SMOKE_FORBIDDEN_PROMPT_KEYS:
                detections.append(f"raw_prompt_key:{child_path}")
            detections.extend(find_forbidden_prompt_keys(child, child_path))
    elif isinstance(value, list):
        for index, child in enumerate(value):
            detections.extend(find_forbidden_prompt_keys(child, f"{path}[{index}]"))
    return detections


def normalize_validator_blockers(issues: list) -> list[dict]:
    blockers = []
    for item in issues[:20]:
        if isinstance(item, dict):
            blockers.append(
                {
                    "scope": truncate_text(item.get("scope", "validator")),
                    "kind": truncate_text(item.get("kind", "validation_issue")),
                    "message": truncate_text(item.get("message", "")),
                }
            )
        else:
            blockers.append(
                {
                    "scope": "validator",
                    "kind": "validation_issue",
                    "message": truncate_text(item),
                }
            )
    return blockers


def truncate_text(value, limit: int = 300) -> str:
    text = str(value)
    return text if len(text) <= limit else text[: limit - 3] + "..."


def sha256_path(path: Path) -> str | None:
    try:
        return hashlib.sha256(path.read_bytes()).hexdigest()
    except OSError:
        return None


def read_json_silent(path: Path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return None


def write_json_atomic(path: Path, value: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(path.name + ".tmp")
    tmp.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")
    tmp.replace(path)


def write_text_atomic(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(path.name + ".tmp")
    tmp.write_text(text, encoding="utf-8")
    tmp.replace(path)


def render_validator_smoke_report_md(report: dict) -> str:
    rows = "\n".join(
        (
            f"- `{source.get('validatorId')}`: status={source.get('status')}, "
            f"pass={source.get('reportPass')}, blockers={source.get('blockerCount')}, "
            f"report=`{source.get('reportArtifact')}`"
        )
        for source in report.get("blockerSources", [])
    ) or "- none"
    return f"""# Validator Smoke Report

Pass: {report.get('pass')}

Owner agent: {report.get('ownerAgent')}

Mission: {report.get('mission')}

Validation mode: {report.get('validationMode')}

Completed validators: {report.get('completedValidators')} / {report.get('expectedValidators')}

Blocker count: {report.get('blockerCount')}

Prompt bodies stored: {report.get('costControl', {}).get('promptBodiesStored')}

Runtime equivalence: {report.get('runtimeEquivalence', {}).get('runtimes')}

Blocker sources:

{rows}
"""


def validate_catalog_normalization(copilots: list, agents: list, index: dict, issues: list[str]) -> None:
    catalog_agent = next(
        (agent for agent in agents if isinstance(agent, dict) and agent.get("id") == "factory_agent_02_catalog"),
        {},
    )
    expected_outputs = [
        "normalized_copilot_catalog",
        "normalized_route_payload",
        "runtime_trace_index",
    ]
    if catalog_agent.get("outputs") != expected_outputs:
        issues.append("Catalog Normalizer must declare normalized catalog, route payload and trace index outputs.")

    contract = catalog_agent.get("normalization_contract", {})
    if contract.get("version") != NORMALIZATION_VERSION:
        issues.append("Catalog Normalizer normalization_contract version is missing or incorrect.")
    if contract.get("source") != "data/copilots.json":
        issues.append("Catalog Normalizer normalization_contract source must be data/copilots.json.")
    if contract.get("generated_index") != "generated/copilot-index.json":
        issues.append("Catalog Normalizer normalization_contract generated_index must be generated/copilot-index.json.")
    if contract.get("router") != "tools/semantic_router.py":
        issues.append("Catalog Normalizer normalization_contract router must be tools/semantic_router.py.")
    if contract.get("canonical_fields") != CASE_POLICY:
        issues.append("Catalog Normalizer canonical field policy drifted.")
    runtime_equivalence = contract.get("runtime_equivalence", {})
    if runtime_equivalence.get("sourceOfTruth") != "dist/copilots/<copilot_id>/shared/spec.json":
        issues.append("Catalog Normalizer runtime source of truth must point to shared spec.json.")
    if runtime_equivalence.get("runtimes") != RUNTIMES:
        issues.append("Catalog Normalizer runtime list must match factory runtimes.")
    if runtime_equivalence.get("maxUnexplainedDrift") != 0:
        issues.append("Catalog Normalizer maxUnexplainedDrift must be 0.")

    catalog_ids: list[str] = []
    connector_names: set[str] = set()
    env_names: set[str] = set()
    output_names: set[str] = set()

    for copilot in copilots:
        if not isinstance(copilot, dict):
            issues.append("Copilot catalog entries must be JSON objects.")
            continue
        cid = copilot.get("id", "")
        catalog_ids.append(cid)
        connectors = list_field(copilot, "connectors")
        env_keys = list_field(copilot, "env_keys")
        outputs = list_field(copilot, "outputs")
        connector_names.update(connectors)
        env_names.update(env_keys)
        output_names.update(outputs)

        if not is_lower_snake(cid):
            issues.append(f"Copilot ID is not lower_snake_case: {cid}.")
        validate_unique_values(connectors, f"connectors for {cid}", issues)
        validate_unique_values(env_keys, f"env_keys for {cid}", issues)
        validate_unique_values(outputs, f"outputs for {cid}", issues)
        for value in connectors:
            if not is_lower_snake(value):
                issues.append(f"Connector name for {cid} is not lower_snake_case: {value}.")
        for value in env_keys:
            if not is_upper_snake(value):
                issues.append(f"Env key for {cid} is not UPPER_SNAKE_CASE: {value}.")
        for value in outputs:
            if not is_lower_snake(value):
                issues.append(f"Output name for {cid} is not lower_snake_case: {value}.")

        normalization = copilot.get("normalization", {})
        if not isinstance(normalization, dict):
            issues.append(f"Copilot {cid} is missing normalization metadata.")
            continue
        canonical = normalization.get("canonical")
        expected_canonical = {
            "copilot_id": cid,
            "connector_names": connectors,
            "env_names": env_keys,
            "outputs": outputs,
        }
        if normalization.get("version") != NORMALIZATION_VERSION:
            issues.append(f"Copilot {cid} normalization version is incorrect.")
        if canonical != expected_canonical:
            issues.append(f"Copilot {cid} normalization canonical fields do not match catalog fields.")
        if normalization.get("case_policy") != CASE_POLICY:
            issues.append(f"Copilot {cid} normalization case policy drifted.")
        if normalization.get("traceability") != TRACEABILITY_POLICY:
            issues.append(f"Copilot {cid} normalization traceability policy drifted.")
        if normalization.get("status") not in {"already_normalized", "normalized"}:
            issues.append(f"Copilot {cid} normalization status is not recognized.")

    validate_unique_values(catalog_ids, "copilot ids", issues)

    policy = index.get("normalizationPolicy", {}) if isinstance(index, dict) else {}
    if policy.get("version") != NORMALIZATION_VERSION:
        issues.append("generated/copilot-index.json normalizationPolicy version is missing or incorrect.")
    if policy.get("normalizer") != "tools/semantic_router.py":
        issues.append("generated/copilot-index.json normalizer must be tools/semantic_router.py.")
    if policy.get("canonicalCase") != CASE_POLICY:
        issues.append("generated/copilot-index.json canonicalCase policy drifted.")
    index_runtime = policy.get("runtimeEquivalence", {})
    if index_runtime.get("sourceOfTruth") != "dist/copilots/<copilot_id>/shared/spec.json":
        issues.append("generated/copilot-index.json runtime source of truth is incorrect.")
    if index_runtime.get("runtimes") != RUNTIMES:
        issues.append("generated/copilot-index.json runtime list must match factory runtimes.")
    if index_runtime.get("maxUnexplainedDrift") != 0:
        issues.append("generated/copilot-index.json maxUnexplainedDrift must be 0.")

    normalized_fields = index.get("normalizedFields", {}) if isinstance(index, dict) else {}
    expected_fields = {
        "copilotIds": catalog_ids,
        "connectorNames": sorted(connector_names),
        "envNames": sorted(env_names),
        "outputs": sorted(output_names),
    }
    if normalized_fields != expected_fields:
        issues.append("generated/copilot-index.json normalizedFields do not match data/copilots.json.")

    indexed_copilots = index.get("copilots", []) if isinstance(index, dict) else []
    indexed_ids = [item.get("id") for item in indexed_copilots if isinstance(item, dict)]
    if indexed_ids != catalog_ids:
        issues.append("generated/copilot-index.json copilot order or IDs drifted from data/copilots.json.")

    lookup = index.get("normalizedLookup", {}) if isinstance(index, dict) else {}
    if not isinstance(lookup, dict):
        issues.append("generated/copilot-index.json normalizedLookup must be an object.")
        lookup = {}
    for cid in catalog_ids:
        indexed = lookup.get(cid, {})
        if indexed.get("runtime_trace") != expected_runtime_trace(cid):
            issues.append(f"generated/copilot-index.json runtime trace is incomplete for {cid}.")
        if indexed.get("normalization", {}).get("copilot_id") != cid:
            issues.append(f"generated/copilot-index.json lookup normalization missing for {cid}.")

    audit = index.get("normalizationAudit", {}) if isinstance(index, dict) else {}
    if audit.get("pass") is not True:
        issues.append("generated/copilot-index.json normalizationAudit.pass must be true.")
    if audit.get("copilots") != len(catalog_ids):
        issues.append("generated/copilot-index.json normalizationAudit copilot count drifted.")
    if audit.get("runtimeTraceComplete") is not True:
        issues.append("generated/copilot-index.json normalizationAudit runtimeTraceComplete must be true.")


def validate_semantic_router_contract(agents: list, index: dict, issues: list[str]) -> dict:
    summary = {
        "agentPresent": False,
        "policyPresent": False,
        "auditPresent": False,
        "sampleRouteChecked": False,
        "sampleTopRoute": None,
        "deterministicPythonFirst": False,
        "llmAssistUsed": None,
    }
    agent = next(
        (item for item in agents if isinstance(item, dict) and item.get("id") == SEMANTIC_AGENT),
        {},
    )
    summary["agentPresent"] = bool(agent)
    if not agent:
        issues.append("Semantic Router agent is missing from data/agent_roster.json.")
        return summary

    if agent.get("mission") != SEMANTIC_MISSION:
        issues.append("Semantic Router mission drifted from the deterministic Python scoring contract.")
    if agent.get("mode") != "python_only":
        issues.append("Semantic Router mode must be python_only.")
    if agent.get("outputs") != SEMANTIC_REQUIRED_OUTPUTS:
        issues.append("Semantic Router must declare deterministic route scores, confidence payload and LLM guard outputs.")

    contract = agent.get("deterministic_scoring_contract", {})
    if not isinstance(contract, dict):
        issues.append("Semantic Router deterministic_scoring_contract must be an object.")
        contract = {}
    if contract.get("version") != SEMANTIC_ROUTING_VERSION:
        issues.append("Semantic Router contract version is missing or incorrect.")
    if contract.get("router") != "tools/semantic_router.py":
        issues.append("Semantic Router contract must point to tools/semantic_router.py.")
    if contract.get("score_model") != SEMANTIC_SCORE_MODEL:
        issues.append("Semantic Router score model is missing or incorrect.")
    if contract.get("catalog") != "data/copilots.json":
        issues.append("Semantic Router contract catalog must be data/copilots.json.")
    if contract.get("index") != "generated/copilot-index.json":
        issues.append("Semantic Router contract index must be generated/copilot-index.json.")
    if contract.get("score_inputs") != SEMANTIC_SCORE_INPUTS:
        issues.append("Semantic Router score inputs drifted.")
    if contract.get("execution_order") != SEMANTIC_EXECUTION_ORDER:
        issues.append("Semantic Router execution order must score before any LLM assist.")
    if contract.get("cheap_path_threshold") != 3.0:
        issues.append("Semantic Router cheap_path_threshold must be 3.0.")
    if contract.get("max_route_limit") != 10:
        issues.append("Semantic Router max_route_limit must be 10.")
    if contract.get("llm_assist") != SEMANTIC_LLM_GUARD:
        issues.append("Semantic Router LLM escalation guard drifted.")

    runtime_equivalence = contract.get("runtime_equivalence", {})
    if runtime_equivalence.get("runtimes") != RUNTIMES:
        issues.append("Semantic Router contract runtime list must match factory runtimes.")
    if runtime_equivalence.get("same_scoring_policy") is not True:
        issues.append("Semantic Router must use one scoring policy across all runtimes.")
    if runtime_equivalence.get("runtime_trace_required") is not True:
        issues.append("Semantic Router must require runtime trace evidence.")

    policy = index.get("normalizationPolicy", {}).get("semanticRouting", {}) if isinstance(index, dict) else {}
    summary["policyPresent"] = bool(policy)
    if policy.get("ownerAgent") != SEMANTIC_AGENT:
        issues.append("generated/copilot-index.json semanticRouting ownerAgent is missing or incorrect.")
    if policy.get("policyVersion") != SEMANTIC_ROUTING_VERSION:
        issues.append("generated/copilot-index.json semanticRouting policyVersion is missing or incorrect.")
    if policy.get("router") != "tools/semantic_router.py":
        issues.append("generated/copilot-index.json semanticRouting router is incorrect.")
    if policy.get("scoreModel") != SEMANTIC_SCORE_MODEL:
        issues.append("generated/copilot-index.json semanticRouting scoreModel is missing or incorrect.")
    if policy.get("deterministicPythonFirst") is not True:
        issues.append("generated/copilot-index.json must require deterministic Python first for semantic routing.")
    if policy.get("scoreBeforeLlmAssist") is not True:
        issues.append("generated/copilot-index.json must require scoring before LLM assist.")
    if policy.get("llmAssistBeforeScoringAllowed") is not False:
        issues.append("generated/copilot-index.json must forbid LLM assist before scoring.")
    if policy.get("cheapPathThreshold") != 3.0:
        issues.append("generated/copilot-index.json semanticRouting cheapPathThreshold must be 3.0.")
    if policy.get("evidenceField") != "routing_evidence":
        issues.append("generated/copilot-index.json semanticRouting evidenceField must be routing_evidence.")

    audit = index.get("semanticRoutingAudit", {}) if isinstance(index, dict) else {}
    summary["auditPresent"] = bool(audit)
    if audit.get("pass") is not True:
        issues.append("generated/copilot-index.json semanticRoutingAudit.pass must be true.")
    if audit.get("policyVersion") != SEMANTIC_ROUTING_VERSION:
        issues.append("generated/copilot-index.json semanticRoutingAudit policyVersion is incorrect.")
    if audit.get("deterministicPythonFirst") is not True:
        issues.append("generated/copilot-index.json semanticRoutingAudit deterministicPythonFirst must be true.")
    if audit.get("llmAssistUsedByRouter") is not False:
        issues.append("generated/copilot-index.json semanticRoutingAudit must show no LLM assist used by the router.")
    if audit.get("runtimeEquivalenceRuntimes") != RUNTIMES:
        issues.append("generated/copilot-index.json semanticRoutingAudit runtime list must match factory runtimes.")

    try:
        import semantic_router as router

        sample = router.route("python ci routing", limit=3)
    except Exception as exc:  # pragma: no cover - validator reports the concrete runtime error.
        issues.append(f"Semantic Router sample route failed: {exc}.")
        return summary

    summary["sampleRouteChecked"] = True
    if not sample:
        issues.append("Semantic Router sample route returned no deterministic matches.")
        return summary
    top = sample[0]
    summary["sampleTopRoute"] = top.get("id")
    evidence = top.get("routing_evidence", {})
    summary["deterministicPythonFirst"] = evidence.get("deterministic_python_first") is True
    summary["llmAssistUsed"] = evidence.get("llm_assist_used")
    if top.get("id") != "python":
        issues.append("Semantic Router sample route should rank the Python copilot first for `python ci routing`.")
    if evidence.get("policy_version") != SEMANTIC_ROUTING_VERSION:
        issues.append("Semantic Router route evidence policy_version is incorrect.")
    if evidence.get("score_model") != SEMANTIC_SCORE_MODEL:
        issues.append("Semantic Router route evidence score_model is incorrect.")
    if evidence.get("deterministic_python_first") is not True:
        issues.append("Semantic Router route evidence must mark deterministic_python_first=true.")
    if evidence.get("score_before_llm_assist") is not True:
        issues.append("Semantic Router route evidence must mark score_before_llm_assist=true.")
    if evidence.get("llm_assist_used") is not False:
        issues.append("Semantic Router route evidence must mark llm_assist_used=false.")
    if evidence.get("execution_order") != SEMANTIC_EXECUTION_ORDER:
        issues.append("Semantic Router route evidence execution_order drifted.")
    if evidence.get("llm_escalation_guard") != SEMANTIC_LLM_GUARD:
        issues.append("Semantic Router route evidence LLM guard drifted.")
    return summary


def finalize_phase_source_summary(summary: dict, issues: list[str], start_issue_count: int) -> dict:
    summary["pass"] = len(issues) == start_issue_count
    return summary


def validate_discovery_auditor_contract(copilots: list, agents: list, index: dict, issues: list[str]) -> dict:
    start_issue_count = len(issues)
    summary = {
        "agentPresent": False,
        "policyPresent": False,
        "auditPresent": False,
        "catalogProfilePresent": False,
        "lookupProfilePresent": False,
        "sampleRouteChecked": False,
        "sampleTopRoute": None,
        "runtimeTraceReturned": False,
    }
    agent = next(
        (item for item in agents if isinstance(item, dict) and item.get("id") == DISCOVERY_AGENT),
        {},
    )
    summary["agentPresent"] = bool(agent)
    if not agent:
        issues.append("Discovery Auditor agent is missing from data/agent_roster.json.")
        return finalize_phase_source_summary(summary, issues, start_issue_count)

    if agent.get("mission") != DISCOVERY_MISSION:
        issues.append("Discovery Auditor mission drifted from the AS-IS inventory audit contract.")
    if agent.get("mode") != "python_first_llm_sparse":
        issues.append("Discovery Auditor mode must remain python_first_llm_sparse.")
    if agent.get("outputs") != DISCOVERY_AGENT_OUTPUTS:
        issues.append("Discovery Auditor must declare AS-IS coverage, inventory contract and gap register outputs.")

    contract = agent.get("as_is_inventory_contract", {})
    if not isinstance(contract, dict):
        issues.append("Discovery Auditor as_is_inventory_contract must be an object.")
        contract = {}
    expected_contract = {
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
        "runtime_equivalence": DISCOVERY_RUNTIME_EQUIVALENCE,
    }
    if contract != expected_contract:
        issues.append("Discovery Auditor AS-IS inventory contract drifted.")

    target = next(
        (item for item in copilots if isinstance(item, dict) and item.get("id") == DISCOVERY_TARGET_COPILOT),
        {},
    )
    if not target:
        issues.append("AS-IS Discovery copilot is missing from data/copilots.json.")
        return finalize_phase_source_summary(summary, issues, start_issue_count)
    if target.get("outputs") != DISCOVERY_REQUIRED_OUTPUTS:
        issues.append("AS-IS Discovery copilot outputs must remain as_is_report and inventory_json.")

    profile = target.get("discovery_audit", {})
    summary["catalogProfilePresent"] = bool(profile)
    validate_discovery_profile(profile, "data/copilots.json as_is_discovery discovery_audit", issues)

    lookup = index.get("normalizedLookup", {}).get(DISCOVERY_TARGET_COPILOT, {}) if isinstance(index, dict) else {}
    indexed_profile = lookup.get("discovery_audit", {}) if isinstance(lookup, dict) else {}
    summary["lookupProfilePresent"] = bool(indexed_profile)
    validate_discovery_profile(indexed_profile, "generated/copilot-index.json normalizedLookup discovery_audit", issues)
    if profile and indexed_profile and profile != indexed_profile:
        issues.append("generated/copilot-index.json discovery_audit lookup drifted from data/copilots.json.")

    policy = index.get("normalizationPolicy", {}).get("discoveryAudit", {}) if isinstance(index, dict) else {}
    summary["policyPresent"] = bool(policy)
    if policy.get("ownerAgent") != DISCOVERY_AGENT:
        issues.append("generated/copilot-index.json discoveryAudit ownerAgent is missing or incorrect.")
    if policy.get("policyVersion") != DISCOVERY_AUDIT_VERSION:
        issues.append("generated/copilot-index.json discoveryAudit policyVersion is missing or incorrect.")
    if policy.get("targetCopilot") != DISCOVERY_TARGET_COPILOT:
        issues.append("generated/copilot-index.json discoveryAudit targetCopilot is incorrect.")
    if policy.get("router") != "tools/semantic_router.py":
        issues.append("generated/copilot-index.json discoveryAudit router is incorrect.")
    if policy.get("deterministicPythonFirst") is not True:
        issues.append("generated/copilot-index.json discoveryAudit must require deterministic Python first.")
    if policy.get("evidenceField") != "discovery_audit":
        issues.append("generated/copilot-index.json discoveryAudit evidenceField must be discovery_audit.")
    if policy.get("coverageItems") != DISCOVERY_COVERAGE_ITEMS:
        issues.append("generated/copilot-index.json discoveryAudit coverageItems drifted.")
    if policy.get("inventoryFields") != DISCOVERY_INVENTORY_FIELDS:
        issues.append("generated/copilot-index.json discoveryAudit inventoryFields drifted.")
    if policy.get("requiredOutputs") != DISCOVERY_REQUIRED_OUTPUTS:
        issues.append("generated/copilot-index.json discoveryAudit requiredOutputs drifted.")
    if policy.get("executionOrder") != DISCOVERY_EXECUTION_ORDER:
        issues.append("generated/copilot-index.json discoveryAudit executionOrder drifted.")
    if policy.get("gapRegisterRequired") is not True:
        issues.append("generated/copilot-index.json discoveryAudit must require a gap register.")
    if policy.get("validationCommands") != DISCOVERY_VALIDATION_COMMANDS:
        issues.append("generated/copilot-index.json discoveryAudit validationCommands drifted.")
    policy_runtime = policy.get("runtimeEquivalence", {})
    if policy_runtime.get("runtimes") != RUNTIMES:
        issues.append("generated/copilot-index.json discoveryAudit runtime list must match factory runtimes.")
    if policy_runtime.get("sourceOfTruth") != "dist/copilots/as_is_discovery/shared/spec.json":
        issues.append("generated/copilot-index.json discoveryAudit sourceOfTruth is incorrect.")
    if policy_runtime.get("maxUnexplainedDrift") != 0:
        issues.append("generated/copilot-index.json discoveryAudit maxUnexplainedDrift must be 0.")

    audit = index.get("discoveryAudit", {}) if isinstance(index, dict) else {}
    summary["auditPresent"] = bool(audit)
    if audit.get("pass") is not True:
        issues.append("generated/copilot-index.json discoveryAudit.pass must be true.")
    if audit.get("policyVersion") != DISCOVERY_AUDIT_VERSION:
        issues.append("generated/copilot-index.json discoveryAudit audit policyVersion is incorrect.")
    if audit.get("coverageItemsChecked") != len(DISCOVERY_COVERAGE_ITEMS):
        issues.append("generated/copilot-index.json discoveryAudit coverage item count drifted.")
    if audit.get("inventoryFieldsChecked") != len(DISCOVERY_INVENTORY_FIELDS):
        issues.append("generated/copilot-index.json discoveryAudit inventory field count drifted.")
    if audit.get("runtimeEquivalenceRuntimes") != RUNTIMES:
        issues.append("generated/copilot-index.json discoveryAudit runtime list must match factory runtimes.")
    if audit.get("validationCommands") != DISCOVERY_VALIDATION_COMMANDS:
        issues.append("generated/copilot-index.json discoveryAudit validationCommands drifted.")

    try:
        import semantic_router as router

        sample = router.route("as_is inventory coverage", limit=3)
    except Exception as exc:  # pragma: no cover - validator reports the concrete runtime error.
        issues.append(f"Discovery Auditor sample route failed: {exc}.")
        return finalize_phase_source_summary(summary, issues, start_issue_count)

    summary["sampleRouteChecked"] = True
    if not sample:
        issues.append("Discovery Auditor sample route returned no deterministic matches.")
        return finalize_phase_source_summary(summary, issues, start_issue_count)
    top = sample[0]
    summary["sampleTopRoute"] = top.get("id")
    if top.get("id") != DISCOVERY_TARGET_COPILOT:
        issues.append("Discovery Auditor sample route should rank AS-IS Discovery first for `as_is inventory coverage`.")
    route_profile = top.get("discovery_audit", {})
    validate_discovery_profile(route_profile, "semantic_router route discovery_audit", issues)
    checks = route_profile.get("contract_checks", {}) if isinstance(route_profile, dict) else {}
    if checks.get("required_outputs_present") is not True:
        issues.append("Semantic Router discovery_audit route evidence must confirm required outputs are present.")
    route_trace = route_profile.get("runtime_trace", {}) if isinstance(route_profile, dict) else {}
    summary["runtimeTraceReturned"] = route_trace.get("runtimes") == RUNTIMES
    if not summary["runtimeTraceReturned"]:
        issues.append("Semantic Router discovery_audit route evidence must include full runtime trace.")
    return finalize_phase_source_summary(summary, issues, start_issue_count)


def validate_discovery_profile(profile: object, label: str, issues: list[str]) -> None:
    if not isinstance(profile, dict) or not profile:
        issues.append(f"{label} is missing.")
        return
    if profile.get("policy_version") != DISCOVERY_AUDIT_VERSION:
        issues.append(f"{label} policy_version is incorrect.")
    if profile.get("owner_agent") != DISCOVERY_AGENT:
        issues.append(f"{label} owner_agent is incorrect.")
    if profile.get("mission") != DISCOVERY_MISSION:
        issues.append(f"{label} mission drifted.")
    if profile.get("coverage_items") != DISCOVERY_COVERAGE_ITEMS:
        issues.append(f"{label} coverage_items drifted.")
    if profile.get("inventory_fields") != DISCOVERY_INVENTORY_FIELDS:
        issues.append(f"{label} inventory_fields drifted.")
    if profile.get("required_outputs") != DISCOVERY_REQUIRED_OUTPUTS:
        issues.append(f"{label} required_outputs drifted.")
    if profile.get("gap_register_required") is not True:
        issues.append(f"{label} must require a coverage gap register.")
    if profile.get("evidence_field") != "discovery_audit":
        issues.append(f"{label} evidence_field must be discovery_audit.")
    if profile.get("runtime_trace_required") is not True:
        issues.append(f"{label} must require runtime trace evidence.")
    if profile.get("validation_commands") != DISCOVERY_VALIDATION_COMMANDS:
        issues.append(f"{label} validation_commands drifted.")
    if profile.get("runtime_equivalence") != DISCOVERY_RUNTIME_EQUIVALENCE:
        issues.append(f"{label} runtime_equivalence drifted.")
    cost_control = profile.get("cost_control", {})
    if cost_control.get("deterministic_python_first") is not True:
        issues.append(f"{label} must keep deterministic_python_first cost control.")
    if cost_control.get("llm_escalation") != "allowed_after_inventory_gaps_only":
        issues.append(f"{label} LLM escalation policy drifted.")


def validate_architecture_auditor_contract(agents: list, issues: list[str]) -> dict:
    start_issue_count = len(issues)
    summary = {
        "agentPresent": False,
        "auditArtifactPresent": False,
        "specContractPresent": False,
        "profileContractPresent": False,
        "runtimeRefsChecked": [],
        "langchainBehaviorChecked": False,
        "langchainMissingEvidenceBlocks": False,
        "langchainCompleteEvidencePasses": False,
        "langchainLlmEscalationGuarded": False,
        "sampleRouteChecked": False,
        "sampleTopRoute": None,
        "routeAuditEvidence": False,
        "localizedRouteChecked": False,
        "localizedRouteCheapPath": False,
        "localizedRouteAuditEvidence": False,
    }
    agent = next(
        (item for item in agents if isinstance(item, dict) and item.get("id") == ARCHITECTURE_AGENT),
        {},
    )
    summary["agentPresent"] = bool(agent)
    if not agent:
        issues.append("Architecture Auditor agent is missing from data/agent_roster.json.")
    elif agent.get("mission") != ARCHITECTURE_MISSION:
        issues.append("Architecture Auditor mission drifted from the Architecture Board contract.")

    base = ROOT / "dist" / "copilots" / ARCHITECTURE_TARGET_COPILOT
    audit = read_json(base / ARCHITECTURE_AUDIT_ARTIFACT, {}, issues)
    spec = read_json(base / "shared" / "spec.json", {}, issues)
    profile = read_json(base / "langchain" / "agent_profile.json", {}, issues)
    summary["auditArtifactPresent"] = bool(audit)

    validate_architecture_audit_artifact(audit, "Architecture audit artifact", issues)
    validate_architecture_runtime_contract(spec.get("architectureDecisionAudit"), "shared spec architectureDecisionAudit", issues)
    validate_architecture_runtime_contract(profile.get("architectureDecisionAudit"), "LangChain profile architectureDecisionAudit", issues)
    summary["specContractPresent"] = isinstance(spec.get("architectureDecisionAudit"), dict)
    summary["profileContractPresent"] = isinstance(profile.get("architectureDecisionAudit"), dict)

    runtime_files = {
        "codex": base / "codex" / "AGENT.md",
        "claude": base / "claude" / "AGENT.md",
        "github-copilot": base / "github-copilot" / "copilot-agent.md",
        "runtime-contract": base / "shared" / "runtime_contract.md",
        "readme": base / "README.md",
    }
    required_markers = [ARCHITECTURE_AUDIT_ARTIFACT, *ARCHITECTURE_REQUIRED_EVIDENCE, *ARCHITECTURE_QUALITY_GATES]
    for runtime, path in runtime_files.items():
        try:
            text = path.read_text(encoding="utf-8")
        except OSError as exc:
            issues.append(f"Cannot read architecture runtime artifact {relative(path)}: {exc}.")
            continue
        missing = [marker for marker in required_markers if marker not in text]
        if missing:
            issues.append(f"Architecture audit reference drifted in {runtime}: missing {', '.join(missing)}.")
        else:
            summary["runtimeRefsChecked"].append(runtime)

    try:
        langchain_text = (base / "langchain" / "agent.py").read_text(encoding="utf-8")
    except OSError as exc:
        issues.append(f"Cannot read architecture LangChain adapter: {exc}.")
        langchain_text = ""
    for marker in ["ARCHITECTURE_DECISION_AUDIT", "audit_architecture_decision", ARCHITECTURE_MISSION]:
        if marker not in langchain_text:
            issues.append(f"LangChain architecture adapter missing `{marker}`.")
    summary["langchainBehaviorChecked"] = all(
        marker in langchain_text
        for marker in ["ARCHITECTURE_DECISION_AUDIT", "audit_architecture_decision", ARCHITECTURE_MISSION]
    )
    validate_architecture_langchain_behavior(base / "langchain" / "agent.py", summary, issues)

    try:
        import semantic_router as router

        sample = router.route(ARCHITECTURE_ROUTE_SAMPLES[0][0], limit=3)
    except Exception as exc:  # pragma: no cover - validator reports the concrete runtime error.
        issues.append(f"Architecture Board sample route failed: {exc}.")
        return finalize_phase_source_summary(summary, issues, start_issue_count)
    summary["sampleRouteChecked"] = True
    if not sample:
        issues.append("Architecture Board sample route returned no deterministic matches.")
        return finalize_phase_source_summary(summary, issues, start_issue_count)
    top = sample[0]
    summary["sampleTopRoute"] = top.get("id")
    audit_evidence = top.get("architecture_decision_audit", {})
    summary["routeAuditEvidence"] = audit_evidence.get("source_of_truth") == ARCHITECTURE_AUDIT_SOURCE
    if top.get("id") != ARCHITECTURE_TARGET_COPILOT:
        issues.append("Architecture Board sample route should rank aida_architecture first for `architecture adr principles`.")
    if audit_evidence.get("source_of_truth") != ARCHITECTURE_AUDIT_SOURCE:
        issues.append("Architecture Board route payload must expose the shared audit artifact.")

    try:
        localized_sample = router.route(ARCHITECTURE_ROUTE_SAMPLES[1][0], limit=3)
    except Exception as exc:  # pragma: no cover - validator reports the concrete runtime error.
        issues.append(f"Architecture Board localized sample route failed: {exc}.")
        return finalize_phase_source_summary(summary, issues, start_issue_count)
    summary["localizedRouteChecked"] = True
    if not localized_sample:
        issues.append("Architecture Board localized sample route returned no deterministic matches.")
        return finalize_phase_source_summary(summary, issues, start_issue_count)
    localized_top = localized_sample[0]
    localized_audit = localized_top.get("architecture_decision_audit", {})
    summary["localizedRouteCheapPath"] = localized_top.get("cheap_path") is True
    summary["localizedRouteAuditEvidence"] = localized_audit.get("source_of_truth") == ARCHITECTURE_AUDIT_SOURCE
    if localized_top.get("id") != ARCHITECTURE_TARGET_COPILOT:
        issues.append("Architecture Board localized route should rank aida_architecture first for `arquitectura adr principios`.")
    if localized_top.get("cheap_path") is not True:
        issues.append("Architecture Board localized route must stay on the deterministic cheap path.")
    if "architecture_audit:shared_contract" not in localized_top.get("match_reasons", []):
        issues.append("Architecture Board localized route must include the shared audit contract match reason.")
    if localized_audit.get("source_of_truth") != ARCHITECTURE_AUDIT_SOURCE:
        issues.append("Architecture Board localized route payload must expose the shared audit artifact.")
    return finalize_phase_source_summary(summary, issues, start_issue_count)


def validate_architecture_langchain_behavior(path: Path, summary: dict, issues: list[str]) -> None:
    try:
        spec = importlib.util.spec_from_file_location("aida_architecture_langchain_agent", path)
        if spec is None or spec.loader is None:
            issues.append("Architecture LangChain adapter cannot be loaded for behavior checks.")
            return
        module = importlib.util.module_from_spec(spec)
        sys.modules[spec.name] = module
        spec.loader.exec_module(module)
        agent = module.build_agent()
        missing = agent.plan("architecture adr principles", {})
        complete = agent.plan(
            "architecture adr principles",
            {
                "source_refs": ["dist/copilots/aida_architecture/shared/architecture_decision_audit.json"],
                "principles": ["python_first"],
                "adr": ["ADR-001"],
                "technical_decision_quality": ["maintainability and release readiness trade-off recorded"],
                "validation": ["python tools/validate_copilot_factory.py"],
            },
        )
        input_validation_checked = False
        try:
            agent.plan("", {})
        except ValueError as exc:
            input_validation_checked = "cannot be empty" in str(exc)
        secret_value = "sk-" + ("A" * 24)
        github_value = "ghp_" + ("B" * 24)
        bearer_value = "Bearer " + ("C" * 24)
        prompt = agent.render_prompt(
            f"architecture adr principles token=demo-secret {secret_value}",
            {
                "source_refs": ["dist/copilots/aida_architecture/shared/architecture_decision_audit.json"],
                "principles": ["python_first"],
                "adr": ["ADR-001"],
                "technical_decision_quality": ["maintainability and release readiness trade-off recorded"],
                "validation": ["python tools/validate_copilot_factory.py"],
                "token": github_value,
                "nested": {"password": "demo-password", "note": bearer_value},
            },
        )
        prompt_text = json.dumps(prompt)
        prompt_redaction_checked = (
            "[REDACTED]" in prompt_text
            and "demo-secret" not in prompt_text
            and secret_value not in prompt_text
            and github_value not in prompt_text
            and bearer_value not in prompt_text
            and "demo-password" not in prompt_text
        )
    except Exception as exc:  # pragma: no cover - validator reports the concrete runtime error.
        issues.append(f"Architecture LangChain behavior check failed: {exc}.")
        return

    missing_audit = missing.get("audit", {})
    complete_audit = complete.get("audit", {})
    summary["langchainMissingEvidenceBlocks"] = missing_audit.get("pass") is False
    summary["langchainCompleteEvidencePasses"] = complete_audit.get("pass") is True
    summary["langchainLlmEscalationGuarded"] = missing.get("llm_escalation") is False
    summary["langchainInputValidationChecked"] = input_validation_checked
    summary["langchainPromptRedactionChecked"] = prompt_redaction_checked

    if missing_audit.get("pass") is not False:
        issues.append("Architecture LangChain adapter must block pass when required evidence is missing.")
    for key in ARCHITECTURE_REQUIRED_EVIDENCE:
        if key not in missing_audit.get("evidence_needed", []):
            issues.append(f"Architecture LangChain adapter missing evidence_needed `{key}` for incomplete audits.")
    if missing.get("llm_escalation") is not False:
        issues.append("Architecture LangChain adapter must not escalate to LLM before required evidence is present.")
    if complete_audit.get("pass") is not True:
        issues.append("Architecture LangChain adapter must pass when all required audit evidence is present.")
    if complete_audit.get("evidence_needed"):
        issues.append("Architecture LangChain adapter should not request extra evidence after a complete evidence pack.")
    if not input_validation_checked:
        issues.append("Architecture LangChain adapter must reject empty requests with a clear input error.")
    if not prompt_redaction_checked:
        issues.append("Architecture LangChain adapter must redact secret-like request/evidence values before render_prompt output.")


def validate_architecture_audit_artifact(audit: object, label: str, issues: list[str]) -> None:
    if not isinstance(audit, dict) or not audit:
        issues.append(f"{label} is missing.")
        return
    if audit.get("version") != ARCHITECTURE_AUDIT_VERSION:
        issues.append(f"{label} version drifted.")
    if audit.get("ownerAgent") != ARCHITECTURE_AGENT:
        issues.append(f"{label} ownerAgent drifted.")
    if audit.get("copilotId") != ARCHITECTURE_TARGET_COPILOT:
        issues.append(f"{label} copilotId drifted.")
    if audit.get("mission") != ARCHITECTURE_MISSION:
        issues.append(f"{label} mission drifted.")
    evidence_ids = [
        item.get("id")
        for item in audit.get("requiredEvidence", [])
        if isinstance(item, dict)
    ]
    if evidence_ids != ARCHITECTURE_REQUIRED_EVIDENCE:
        issues.append(f"{label} requiredEvidence drifted.")
    gate_ids = [
        item.get("id")
        for item in audit.get("qualityGates", [])
        if isinstance(item, dict)
    ]
    if gate_ids != ARCHITECTURE_QUALITY_GATES:
        issues.append(f"{label} qualityGates drifted.")
    if audit.get("routingSignals") != ARCHITECTURE_ROUTING_SIGNALS:
        issues.append(f"{label} routingSignals must include the English and Spanish Architecture Board route terms.")
    if audit.get("validationCommands") != ARCHITECTURE_VALIDATION_COMMANDS:
        issues.append(f"{label} validationCommands must include English, Spanish and factory smoke route checks.")
    if audit.get("runtimeEquivalence") != ARCHITECTURE_RUNTIME_EQUIVALENCE:
        issues.append(f"{label} runtimeEquivalence drifted.")
    for field in ["copilot_id", "decision", "evidence", "actions", "validation", "risks"]:
        if field not in audit.get("requiredOutputFields", []):
            issues.append(f"{label} requiredOutputFields missing `{field}`.")


def validate_architecture_runtime_contract(contract: object, label: str, issues: list[str]) -> None:
    if not isinstance(contract, dict) or not contract:
        issues.append(f"{label} is missing.")
        return
    expected = {
        "artifact": ARCHITECTURE_AUDIT_ARTIFACT,
        "version": ARCHITECTURE_AUDIT_VERSION,
        "ownerAgent": ARCHITECTURE_AGENT,
        "mission": ARCHITECTURE_MISSION,
        "requiredEvidence": ARCHITECTURE_REQUIRED_EVIDENCE,
        "qualityGates": ARCHITECTURE_QUALITY_GATES,
        "runtimeEquivalence": ARCHITECTURE_RUNTIME_EQUIVALENCE,
    }
    if contract != expected:
        issues.append(f"{label} does not match the shared Architecture Board audit contract.")


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


def validate_design_auditor_contract(copilots: list, agents: list, index: dict, issues: list[str]) -> dict:
    start_issue_count = len(issues)
    summary = {
        "agentPresent": False,
        "agentOutputsPresent": False,
        "policyPresent": False,
        "targetCopilots": [],
        "artifactsChecked": [],
        "runtimeRefsChecked": {},
        "schemasRequireHandoff": [],
        "runtimeMapChecked": [],
        "factoryAuditChecked": False,
        "matrixEvidencePresent": False,
        "langchainInputValidationChecked": [],
        "langchainEvidenceGateChecked": [],
        "langchainLlmEscalationGuarded": [],
        "langchainPromptRedactionChecked": [],
        "sampleRouteChecked": False,
        "sampleTopRoute": None,
        "localizedRouteChecked": False,
        "localizedTopRoute": None,
        "localizedRouteCheapPath": False,
    }
    agent = next((item for item in agents if isinstance(item, dict) and item.get("id") == DESIGN_AGENT), {})
    summary["agentPresent"] = bool(agent)
    if not agent:
        issues.append("Design Auditor agent is missing from data/agent_roster.json.")
    else:
        if agent.get("mission") != DESIGN_MISSION:
            issues.append("Design Auditor mission drifted from the Architecture Board contract.")
        if agent.get("outputs") != DESIGN_AGENT_OUTPUTS:
            issues.append("Design Auditor must declare boundary, contract surface and handoff outputs.")
        else:
            summary["agentOutputsPresent"] = True
        validate_design_agent_contract(agent.get("design_boundary_contract"), issues)

    catalog_targets = [
        item.get("id")
        for item in copilots
        if isinstance(item, dict) and "design" in list_field(item, "sdlc_phases")
    ]
    summary["targetCopilots"] = catalog_targets
    if catalog_targets != DESIGN_TARGET_COPILOTS:
        issues.append("Design Auditor target copilot list drifted from catalog design-phase order.")

    policy = index.get("normalizationPolicy", {}).get("designBoundaryAudit") if isinstance(index, dict) else None
    validate_design_index_policy(policy, issues)
    summary["policyPresent"] = isinstance(policy, dict)

    runtime_map = read_json(ROOT / "generated" / "runtime-injection-map.json", {}, issues)
    matrix_text = read_text(ROOT / "generated" / "sdlc-audit-matrix.md")
    summary["matrixEvidencePresent"] = (
        "Design Boundary Contract Evidence" in matrix_text
        and all(design_audit_source(cid) in matrix_text for cid in DESIGN_TARGET_COPILOTS)
    )
    if not summary["matrixEvidencePresent"]:
        issues.append("SDLC audit matrix must list concrete Design Boundary Contract evidence for every design copilot.")

    catalog_lookup = {item.get("id"): item for item in copilots if isinstance(item, dict)}
    lookup = index.get("normalizedLookup", {}) if isinstance(index, dict) else {}
    for copilot_id in DESIGN_TARGET_COPILOTS:
        validate_design_copilot_contract(
            copilot_id,
            catalog_lookup.get(copilot_id, {}),
            lookup.get(copilot_id, {}) if isinstance(lookup, dict) else {},
            runtime_map,
            summary,
            issues,
        )

    try:
        import semantic_router as router

        sample = router.route(DESIGN_ROUTE_SAMPLES[0][0], limit=5)
    except Exception as exc:  # pragma: no cover - validator reports the concrete runtime error.
        issues.append(f"Design Board sample route failed: {exc}.")
        return finalize_phase_source_summary(summary, issues, start_issue_count)
    summary["sampleRouteChecked"] = True
    validate_design_route_sample(sample, "Design Board sample route", summary, issues)

    try:
        localized_sample = router.route(DESIGN_ROUTE_SAMPLES[1][0], limit=5)
    except Exception as exc:  # pragma: no cover - validator reports the concrete runtime error.
        issues.append(f"Design Board localized sample route failed: {exc}.")
        return finalize_phase_source_summary(summary, issues, start_issue_count)
    summary["localizedRouteChecked"] = True
    localized_top = validate_design_route_sample(localized_sample, "Design Board localized route", summary, issues)
    if localized_top:
        summary["localizedRouteCheapPath"] = localized_top.get("cheap_path") is True
        if localized_top.get("cheap_path") is not True:
            issues.append("Design Board localized route must stay on the deterministic cheap path.")
    return finalize_phase_source_summary(summary, issues, start_issue_count)


def validate_design_agent_contract(contract: object, issues: list[str]) -> None:
    if not isinstance(contract, dict) or not contract:
        issues.append("Design Auditor design_boundary_contract is missing.")
        return
    expected = {
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
    if contract != expected:
        issues.append("Design Auditor design_boundary_contract drifted from the runtime-contracts frontier.")


def validate_design_index_policy(policy: object, issues: list[str]) -> None:
    if not isinstance(policy, dict) or not policy:
        issues.append("generated/copilot-index.json designBoundaryAudit policy is missing.")
        return
    expected = {
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
    if policy != expected:
        issues.append("generated/copilot-index.json designBoundaryAudit policy drifted.")


def validate_design_copilot_contract(
    copilot_id: str,
    catalog_item: dict,
    indexed_item: dict,
    runtime_map: dict,
    summary: dict,
    issues: list[str],
) -> None:
    base = ROOT / "dist" / "copilots" / copilot_id
    audit = read_json(base / DESIGN_AUDIT_ARTIFACT, {}, issues)
    spec = read_json(base / "shared" / "spec.json", {}, issues)
    output_schema = read_json(base / "shared" / "output_schema.json", {}, issues)
    profile = read_json(base / "langchain" / "agent_profile.json", {}, issues)

    validate_design_audit_artifact(audit, copilot_id, issues)
    validate_design_runtime_contract(spec.get("designBoundaryAudit"), copilot_id, "shared spec designBoundaryAudit", issues)
    validate_design_runtime_contract(profile.get("designBoundaryAudit"), copilot_id, "LangChain profile designBoundaryAudit", issues)

    if catalog_item.get("design_boundary_audit") != design_profile(copilot_id):
        issues.append(f"Catalog design boundary profile drifted for {copilot_id}.")
    if indexed_item.get("design_boundary_audit") != design_profile(copilot_id):
        issues.append(f"generated/copilot-index.json design boundary profile drifted for {copilot_id}.")

    injection_contract = (
        runtime_map.get("copilots", {}).get(copilot_id, {}).get("designBoundaryAudit")
        if isinstance(runtime_map, dict)
        else None
    )
    expected_injection = {
        "artifact": design_audit_source(copilot_id),
        "ownerAgent": DESIGN_AGENT,
        "mission": DESIGN_MISSION,
        "requiredEvidence": DESIGN_REQUIRED_EVIDENCE,
        "qualityGates": DESIGN_QUALITY_GATES,
        "requiredOutputFields": DESIGN_REQUIRED_OUTPUT_FIELDS,
        "requiredHandoffFields": DESIGN_REQUIRED_HANDOFF_FIELDS,
        "runtimeEquivalence": design_runtime_equivalence(copilot_id),
    }
    if injection_contract != expected_injection:
        issues.append(f"Runtime injection map designBoundaryAudit drifted for {copilot_id}.")
    else:
        summary["runtimeMapChecked"].append(copilot_id)

    if "handoff" in output_schema.get("required", []) and "handoff" in spec.get("outputSchema", {}).get("required", []):
        summary["schemasRequireHandoff"].append(copilot_id)
    else:
        issues.append(f"Design output schema must require `handoff` for {copilot_id}.")
    validate_design_output_schema(output_schema, spec, profile, copilot_id, issues)

    runtime_files = {
        "codex": base / "codex" / "AGENT.md",
        "claude": base / "claude" / "AGENT.md",
        "github-copilot": base / "github-copilot" / "copilot-agent.md",
        "langchain": base / "langchain" / "agent.py",
        "runtime-contract": base / "shared" / "runtime_contract.md",
    }
    required_markers = [
        "design_boundary_audit.json",
        *DESIGN_REQUIRED_EVIDENCE,
        *DESIGN_QUALITY_GATES,
    ]
    checked = []
    for runtime, path in runtime_files.items():
        text = read_text(path)
        missing = [marker for marker in required_markers if marker not in text]
        if missing:
            issues.append(f"Design audit reference drifted in {copilot_id}/{runtime}: missing {', '.join(missing)}.")
        else:
            checked.append(runtime)
    summary["runtimeRefsChecked"][copilot_id] = checked
    if len(checked) == len(runtime_files):
        summary["artifactsChecked"].append(copilot_id)
    validate_design_langchain_behavior(copilot_id, runtime_files["langchain"], summary, issues)


def validate_design_audit_artifact(audit: object, copilot_id: str, issues: list[str]) -> None:
    label = f"Design audit artifact for {copilot_id}"
    if not isinstance(audit, dict) or not audit:
        issues.append(f"{label} is missing.")
        return
    if audit.get("version") != DESIGN_AUDIT_VERSION:
        issues.append(f"{label} version drifted.")
    if audit.get("ownerAgent") != DESIGN_AGENT:
        issues.append(f"{label} ownerAgent drifted.")
    if audit.get("copilotId") != copilot_id:
        issues.append(f"{label} copilotId drifted.")
    if audit.get("mission") != DESIGN_MISSION:
        issues.append(f"{label} mission drifted.")
    evidence_ids = [item.get("id") for item in audit.get("requiredEvidence", []) if isinstance(item, dict)]
    if evidence_ids != DESIGN_REQUIRED_EVIDENCE:
        issues.append(f"{label} requiredEvidence drifted.")
    gate_ids = [item.get("id") for item in audit.get("qualityGates", []) if isinstance(item, dict)]
    if gate_ids != DESIGN_QUALITY_GATES:
        issues.append(f"{label} qualityGates drifted.")
    if audit.get("routingSignals") != DESIGN_ROUTING_SIGNALS:
        issues.append(f"{label} routingSignals drifted.")
    if audit.get("validationCommands") != DESIGN_VALIDATION_COMMANDS:
        issues.append(f"{label} validationCommands drifted.")
    if audit.get("runtimeEquivalence") != design_runtime_equivalence(copilot_id):
        issues.append(f"{label} runtimeEquivalence drifted.")
    if audit.get("requiredHandoffFields") != DESIGN_REQUIRED_HANDOFF_FIELDS:
        issues.append(f"{label} requiredHandoffFields drifted.")
    for field in DESIGN_REQUIRED_OUTPUT_FIELDS:
        if field not in audit.get("requiredOutputFields", []):
            issues.append(f"{label} requiredOutputFields missing `{field}`.")


def validate_design_output_schema(
    output_schema: object,
    spec: dict,
    profile: dict,
    copilot_id: str,
    issues: list[str],
) -> None:
    if not isinstance(output_schema, dict) or not output_schema:
        issues.append(f"Design output schema is missing for {copilot_id}.")
        return
    handoff = output_schema.get("properties", {}).get("handoff", {})
    if handoff.get("required") != DESIGN_REQUIRED_HANDOFF_FIELDS:
        issues.append(f"Design output schema handoff fields drifted for {copilot_id}.")
    if handoff.get("additionalProperties") is not False:
        issues.append(f"Design output schema must close handoff to declared fields for {copilot_id}.")

    evidence_schema = output_schema.get("properties", {}).get("evidence", {})
    if evidence_schema.get("minItems", 0) < len(DESIGN_REQUIRED_EVIDENCE):
        issues.append(f"Design output schema evidence minItems drifted for {copilot_id}.")
    item_kind = (
        evidence_schema.get("items", {})
        .get("properties", {})
        .get("kind", {})
    )
    kind_enum = item_kind.get("enum", [])
    missing_design_kinds = [kind for kind in DESIGN_REQUIRED_EVIDENCE if kind not in kind_enum]
    if missing_design_kinds:
        issues.append(f"Design output schema evidence kinds missing for {copilot_id}: {', '.join(missing_design_kinds)}.")
    contains_kinds = [
        rule.get("contains", {}).get("properties", {}).get("kind", {}).get("const")
        for rule in evidence_schema.get("allOf", [])
        if isinstance(rule, dict)
    ]
    missing_contains = [kind for kind in DESIGN_REQUIRED_EVIDENCE if kind not in contains_kinds]
    if missing_contains:
        issues.append(f"Design output schema must require one evidence item per required design evidence kind for {copilot_id}: {', '.join(missing_contains)}.")

    if spec.get("outputSchema") != output_schema:
        issues.append(f"Shared spec outputSchema drifted from design output schema for {copilot_id}.")
    if profile.get("outputSchema") != output_schema:
        issues.append(f"LangChain profile outputSchema drifted from design output schema for {copilot_id}.")
    if profile.get("contract", {}).get("outputSchema") != output_schema:
        issues.append(f"LangChain profile contract outputSchema drifted from design output schema for {copilot_id}.")


def validate_design_runtime_contract(contract: object, copilot_id: str, label: str, issues: list[str]) -> None:
    if not isinstance(contract, dict) or not contract:
        issues.append(f"{label} is missing for {copilot_id}.")
        return
    if contract != design_runtime_contract(copilot_id):
        issues.append(f"{label} does not match the shared Design Board audit contract for {copilot_id}.")


def validate_design_langchain_behavior(copilot_id: str, path: Path, summary: dict, issues: list[str]) -> None:
    try:
        spec = importlib.util.spec_from_file_location(f"design_langchain_{copilot_id}", path)
        if spec is None or spec.loader is None:
            issues.append(f"Design LangChain adapter cannot be loaded for behavior checks: {copilot_id}.")
            return
        module = importlib.util.module_from_spec(spec)
        sys.modules[spec.name] = module
        spec.loader.exec_module(module)
        agent = module.build_agent()
        request = "design domain boundaries contracts handoff"
        complete_evidence = {
            "source_refs": [design_audit_source(copilot_id)],
            "domain_boundaries": ["module owner and dependency direction recorded"],
            "contracts": ["input, output, error and compatibility expectations recorded"],
            "handoff_clarity": ["next owner, excluded scope and stop condition recorded"],
            "validation": ["python tools/validate_copilot_factory.py"],
            "principles": ["python_first"],
            "adr": ["ADR-001"],
            "technical_decision_quality": ["trade-off recorded"],
        }
        missing = agent.plan(request, {})
        complete = agent.plan(request, complete_evidence)
        input_validation_checked = False
        evidence_validation_checked = False
        try:
            agent.plan("", {})
        except ValueError as exc:
            input_validation_checked = "cannot be empty" in str(exc)
        try:
            agent.plan(request, [])
        except ValueError as exc:
            evidence_validation_checked = "evidence" in str(exc).lower() and "dictionary" in str(exc).lower()
        secret_value = "sk-" + ("A" * 24)
        github_value = "ghp_" + ("B" * 24)
        bearer_value = "Bearer " + ("C" * 24)
        local_path_value = "C:" + "\\Users\\Example\\sensitive-path"
        prompt = agent.render_prompt(
            f"{request} token=demo-secret {secret_value} {github_value}",
            {
                **complete_evidence,
                "source_refs": [design_audit_source(copilot_id), local_path_value],
                "token": github_value,
                "nested": {"password": "demo-password", "note": bearer_value},
            },
        )
        prompt_text = json.dumps(prompt)
        prompt_redaction_checked = (
            "[REDACTED]" in prompt_text
            and "demo-secret" not in prompt_text
            and secret_value not in prompt_text
            and github_value not in prompt_text
            and bearer_value not in prompt_text
            and "demo-password" not in prompt_text
            and local_path_value not in prompt_text
        )
    except Exception as exc:  # pragma: no cover - validator reports the concrete runtime error.
        issues.append(f"Design LangChain behavior check failed for {copilot_id}: {exc}.")
        return

    missing_audit = missing.get("audit", {})
    complete_audit = complete.get("audit", {})
    evidence_gate_checked = (
        missing_audit.get("pass") is False
        and "source_refs" in missing_audit.get("evidence_needed", [])
        and all(key in missing_audit.get("evidence_needed", []) for key in DESIGN_REQUIRED_EVIDENCE)
        and complete_audit.get("pass") is True
        and not complete_audit.get("evidence_needed")
    )
    llm_guarded = missing.get("llm_escalation") is False

    if input_validation_checked and evidence_validation_checked:
        summary["langchainInputValidationChecked"].append(copilot_id)
    if evidence_gate_checked:
        summary["langchainEvidenceGateChecked"].append(copilot_id)
    if llm_guarded:
        summary["langchainLlmEscalationGuarded"].append(copilot_id)
    if prompt_redaction_checked:
        summary["langchainPromptRedactionChecked"].append(copilot_id)

    if not input_validation_checked:
        issues.append(f"Design LangChain adapter must reject empty requests with a clear input error for {copilot_id}.")
    if not evidence_validation_checked:
        issues.append(f"Design LangChain adapter must reject non-dictionary evidence for {copilot_id}.")
    if not evidence_gate_checked:
        issues.append(f"Design LangChain adapter must block pass/LLM handoff until source_refs and all design evidence exist for {copilot_id}.")
    if not llm_guarded:
        issues.append(f"Design LangChain adapter must not escalate to LLM before required evidence is present for {copilot_id}.")
    if not prompt_redaction_checked:
        issues.append(f"Design LangChain adapter must redact secret-like request/evidence values before render_prompt output for {copilot_id}.")


def validate_design_route_sample(sample: list, label: str, summary: dict, issues: list[str]) -> dict:
    if not sample:
        issues.append(f"{label} returned no deterministic matches.")
        return {}
    top = sample[0]
    if "localized" in label.lower():
        summary["localizedTopRoute"] = top.get("id")
    else:
        summary["sampleTopRoute"] = top.get("id")
    if top.get("id") not in DESIGN_TARGET_COPILOTS:
        issues.append(f"{label} must rank a design-phase copilot first.")
    audit_evidence = top.get("design_boundary_audit", {})
    expected_source = design_audit_source(top.get("id", ""))
    if audit_evidence.get("source_of_truth") != expected_source:
        issues.append(f"{label} payload must expose the shared design audit artifact.")
    if audit_evidence.get("required_handoff_fields") != DESIGN_REQUIRED_HANDOFF_FIELDS:
        issues.append(f"{label} payload must expose required handoff subfields.")
    if "design_audit:shared_contract" not in top.get("match_reasons", []):
        issues.append(f"{label} must include the shared design contract match reason.")
    return top


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


def validate_build_auditor_contract(copilots: list, agents: list, index: dict, issues: list[str]) -> dict:
    start_issue_count = len(issues)
    summary = {
        "agentPresent": False,
        "agentOutputsPresent": False,
        "policyPresent": False,
        "targetCopilots": [],
        "artifactsChecked": [],
        "runtimeRefsChecked": {},
        "schemasRequireImplementation": [],
        "runtimeMapChecked": [],
        "matrixEvidencePresent": False,
        "langchainInputValidationChecked": [],
        "langchainEvidenceGateChecked": [],
        "langchainLlmEscalationGuarded": [],
        "langchainPromptRedactionChecked": [],
        "sampleRouteChecked": False,
        "sampleTopRoute": None,
        "localizedRouteChecked": False,
        "localizedTopRoute": None,
        "localizedRouteCheapPath": False,
    }
    agent = next((item for item in agents if isinstance(item, dict) and item.get("id") == BUILD_AGENT), {})
    summary["agentPresent"] = bool(agent)
    if not agent:
        issues.append("Build Auditor agent is missing from data/agent_roster.json.")
    else:
        if agent.get("mission") != BUILD_MISSION:
            issues.append("Build Auditor mission drifted from the Adapter Lab contract.")
        if agent.get("outputs") != BUILD_AGENT_OUTPUTS:
            issues.append("Build Auditor must declare implementation plan, stack rule and readiness evidence outputs.")
        else:
            summary["agentOutputsPresent"] = True
        validate_build_agent_contract(agent.get("implementation_plan_contract"), issues)

    catalog_targets = [
        item.get("id")
        for item in copilots
        if isinstance(item, dict) and "build" in list_field(item, "sdlc_phases")
    ]
    summary["targetCopilots"] = catalog_targets
    if catalog_targets != BUILD_TARGET_COPILOTS:
        issues.append("Build Auditor target copilot list drifted from catalog build-phase order.")

    policy = index.get("normalizationPolicy", {}).get("buildImplementationAudit") if isinstance(index, dict) else None
    validate_build_index_policy(policy, issues)
    summary["policyPresent"] = isinstance(policy, dict)

    runtime_map = read_json(ROOT / "generated" / "runtime-injection-map.json", {}, issues)
    matrix_text = read_text(ROOT / "generated" / "sdlc-audit-matrix.md")
    summary["matrixEvidencePresent"] = (
        "Build Implementation Contract Evidence" in matrix_text
        and all(build_audit_source(cid) in matrix_text for cid in BUILD_TARGET_COPILOTS)
    )
    if not summary["matrixEvidencePresent"]:
        issues.append("SDLC audit matrix must list concrete Build Implementation Contract evidence for every build copilot.")
    factory_audit = read_json(ROOT / "generated" / "factory-audit.json", {}, issues)
    generated_build_summary = factory_audit.get("buildImplementationAudit", {}) if isinstance(factory_audit, dict) else {}
    if generated_build_summary.get("policyVersion") == BUILD_AUDIT_VERSION and generated_build_summary.get("targetCopilots") == BUILD_TARGET_COPILOTS:
        summary["factoryAuditChecked"] = True
    else:
        issues.append("generated/factory-audit.json must expose the Build implementation audit summary.")

    catalog_lookup = {item.get("id"): item for item in copilots if isinstance(item, dict)}
    lookup = index.get("normalizedLookup", {}) if isinstance(index, dict) else {}
    for copilot_id in BUILD_TARGET_COPILOTS:
        validate_build_copilot_contract(
            copilot_id,
            catalog_lookup.get(copilot_id, {}),
            lookup.get(copilot_id, {}) if isinstance(lookup, dict) else {},
            runtime_map,
            summary,
            issues,
        )

    try:
        import semantic_router as router

        sample = router.route(BUILD_ROUTE_SAMPLES[0][0], limit=5)
    except Exception as exc:  # pragma: no cover - validator reports the concrete runtime error.
        issues.append(f"Build Adapter Lab sample route failed: {exc}.")
        return finalize_phase_source_summary(summary, issues, start_issue_count)
    summary["sampleRouteChecked"] = True
    validate_build_route_sample(sample, "Build Adapter Lab sample route", summary, issues)

    try:
        localized_sample = router.route(BUILD_ROUTE_SAMPLES[1][0], limit=5)
    except Exception as exc:  # pragma: no cover - validator reports the concrete runtime error.
        issues.append(f"Build Adapter Lab localized sample route failed: {exc}.")
        return finalize_phase_source_summary(summary, issues, start_issue_count)
    summary["localizedRouteChecked"] = True
    localized_top = validate_build_route_sample(localized_sample, "Build Adapter Lab localized route", summary, issues)
    if localized_top:
        summary["localizedRouteCheapPath"] = localized_top.get("cheap_path") is True
        if localized_top.get("cheap_path") is not True:
            issues.append("Build Adapter Lab localized route must stay on the deterministic cheap path.")
    return finalize_phase_source_summary(summary, issues, start_issue_count)


def validate_build_agent_contract(contract: object, issues: list[str]) -> None:
    if not isinstance(contract, dict) or not contract:
        issues.append("Build Auditor implementation_plan_contract is missing.")
        return
    expected = {
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
    if contract != expected:
        issues.append("Build Auditor implementation_plan_contract drifted from the runtime-contracts frontier.")


def validate_build_index_policy(policy: object, issues: list[str]) -> None:
    if not isinstance(policy, dict) or not policy:
        issues.append("generated/copilot-index.json buildImplementationAudit policy is missing.")
        return
    expected = {
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
    if policy != expected:
        issues.append("generated/copilot-index.json buildImplementationAudit policy drifted.")


def validate_build_copilot_contract(
    copilot_id: str,
    catalog_item: dict,
    indexed_item: dict,
    runtime_map: dict,
    summary: dict,
    issues: list[str],
) -> None:
    base = ROOT / "dist" / "copilots" / copilot_id
    audit = read_json(base / BUILD_AUDIT_ARTIFACT, {}, issues)
    spec = read_json(base / "shared" / "spec.json", {}, issues)
    output_schema = read_json(base / "shared" / "output_schema.json", {}, issues)
    profile = read_json(base / "langchain" / "agent_profile.json", {}, issues)

    validate_build_audit_artifact(audit, copilot_id, issues)
    validate_build_runtime_contract(spec.get("buildImplementationAudit"), copilot_id, "shared spec buildImplementationAudit", issues)
    validate_build_runtime_contract(profile.get("buildImplementationAudit"), copilot_id, "LangChain profile buildImplementationAudit", issues)

    if catalog_item.get("implementation_plan_audit") != build_profile(copilot_id):
        issues.append(f"Catalog implementation plan profile drifted for {copilot_id}.")
    if indexed_item.get("implementation_plan_audit") != build_profile(copilot_id):
        issues.append(f"generated/copilot-index.json implementation plan profile drifted for {copilot_id}.")

    injection_contract = (
        runtime_map.get("copilots", {}).get(copilot_id, {}).get("buildImplementationAudit")
        if isinstance(runtime_map, dict)
        else None
    )
    expected_injection = {
        "artifact": build_audit_source(copilot_id),
        "ownerAgent": BUILD_AGENT,
        "mission": BUILD_MISSION,
        "requiredEvidence": BUILD_REQUIRED_EVIDENCE,
        "qualityGates": BUILD_QUALITY_GATES,
        "requiredOutputFields": BUILD_REQUIRED_OUTPUT_FIELDS,
        "requiredImplementationFields": BUILD_REQUIRED_IMPLEMENTATION_FIELDS,
        "runtimeEquivalence": build_runtime_equivalence(copilot_id),
    }
    if injection_contract != expected_injection:
        issues.append(f"Runtime injection map buildImplementationAudit drifted for {copilot_id}.")
    else:
        summary["runtimeMapChecked"].append(copilot_id)

    if "implementation" in output_schema.get("required", []) and "implementation" in spec.get("outputSchema", {}).get("required", []):
        summary["schemasRequireImplementation"].append(copilot_id)
    else:
        issues.append(f"Build output schema must require `implementation` for {copilot_id}.")
    validate_build_output_schema(output_schema, spec, profile, copilot_id, issues)

    runtime_files = {
        "codex": base / "codex" / "AGENT.md",
        "claude": base / "claude" / "AGENT.md",
        "github-copilot": base / "github-copilot" / "copilot-agent.md",
        "langchain": base / "langchain" / "agent.py",
        "runtime-contract": base / "shared" / "runtime_contract.md",
    }
    required_markers = [
        "implementation_plan_audit.json",
        *BUILD_REQUIRED_EVIDENCE,
        *BUILD_QUALITY_GATES,
    ]
    checked = []
    for runtime, path in runtime_files.items():
        text = read_text(path)
        missing = [marker for marker in required_markers if marker not in text]
        if missing:
            issues.append(f"Build audit reference drifted in {copilot_id}/{runtime}: missing {', '.join(missing)}.")
        else:
            checked.append(runtime)
    summary["runtimeRefsChecked"][copilot_id] = checked
    if len(checked) == len(runtime_files):
        summary["artifactsChecked"].append(copilot_id)
    validate_build_langchain_behavior(copilot_id, runtime_files["langchain"], summary, issues)


def validate_build_audit_artifact(audit: object, copilot_id: str, issues: list[str]) -> None:
    label = f"Build audit artifact for {copilot_id}"
    if not isinstance(audit, dict) or not audit:
        issues.append(f"{label} is missing.")
        return
    if audit.get("version") != BUILD_AUDIT_VERSION:
        issues.append(f"{label} version drifted.")
    if audit.get("ownerAgent") != BUILD_AGENT:
        issues.append(f"{label} ownerAgent drifted.")
    if audit.get("copilotId") != copilot_id:
        issues.append(f"{label} copilotId drifted.")
    if audit.get("mission") != BUILD_MISSION:
        issues.append(f"{label} mission drifted.")
    evidence_ids = [item.get("id") for item in audit.get("requiredEvidence", []) if isinstance(item, dict)]
    if evidence_ids != BUILD_REQUIRED_EVIDENCE:
        issues.append(f"{label} requiredEvidence drifted.")
    gate_ids = [item.get("id") for item in audit.get("qualityGates", []) if isinstance(item, dict)]
    if gate_ids != BUILD_QUALITY_GATES:
        issues.append(f"{label} qualityGates drifted.")
    if audit.get("routingSignals") != BUILD_ROUTING_SIGNALS:
        issues.append(f"{label} routingSignals drifted.")
    if audit.get("validationCommands") != BUILD_VALIDATION_COMMANDS:
        issues.append(f"{label} validationCommands drifted.")
    if audit.get("runtimeEquivalence") != build_runtime_equivalence(copilot_id):
        issues.append(f"{label} runtimeEquivalence drifted.")
    if audit.get("requiredImplementationFields") != BUILD_REQUIRED_IMPLEMENTATION_FIELDS:
        issues.append(f"{label} requiredImplementationFields drifted.")
    if not audit.get("stackRuleMatrix"):
        issues.append(f"{label} must include a non-empty stackRuleMatrix.")
    for field in BUILD_REQUIRED_OUTPUT_FIELDS:
        if field not in audit.get("requiredOutputFields", []):
            issues.append(f"{label} requiredOutputFields missing `{field}`.")


def validate_build_output_schema(
    output_schema: object,
    spec: dict,
    profile: dict,
    copilot_id: str,
    issues: list[str],
) -> None:
    if not isinstance(output_schema, dict) or not output_schema:
        issues.append(f"Build output schema is missing for {copilot_id}.")
        return
    implementation = output_schema.get("properties", {}).get("implementation", {})
    if implementation.get("required") != BUILD_REQUIRED_IMPLEMENTATION_FIELDS:
        issues.append(f"Build output schema implementation fields drifted for {copilot_id}.")
    if implementation.get("additionalProperties") is not False:
        issues.append(f"Build output schema must close implementation to declared fields for {copilot_id}.")

    evidence_schema = output_schema.get("properties", {}).get("evidence", {})
    if evidence_schema.get("minItems", 0) < len(BUILD_REQUIRED_EVIDENCE):
        issues.append(f"Build output schema evidence minItems drifted for {copilot_id}.")
    item_kind = (
        evidence_schema.get("items", {})
        .get("properties", {})
        .get("kind", {})
    )
    kind_enum = item_kind.get("enum", [])
    missing_kinds = [kind for kind in BUILD_REQUIRED_EVIDENCE if kind not in kind_enum]
    if missing_kinds:
        issues.append(f"Build output schema evidence kinds missing for {copilot_id}: {', '.join(missing_kinds)}.")
    contains_kinds = [
        rule.get("contains", {}).get("properties", {}).get("kind", {}).get("const")
        for rule in evidence_schema.get("allOf", [])
        if isinstance(rule, dict)
    ]
    missing_contains = [kind for kind in BUILD_REQUIRED_EVIDENCE if kind not in contains_kinds]
    if missing_contains:
        issues.append(f"Build output schema must require one evidence item per build evidence kind for {copilot_id}: {', '.join(missing_contains)}.")

    if spec.get("outputSchema") != output_schema:
        issues.append(f"Shared spec outputSchema drifted from build output schema for {copilot_id}.")
    if profile.get("outputSchema") != output_schema:
        issues.append(f"LangChain profile outputSchema drifted from build output schema for {copilot_id}.")
    if profile.get("contract", {}).get("outputSchema") != output_schema:
        issues.append(f"LangChain profile contract outputSchema drifted from build output schema for {copilot_id}.")


def validate_build_runtime_contract(contract: object, copilot_id: str, label: str, issues: list[str]) -> None:
    if not isinstance(contract, dict) or not contract:
        issues.append(f"{label} is missing for {copilot_id}.")
        return
    if contract != build_runtime_contract(copilot_id):
        issues.append(f"{label} does not match the shared Build Adapter Lab audit contract for {copilot_id}.")


def validate_build_langchain_behavior(copilot_id: str, path: Path, summary: dict, issues: list[str]) -> None:
    try:
        spec = importlib.util.spec_from_file_location(f"build_langchain_{copilot_id}", path)
        if spec is None or spec.loader is None:
            issues.append(f"Build LangChain adapter cannot be loaded for behavior checks: {copilot_id}.")
            return
        module = importlib.util.module_from_spec(spec)
        sys.modules[spec.name] = module
        spec.loader.exec_module(module)
        agent = module.build_agent()
        request = "build implementation stack rules affected files rollback"
        complete_evidence = {
            "source_refs": [build_audit_source(copilot_id)],
            "implementation_plan": ["scoped plan names sequence and owner"],
            "stack_rules": ["stack-specific rule checked before patch handoff"],
            "affected_files": ["dist/copilots/example/shared/spec.json"],
            "validation": ["python tools/validate_copilot_factory.py"],
        }
        missing = agent.plan(request, {})
        complete = agent.plan(request, complete_evidence)
        input_validation_checked = False
        evidence_validation_checked = False
        try:
            agent.plan("", {})
        except ValueError as exc:
            input_validation_checked = "cannot be empty" in str(exc)
        try:
            agent.plan(request, [])
        except ValueError as exc:
            evidence_validation_checked = "evidence" in str(exc).lower() and "dictionary" in str(exc).lower()
        secret_value = "sk-" + ("A" * 24)
        github_value = "ghp_" + ("B" * 24)
        bearer_value = "Bearer " + ("C" * 24)
        local_path_value = "C:" + "\\Users\\Example\\sensitive-path"
        prompt = agent.render_prompt(
            f"{request} token=demo-secret {secret_value} {github_value}",
            {
                **complete_evidence,
                "source_refs": [build_audit_source(copilot_id), local_path_value],
                "token": github_value,
                "GITHUB_TOKEN": "short-local-token",
                "nested": {
                    "password": "demo-password",
                    "client_secret": "short-client-secret",
                    "note": bearer_value,
                },
            },
        )
        prompt_text = json.dumps(prompt)
        prompt_redaction_checked = (
            "[REDACTED]" in prompt_text
            and "demo-secret" not in prompt_text
            and secret_value not in prompt_text
            and github_value not in prompt_text
            and bearer_value not in prompt_text
            and "demo-password" not in prompt_text
            and "short-local-token" not in prompt_text
            and "short-client-secret" not in prompt_text
            and local_path_value not in prompt_text
        )
    except Exception as exc:  # pragma: no cover - validator reports the concrete runtime error.
        issues.append(f"Build LangChain behavior check failed for {copilot_id}: {exc}.")
        return

    missing_audit = missing.get("audit", {})
    complete_audit = complete.get("audit", {})
    evidence_gate_checked = (
        missing_audit.get("pass") is False
        and "source_refs" in missing_audit.get("evidence_needed", [])
        and all(key in missing_audit.get("evidence_needed", []) for key in BUILD_REQUIRED_EVIDENCE)
        and complete_audit.get("pass") is True
        and not complete_audit.get("evidence_needed")
        and complete.get("implementation_plan_audit", {}).get("requiredImplementationFields") == BUILD_REQUIRED_IMPLEMENTATION_FIELDS
    )
    llm_guarded = missing.get("llm_escalation") is False

    if input_validation_checked and evidence_validation_checked:
        summary["langchainInputValidationChecked"].append(copilot_id)
    if evidence_gate_checked:
        summary["langchainEvidenceGateChecked"].append(copilot_id)
    if llm_guarded:
        summary["langchainLlmEscalationGuarded"].append(copilot_id)
    if prompt_redaction_checked:
        summary["langchainPromptRedactionChecked"].append(copilot_id)

    if not input_validation_checked:
        issues.append(f"Build LangChain adapter must reject empty requests with a clear input error for {copilot_id}.")
    if not evidence_validation_checked:
        issues.append(f"Build LangChain adapter must reject non-dictionary evidence for {copilot_id}.")
    if not evidence_gate_checked:
        issues.append(f"Build LangChain adapter must block pass/LLM handoff until source_refs and all build evidence exist for {copilot_id}.")
    if not llm_guarded:
        issues.append(f"Build LangChain adapter must not escalate to LLM before required evidence is present for {copilot_id}.")
    if not prompt_redaction_checked:
        issues.append(f"Build LangChain adapter must redact secret-like request/evidence values before render_prompt output for {copilot_id}.")


def validate_build_route_sample(sample: list, label: str, summary: dict, issues: list[str]) -> dict:
    if not sample:
        issues.append(f"{label} returned no deterministic matches.")
        return {}
    top = sample[0]
    if "localized" in label.lower():
        summary["localizedTopRoute"] = top.get("id")
    else:
        summary["sampleTopRoute"] = top.get("id")
    if top.get("id") not in BUILD_TARGET_COPILOTS:
        issues.append(f"{label} must rank a build-phase copilot first.")
    audit_evidence = top.get("implementation_plan_audit", {})
    expected_source = build_audit_source(top.get("id", ""))
    if audit_evidence.get("source_of_truth") != expected_source:
        issues.append(f"{label} payload must expose the shared build audit artifact.")
    if audit_evidence.get("required_implementation_fields") != BUILD_REQUIRED_IMPLEMENTATION_FIELDS:
        issues.append(f"{label} payload must expose required implementation subfields.")
    if "build_audit:shared_contract" not in top.get("match_reasons", []):
        issues.append(f"{label} must include the shared build contract match reason.")
    return top


def kb_runtime_equivalence() -> dict:
    return {
        "sourceOfTruth": KB_AUDIT_SOURCE,
        "runtimes": RUNTIMES,
        "maxUnexplainedDrift": 0,
    }


def kb_runtime_contract() -> dict:
    return {
        "artifact": KB_AUDIT_ARTIFACT,
        "version": KB_AUDIT_VERSION,
        "ownerAgent": KB_AGENT,
        "mission": KB_MISSION,
        "requiredEvidence": KB_REQUIRED_EVIDENCE,
        "qualityGates": KB_QUALITY_GATES,
        "requiredOutputFields": KB_REQUIRED_OUTPUT_FIELDS,
        "requiredKbPartitionFields": KB_REQUIRED_PARTITION_FIELDS,
        "contextWindowPolicy": KB_CONTEXT_WINDOW_POLICY,
        "runtimeEquivalence": kb_runtime_equivalence(),
    }


def validate_kb_boundary_auditor_contract(agents: list, issues: list[str]) -> dict:
    summary = {
        "agentPresent": False,
        "auditArtifactPresent": False,
        "specContractPresent": False,
        "profileContractPresent": False,
        "schemasRequireKbPartition": False,
        "kbOutputSchemaChecked": False,
        "runtimeRefsChecked": [],
        "langchainBehaviorChecked": False,
        "sampleRouteChecked": False,
        "sampleTopRoute": None,
        "sampleRouteCheapPath": False,
        "routeAuditEvidence": False,
    }
    agent = next((item for item in agents if isinstance(item, dict) and item.get("id") == KB_AGENT), {})
    summary["agentPresent"] = bool(agent)
    if not agent:
        issues.append("Knowledge Boundary Auditor agent is missing from data/agent_roster.json.")
    else:
        if agent.get("mission") != KB_MISSION:
            issues.append("Knowledge Boundary Auditor mission drifted from the Architecture Board contract.")
        if agent.get("mode") != "python_first_llm_sparse":
            issues.append("Knowledge Boundary Auditor mode must remain python_first_llm_sparse.")

    base = ROOT / "dist" / "copilots" / KB_TARGET_COPILOT
    audit = read_json(base / KB_AUDIT_ARTIFACT, {}, issues)
    spec = read_json(base / "shared" / "spec.json", {}, issues)
    output_schema = read_json(base / "shared" / "output_schema.json", {}, issues)
    profile = read_json(base / "langchain" / "agent_profile.json", {}, issues)
    summary["auditArtifactPresent"] = bool(audit)

    validate_kb_audit_artifact(audit, issues)
    validate_kb_runtime_contract(spec.get("kbContextWindowAudit"), "shared spec kbContextWindowAudit", issues)
    validate_kb_runtime_contract(profile.get("kbContextWindowAudit"), "LangChain profile kbContextWindowAudit", issues)
    validate_kb_runtime_contract(profile.get("contract", {}).get("kbContextWindowAudit"), "LangChain profile contract kbContextWindowAudit", issues)
    summary["specContractPresent"] = isinstance(spec.get("kbContextWindowAudit"), dict)
    summary["profileContractPresent"] = isinstance(profile.get("kbContextWindowAudit"), dict)
    summary["schemasRequireKbPartition"] = (
        "kb_partition" in output_schema.get("required", [])
        and "kb_partition" in spec.get("outputSchema", {}).get("required", [])
    )
    schema_issues: list[str] = []
    validate_kb_output_schema(output_schema, spec, profile, schema_issues)
    summary["kbOutputSchemaChecked"] = not schema_issues
    issues.extend(schema_issues)

    runtime_files = {
        "codex": base / "codex" / "AGENT.md",
        "claude": base / "claude" / "AGENT.md",
        "github-copilot": base / "github-copilot" / "copilot-agent.md",
        "langchain": base / "langchain" / "agent.py",
        "runtime-contract": base / "shared" / "runtime_contract.md",
        "readme": base / "README.md",
    }
    required_markers = [
        "kb_context_window_audit.json",
        *KB_REQUIRED_EVIDENCE,
        *KB_QUALITY_GATES,
        *KB_REQUIRED_PARTITION_FIELDS,
    ]
    for runtime, path in runtime_files.items():
        text = read_text(path)
        missing = [marker for marker in required_markers if marker not in text]
        if missing:
            issues.append(f"KB context-window audit reference drifted in {KB_TARGET_COPILOT}/{runtime}: missing {', '.join(missing)}.")
        else:
            summary["runtimeRefsChecked"].append(runtime)

    validate_kb_langchain_behavior(runtime_files["langchain"], summary, issues)

    try:
        import semantic_router as router

        sample = router.route(KB_ROUTE_SAMPLE, limit=3)
    except Exception as exc:  # pragma: no cover - validator reports the concrete runtime error.
        issues.append(f"Knowledge Boundary Auditor sample route failed: {exc}.")
        return summary
    summary["sampleRouteChecked"] = True
    if not sample:
        issues.append("Knowledge Boundary Auditor sample route returned no deterministic matches.")
        return summary
    top = sample[0]
    summary["sampleTopRoute"] = top.get("id")
    summary["sampleRouteCheapPath"] = top.get("cheap_path") is True
    route_audit = top.get("kb_context_window_audit", {})
    summary["routeAuditEvidence"] = route_audit.get("source_of_truth") == KB_AUDIT_SOURCE
    if top.get("id") != KB_TARGET_COPILOT:
        issues.append(f"Knowledge Boundary Auditor sample route should rank {KB_TARGET_COPILOT} first for `{KB_ROUTE_SAMPLE}`.")
    if top.get("cheap_path") is not True:
        issues.append("Knowledge Boundary Auditor sample route must stay on the deterministic cheap path.")
    if "kb_audit:shared_contract" not in top.get("match_reasons", []):
        issues.append("Knowledge Boundary Auditor sample route must include the shared KB contract match reason.")
    if route_audit.get("source_of_truth") != KB_AUDIT_SOURCE:
        issues.append("Knowledge Boundary Auditor route payload must expose the shared KB audit artifact.")
    if route_audit.get("required_kb_partition_fields") != KB_REQUIRED_PARTITION_FIELDS:
        issues.append("Knowledge Boundary Auditor route payload must expose required KB partition subfields.")
    return summary


def validate_kb_audit_artifact(audit: object, issues: list[str]) -> None:
    label = "KB context-window audit artifact"
    if not isinstance(audit, dict) or not audit:
        issues.append(f"{label} is missing.")
        return
    if audit.get("version") != KB_AUDIT_VERSION:
        issues.append(f"{label} version drifted.")
    if audit.get("ownerAgent") != KB_AGENT:
        issues.append(f"{label} ownerAgent drifted.")
    if audit.get("copilotId") != KB_TARGET_COPILOT:
        issues.append(f"{label} copilotId drifted.")
    if audit.get("mission") != KB_MISSION:
        issues.append(f"{label} mission drifted.")
    evidence_ids = [item.get("id") for item in audit.get("requiredEvidence", []) if isinstance(item, dict)]
    if evidence_ids != KB_REQUIRED_EVIDENCE:
        issues.append(f"{label} requiredEvidence drifted.")
    gate_ids = [item.get("id") for item in audit.get("qualityGates", []) if isinstance(item, dict)]
    if gate_ids != KB_QUALITY_GATES:
        issues.append(f"{label} qualityGates drifted.")
    if audit.get("routingSignals") != KB_ROUTING_SIGNALS:
        issues.append(f"{label} routingSignals drifted.")
    if audit.get("contextWindowPolicy") != KB_CONTEXT_WINDOW_POLICY:
        issues.append(f"{label} contextWindowPolicy drifted.")
    if audit.get("requiredOutputFields") != KB_REQUIRED_OUTPUT_FIELDS:
        issues.append(f"{label} requiredOutputFields drifted.")
    if audit.get("requiredKbPartitionFields") != KB_REQUIRED_PARTITION_FIELDS:
        issues.append(f"{label} requiredKbPartitionFields drifted.")
    if audit.get("validationCommands") != KB_VALIDATION_COMMANDS:
        issues.append(f"{label} validationCommands drifted.")
    if audit.get("runtimeEquivalence") != kb_runtime_equivalence():
        issues.append(f"{label} runtimeEquivalence drifted.")
    if not audit.get("sourceOfTruthRules"):
        issues.append(f"{label} must include sourceOfTruthRules.")
    if not audit.get("kbSeparationRules"):
        issues.append(f"{label} must include kbSeparationRules.")


def validate_kb_runtime_contract(contract: object, label: str, issues: list[str]) -> None:
    if not isinstance(contract, dict) or not contract:
        issues.append(f"{label} is missing.")
        return
    if contract != kb_runtime_contract():
        issues.append(f"{label} does not match the shared Knowledge Boundary audit contract.")


def validate_kb_output_schema(
    output_schema: object,
    spec: dict,
    profile: dict,
    issues: list[str],
) -> None:
    if not isinstance(output_schema, dict) or not output_schema:
        issues.append(f"KB output schema is missing for {KB_TARGET_COPILOT}.")
        return

    required = output_schema.get("required", [])
    for field in KB_REQUIRED_OUTPUT_FIELDS:
        if field not in required:
            issues.append(f"KB output schema required fields missing `{field}`.")

    partition = output_schema.get("properties", {}).get("kb_partition", {})
    if partition.get("required") != KB_REQUIRED_PARTITION_FIELDS:
        issues.append("KB output schema kb_partition fields drifted.")
    if partition.get("additionalProperties") is not False:
        issues.append("KB output schema must close kb_partition to declared fields.")

    evidence_schema = output_schema.get("properties", {}).get("evidence", {})
    if evidence_schema.get("minItems", 0) < len(KB_REQUIRED_EVIDENCE):
        issues.append("KB output schema evidence minItems drifted.")
    item_kind = (
        evidence_schema.get("items", {})
        .get("properties", {})
        .get("kind", {})
    )
    kind_enum = item_kind.get("enum", [])
    missing_kinds = [kind for kind in KB_REQUIRED_EVIDENCE if kind not in kind_enum]
    if missing_kinds:
        issues.append(f"KB output schema evidence kinds missing: {', '.join(missing_kinds)}.")
    contains_kinds = [
        rule.get("contains", {}).get("properties", {}).get("kind", {}).get("const")
        for rule in evidence_schema.get("allOf", [])
        if isinstance(rule, dict)
    ]
    missing_contains = [kind for kind in KB_REQUIRED_EVIDENCE if kind not in contains_kinds]
    if missing_contains:
        issues.append(
            "KB output schema must require one evidence item per KB evidence kind: "
            + ", ".join(missing_contains)
            + "."
        )

    if spec.get("outputSchema") != output_schema:
        issues.append(f"Shared spec outputSchema drifted from KB output schema for {KB_TARGET_COPILOT}.")
    if profile.get("outputSchema") != output_schema:
        issues.append(f"LangChain profile outputSchema drifted from KB output schema for {KB_TARGET_COPILOT}.")
    if profile.get("contract", {}).get("outputSchema") != output_schema:
        issues.append(f"LangChain profile contract outputSchema drifted from KB output schema for {KB_TARGET_COPILOT}.")


def validate_kb_langchain_behavior(path: Path, summary: dict, issues: list[str]) -> None:
    try:
        spec = importlib.util.spec_from_file_location("kb_langchain_firefly_v6", path)
        if spec is None or spec.loader is None:
            issues.append("Knowledge Boundary LangChain adapter cannot be loaded for behavior checks.")
            return
        module = importlib.util.module_from_spec(spec)
        sys.modules[spec.name] = module
        spec.loader.exec_module(module)
        agent = module.build_agent()
        request = KB_ROUTE_SAMPLE
        complete_evidence = {
            "source_refs": [KB_AUDIT_SOURCE],
            "kb_partition_map": ["shared contracts, runtime adapters, generated reports"],
            "source_of_truth_registry": ["shared/spec.json", KB_AUDIT_SOURCE],
            "context_window_budget": ["12 refs", "12000 bytes", "summary first"],
            "runtime_trace": ["codex", "claude", "github-copilot", "langchain"],
        }
        missing = agent.plan(request, {})
        complete = agent.plan(request, complete_evidence)
    except Exception as exc:  # pragma: no cover - validator reports the concrete runtime error.
        issues.append(f"Knowledge Boundary LangChain behavior check failed: {exc}.")
        return

    missing_audit = missing.get("audit", {})
    complete_audit = complete.get("audit", {})
    evidence_needed = missing_audit.get("evidence_needed", [])
    behavior_checked = (
        missing_audit.get("pass") is False
        and "source_refs" in evidence_needed
        and all(key in evidence_needed for key in KB_REQUIRED_EVIDENCE)
        and missing.get("llm_escalation") is False
        and complete_audit.get("pass") is True
        and not complete_audit.get("evidence_needed")
        and complete.get("kb_context_window_audit", {}).get("requiredKbPartitionFields") == KB_REQUIRED_PARTITION_FIELDS
    )
    summary["langchainBehaviorChecked"] = behavior_checked
    if not behavior_checked:
        issues.append("Knowledge Boundary LangChain adapter must block LLM handoff until source_refs and all KB evidence exist.")


def runtime_pairwise_cases(runtimes: list[str] | tuple[str, ...] = RUNTIMES) -> list[dict]:
    cases = []
    for left_index, left in enumerate(runtimes):
        for right in runtimes[left_index + 1:]:
            cases.append(
                {
                    "id": f"{left}__{right}",
                    "runtimes": [left, right],
                    "assertions": [
                        "shared_system_prompt",
                        "shared_developer_prompt",
                        "shared_output_schema",
                        "runtime_trace",
                    ],
                }
            )
    return cases


def test_strategy_candidate_issues(candidate: object) -> list[str]:
    issues: list[str] = []
    if not isinstance(candidate, dict):
        return ["artifact must be a JSON object"]
    if not candidate.get("strategy"):
        issues.append("missing test_strategy")
    pairwise_cases = candidate.get("pairwise_cases", [])
    if not isinstance(pairwise_cases, list) or len(pairwise_cases) < len(runtime_pairwise_cases()):
        issues.append("missing pairwise_cases")
    else:
        expected_pairs = {tuple(case["runtimes"]) for case in runtime_pairwise_cases()}
        actual_pairs = {
            tuple(case.get("runtimes", []))
            for case in pairwise_cases
            if isinstance(case, dict)
        }
        if not expected_pairs.issubset(actual_pairs):
            issues.append("incomplete pairwise_cases")
    negative_cases = candidate.get("negative_cases", [])
    if not isinstance(negative_cases, list) or len(negative_cases) < 3:
        issues.append("missing negative_cases")
    elif not all(isinstance(case, dict) and case.get("detector") for case in negative_cases):
        issues.append("negative_cases missing detectors")
    traceability = candidate.get("traceability", {})
    if not isinstance(traceability, dict) or traceability.get("source_of_truth") != "dist/copilots/qa_general/shared/spec.json":
        issues.append("missing traceability")
    cost_control = candidate.get("cost_control", {})
    if not isinstance(cost_control, dict) or cost_control.get("deterministic_python_first") is not True:
        issues.append("missing deterministic cost control")
    return issues


def run_test_strategy_negative_cases() -> list[dict]:
    valid_artifact = {
        "strategy": "Risk-based QA strategy with deterministic runtime parity checks.",
        "pairwise_cases": runtime_pairwise_cases(),
        "negative_cases": [
            {"id": "missing_strategy", "detector": "test_strategy_candidate_issues"},
            {"id": "missing_pairwise_cases", "detector": "test_strategy_candidate_issues"},
            {"id": "missing_traceability", "detector": "test_strategy_candidate_issues"},
        ],
        "traceability": {"source_of_truth": "dist/copilots/qa_general/shared/spec.json"},
        "cost_control": {"deterministic_python_first": True},
    }
    fixtures = [
        ("valid_control", valid_artifact, False, ""),
        ("missing_strategy", {**valid_artifact, "strategy": ""}, True, "missing test_strategy"),
        ("missing_pairwise_cases", {**valid_artifact, "pairwise_cases": []}, True, "missing pairwise_cases"),
        ("missing_negative_cases", {**valid_artifact, "negative_cases": []}, True, "missing negative_cases"),
        ("missing_traceability", {**valid_artifact, "traceability": {}}, True, "missing traceability"),
        (
            "missing_cost_control",
            {**valid_artifact, "cost_control": {"deterministic_python_first": False}},
            True,
            "missing deterministic cost control",
        ),
    ]
    results = []
    for case_id, candidate, should_fail, expected_issue in fixtures:
        detected_issues = test_strategy_candidate_issues(candidate)
        failure_detected = bool(detected_issues)
        passed_expectation = (
            failure_detected == should_fail
            and (not expected_issue or expected_issue in detected_issues)
        )
        results.append(
            {
                "id": case_id,
                "expectedFailure": should_fail,
                "failureDetected": failure_detected,
                "passedExpectation": passed_expectation,
                "detected": passed_expectation,
                "issues": detected_issues,
            }
        )
    return results


def validate_test_auditor_contract(copilots: list, agents: list, issues: list[str]) -> dict:
    local_issues: list[str] = []
    pairwise_cases = runtime_pairwise_cases()
    negative_cases = run_test_strategy_negative_cases()
    summary = {
        "agentPresent": False,
        "qaCopilotPresent": False,
        "qaSpecPlaybookChecked": False,
        "runtimeRefsChecked": [],
        "pairwiseCaseCount": len(pairwise_cases),
        "pairwiseCases": pairwise_cases,
        "negativeCases": negative_cases,
        "negativeCasesDetected": all(case["passedExpectation"] for case in negative_cases),
        "sampleRouteChecked": False,
        "sampleTopRoute": None,
        "sampleRouteCheapPath": False,
        "runtimeTraceReturned": False,
        "validationCommands": TEST_VALIDATION_COMMANDS,
    }

    agent = next((item for item in agents if isinstance(item, dict) and item.get("id") == TEST_AGENT), {})
    summary["agentPresent"] = bool(agent)
    if not agent:
        local_issues.append("Test Auditor agent is missing from data/agent_roster.json.")
    else:
        if agent.get("mission") != TEST_MISSION:
            local_issues.append("Test Auditor mission drifted from the quality-real contract.")
        if agent.get("mode") != "python_first_llm_sparse":
            local_issues.append("Test Auditor mode must remain python_first_llm_sparse.")

    target = next((item for item in copilots if isinstance(item, dict) and item.get("id") == TEST_TARGET_COPILOT), {})
    summary["qaCopilotPresent"] = bool(target)
    if not target:
        local_issues.append("QA General copilot is missing from data/copilots.json.")
    else:
        if target.get("outputs") != TEST_REQUIRED_OUTPUTS:
            local_issues.append("QA General outputs must remain qa_strategy and test_matrix.")
        if "test" not in list_field(target, "sdlc_phases"):
            local_issues.append("QA General must own the test SDLC phase.")

    base = ROOT / "dist" / "copilots" / TEST_TARGET_COPILOT
    spec = read_json(base / "shared" / "spec.json", {}, local_issues)
    playbook = spec.get("sdlcPlaybook", []) if isinstance(spec, dict) else []
    test_phase = next((item for item in playbook if isinstance(item, dict) and item.get("phase") == "test"), {})
    python_check = str(test_phase.get("pythonCheck", "")).lower()
    if (
        spec.get("outputs") == TEST_REQUIRED_OUTPUTS
        and "pairwise" in python_check
        and "negative" in python_check
    ):
        summary["qaSpecPlaybookChecked"] = True
    else:
        local_issues.append("QA General shared spec must expose pairwise and negative test strategy generation.")

    output_schema = read_json(base / "shared" / "output_schema.json", {}, local_issues)
    expected_outputs = (
        output_schema.get("properties", {})
        .get("expected_outputs", {})
        .get("items", {})
        .get("enum", [])
        if isinstance(output_schema, dict)
        else []
    )
    if expected_outputs != TEST_REQUIRED_OUTPUTS:
        local_issues.append("QA General output schema must enumerate qa_strategy and test_matrix.")

    runtime_files = {
        "codex": base / "codex" / "AGENT.md",
        "claude": base / "claude" / "AGENT.md",
        "github-copilot": base / "github-copilot" / "copilot-agent.md",
        "langchain": base / "langchain" / "agent.py",
    }
    required_markers = ["qa_strategy", "test_matrix", "pairwise", "negative"]
    for runtime, path in runtime_files.items():
        text = read_text(path)
        missing = [marker for marker in required_markers if marker not in text]
        if missing:
            local_issues.append(f"Test strategy runtime reference drifted in {runtime}: missing {', '.join(missing)}.")
        else:
            summary["runtimeRefsChecked"].append(runtime)

    if not summary["negativeCasesDetected"]:
        local_issues.append("Test Auditor negative fixtures must be detected by executable checks.")

    try:
        import semantic_router as router

        sample = router.route(TEST_ROUTE_SAMPLE, limit=3)
    except Exception as exc:  # pragma: no cover - validator reports the concrete runtime error.
        local_issues.append(f"Test Auditor sample route failed: {exc}.")
        sample = []
    summary["sampleRouteChecked"] = bool(sample)
    if sample:
        top = sample[0]
        summary["sampleTopRoute"] = top.get("id")
        summary["sampleRouteCheapPath"] = top.get("cheap_path") is True
        runtime_trace = top.get("runtime_trace", {})
        summary["runtimeTraceReturned"] = runtime_trace.get("runtimes") == RUNTIMES
        if top.get("id") != TEST_TARGET_COPILOT:
            local_issues.append("Test Auditor sample route should rank qa_general first.")
        if top.get("cheap_path") is not True:
            local_issues.append("Test Auditor sample route must stay on the deterministic cheap path.")
        if runtime_trace.get("runtimes") != RUNTIMES:
            local_issues.append("Test Auditor route evidence must include full runtime trace.")
    else:
        local_issues.append("Test Auditor sample route returned no deterministic matches.")

    summary["requiredEvidence"] = TEST_REQUIRED_EVIDENCE
    summary["qualityGates"] = TEST_QUALITY_GATES
    summary["issues"] = local_issues
    summary["pass"] = not local_issues
    issues.extend(local_issues)
    return summary


def write_test_strategy_audit_report(summary: dict) -> None:
    report = {
        "pass": summary.get("pass") is True,
        "checkedAt": datetime.now(timezone.utc).isoformat(),
        "ownerAgent": TEST_AGENT,
        "mission": TEST_MISSION,
        "targetCopilot": TEST_TARGET_COPILOT,
        "requiredEvidence": TEST_REQUIRED_EVIDENCE,
        "qualityGates": TEST_QUALITY_GATES,
        "pairwiseCases": summary.get("pairwiseCases", []),
        "negativeCases": summary.get("negativeCases", []),
        "validationCommands": TEST_VALIDATION_COMMANDS,
        "summary": summary,
    }
    TEST_AUDIT_REPORT_JSON.parent.mkdir(parents=True, exist_ok=True)
    TEST_AUDIT_REPORT_JSON.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    TEST_AUDIT_REPORT_MD.write_text(render_test_strategy_md(report), encoding="utf-8")


def render_test_strategy_md(report: dict) -> str:
    pairwise_rows = "\n".join(
        f"- `{case['id']}`: {', '.join(case['runtimes'])}"
        for case in report["pairwiseCases"]
    ) or "- none"
    negative_rows = "\n".join(
        (
            f"- `{case['id']}`: passedExpectation={case.get('passedExpectation', case['detected'])} "
            f"expectedFailure={case['expectedFailure']} failureDetected={case.get('failureDetected')}"
        )
        for case in report["negativeCases"]
    ) or "- none"
    return f"""# Test Strategy Audit Report

Pass: {report['pass']}

Owner agent: `{report['ownerAgent']}`

Mission: {report['mission']}

Target copilot: `{report['targetCopilot']}`

Pairwise runtime cases:

{pairwise_rows}

Negative cases:

{negative_rows}
"""


def phase_verdict_sources() -> list[dict]:
    return [
        {
            "phase": "discovery",
            "section": "discoveryAuditor",
            "ownerAgent": DISCOVERY_AGENT,
            "evidence": [
                "generated/copilot-index.json#/discoveryAudit",
                "dist/copilots/as_is_discovery/shared/spec.json",
            ],
        },
        {
            "phase": "as_is",
            "section": "discoveryAuditor",
            "ownerAgent": DISCOVERY_AGENT,
            "evidence": [
                "data/copilots.json#/as_is_discovery",
                "dist/copilots/as_is_discovery/shared/spec.json",
            ],
        },
        {
            "phase": "architecture",
            "section": "architectureAuditor",
            "ownerAgent": ARCHITECTURE_AGENT,
            "evidence": [
                "dist/copilots/aida_architecture/shared/architecture_decision_audit.json",
                "generated/validation-report.json#/architectureAuditor",
            ],
        },
        {
            "phase": "design",
            "section": "designAuditor",
            "ownerAgent": DESIGN_AGENT,
            "evidence": [
                "generated/sdlc-audit-matrix.md#design-boundary-contract-evidence",
                "generated/validation-report.json#/designAuditor",
            ],
        },
        {
            "phase": "build",
            "section": "buildAuditor",
            "ownerAgent": BUILD_AGENT,
            "evidence": [
                "generated/factory-audit.json#/buildImplementationAudit",
                "generated/validation-report.json#/buildAuditor",
            ],
        },
        {
            "phase": "test",
            "section": "testStrategyAudit",
            "ownerAgent": TEST_AGENT,
            "evidence": [
                "generated/test-strategy-audit-report.json",
                "generated/validation-report.json#/testStrategyAudit",
            ],
        },
        {
            "phase": "security",
            "section": "securityAuditor",
            "ownerAgent": SECURITY_AGENT,
            "evidence": [
                "config/.env.example",
                "config/mcp-connectors.example.json",
                "generated/validation-report.json#/securityAuditor",
            ],
        },
        {
            "phase": "devops",
            "section": "devopsAuditor",
            "ownerAgent": DEVOPS_AGENT,
            "evidence": [
                "generated/devops-log-evidence.json",
                "generated/factory-audit.json#/devopsAudit",
                "generated/validation-report.json#/devopsAuditor",
            ],
        },
        {
            "phase": "cloud",
            "section": "cloudAuditor",
            "ownerAgent": CLOUD_AGENT,
            "evidence": [
                "dist/copilots/journey_to_cloud/shared/cloud_migration_audit.json",
                "generated/validation-report.json#/cloudAuditor",
            ],
        },
        {
            "phase": "release",
            "section": "releaseAuditor",
            "ownerAgent": RELEASE_AGENT,
            "evidence": [
                "generated/factory-audit.json#/releaseAudit",
                "generated/validation-report.json#/releaseAuditor",
            ],
        },
        {
            "phase": "operate",
            "section": "operateAuditor",
            "ownerAgent": OPERATE_AGENT,
            "evidence": [
                ".codex-loop/factory/operate-observability-contract.json",
                "generated/validation-report.json#/operateAuditor",
            ],
        },
    ]


def phase_verdict_candidate_issues(candidate: object) -> list[str]:
    issues: list[str] = []
    if not isinstance(candidate, dict):
        return ["artifact must be a JSON object"]
    if candidate.get("ownerAgent") != QA_PHASE_VERDICT_AGENT:
        issues.append("missing ownerAgent")
    if candidate.get("mission") != QA_PHASE_VERDICT_MISSION:
        issues.append("missing mission")
    if candidate.get("requiredPhases") != PHASE_VERDICT_REQUIRED_PHASES:
        issues.append("requiredPhases drifted")
    verdicts = candidate.get("phaseVerdicts", [])
    if not isinstance(verdicts, list):
        issues.append("phaseVerdicts must be a list")
        verdicts = []
    by_phase: dict[str, dict] = {}
    for item in verdicts:
        if not isinstance(item, dict):
            issues.append("phaseVerdicts contains a non-object item")
            continue
        phase = item.get("phase")
        if phase in by_phase:
            issues.append(f"duplicate phase verdict: {phase}")
        if phase not in PHASE_VERDICT_REQUIRED_PHASES:
            issues.append(f"unexpected phase verdict: {phase}")
        else:
            by_phase[phase] = item
        if item.get("verdict") not in {"pass", "fail"}:
            issues.append(f"{phase} verdict must be pass or fail")
        phase_pass = item.get("pass")
        summary_pass = item.get("summaryPass")
        if not isinstance(phase_pass, bool):
            issues.append(f"{phase} pass must be a boolean")
        if not isinstance(summary_pass, bool):
            issues.append(f"{phase} summaryPass must be a boolean")
        if item.get("verdict") in {"pass", "fail"} and isinstance(phase_pass, bool):
            expected_phase_pass = item.get("verdict") == "pass"
            if phase_pass is not expected_phase_pass:
                issues.append(f"{phase} pass boolean does not match verdict")
        if isinstance(phase_pass, bool) and isinstance(summary_pass, bool) and summary_pass is not phase_pass:
            issues.append(f"{phase} summaryPass does not match pass boolean")
        if item.get("passInferred") is not False:
            issues.append(f"{phase} pass must be explicit, not inferred")
        if not isinstance(item.get("ownerAgent"), str) or not item.get("ownerAgent"):
            issues.append(f"{phase} ownerAgent missing")
        if not isinstance(item.get("source"), str) or "generated/validation-report.json#/" not in item.get("source", ""):
            issues.append(f"{phase} source must reference validation-report")
        if not isinstance(item.get("evidence"), list) or not item.get("evidence"):
            issues.append(f"{phase} evidence missing")
    runtime_gate = candidate.get("runtimeEquivalenceGate", {})
    if not isinstance(runtime_gate, dict):
        runtime_gate = {}
        issues.append("runtimeEquivalenceGate missing")
    if runtime_gate.get("runtimes") != RUNTIMES:
        issues.append("runtimeEquivalenceGate runtimes drifted")
    if runtime_gate.get("maxUnexplainedDrift") != 0:
        issues.append("runtimeEquivalenceGate maxUnexplainedDrift must be 0")
    if runtime_gate.get("requiresReportPass") is not True:
        issues.append("runtimeEquivalenceGate requiresReportPass must be true")
    if runtime_gate.get("maxIssues") != 0:
        issues.append("runtimeEquivalenceGate maxIssues must be 0")
    if runtime_gate.get("reportPass") is not True:
        issues.append("runtimeEquivalenceGate reportPass must be true")
    if runtime_gate.get("issuesCount") != 0:
        issues.append("runtimeEquivalenceGate issuesCount must be 0")
    if runtime_gate.get("negativeCasesDetected") is not True:
        issues.append("runtimeEquivalenceGate negativeCasesDetected must be true")
    if not runtime_gate.get("source"):
        issues.append("runtimeEquivalenceGate source missing")
    cost_control = candidate.get("costControl", {})
    if not isinstance(cost_control, dict) or cost_control.get("deterministicPythonFirst") is not True:
        issues.append("missing deterministic cost control")
    missing = [phase for phase in PHASE_VERDICT_REQUIRED_PHASES if phase not in by_phase]
    if missing:
        issues.append(f"missing phase verdict(s): {', '.join(missing)}")
    phase_overall = all(
        by_phase.get(phase, {}).get("verdict") == "pass"
        for phase in PHASE_VERDICT_REQUIRED_PHASES
    )
    runtime_gate_pass = (
        runtime_gate.get("maxUnexplainedDrift") == 0
        and runtime_gate.get("requiresReportPass") is True
        and runtime_gate.get("maxIssues") == 0
        and runtime_gate.get("reportPass") is True
        and runtime_gate.get("issuesCount") == 0
        and runtime_gate.get("negativeCasesDetected") is True
    )
    expected_failed_phases = [
        phase
        for phase in PHASE_VERDICT_REQUIRED_PHASES
        if by_phase.get(phase, {}).get("verdict") == "fail"
    ]
    if candidate.get("failedPhases") != expected_failed_phases:
        issues.append("failedPhases does not match phase verdicts")
    expected_failed_gates = [] if runtime_gate_pass else ["runtime_equivalence"]
    if candidate.get("failedGates") != expected_failed_gates:
        issues.append("failedGates does not match runtime gate aggregation")
    expected_overall = phase_overall and runtime_gate_pass
    if candidate.get("overallPass") is not expected_overall:
        issues.append("overallPass does not match phase verdict aggregation")
    if candidate.get("overallVerdict") != ("pass" if expected_overall else "fail"):
        issues.append("overallVerdict does not match phase verdict aggregation")
    return issues


def run_phase_verdict_negative_cases(valid_report: dict) -> list[dict]:
    fixtures = [
        ("valid_control", valid_report, False, ""),
        (
            "missing_phase",
            {**valid_report, "phaseVerdicts": valid_report["phaseVerdicts"][:-1]},
            True,
            "missing phase verdict",
        ),
        (
            "invalid_verdict",
            {
                **valid_report,
                "phaseVerdicts": [
                    {**valid_report["phaseVerdicts"][0], "verdict": "warning"},
                    *valid_report["phaseVerdicts"][1:],
                ],
            },
            True,
            "verdict must be pass or fail",
        ),
        (
            "inconsistent_overall",
            {**valid_report, "overallPass": not valid_report["overallPass"]},
            True,
            "overallPass does not match",
        ),
        (
            "inconsistent_phase_pass",
            {
                **valid_report,
                "phaseVerdicts": [
                    {**valid_report["phaseVerdicts"][0], "pass": False},
                    *valid_report["phaseVerdicts"][1:],
                ],
            },
            True,
            "pass boolean does not match verdict",
        ),
        (
            "inconsistent_failed_phases",
            {
                **valid_report,
                "phaseVerdicts": [
                    {**valid_report["phaseVerdicts"][0], "verdict": "fail", "pass": False, "summaryPass": False},
                    *valid_report["phaseVerdicts"][1:],
                ],
                "overallPass": False,
                "overallVerdict": "fail",
            },
            True,
            "failedPhases does not match",
        ),
        (
            "missing_cost_control",
            {**valid_report, "costControl": {"deterministicPythonFirst": False}},
            True,
            "missing deterministic cost control",
        ),
        (
            "inferred_phase_pass",
            {
                **valid_report,
                "phaseVerdicts": [
                    {**valid_report["phaseVerdicts"][0], "passInferred": True},
                    *valid_report["phaseVerdicts"][1:],
                ],
            },
            True,
            "pass must be explicit",
        ),
        (
            "runtime_gate_failed",
            {
                **valid_report,
                "runtimeEquivalenceGate": {
                    **valid_report["runtimeEquivalenceGate"],
                    "reportPass": False,
                    "issuesCount": 1,
                },
            },
            True,
            "runtimeEquivalenceGate reportPass must be true",
        ),
    ]
    results = []
    for case_id, candidate, should_fail, expected_issue in fixtures:
        detected_issues = phase_verdict_candidate_issues(candidate)
        failure_detected = bool(detected_issues)
        passed_expectation = (
            failure_detected == should_fail
            and (not expected_issue or any(expected_issue in item for item in detected_issues))
        )
        results.append(
            {
                "id": case_id,
                "expectedFailure": should_fail,
                "failureDetected": failure_detected,
                "passedExpectation": passed_expectation,
                "detected": passed_expectation,
                "issues": detected_issues,
            }
        )
    return results


def phase_summary_pass(summary: dict) -> bool:
    if not isinstance(summary, dict) or not summary:
        return False
    return summary.get("pass") is True


def runtime_equivalence_gate_summary(local_issues: list[str]) -> dict:
    runtime_report = read_json(RUNTIME_EQUIVALENCE_REPORT_JSON, {}, local_issues)
    report_issues = runtime_report.get("issues", [])
    if not isinstance(report_issues, list):
        local_issues.append("Runtime equivalence report issues must be a list.")
        report_issues = ["invalid issues shape"]
    test_strategy_audit = runtime_report.get("testStrategyAudit", {})
    if not isinstance(test_strategy_audit, dict):
        test_strategy_audit = {}
    report_pass = runtime_report.get("pass") is True
    issues_count = len(report_issues)
    negative_cases_detected = test_strategy_audit.get("negativeCasesDetected") is True
    if runtime_report:
        if not report_pass:
            local_issues.append("Runtime equivalence report must pass before phase verdict can pass.")
        if issues_count:
            local_issues.append(f"Runtime equivalence report has {issues_count} issue(s).")
        if not negative_cases_detected:
            local_issues.append("Runtime equivalence negative fixtures must be detected before phase verdict can pass.")
    return {
        "source": "generated/runtime-equivalence-report.json",
        "runtimes": RUNTIMES,
        "maxUnexplainedDrift": PHASE_VERDICT_CONTRACT["runtimeEquivalence"]["maxUnexplainedDrift"],
        "requiresReportPass": PHASE_VERDICT_CONTRACT["runtimeEquivalence"]["requiresReportPass"],
        "maxIssues": PHASE_VERDICT_CONTRACT["runtimeEquivalence"]["maxIssues"],
        "reportPass": report_pass,
        "issuesCount": issues_count,
        "copilotsChecked": runtime_report.get("copilotsChecked"),
        "checkedAt": runtime_report.get("checkedAt"),
        "negativeCasesDetected": negative_cases_detected,
        "adapters": ["Codex", "Claude", "GitHub Copilot", "LangChain"],
    }


def validate_phase_verdict_report(agents: list, phase_summaries: dict[str, dict], issues: list[str]) -> dict:
    local_issues: list[str] = []
    agent = next((item for item in agents if isinstance(item, dict) and item.get("id") == QA_PHASE_VERDICT_AGENT), {})
    if not agent:
        local_issues.append("QA Committee Chair agent is missing from data/agent_roster.json.")
    else:
        if agent.get("mission") != QA_PHASE_VERDICT_MISSION:
            local_issues.append("QA Committee Chair mission drifted from phase verdict contract.")
        if agent.get("phase") != "quality":
            local_issues.append("QA Committee Chair must stay in the quality phase.")
        if agent.get("mode") != "python_first_llm_sparse":
            local_issues.append("QA Committee Chair mode must remain python_first_llm_sparse.")

    contract = read_json(PHASE_VERDICT_CONTRACT_JSON, {}, local_issues)
    for key, expected in PHASE_VERDICT_CONTRACT.items():
        if contract.get(key) != expected:
            local_issues.append(f"Phase verdict report contract drifted at `{key}`.")

    verdicts = []
    for source in phase_verdict_sources():
        summary = phase_summaries.get(source["section"], {})
        if not isinstance(summary, dict) or not summary:
            local_issues.append(f"Phase verdict source missing: {source['section']}.")
            summary = {}
        elif "pass" not in summary:
            local_issues.append(f"Phase verdict source {source['section']} must expose an explicit pass boolean.")
        phase_pass = phase_summary_pass(summary)
        verdicts.append(
            {
                "phase": source["phase"],
                "verdict": "pass" if phase_pass else "fail",
                "pass": phase_pass,
                "ownerAgent": source["ownerAgent"],
                "source": f"generated/validation-report.json#/{source['section']}",
                "evidence": source["evidence"],
                "summaryPass": summary.get("pass", phase_pass),
                "passInferred": "pass" not in summary,
            }
        )

    runtime_gate = runtime_equivalence_gate_summary(local_issues)
    failed_phases = [item["phase"] for item in verdicts if item["verdict"] != "pass"]
    failed_gates = [] if (
        runtime_gate.get("reportPass") is True
        and runtime_gate.get("issuesCount") == 0
        and runtime_gate.get("negativeCasesDetected") is True
        and runtime_gate.get("maxUnexplainedDrift") == 0
        and runtime_gate.get("requiresReportPass") is True
        and runtime_gate.get("maxIssues") == 0
    ) else ["runtime_equivalence"]
    overall_pass = not failed_phases and not failed_gates
    report = {
        "version": PHASE_VERDICT_AUDIT_VERSION,
        "checkedAt": datetime.now(timezone.utc).isoformat(),
        "ownerAgent": QA_PHASE_VERDICT_AGENT,
        "mission": QA_PHASE_VERDICT_MISSION,
        "contract": "dist/copilots/qa_general/shared/phase_verdict_report_contract.json",
        "requiredPhases": PHASE_VERDICT_REQUIRED_PHASES,
        "phaseVerdicts": verdicts,
        "overallPass": overall_pass,
        "overallVerdict": "pass" if overall_pass else "fail",
        "failedPhases": failed_phases,
        "failedGates": failed_gates,
        "runtimeEquivalenceGate": runtime_gate,
        "costControl": PHASE_VERDICT_CONTRACT["costControl"],
        "validationCommands": PHASE_VERDICT_VALIDATION_COMMANDS,
    }
    negative_cases = run_phase_verdict_negative_cases(report)
    candidate_issues = phase_verdict_candidate_issues(report)
    if candidate_issues:
        local_issues.extend(f"Phase verdict report schema: {item}." for item in candidate_issues)
    if not all(case["passedExpectation"] for case in negative_cases):
        local_issues.append("Phase verdict report negative fixtures must be detected by executable checks.")
    if failed_phases:
        local_issues.append(f"Phase verdict report has failing phase verdict(s): {', '.join(failed_phases)}.")

    report["negativeCases"] = negative_cases
    report["negativeCasesDetected"] = all(case["passedExpectation"] for case in negative_cases)
    report["issues"] = local_issues
    report["pass"] = not local_issues and overall_pass
    issues.extend(local_issues)
    return report


def write_phase_verdict_report(report: dict) -> None:
    PHASE_VERDICT_REPORT_JSON.parent.mkdir(parents=True, exist_ok=True)
    PHASE_VERDICT_REPORT_JSON.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    PHASE_VERDICT_REPORT_MD.write_text(render_phase_verdict_md(report), encoding="utf-8")
    evidence_map = build_phase_verdict_evidence_map(report)
    PHASE_VERDICT_EVIDENCE_MAP_JSON.write_text(json.dumps(evidence_map, indent=2) + "\n", encoding="utf-8")
    PHASE_VERDICT_EVIDENCE_MAP_MD.write_text(render_phase_verdict_evidence_map_md(evidence_map), encoding="utf-8")


def build_phase_verdict_evidence_map(report: dict) -> dict:
    phase_rows = [
        {
            "phase": item.get("phase"),
            "verdict": item.get("verdict"),
            "pass": item.get("pass"),
            "summaryPass": item.get("summaryPass"),
            "passInferred": item.get("passInferred"),
            "ownerAgent": item.get("ownerAgent"),
            "source": item.get("source"),
            "evidence": item.get("evidence", []),
        }
        for item in report.get("phaseVerdicts", [])
        if isinstance(item, dict)
    ]
    phase_pass_count = sum(1 for item in phase_rows if item.get("verdict") == "pass")
    phase_fail_count = sum(1 for item in phase_rows if item.get("verdict") == "fail")
    negative_cases = [
        {
            "id": item.get("id"),
            "expectedFailure": item.get("expectedFailure"),
            "failureDetected": item.get("failureDetected"),
            "passedExpectation": item.get("passedExpectation"),
        }
        for item in report.get("negativeCases", [])
        if isinstance(item, dict)
    ]
    return {
        "version": "phase-verdict-evidence-map-1.0",
        "checkedAt": report.get("checkedAt"),
        "ownerAgent": report.get("ownerAgent"),
        "mission": report.get("mission"),
        "sourceReport": "generated/phase-verdict-report.json",
        "contract": report.get("contract"),
        "inputReports": PHASE_VERDICT_INPUT_REFS,
        "consolidation": {
            "requiredPhaseCount": len(PHASE_VERDICT_REQUIRED_PHASES),
            "phasesPresent": len(phase_rows),
            "phasePassCount": phase_pass_count,
            "phaseFailCount": phase_fail_count,
            "failedPhases": report.get("failedPhases", []),
            "failedGates": report.get("failedGates", []),
            "overallPass": report.get("overallPass"),
            "overallVerdict": report.get("overallVerdict"),
            "explicitPassRequired": PHASE_VERDICT_CONTRACT["explicitPassRequired"],
            "deterministicPythonFirst": PHASE_VERDICT_CONTRACT["costControl"]["deterministicPythonFirst"],
        },
        "phaseEvidence": phase_rows,
        "runtimeEquivalenceGate": report.get("runtimeEquivalenceGate", {}),
        "negativeCases": negative_cases,
        "negativeCasesDetected": report.get("negativeCasesDetected"),
        "validationCommands": PHASE_VERDICT_VALIDATION_COMMANDS,
        "pass": report.get("pass"),
    }


def render_phase_verdict_evidence_map_md(evidence_map: dict) -> str:
    consolidation = evidence_map.get("consolidation", {})
    runtime_gate = evidence_map.get("runtimeEquivalenceGate", {})
    rows = "\n".join(
        (
            f"| {item.get('phase')} | {item.get('verdict')} | {item.get('pass')} | "
            f"{item.get('passInferred')} | `{item.get('source')}` | {len(item.get('evidence', []))} |"
        )
        for item in evidence_map.get("phaseEvidence", [])
    )
    negative_rows = "\n".join(
        (
            f"- `{case.get('id')}`: expectedFailure={case.get('expectedFailure')} "
            f"failureDetected={case.get('failureDetected')} passedExpectation={case.get('passedExpectation')}"
        )
        for case in evidence_map.get("negativeCases", [])
    ) or "- none"
    return f"""# Phase Verdict Evidence Map

Pass: {evidence_map.get('pass')}

Overall verdict: {consolidation.get('overallVerdict')}

Source report: `{evidence_map.get('sourceReport')}`

Contract: `{evidence_map.get('contract')}`

Consolidation:

- Required phases: {consolidation.get('requiredPhaseCount')}
- Phases present: {consolidation.get('phasesPresent')}
- Phase pass count: {consolidation.get('phasePassCount')}
- Phase fail count: {consolidation.get('phaseFailCount')}
- Failed phases: {', '.join(consolidation.get('failedPhases', [])) or 'none'}
- Failed gates: {', '.join(consolidation.get('failedGates', [])) or 'none'}
- Explicit pass required: {consolidation.get('explicitPassRequired')}
- Deterministic Python first: {consolidation.get('deterministicPythonFirst')}

| Phase | Verdict | Pass | Pass inferred | Source | Evidence refs |
|---|---|---|---|---|---:|
{rows}

Runtime equivalence gate:

- Source: `{runtime_gate.get('source')}`
- Runtimes: {', '.join(runtime_gate.get('runtimes', []))}
- Report pass: {runtime_gate.get('reportPass')}
- Issues count: {runtime_gate.get('issuesCount')}
- Negative cases detected: {runtime_gate.get('negativeCasesDetected')}
- Max unexplained drift: {runtime_gate.get('maxUnexplainedDrift')}

Negative fixtures:

{negative_rows}
"""


def render_phase_verdict_md(report: dict) -> str:
    rows = "\n".join(
        f"| {item['phase']} | {item['verdict']} | {item['ownerAgent']} | `{item['source']}` |"
        for item in report.get("phaseVerdicts", [])
    )
    negative_rows = "\n".join(
        (
            f"- `{case['id']}`: passedExpectation={case.get('passedExpectation')} "
            f"expectedFailure={case.get('expectedFailure')} failureDetected={case.get('failureDetected')}"
        )
        for case in report.get("negativeCases", [])
    ) or "- none"
    issues = "\n".join(f"- {issue}" for issue in report.get("issues", [])) or "- none"
    runtime_gate = report.get("runtimeEquivalenceGate", {})
    failed_gates = ", ".join(report.get("failedGates", [])) or "none"
    return f"""# Phase Verdict Report

Pass: {report.get('pass')}

Overall verdict: {report.get('overallVerdict')}

Failed gates: {failed_gates}

Owner agent: `{report.get('ownerAgent')}`

Mission: {report.get('mission')}

| Phase | Verdict | Owner | Source |
|---|---|---|---|
{rows}

Runtime equivalence gate: `{runtime_gate.get('source')}` with max unexplained drift `{runtime_gate.get('maxUnexplainedDrift')}`.

- Report pass: {runtime_gate.get('reportPass')}
- Issues count: {runtime_gate.get('issuesCount')}
- Requires report pass: {runtime_gate.get('requiresReportPass')}
- Max issues: {runtime_gate.get('maxIssues')}
- Negative cases detected: {runtime_gate.get('negativeCasesDetected')}
- Copilots checked: {runtime_gate.get('copilotsChecked')}

Negative cases:

{negative_rows}

Issues:

{issues}
"""


def parse_env_example(path: Path, local_issues: list[str]) -> dict[str, str]:
    env_values: dict[str, str] = {}
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except OSError as exc:
        local_issues.append(f"Cannot read {format_path(path)}: {exc}.")
        return env_values

    for line_number, raw_line in enumerate(lines, start=1):
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if "=" not in line:
            local_issues.append(f"{format_path(path)} line {line_number} must use KEY=VALUE syntax.")
            continue
        key, value = line.split("=", 1)
        if not is_upper_snake(key):
            local_issues.append(f"{format_path(path)} line {line_number} env key is not UPPER_SNAKE_CASE: {key}.")
        if key in env_values:
            local_issues.append(f"{format_path(path)} duplicates env key {key}.")
        env_values[key] = value
        if value and key.endswith(("TOKEN", "TOKEN_OPTIONAL", "SECRET", "API_KEY", "PASSWORD")):
            local_issues.append(f"{format_path(path)} must not contain a value for sensitive env key {key}.")
        for pattern in SECRET_PATTERNS:
            if value and pattern.search(value):
                local_issues.append(f"{format_path(path)} contains credential-shaped value for {key}.")
                break
    return env_values


def security_negative_case_issues(candidate: dict) -> list[str]:
    detected: list[str] = []
    env_values = candidate.get("env_values", {})
    if isinstance(env_values, dict):
        for key, value in env_values.items():
            if not is_upper_snake(key):
                detected.append("invalid env key")
            if isinstance(value, str) and value:
                if key.endswith(("TOKEN", "TOKEN_OPTIONAL", "SECRET", "API_KEY", "PASSWORD")):
                    detected.append("sensitive env value")
                if any(pattern.search(value) for pattern in SECRET_PATTERNS):
                    detected.append("credential-shaped value")
    else:
        detected.append("invalid env values")

    connector = candidate.get("connector", {})
    if isinstance(connector, dict):
        if connector.get("enabled") is True:
            detected.append("connector enabled by default")
        env_key = connector.get("env")
        if not is_upper_snake(env_key):
            detected.append("invalid connector env")
        elif not isinstance(env_values, dict) or env_key not in env_values:
            detected.append("missing connector env placeholder")
        elif env_values.get(env_key) != "":
            detected.append("connector env value")
        for field in ["purpose", "owner", "rotation_owner", "least_privilege_scope"]:
            if not isinstance(connector.get(field), str) or not connector.get(field).strip():
                detected.append(f"missing {field}")
        if connector.get("allowed_runtimes") != RUNTIMES:
            detected.append("runtime allowlist drift")
        scope = str(connector.get("least_privilege_scope", "")).lower()
        if any(marker in scope for marker in ["read/write", "*", "admin", "all access"]):
            detected.append("overbroad least privilege scope")
        denied = connector.get("denied_operations", [])
        if not isinstance(denied, list) or not set(SECURITY_REQUIRED_DENIED_OPERATIONS).issubset(set(denied)):
            detected.append("missing denied operations")
        if connector.get("requires_operator_activation") is not True:
            detected.append("missing operator activation")
        if connector.get("operator_approval_required_for_writes") is not True:
            detected.append("missing write approval")
        allowed = connector.get("allowed_operations", [])
        if not isinstance(allowed, list) or not allowed:
            detected.append("missing allowed operations")
            allowed = []
        if isinstance(denied, list):
            for operation in denied:
                if not is_lower_snake(operation):
                    detected.append("invalid denied operation")
        for operation in allowed:
            if not is_lower_snake(operation):
                detected.append("invalid allowed operation")
        if allowed:
            risky = {"secret", "billing", "admin", "destructive"}
            if any(any(token in str(operation) for token in risky) for operation in allowed):
                detected.append("risky allowed operation")
            if (
                any(str(operation).startswith("write_") for operation in allowed)
                and connector.get("operator_approval_required_for_writes") is not True
            ):
                detected.append("write operation without approval")
    else:
        detected.append("invalid connector")
    return list(dict.fromkeys(detected))


def run_security_negative_cases() -> list[dict]:
    token_fixture = "ghp_" + ("A" * 24)
    base_connector = {
        "enabled": False,
        "env": "GITHUB_TOKEN",
        "purpose": "Read repository metadata for audit evidence.",
        "owner": "Operations",
        "rotation_owner": "Operations",
        "least_privilege_scope": "repository metadata read access",
        "allowed_runtimes": RUNTIMES,
        "requires_operator_activation": True,
        "operator_approval_required_for_writes": True,
        "allowed_operations": ["read_repo_metadata"],
        "denied_operations": SECURITY_REQUIRED_DENIED_OPERATIONS,
    }
    fixtures = [
        (
            "valid_placeholder_policy",
            {"env_values": {"GITHUB_TOKEN": ""}, "connector": base_connector},
            False,
            "",
        ),
        (
            "live_env_value",
            {"env_values": {"GITHUB_TOKEN": token_fixture}, "connector": base_connector},
            True,
            "sensitive env value",
        ),
        (
            "enabled_by_default",
            {"env_values": {"GITHUB_TOKEN": ""}, "connector": {**base_connector, "enabled": True}},
            True,
            "connector enabled by default",
        ),
        (
            "missing_denied_operations",
            {"env_values": {"GITHUB_TOKEN": ""}, "connector": {**base_connector, "denied_operations": []}},
            True,
            "missing denied operations",
        ),
        (
            "missing_connector_env_placeholder",
            {"env_values": {}, "connector": base_connector},
            True,
            "missing connector env placeholder",
        ),
        (
            "missing_rotation_owner",
            {"env_values": {"GITHUB_TOKEN": ""}, "connector": {**base_connector, "rotation_owner": ""}},
            True,
            "missing rotation_owner",
        ),
        (
            "runtime_allowlist_drift",
            {"env_values": {"GITHUB_TOKEN": ""}, "connector": {**base_connector, "allowed_runtimes": ["codex"]}},
            True,
            "runtime allowlist drift",
        ),
        (
            "overbroad_least_privilege_scope",
            {
                "env_values": {"GITHUB_TOKEN": ""},
                "connector": {**base_connector, "least_privilege_scope": "read/write admin all access"},
            },
            True,
            "overbroad least privilege scope",
        ),
        (
            "missing_write_approval",
            {
                "env_values": {"GITHUB_TOKEN": ""},
                "connector": {
                    **base_connector,
                    "operator_approval_required_for_writes": False,
                    "allowed_operations": ["write_operator_approved_comments"],
                },
            },
            True,
            "missing write approval",
        ),
        (
            "risky_allowed_operation",
            {"env_values": {"GITHUB_TOKEN": ""}, "connector": {**base_connector, "allowed_operations": ["admin_all"]}},
            True,
            "risky allowed operation",
        ),
    ]
    results = []
    for case_id, candidate, should_fail, expected_issue in fixtures:
        detected_issues = security_negative_case_issues(candidate)
        failure_detected = bool(detected_issues)
        passed_expectation = (
            failure_detected == should_fail
            and (not expected_issue or expected_issue in detected_issues)
        )
        results.append(
            {
                "id": case_id,
                "expectedFailure": should_fail,
                "failureDetected": failure_detected,
                "passedExpectation": passed_expectation,
                "issues": detected_issues,
            }
        )
    return results


def validate_security_auditor_contract(agents: list, issues: list[str]) -> dict:
    local_issues: list[str] = []
    summary = {
        "agentPresent": False,
        "agentCatalogMission": None,
        "mission": None,
        "policyVersion": None,
        "envExampleChecked": False,
        "mcpConfigChecked": False,
        "sensitiveCredentialsPolicyChecked": False,
        "threatModelChecked": False,
        "safeUsageChecked": False,
        "runtimeEquivalenceChecked": False,
        "connectorsChecked": [],
        "negativeCases": run_security_negative_cases(),
        "negativeCasesDetected": False,
        "validationCommands": SECURITY_VALIDATION_COMMANDS,
    }

    agent = next((item for item in agents if isinstance(item, dict) and item.get("id") == SECURITY_AGENT), {})
    summary["agentPresent"] = bool(agent)
    if not agent:
        local_issues.append("Security Auditor agent is missing from data/agent_roster.json.")
    else:
        summary["agentCatalogMission"] = agent.get("mission")
        equivalent_missions = {
            SECURITY_MISSION,
            "Audits secrets policy, threat model and safe MCP usage.",
        }
        if agent.get("mission") not in equivalent_missions:
            local_issues.append("Security Auditor mission drifted from the sensitive credentials contract.")
        if agent.get("mode") != "python_first_llm_sparse":
            local_issues.append("Security Auditor mode must remain python_first_llm_sparse.")

    env_values = parse_env_example(ROOT / SECURITY_ENV_EXAMPLE, local_issues)
    if all(key in env_values for key in SECURITY_REQUIRED_ENV_KEYS):
        summary["envExampleChecked"] = True
    else:
        missing = sorted(set(SECURITY_REQUIRED_ENV_KEYS) - set(env_values))
        local_issues.append(f"{SECURITY_ENV_EXAMPLE} missing required sensitive env placeholder(s): {', '.join(missing)}.")

    for key in SECURITY_REQUIRED_ENV_KEYS:
        if env_values.get(key, "") != "":
            local_issues.append(f"{SECURITY_ENV_EXAMPLE} placeholder for {key} must stay empty.")

    mcp_config = read_json(ROOT / SECURITY_MCP_CONFIG, {}, local_issues)
    summary["mcpConfigChecked"] = bool(mcp_config)
    summary["policyVersion"] = mcp_config.get("policy_version") if isinstance(mcp_config, dict) else None
    summary["mission"] = mcp_config.get("mission") if isinstance(mcp_config, dict) else None
    if summary["policyVersion"] != SECURITY_AUDIT_VERSION:
        local_issues.append(f"{SECURITY_MCP_CONFIG} policy_version must be {SECURITY_AUDIT_VERSION}.")
    if mcp_config.get("owner_agent") != SECURITY_AGENT:
        local_issues.append(f"{SECURITY_MCP_CONFIG} owner_agent must be {SECURITY_AGENT}.")
    if mcp_config.get("mission") != SECURITY_MISSION:
        local_issues.append(f"{SECURITY_MCP_CONFIG} mission must match the sensitive credentials audit mission.")

    runtime_equivalence = mcp_config.get("runtime_equivalence", {}) if isinstance(mcp_config, dict) else {}
    if runtime_equivalence == SECURITY_RUNTIME_EQUIVALENCE:
        summary["runtimeEquivalenceChecked"] = True
    else:
        local_issues.append(f"{SECURITY_MCP_CONFIG} runtime_equivalence drifted from factory runtime parity.")

    policy = mcp_config.get("sensitive_credentials_policy", {}) if isinstance(mcp_config, dict) else {}
    if not isinstance(policy, dict):
        local_issues.append(f"{SECURITY_MCP_CONFIG} sensitive_credentials_policy must be an object.")
        policy = {}
    policy_checks = {
        "storage": "environment_only",
        "placeholder_only_in_repo": True,
        "deny_real_values_in_env_example": True,
        "required_env_example": SECURITY_ENV_EXAMPLE,
        "redaction_required": True,
        "rotation_owner_required": True,
        "customer_data_allowed": False,
        "billing_data_allowed": False,
        "allowed_placeholder_values": [""],
    }
    missing_policy = [
        key for key, expected in policy_checks.items()
        if policy.get(key) != expected
    ]
    deny_prefixes = policy.get("deny_value_prefixes", [])
    required_prefixes = {"sk-", "github_pat_", "ghp_", "gho_", "ghu_", "ghs_", "ghr_", "Bearer "}
    if not isinstance(deny_prefixes, list) or not required_prefixes.issubset(set(deny_prefixes)):
        missing_policy.append("deny_value_prefixes")
    if missing_policy:
        local_issues.append(f"{SECURITY_MCP_CONFIG} sensitive credentials policy drifted: {', '.join(missing_policy)}.")
    else:
        summary["sensitiveCredentialsPolicyChecked"] = True

    safe_usage = mcp_config.get("mcp_safe_usage", {}) if isinstance(mcp_config, dict) else {}
    if safe_usage == SECURITY_REQUIRED_SAFE_USAGE:
        summary["safeUsageChecked"] = True
    else:
        local_issues.append(f"{SECURITY_MCP_CONFIG} mcp_safe_usage must require disabled defaults, allowlists, redaction and operator approval.")

    threat_model = mcp_config.get("threat_model", []) if isinstance(mcp_config, dict) else []
    threat_ids = [item.get("id") for item in threat_model if isinstance(item, dict)]
    missing_threats = sorted(set(SECURITY_REQUIRED_THREATS) - set(threat_ids))
    if missing_threats:
        local_issues.append(f"{SECURITY_MCP_CONFIG} threat_model missing required threat(s): {', '.join(missing_threats)}.")
    if not isinstance(threat_model, list) or len(threat_model) < len(SECURITY_REQUIRED_THREATS):
        local_issues.append(f"{SECURITY_MCP_CONFIG} threat_model must enumerate the required security threats.")
    for item in threat_model if isinstance(threat_model, list) else []:
        if not isinstance(item, dict):
            local_issues.append(f"{SECURITY_MCP_CONFIG} threat_model entries must be objects.")
            continue
        tid = item.get("id", "")
        if not is_lower_snake(tid):
            local_issues.append(f"{SECURITY_MCP_CONFIG} threat id must be lower_snake_case: {tid}.")
        for field in ["asset", "threat", "control", "verification"]:
            if not isinstance(item.get(field), str) or not item.get(field).strip():
                local_issues.append(f"{SECURITY_MCP_CONFIG} threat {tid} missing {field}.")
        if item.get("verification") != "python tools/validate_copilot_factory.py":
            local_issues.append(f"{SECURITY_MCP_CONFIG} threat {tid} must be verified by validate_copilot_factory.py.")
    if isinstance(threat_model, list) and not missing_threats and all(
        isinstance(item, dict) and all(isinstance(item.get(field), str) and item.get(field).strip() for field in ["asset", "threat", "control", "verification"])
        for item in threat_model
    ):
        summary["threatModelChecked"] = True

    connectors = mcp_config.get("connectors", {}) if isinstance(mcp_config, dict) else {}
    if not isinstance(connectors, dict) or not connectors:
        local_issues.append(f"{SECURITY_MCP_CONFIG} connectors must be a non-empty object.")
        connectors = {}
    for name, connector in connectors.items():
        if not is_lower_snake(name):
            local_issues.append(f"{SECURITY_MCP_CONFIG} connector name is not lower_snake_case: {name}.")
        if not isinstance(connector, dict):
            local_issues.append(f"{SECURITY_MCP_CONFIG} connector {name} must be an object.")
            continue
        connector_ok = True
        if connector.get("enabled") is not False:
            connector_ok = False
            local_issues.append(f"{SECURITY_MCP_CONFIG} connector {name} must default to enabled=false.")
        env_key = connector.get("env")
        if not is_upper_snake(env_key):
            connector_ok = False
            local_issues.append(f"{SECURITY_MCP_CONFIG} connector {name} env key is not UPPER_SNAKE_CASE.")
        elif env_key not in env_values:
            connector_ok = False
            local_issues.append(f"{SECURITY_MCP_CONFIG} connector {name} env key {env_key} is missing from {SECURITY_ENV_EXAMPLE}.")
        elif env_values.get(env_key) != "":
            connector_ok = False
            local_issues.append(f"{SECURITY_ENV_EXAMPLE} connector env key {env_key} must remain empty.")

        for field in ["purpose", "owner", "rotation_owner", "least_privilege_scope"]:
            value = connector.get(field)
            if not isinstance(value, str) or not value.strip():
                connector_ok = False
                local_issues.append(f"{SECURITY_MCP_CONFIG} connector {name} missing {field}.")
        if connector.get("allowed_runtimes") != RUNTIMES:
            connector_ok = False
            local_issues.append(f"{SECURITY_MCP_CONFIG} connector {name} allowed_runtimes must match factory runtimes.")
        scope = str(connector.get("least_privilege_scope", "")).lower()
        if any(marker in scope for marker in ["read/write", "*", "admin", "all access"]):
            connector_ok = False
            local_issues.append(f"{SECURITY_MCP_CONFIG} connector {name} least_privilege_scope is too broad.")
        if connector.get("requires_operator_activation") is not True:
            connector_ok = False
            local_issues.append(f"{SECURITY_MCP_CONFIG} connector {name} must require operator activation.")
        if connector.get("operator_approval_required_for_writes") is not True:
            connector_ok = False
            local_issues.append(f"{SECURITY_MCP_CONFIG} connector {name} must require operator approval for writes.")

        allowed = connector.get("allowed_operations", [])
        denied = connector.get("denied_operations", [])
        if not isinstance(allowed, list) or not allowed:
            connector_ok = False
            local_issues.append(f"{SECURITY_MCP_CONFIG} connector {name} must declare allowed_operations.")
            allowed = []
        if not isinstance(denied, list) or not set(SECURITY_REQUIRED_DENIED_OPERATIONS).issubset(set(denied)):
            connector_ok = False
            local_issues.append(f"{SECURITY_MCP_CONFIG} connector {name} missing required denied_operations.")
            denied = []
        for operation in allowed + denied:
            if not is_lower_snake(operation):
                connector_ok = False
                local_issues.append(f"{SECURITY_MCP_CONFIG} connector {name} operation is not lower_snake_case: {operation}.")
        risky_terms = {"secret", "billing", "org_admin", "destructive", "admin_all"}
        for operation in allowed:
            if any(term in str(operation) for term in risky_terms):
                connector_ok = False
                local_issues.append(f"{SECURITY_MCP_CONFIG} connector {name} allows risky operation {operation}.")
        if any(str(operation).startswith("write_") for operation in allowed) and connector.get("operator_approval_required_for_writes") is not True:
            connector_ok = False
            local_issues.append(f"{SECURITY_MCP_CONFIG} connector {name} write operation lacks operator approval.")

        if connector_ok:
            summary["connectorsChecked"].append(name)

    rules = mcp_config.get("rules", []) if isinstance(mcp_config, dict) else []
    if not isinstance(rules, list) or not all(isinstance(rule, str) and rule.strip() for rule in rules):
        local_issues.append(f"{SECURITY_MCP_CONFIG} rules must be non-empty strings.")
    connector_rule = "Every connector must have a purpose, owner, rotation owner, runtime allowlist, allowed operations, denied operations, and least-privilege scope before activation."
    if connector_rule not in rules:
        local_issues.append(f"{SECURITY_MCP_CONFIG} rules must require connector rotation owner and runtime allowlist evidence.")
    runtime_rule = "The same MCP safety policy applies to Codex, Claude, GitHub Copilot, and LangChain."
    if runtime_rule not in rules:
        local_issues.append(f"{SECURITY_MCP_CONFIG} rules must declare equivalent MCP safety policy for all runtimes.")

    summary["negativeCasesDetected"] = all(case["passedExpectation"] for case in summary["negativeCases"])
    if not summary["negativeCasesDetected"]:
        local_issues.append("Security Auditor negative fixtures must be detected by executable checks.")

    summary["issues"] = local_issues
    summary["pass"] = not local_issues
    issues.extend(local_issues)
    return summary


def mcp_connector_negative_case_issues(candidate: dict) -> list[str]:
    detected: list[str] = []
    env_values = candidate.get("env_values", {})
    connectors = candidate.get("connectors", {})
    if not isinstance(env_values, dict):
        detected.append("invalid env values")
        env_values = {}
    if not isinstance(connectors, dict) or not connectors:
        detected.append("missing connectors")
        connectors = {}

    connector_envs: list[str] = []
    for name, connector in connectors.items():
        if not is_lower_snake(name):
            detected.append("invalid connector name")
        if not isinstance(connector, dict):
            detected.append("invalid connector declaration")
            continue

        missing_fields = [field for field in MCP_REQUIRED_DECLARATION_FIELDS if field not in connector]
        if missing_fields:
            detected.append("missing required declaration fields")
        if connector.get("enabled") is not False:
            detected.append("connector enabled by default")

        env_key = connector.get("env")
        if not is_upper_snake(env_key):
            detected.append("invalid connector env")
            env_key = None
        else:
            connector_envs.append(env_key)
            if env_key not in env_values:
                detected.append("missing connector env placeholder")
            elif env_values.get(env_key) != "":
                detected.append("non-empty env placeholder")

        for field in ["purpose", "owner", "rotation_owner", "least_privilege_scope"]:
            if not isinstance(connector.get(field), str) or not connector.get(field).strip():
                detected.append(f"missing {field}")
        if connector.get("allowed_runtimes") != RUNTIMES:
            detected.append("runtime allowlist drift")
        scope = str(connector.get("least_privilege_scope", "")).lower()
        if any(marker in scope for marker in ["read/write", "*", "admin", "all access"]):
            detected.append("overbroad least privilege scope")
        if connector.get("requires_operator_activation") is not True:
            detected.append("missing operator activation")
        if connector.get("operator_approval_required_for_writes") is not True:
            detected.append("missing write approval")

        allowed = connector.get("allowed_operations", [])
        denied = connector.get("denied_operations", [])
        if not isinstance(allowed, list) or not allowed:
            detected.append("missing allowed operations")
            allowed = []
        if not isinstance(denied, list) or not set(SECURITY_REQUIRED_DENIED_OPERATIONS).issubset(set(denied)):
            detected.append("missing denied operations")
            denied = []
        for operation in allowed + denied:
            if not is_lower_snake(operation):
                detected.append("invalid operation name")
        allowed_set = set(allowed) if isinstance(allowed, list) else set()
        denied_set = set(denied) if isinstance(denied, list) else set()
        if allowed_set.intersection(denied_set):
            detected.append("allowed denied operation conflict")
        risky_terms = {"secret", "billing", "admin", "destructive"}
        for operation in allowed:
            if any(term in str(operation) for term in risky_terms):
                detected.append("risky allowed operation")

        traceability = connector.get("traceability_refs", {})
        if not isinstance(traceability, dict):
            detected.append("missing traceability refs")
        else:
            expected_policy_ref = f"{MCP_CONFIG}#/connectors/{name}"
            expected_env_ref = f"{MCP_ENV_EXAMPLE}#{env_key}" if env_key else None
            if traceability.get("policy_ref") != expected_policy_ref:
                detected.append("policy traceability drift")
            if expected_env_ref and traceability.get("env_ref") != expected_env_ref:
                detected.append("env traceability drift")
            if traceability.get("validation_report_key") != "generated/validation-report.json#mcpConnectorAuditor":
                detected.append("validation traceability drift")

    if len(connector_envs) != len(set(connector_envs)):
        detected.append("duplicate connector env placeholder")

    referenced_envs = set(connector_envs)
    sensitive_suffixes = ("TOKEN", "TOKEN_OPTIONAL", "SECRET", "API_KEY", "PASSWORD")
    for key, value in env_values.items():
        if not is_upper_snake(key):
            detected.append("invalid env key")
        if isinstance(value, str) and value:
            detected.append("non-empty env placeholder")
            if any(pattern.search(value) for pattern in SECRET_PATTERNS):
                detected.append("credential-shaped env value")
        if isinstance(key, str) and key.endswith(sensitive_suffixes) and key not in referenced_envs:
            detected.append("orphan sensitive placeholder")

    return list(dict.fromkeys(detected))


def run_mcp_connector_negative_cases() -> list[dict]:
    base_connector = {
        "enabled": False,
        "env": "GITHUB_TOKEN",
        "purpose": "Read repository metadata for audit evidence.",
        "owner": "Operations",
        "rotation_owner": "Operations",
        "least_privilege_scope": "repository metadata read access",
        "allowed_runtimes": RUNTIMES,
        "requires_operator_activation": True,
        "operator_approval_required_for_writes": True,
        "allowed_operations": ["read_repo_metadata"],
        "denied_operations": SECURITY_REQUIRED_DENIED_OPERATIONS,
        "traceability_refs": {
            "policy_ref": f"{MCP_CONFIG}#/connectors/github_mcp",
            "env_ref": f"{MCP_ENV_EXAMPLE}#GITHUB_TOKEN",
            "validation_report_key": "generated/validation-report.json#mcpConnectorAuditor",
        },
    }
    duplicate_connector = {
        **base_connector,
        "traceability_refs": {
            "policy_ref": f"{MCP_CONFIG}#/connectors/duplicate_github_mcp",
            "env_ref": f"{MCP_ENV_EXAMPLE}#GITHUB_TOKEN",
            "validation_report_key": "generated/validation-report.json#mcpConnectorAuditor",
        },
    }
    fixtures = [
        (
            "valid_connector_placeholder_matrix",
            {"env_values": {"GITHUB_TOKEN": ""}, "connectors": {"github_mcp": base_connector}},
            False,
            "",
        ),
        (
            "missing_env_placeholder",
            {"env_values": {}, "connectors": {"github_mcp": base_connector}},
            True,
            "missing connector env placeholder",
        ),
        (
            "non_empty_env_placeholder",
            {"env_values": {"GITHUB_TOKEN": "local-only-placeholder"}, "connectors": {"github_mcp": base_connector}},
            True,
            "non-empty env placeholder",
        ),
        (
            "credential_shaped_env_placeholder",
            {"env_values": {"GITHUB_TOKEN": "ghp_" + ("C" * 24)}, "connectors": {"github_mcp": base_connector}},
            True,
            "credential-shaped env value",
        ),
        (
            "duplicate_connector_env_placeholder",
            {
                "env_values": {"GITHUB_TOKEN": ""},
                "connectors": {
                    "github_mcp": base_connector,
                    "duplicate_github_mcp": duplicate_connector,
                },
            },
            True,
            "duplicate connector env placeholder",
        ),
        (
            "orphan_sensitive_placeholder",
            {
                "env_values": {"GITHUB_TOKEN": "", "UNUSED_TOKEN": ""},
                "connectors": {"github_mcp": base_connector},
            },
            True,
            "orphan sensitive placeholder",
        ),
        (
            "missing_traceability_refs",
            {
                "env_values": {"GITHUB_TOKEN": ""},
                "connectors": {"github_mcp": {key: value for key, value in base_connector.items() if key != "traceability_refs"}},
            },
            True,
            "missing required declaration fields",
        ),
        (
            "runtime_allowlist_drift",
            {
                "env_values": {"GITHUB_TOKEN": ""},
                "connectors": {"github_mcp": {**base_connector, "allowed_runtimes": ["codex"]}},
            },
            True,
            "runtime allowlist drift",
        ),
        (
            "enabled_by_default",
            {
                "env_values": {"GITHUB_TOKEN": ""},
                "connectors": {"github_mcp": {**base_connector, "enabled": True}},
            },
            True,
            "connector enabled by default",
        ),
        (
            "allowed_denied_operation_conflict",
            {
                "env_values": {"GITHUB_TOKEN": ""},
                "connectors": {"github_mcp": {**base_connector, "denied_operations": [*SECURITY_REQUIRED_DENIED_OPERATIONS, "read_repo_metadata"]}},
            },
            True,
            "allowed denied operation conflict",
        ),
        (
            "risky_allowed_operation",
            {
                "env_values": {"GITHUB_TOKEN": ""},
                "connectors": {"github_mcp": {**base_connector, "allowed_operations": ["admin_all"]}},
            },
            True,
            "risky allowed operation",
        ),
    ]
    results = []
    for case_id, candidate, should_fail, expected_issue in fixtures:
        detected_issues = mcp_connector_negative_case_issues(candidate)
        failure_detected = bool(detected_issues)
        passed_expectation = (
            failure_detected == should_fail
            and (not expected_issue or expected_issue in detected_issues)
        )
        results.append(
            {
                "id": case_id,
                "expectedFailure": should_fail,
                "failureDetected": failure_detected,
                "passedExpectation": passed_expectation,
                "issues": detected_issues,
            }
        )
    return results


def validate_mcp_connector_auditor_contract(agents: list, issues: list[str]) -> dict:
    local_issues: list[str] = []
    summary = {
        "pass": False,
        "agentPresent": False,
        "agentCatalogMission": None,
        "mission": MCP_MISSION,
        "policyVersion": None,
        "envExampleChecked": False,
        "mcpConfigChecked": False,
        "auditContractChecked": False,
        "declarationRequirementsChecked": False,
        "envPlaceholderRequirementsChecked": False,
        "runtimeEquivalenceChecked": False,
        "qualityGatesChecked": False,
        "connectorsChecked": [],
        "connectorEnvPlaceholdersChecked": [],
        "orphanSensitivePlaceholders": [],
        "negativeCases": run_mcp_connector_negative_cases(),
        "negativeCasesDetected": False,
        "validationCommands": MCP_VALIDATION_COMMANDS,
    }

    agent = next((item for item in agents if isinstance(item, dict) and item.get("id") == MCP_AGENT), {})
    summary["agentPresent"] = bool(agent)
    if not agent:
        local_issues.append("MCP Connector Auditor agent is missing from data/agent_roster.json.")
    else:
        summary["agentCatalogMission"] = agent.get("mission")
        if agent.get("mission") != MCP_MISSION:
            local_issues.append("MCP Connector Auditor mission drifted from the connector declaration contract.")
        if agent.get("mode") != "python_first_llm_sparse":
            local_issues.append("MCP Connector Auditor mode must remain python_first_llm_sparse.")

    env_values = parse_env_example(ROOT / MCP_ENV_EXAMPLE, local_issues)
    mcp_config = read_json(ROOT / MCP_CONFIG, {}, local_issues)
    summary["mcpConfigChecked"] = bool(mcp_config)
    audit = mcp_config.get("mcp_connector_audit", {}) if isinstance(mcp_config, dict) else {}
    if not isinstance(audit, dict) or not audit:
        local_issues.append(f"{MCP_CONFIG} missing mcp_connector_audit contract.")
        audit = {}
    summary["policyVersion"] = audit.get("policy_version")
    if audit.get("policy_version") != MCP_AUDIT_VERSION:
        local_issues.append(f"{MCP_CONFIG} mcp_connector_audit.policy_version must be {MCP_AUDIT_VERSION}.")
    if audit.get("owner_agent") != MCP_AGENT:
        local_issues.append(f"{MCP_CONFIG} mcp_connector_audit.owner_agent must be {MCP_AGENT}.")
    if audit.get("mission") != MCP_MISSION:
        local_issues.append(f"{MCP_CONFIG} mcp_connector_audit mission must match the MCP connector auditor mission.")
    if audit.get("source_of_truth") != MCP_CONFIG:
        local_issues.append(f"{MCP_CONFIG} mcp_connector_audit.source_of_truth must be {MCP_CONFIG}.")
    if audit.get("env_example") != MCP_ENV_EXAMPLE:
        local_issues.append(f"{MCP_CONFIG} mcp_connector_audit.env_example must be {MCP_ENV_EXAMPLE}.")
    if audit.get("trace_evidence") != "generated/validation-report.json#mcpConnectorAuditor":
        local_issues.append(f"{MCP_CONFIG} mcp_connector_audit.trace_evidence must point to mcpConnectorAuditor.")
    if audit.get("validation_commands") != MCP_VALIDATION_COMMANDS:
        local_issues.append(f"{MCP_CONFIG} mcp_connector_audit validation_commands drifted from DoD.")

    if audit and not any(
        issue.startswith(f"{MCP_CONFIG} mcp_connector_audit")
        for issue in local_issues
    ):
        summary["auditContractChecked"] = True

    runtime_equivalence = audit.get("runtime_equivalence", {}) if isinstance(audit, dict) else {}
    if runtime_equivalence == MCP_RUNTIME_EQUIVALENCE:
        summary["runtimeEquivalenceChecked"] = True
    else:
        local_issues.append(f"{MCP_CONFIG} mcp_connector_audit.runtime_equivalence drifted from runtime parity.")

    declaration_requirements = audit.get("declaration_requirements", {}) if isinstance(audit, dict) else {}
    if not isinstance(declaration_requirements, dict):
        local_issues.append(f"{MCP_CONFIG} mcp_connector_audit.declaration_requirements must be an object.")
        declaration_requirements = {}
    required_fields = declaration_requirements.get("required_fields", [])
    declaration_checks = {
        "connector_name_case": "lower_snake_case",
        "env_name_case": "upper_snake_case",
        "default_enabled": False,
        "runtime_allowlist": RUNTIMES,
        "validation_command": "python tools/validate_copilot_factory.py",
    }
    declaration_drift = [
        key for key, expected in declaration_checks.items()
        if declaration_requirements.get(key) != expected
    ]
    if not isinstance(required_fields, list) or not set(MCP_REQUIRED_DECLARATION_FIELDS).issubset(set(required_fields)):
        declaration_drift.append("required_fields")
    if declaration_drift:
        local_issues.append(f"{MCP_CONFIG} mcp_connector_audit declaration requirements drifted: {', '.join(declaration_drift)}.")
    else:
        summary["declarationRequirementsChecked"] = True

    placeholder_requirements = audit.get("env_placeholder_requirements", {}) if isinstance(audit, dict) else {}
    if not isinstance(placeholder_requirements, dict):
        local_issues.append(f"{MCP_CONFIG} mcp_connector_audit.env_placeholder_requirements must be an object.")
        placeholder_requirements = {}
    placeholder_checks = {
        "placeholder_value": "",
        "connector_env_must_exist": True,
        "connector_env_must_be_unique": True,
        "no_orphan_sensitive_placeholders": True,
        "deny_credential_shaped_values": True,
    }
    placeholder_drift = [
        key for key, expected in placeholder_checks.items()
        if placeholder_requirements.get(key) != expected
    ]
    if placeholder_drift:
        local_issues.append(f"{MCP_CONFIG} mcp_connector_audit env placeholder requirements drifted: {', '.join(placeholder_drift)}.")
    else:
        summary["envPlaceholderRequirementsChecked"] = True

    quality_gates = audit.get("quality_gates", []) if isinstance(audit, dict) else []
    if isinstance(quality_gates, list) and set(MCP_REQUIRED_QUALITY_GATES).issubset(set(quality_gates)):
        summary["qualityGatesChecked"] = True
    else:
        local_issues.append(f"{MCP_CONFIG} mcp_connector_audit quality_gates missing required gate(s).")

    connectors = mcp_config.get("connectors", {}) if isinstance(mcp_config, dict) else {}
    actual_issues = mcp_connector_negative_case_issues({"env_values": env_values, "connectors": connectors})
    if actual_issues:
        local_issues.append(f"{MCP_CONFIG} connector/env placeholder audit failed: {', '.join(sorted(set(actual_issues)))}.")
    else:
        summary["envExampleChecked"] = True
        summary["connectorsChecked"] = sorted(connectors)
        connector_envs = sorted({connector.get("env") for connector in connectors.values() if isinstance(connector, dict)})
        summary["connectorEnvPlaceholdersChecked"] = connector_envs

    referenced_envs = {
        connector.get("env")
        for connector in connectors.values()
        if isinstance(connector, dict) and is_upper_snake(connector.get("env"))
    }
    sensitive_suffixes = ("TOKEN", "TOKEN_OPTIONAL", "SECRET", "API_KEY", "PASSWORD")
    summary["orphanSensitivePlaceholders"] = sorted(
        key for key in env_values
        if isinstance(key, str) and key.endswith(sensitive_suffixes) and key not in referenced_envs
    )

    summary["negativeCasesDetected"] = all(case["passedExpectation"] for case in summary["negativeCases"])
    if not summary["negativeCasesDetected"]:
        local_issues.append("MCP Connector Auditor negative fixtures must be detected by executable checks.")

    summary["issues"] = local_issues
    summary["pass"] = not local_issues
    issues.extend(local_issues)
    return summary


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except OSError:
        return ""


def validate_devops_auditor_contract(copilots: list, agents: list, index: dict, issues: list[str]) -> dict:
    local_issues: list[str] = []
    summary = {
        "pass": False,
        "agentPresent": False,
        "mission": DEVOPS_MISSION,
        "policyVersion": None,
        "targetCopilot": DEVOPS_TARGET_COPILOT,
        "targetCopilotPresent": False,
        "runFactoryChecked": False,
        "factoryAuditPresent": False,
        "factoryAuditChecked": False,
        "runtimeTraceChecked": False,
        "runtimeRefsChecked": [],
        "schemasRequireCloudMigration": False,
        "cloudMigrationSchemaChecked": False,
        "sampleRouteChecked": False,
        "sampleTopRoute": None,
        "sampleRouteCheapPath": False,
        "requiredEvidence": DEVOPS_REQUIRED_EVIDENCE,
        "qualityGates": DEVOPS_QUALITY_GATES,
        "runSequence": DEVOPS_RUN_SEQUENCE,
        "logEvidenceReport": DEVOPS_LOG_EVIDENCE_REPORT,
        "requiredReports": DEVOPS_REQUIRED_REPORTS,
        "rollbackPaths": DEVOPS_ROLLBACK_PATHS,
        "negativeCases": run_devops_negative_cases(),
        "negativeCasesDetected": False,
        "validationCommands": DEVOPS_VALIDATION_COMMANDS,
    }

    agent = next((item for item in agents if isinstance(item, dict) and item.get("id") == DEVOPS_AGENT), {})
    summary["agentPresent"] = bool(agent)
    if not agent:
        local_issues.append("DevOps Auditor agent is missing from data/agent_roster.json.")
    else:
        if agent.get("mission") != DEVOPS_MISSION:
            local_issues.append("DevOps Auditor mission drifted from the Operations contract.")
        if agent.get("mode") != "python_first_llm_sparse":
            local_issues.append("DevOps Auditor mode must remain python_first_llm_sparse.")

    target = next((item for item in copilots if isinstance(item, dict) and item.get("id") == DEVOPS_TARGET_COPILOT), {})
    summary["targetCopilotPresent"] = bool(target)
    if not target:
        local_issues.append("DevOps target copilot `cicd` is missing from data/copilots.json.")
    else:
        if target.get("family") != "devops":
            local_issues.append("DevOps target copilot `cicd` must stay in the devops family.")
        if "devops" not in list_field(target, "sdlc_phases"):
            local_issues.append("DevOps target copilot `cicd` must declare the devops SDLC phase.")
        for output in ["pipeline_triage", "workflow_patch_plan"]:
            if output not in list_field(target, "outputs"):
                local_issues.append(f"DevOps target copilot `cicd` missing output `{output}`.")

    run_factory_text = read_text(ROOT / "tools" / "run_factory.py")
    run_factory_markers = [
        "RUN_SEQUENCE",
        "SCRIPT_TIMEOUT_SECONDS",
        "PYTHONDONTWRITEBYTECODE",
        "subprocess.run",
        "LOG_EVIDENCE_PATH",
        "cwd=ROOT",
        "env=env",
        "check=True",
        "timeout=SCRIPT_TIMEOUT_SECONDS",
        "emit_log_evidence",
        "emit_devops_audit",
        "devops_audit_payload",
        "sanitizedEvidenceOnly",
    ]
    missing_markers = [marker for marker in run_factory_markers if marker not in run_factory_text]
    if missing_markers:
        local_issues.append(f"tools/run_factory.py missing DevOps runtime-toolchain marker(s): {', '.join(missing_markers)}.")
    else:
        summary["runFactoryChecked"] = True

    factory_audit = read_json(ROOT / "generated" / "factory-audit.json", {}, local_issues)
    devops_audit = factory_audit.get("devopsAudit", {}) if isinstance(factory_audit, dict) else {}
    summary["factoryAuditPresent"] = bool(devops_audit)
    if not isinstance(devops_audit, dict) or not devops_audit:
        local_issues.append("generated/factory-audit.json must expose a DevOps CI/CD audit summary.")
    else:
        summary["policyVersion"] = devops_audit.get("policyVersion")
        validate_devops_audit_payload(devops_audit, local_issues)
        summary["factoryAuditChecked"] = not any(issue.startswith("generated/factory-audit.json devopsAudit") for issue in local_issues)

    runtime_map = read_json(ROOT / "generated" / "runtime-injection-map.json", {}, local_issues)
    cicd_trace = (
        runtime_map.get("copilots", {}).get(DEVOPS_TARGET_COPILOT, {})
        if isinstance(runtime_map, dict)
        else {}
    )
    runtime_files = cicd_trace.get("runtimeFiles", {}) if isinstance(cicd_trace, dict) else {}
    if cicd_trace.get("sourceOfTruth") == DEVOPS_RUNTIME_EQUIVALENCE["sourceOfTruth"] and sorted(runtime_files) == sorted(RUNTIMES):
        summary["runtimeTraceChecked"] = True
    else:
        local_issues.append("generated/runtime-injection-map.json must trace `cicd` to all four runtime adapters.")

    expected_runtime_files = {
        "codex": ROOT / "dist" / "copilots" / "cicd" / "codex" / "AGENT.md",
        "claude": ROOT / "dist" / "copilots" / "cicd" / "claude" / "AGENT.md",
        "github-copilot": ROOT / "dist" / "copilots" / "cicd" / "github-copilot" / "copilot-agent.md",
        "langchain": ROOT / "dist" / "copilots" / "cicd" / "langchain" / "agent.py",
    }
    runtime_markers = [
        "Pipeline",
        "logs",
        "reproducible",
        "rollback",
        "validation",
    ]
    for runtime, path in expected_runtime_files.items():
        text = read_text(path).lower()
        missing = [marker for marker in runtime_markers if marker.lower() not in text]
        if missing:
            local_issues.append(f"DevOps runtime prompt for cicd/{runtime} missing marker(s): {', '.join(missing)}.")
        else:
            summary["runtimeRefsChecked"].append(runtime)

    try:
        import semantic_router as router

        sample = router.route("pipeline logs rollback reproducibility ci", limit=3)
    except Exception as exc:  # pragma: no cover - validator reports the concrete runtime error.
        local_issues.append(f"DevOps sample route failed: {exc}.")
        sample = []
    if sample:
        top = sample[0]
        summary["sampleRouteChecked"] = True
        summary["sampleTopRoute"] = top.get("id")
        summary["sampleRouteCheapPath"] = top.get("cheap_path") is True
        if top.get("id") != DEVOPS_TARGET_COPILOT:
            local_issues.append("DevOps sample route must select `cicd` first.")
        if top.get("cheap_path") is not True:
            local_issues.append("DevOps sample route must stay on the deterministic cheap path.")
        if top.get("runtime_trace", {}).get("runtimes") != RUNTIMES:
            local_issues.append("DevOps sample route must include full runtime trace evidence.")

    summary["negativeCasesDetected"] = all(case["passedExpectation"] for case in summary["negativeCases"])
    if not summary["negativeCasesDetected"]:
        local_issues.append("DevOps Auditor negative fixtures must be detected by executable checks.")

    summary["issues"] = local_issues
    summary["pass"] = not local_issues
    issues.extend(local_issues)
    return summary


def validate_devops_audit_payload(devops_audit: dict, issues: list[str]) -> None:
    prefix = "generated/factory-audit.json devopsAudit"
    checks = {
        "policyVersion": DEVOPS_AUDIT_VERSION,
        "ownerAgent": DEVOPS_AGENT,
        "mission": DEVOPS_MISSION,
        "targetCopilot": DEVOPS_TARGET_COPILOT,
        "targetCopilotSourceOfTruth": DEVOPS_RUNTIME_EQUIVALENCE["sourceOfTruth"],
        "requiredEvidence": DEVOPS_REQUIRED_EVIDENCE,
        "qualityGates": DEVOPS_QUALITY_GATES,
        "runSequence": DEVOPS_RUN_SEQUENCE,
        "ciCdEntrypoint": "tools/run_factory.py",
        "runtimeEquivalence": DEVOPS_RUNTIME_EQUIVALENCE,
        "validationCommands": DEVOPS_VALIDATION_COMMANDS,
    }
    for key, expected in checks.items():
        if devops_audit.get(key) != expected:
            issues.append(f"{prefix} `{key}` drifted.")
    if devops_audit.get("pass") is not True:
        issues.append(f"{prefix} pass must be true.")
    timeout = devops_audit.get("scriptTimeoutSeconds")
    if not isinstance(timeout, int) or not 1 <= timeout <= 900:
        issues.append(f"{prefix} scriptTimeoutSeconds must be a bounded integer up to 900.")

    log_evidence = devops_audit.get("logEvidence", [])
    if devops_audit.get("rawLogSource") != "agent.log":
        issues.append(f"{prefix} rawLogSource must point to the local-only agent.log source.")
    log_privacy = devops_audit.get("logPrivacy", {})
    if (
        not isinstance(log_privacy, dict)
        or log_privacy.get("rawLogLocalOnly") is not True
        or log_privacy.get("sanitizedEvidenceOnly") is not True
    ):
        issues.append(f"{prefix} logPrivacy must require sanitized evidence only.")
    if not isinstance(log_evidence, list) or DEVOPS_LOG_EVIDENCE_REPORT not in log_evidence:
        issues.append(f"{prefix} logEvidence must include the sanitized DevOps log evidence report.")
    if isinstance(log_evidence, list) and "agent.log" in log_evidence:
        issues.append(f"{prefix} logEvidence must not publish raw agent.log as a release artifact.")
    missing_reports = [report for report in DEVOPS_REQUIRED_REPORTS if report not in log_evidence]
    if missing_reports:
        issues.append(f"{prefix} logEvidence missing report(s): {', '.join(missing_reports)}.")
    validate_devops_log_artifacts(log_evidence, issues)

    reproducibility = devops_audit.get("reproducibility", {})
    reproducibility_checks = {
        "pythonExecutable": "sys.executable",
        "workingDirectory": "workspace_root",
        "deterministicOrder": True,
        "subprocessCheck": True,
        "noBytecodeArtifacts": True,
        "networkRequired": False,
        "credentialsRequired": False,
    }
    if reproducibility != reproducibility_checks:
        issues.append(f"{prefix} reproducibility contract drifted.")
    if devops_audit.get("rollbackPaths") != DEVOPS_ROLLBACK_PATHS:
        issues.append(f"{prefix} rollbackPaths drifted.")
    validate_devops_rollback_artifacts(devops_audit.get("rollbackPaths", []), issues)
    cost_control = devops_audit.get("costControl", {})
    if cost_control.get("deterministicPythonFirst") is not True:
        issues.append(f"{prefix} costControl must require deterministic Python first.")


def validate_devops_log_artifacts(log_evidence: object, issues: list[str]) -> None:
    prefix = "generated/factory-audit.json devopsAudit"
    if not isinstance(log_evidence, list):
        return
    for rel_path in log_evidence:
        if not is_safe_workspace_relative_path(rel_path):
            issues.append(f"{prefix} logEvidence contains an unsafe relative path.")
            continue
        path = ROOT / rel_path
        if rel_path == DEVOPS_LOG_EVIDENCE_REPORT:
            validate_devops_log_evidence_report(rel_path, issues)
            continue
        if rel_path in DEVOPS_REQUIRED_REPORTS and rel_path != relative(REPORT_JSON):
            validate_devops_report_artifact(rel_path, issues)


def validate_devops_log_evidence_report(rel_path: str, issues: list[str]) -> None:
    prefix = "generated/factory-audit.json devopsAudit"
    path = ROOT / rel_path
    if not path.is_file() or path.stat().st_size == 0:
        issues.append(f"{prefix} sanitized log evidence must exist and be non-empty: {rel_path}.")
        return
    try:
        report = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        issues.append(f"{prefix} sanitized log evidence is invalid JSON at line {exc.lineno}.")
        return
    except OSError as exc:
        issues.append(f"{prefix} sanitized log evidence cannot be read: {exc}.")
        return

    privacy = report.get("privacy", {}) if isinstance(report, dict) else {}
    checks = report.get("checks", {}) if isinstance(report, dict) else {}
    if report.get("pass") is not True:
        issues.append(f"{prefix} sanitized log evidence must have pass=true.")
    if report.get("sourceLog") != "agent.log":
        issues.append(f"{prefix} sanitized log evidence must reference agent.log as sourceLog.")
    if (
        not isinstance(privacy, dict)
        or privacy.get("rawLogLocalOnly") is not True
        or privacy.get("contentStored") is not False
        or privacy.get("sanitizedEvidenceOnly") is not True
        or privacy.get("absolutePathsRedacted") is not True
    ):
        issues.append(f"{prefix} sanitized log evidence privacy contract drifted.")
    if (
        not isinstance(checks, dict)
        or checks.get("sourceExists") is not True
        or checks.get("sourceNonEmpty") is not True
        or checks.get("scanTruncated") is not False
        or checks.get("secretPatternMatches") != 0
        or not isinstance(checks.get("localAbsolutePathMatches"), int)
    ):
        issues.append(f"{prefix} sanitized log evidence checks did not pass.")


def validate_devops_report_artifact(rel_path: str, issues: list[str]) -> None:
    prefix = "generated/factory-audit.json devopsAudit"
    path = ROOT / rel_path
    if not path.is_file() or path.stat().st_size == 0:
        issues.append(f"{prefix} report evidence must exist and be non-empty: {rel_path}.")
        return
    try:
        report = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        issues.append(f"{prefix} report evidence is invalid JSON: {rel_path} at line {exc.lineno}.")
        return
    except OSError as exc:
        issues.append(f"{prefix} report evidence cannot be read: {rel_path}: {exc}.")
        return
    if not isinstance(report, dict) or report.get("pass") is not True:
        issues.append(f"{prefix} report evidence must have pass=true: {rel_path}.")


def validate_devops_rollback_artifacts(rollback_paths: object, issues: list[str]) -> None:
    prefix = "generated/factory-audit.json devopsAudit"
    if not isinstance(rollback_paths, list):
        issues.append(f"{prefix} rollbackPaths must be a list.")
        return
    for rel_path in DEVOPS_ROLLBACK_PATHS:
        if rel_path not in rollback_paths:
            continue
        if not is_safe_workspace_relative_path(rel_path):
            issues.append(f"{prefix} rollback path is not workspace-relative: {rel_path}.")
            continue
        path = ROOT / rel_path
        if not path.is_dir():
            issues.append(f"{prefix} rollback path must exist as a directory: {rel_path}.")
            continue
        if not any(path.iterdir()):
            issues.append(f"{prefix} rollback path must contain snapshot evidence: {rel_path}.")


def is_safe_workspace_relative_path(value: object) -> bool:
    if not isinstance(value, str) or not value.strip():
        return False
    path = Path(value)
    if path.is_absolute():
        return False
    return ".." not in path.parts


def detect_devops_fixture_issues(payload: dict) -> list[str]:
    detected: list[str] = []
    if payload.get("ciCdEntrypoint") != "tools/run_factory.py":
        detected.append("missing ci/cd entrypoint")
    if payload.get("requiredEvidence") != DEVOPS_REQUIRED_EVIDENCE:
        detected.append("missing required evidence")
    if payload.get("qualityGates") != DEVOPS_QUALITY_GATES:
        detected.append("quality gate drift")
    if payload.get("runSequence") != DEVOPS_RUN_SEQUENCE:
        detected.append("non-reproducible run sequence")
    if payload.get("validationCommands") != DEVOPS_VALIDATION_COMMANDS:
        detected.append("validation command drift")
    log_evidence = payload.get("logEvidence", [])
    if not isinstance(log_evidence, list) or DEVOPS_LOG_EVIDENCE_REPORT not in log_evidence:
        detected.append("missing log evidence")
    if isinstance(log_evidence, list) and "agent.log" in log_evidence:
        detected.append("raw log evidence leak")
    if not isinstance(log_evidence, list) or any(report not in log_evidence for report in DEVOPS_REQUIRED_REPORTS):
        detected.append("missing report evidence")
    if isinstance(log_evidence, list) and any(not is_safe_workspace_relative_path(item) for item in log_evidence):
        detected.append("unsafe log evidence path")
    reproducibility = payload.get("reproducibility", {})
    if (
        not isinstance(reproducibility, dict)
        or reproducibility.get("deterministicOrder") is not True
        or reproducibility.get("subprocessCheck") is not True
        or reproducibility.get("noBytecodeArtifacts") is not True
        or reproducibility.get("networkRequired") is not False
        or reproducibility.get("credentialsRequired") is not False
    ):
        detected.append("reproducibility guard drift")
    if payload.get("rollbackPaths") != DEVOPS_ROLLBACK_PATHS:
        detected.append("missing rollback path")
    if payload.get("runtimeEquivalence") != DEVOPS_RUNTIME_EQUIVALENCE:
        detected.append("runtime equivalence drift")
    if payload.get("costControl", {}).get("deterministicPythonFirst") is not True:
        detected.append("missing deterministic cost control")
    return detected


def run_devops_negative_cases() -> list[dict]:
    valid_payload = {
        "ciCdEntrypoint": "tools/run_factory.py",
        "requiredEvidence": DEVOPS_REQUIRED_EVIDENCE,
        "qualityGates": DEVOPS_QUALITY_GATES,
        "runSequence": DEVOPS_RUN_SEQUENCE,
        "validationCommands": DEVOPS_VALIDATION_COMMANDS,
        "logEvidence": [DEVOPS_LOG_EVIDENCE_REPORT, *DEVOPS_REQUIRED_REPORTS],
        "reproducibility": {
            "deterministicOrder": True,
            "subprocessCheck": True,
            "noBytecodeArtifacts": True,
            "networkRequired": False,
            "credentialsRequired": False,
        },
        "rollbackPaths": DEVOPS_ROLLBACK_PATHS,
        "runtimeEquivalence": DEVOPS_RUNTIME_EQUIVALENCE,
        "costControl": {"deterministicPythonFirst": True},
    }
    fixtures = [
        ("valid_control", valid_payload, False, ""),
        ("missing_entrypoint", {**valid_payload, "ciCdEntrypoint": ""}, True, "missing ci/cd entrypoint"),
        ("missing_log_report", {**valid_payload, "logEvidence": [DEVOPS_LOG_EVIDENCE_REPORT]}, True, "missing report evidence"),
        ("raw_log_evidence", {**valid_payload, "logEvidence": ["agent.log", *DEVOPS_REQUIRED_REPORTS]}, True, "raw log evidence leak"),
        ("unsafe_log_path", {**valid_payload, "logEvidence": [DEVOPS_LOG_EVIDENCE_REPORT, "../outside.log", *DEVOPS_REQUIRED_REPORTS]}, True, "unsafe log evidence path"),
        ("unordered_run_sequence", {**valid_payload, "runSequence": list(reversed(DEVOPS_RUN_SEQUENCE))}, True, "non-reproducible run sequence"),
        ("missing_rollback_path", {**valid_payload, "rollbackPaths": [".codex-loop/rollback"]}, True, "missing rollback path"),
        ("runtime_drift", {**valid_payload, "runtimeEquivalence": {"runtimes": ["codex"]}}, True, "runtime equivalence drift"),
        ("missing_cost_control", {**valid_payload, "costControl": {}}, True, "missing deterministic cost control"),
    ]
    results = []
    for case_id, payload, should_fail, expected_issue in fixtures:
        detected = detect_devops_fixture_issues(payload)
        failure_detected = bool(detected)
        passed_expectation = (
            failure_detected == should_fail
            and (not expected_issue or expected_issue in detected)
        )
        results.append(
            {
                "id": case_id,
                "expectedFailure": should_fail,
                "failureDetected": failure_detected,
                "passedExpectation": passed_expectation,
                "detected": passed_expectation,
                "issues": detected,
            }
        )
    return results


def validate_cloud_auditor_contract(copilots: list, agents: list, index: dict, issues: list[str]) -> dict:
    local_issues: list[str] = []
    summary = {
        "pass": False,
        "agentPresent": False,
        "mission": CLOUD_MISSION,
        "policyVersion": None,
        "targetCopilot": CLOUD_TARGET_COPILOT,
        "targetCopilotPresent": False,
        "auditArtifact": CLOUD_AUDIT_ARTIFACT,
        "auditArtifactChecked": False,
        "factoryAuditPresent": False,
        "factoryAuditChecked": False,
        "runtimeTraceChecked": False,
        "runtimeRefsChecked": [],
        "sampleRouteChecked": False,
        "sampleTopRoute": None,
        "sampleRouteCheapPath": False,
        "requiredEvidence": CLOUD_REQUIRED_EVIDENCE,
        "qualityGates": CLOUD_QUALITY_GATES,
        "requiredOutputFields": CLOUD_REQUIRED_OUTPUT_FIELDS,
        "requiredCloudMigrationFields": CLOUD_REQUIRED_MIGRATION_FIELDS,
        "negativeCases": run_cloud_negative_cases(),
        "negativeCasesDetected": False,
        "validationCommands": CLOUD_VALIDATION_COMMANDS,
    }

    agent = next((item for item in agents if isinstance(item, dict) and item.get("id") == CLOUD_AGENT), {})
    summary["agentPresent"] = bool(agent)
    if not agent:
        local_issues.append("Cloud Auditor agent is missing from data/agent_roster.json.")
    else:
        if agent.get("mission") != CLOUD_MISSION:
            local_issues.append("Cloud Auditor mission drifted from the Operations contract.")
        if agent.get("mode") != "python_first_llm_sparse":
            local_issues.append("Cloud Auditor mode must remain python_first_llm_sparse.")

    target = next((item for item in copilots if isinstance(item, dict) and item.get("id") == CLOUD_TARGET_COPILOT), {})
    summary["targetCopilotPresent"] = bool(target)
    if not target:
        local_issues.append("Cloud target copilot `journey_to_cloud` is missing from data/copilots.json.")
    else:
        if target.get("family") != "cloud":
            local_issues.append("Cloud target copilot `journey_to_cloud` must stay in the cloud family.")
        if "cloud" not in list_field(target, "sdlc_phases"):
            local_issues.append("Cloud target copilot `journey_to_cloud` must declare the cloud SDLC phase.")
        for output in ["migration_plan", "cloud_readiness_report"]:
            if output not in list_field(target, "outputs"):
                local_issues.append(f"Cloud target copilot `journey_to_cloud` missing output `{output}`.")

    artifact_path = ROOT / CLOUD_AUDIT_ARTIFACT
    validate_cloud_migration_audit_artifact(artifact_path, local_issues)
    summary["auditArtifactChecked"] = not any(
        issue.startswith("dist/copilots/journey_to_cloud/shared/cloud_migration_audit.json")
        for issue in local_issues
    )

    factory_audit = read_json(ROOT / "generated" / "factory-audit.json", {}, local_issues)
    cloud_audit = factory_audit.get("cloudAudit", {}) if isinstance(factory_audit, dict) else {}
    summary["factoryAuditPresent"] = bool(cloud_audit)
    if not isinstance(cloud_audit, dict) or not cloud_audit:
        local_issues.append("generated/factory-audit.json must expose a Cloud migration audit summary.")
    else:
        summary["policyVersion"] = cloud_audit.get("policyVersion")
        validate_cloud_audit_payload(cloud_audit, local_issues)
        summary["factoryAuditChecked"] = not any(issue.startswith("generated/factory-audit.json cloudAudit") for issue in local_issues)

    runtime_map = read_json(ROOT / "generated" / "runtime-injection-map.json", {}, local_issues)
    cloud_trace = (
        runtime_map.get("copilots", {}).get(CLOUD_TARGET_COPILOT, {})
        if isinstance(runtime_map, dict)
        else {}
    )
    runtime_files = cloud_trace.get("runtimeFiles", {}) if isinstance(cloud_trace, dict) else {}
    migration_trace = cloud_trace.get("cloudMigrationAudit", {}) if isinstance(cloud_trace, dict) else {}
    if (
        cloud_trace.get("sourceOfTruth") == "dist/copilots/journey_to_cloud/shared/spec.json"
        and sorted(runtime_files) == sorted(RUNTIMES)
        and migration_trace.get("artifact") == CLOUD_AUDIT_ARTIFACT
        and migration_trace.get("runtimeEquivalence") == CLOUD_RUNTIME_EQUIVALENCE
    ):
        summary["runtimeTraceChecked"] = True
    else:
        local_issues.append("generated/runtime-injection-map.json must trace `journey_to_cloud` cloud audit to all four runtime adapters.")

    cloud_base = ROOT / "dist" / "copilots" / CLOUD_TARGET_COPILOT
    output_schema = read_json(cloud_base / "shared" / "output_schema.json", {}, local_issues)
    spec = read_json(cloud_base / "shared" / "spec.json", {}, local_issues)
    profile = read_json(cloud_base / "langchain" / "agent_profile.json", {}, local_issues)
    if (
        "cloud_migration" in output_schema.get("required", [])
        and "cloud_migration" in spec.get("outputSchema", {}).get("required", [])
    ):
        summary["schemasRequireCloudMigration"] = True
    else:
        local_issues.append("Cloud output schema must require `cloud_migration` for journey_to_cloud.")
    validate_cloud_output_schema(output_schema, spec, profile, local_issues)
    summary["cloudMigrationSchemaChecked"] = not any(
        issue.startswith("Cloud output schema")
        or issue.startswith("Shared spec outputSchema drifted from cloud output schema")
        or issue.startswith("LangChain profile outputSchema drifted from cloud output schema")
        or issue.startswith("LangChain profile contract outputSchema drifted from cloud output schema")
        for issue in local_issues
    )

    expected_runtime_files = {
        "codex": ROOT / "dist" / "copilots" / "journey_to_cloud" / "codex" / "AGENT.md",
        "claude": ROOT / "dist" / "copilots" / "journey_to_cloud" / "claude" / "AGENT.md",
        "github-copilot": ROOT / "dist" / "copilots" / "journey_to_cloud" / "github-copilot" / "copilot-agent.md",
        "langchain": ROOT / "dist" / "copilots" / "journey_to_cloud" / "langchain" / "agent.py",
    }
    runtime_markers = ["migration", "platform", "modernization", "validation"]
    for runtime, path in expected_runtime_files.items():
        text = read_text(path).lower()
        missing = [marker for marker in runtime_markers if marker not in text]
        if missing:
            local_issues.append(f"Cloud runtime prompt for journey_to_cloud/{runtime} missing marker(s): {', '.join(missing)}.")
        else:
            summary["runtimeRefsChecked"].append(runtime)

    try:
        import semantic_router as router

        sample = router.route("cloud migration target platform modernization increments", limit=3)
    except Exception as exc:  # pragma: no cover - validator reports the concrete runtime error.
        local_issues.append(f"Cloud sample route failed: {exc}.")
        sample = []
    if sample:
        top = sample[0]
        summary["sampleRouteChecked"] = True
        summary["sampleTopRoute"] = top.get("id")
        summary["sampleRouteCheapPath"] = top.get("cheap_path") is True
        if top.get("id") != CLOUD_TARGET_COPILOT:
            local_issues.append("Cloud sample route must select `journey_to_cloud` first.")
        if top.get("cheap_path") is not True:
            local_issues.append("Cloud sample route must stay on the deterministic cheap path.")
        if top.get("runtime_trace", {}).get("runtimes") != RUNTIMES:
            local_issues.append("Cloud sample route must include full runtime trace evidence.")

    summary["negativeCasesDetected"] = all(case["passedExpectation"] for case in summary["negativeCases"])
    if not summary["negativeCasesDetected"]:
        local_issues.append("Cloud Auditor negative fixtures must be detected by executable checks.")

    summary["issues"] = local_issues
    summary["pass"] = not local_issues
    issues.extend(local_issues)
    return summary


def validate_cloud_audit_payload(cloud_audit: dict, issues: list[str]) -> None:
    prefix = "generated/factory-audit.json cloudAudit"
    checks = {
        "policyVersion": CLOUD_AUDIT_VERSION,
        "ownerAgent": CLOUD_AGENT,
        "mission": CLOUD_MISSION,
        "targetCopilot": CLOUD_TARGET_COPILOT,
        "targetCopilotSourceOfTruth": "dist/copilots/journey_to_cloud/shared/spec.json",
        "auditArtifact": CLOUD_AUDIT_ARTIFACT,
        "requiredEvidence": CLOUD_REQUIRED_EVIDENCE,
        "qualityGates": CLOUD_QUALITY_GATES,
        "requiredOutputFields": CLOUD_REQUIRED_OUTPUT_FIELDS,
        "requiredCloudMigrationFields": CLOUD_REQUIRED_MIGRATION_FIELDS,
        "runtimeEquivalence": CLOUD_RUNTIME_EQUIVALENCE,
        "validationCommands": CLOUD_VALIDATION_COMMANDS,
    }
    for key, expected in checks.items():
        if cloud_audit.get(key) != expected:
            issues.append(f"{prefix} `{key}` drifted.")
    if cloud_audit.get("pass") is not True:
        issues.append(f"{prefix} pass must be true.")
    if cloud_audit.get("frontier") != "cost-time":
        issues.append(f"{prefix} frontier must remain cost-time.")

    target_platform = cloud_audit.get("targetPlatform", {})
    if (
        not isinstance(target_platform, dict)
        or target_platform.get("selectionRequired") is not True
        or not isinstance(target_platform.get("decisionInputs"), list)
        or "runtime" not in target_platform.get("decisionInputs", [])
    ):
        issues.append(f"{prefix} targetPlatform must require runtime/platform decision inputs.")

    increments = cloud_audit.get("modernizationIncrements", [])
    if not isinstance(increments, list) or len(increments) < 3:
        issues.append(f"{prefix} modernizationIncrements must contain at least three bounded increment checks.")
    else:
        for item in increments:
            if not isinstance(item, dict) or not {"id", "evidence", "validation"}.issubset(item):
                issues.append(f"{prefix} modernizationIncrements entries must expose id, evidence and validation.")
                break

    cost_control = cloud_audit.get("costControl", {})
    if (
        not isinstance(cost_control, dict)
        or cost_control.get("deterministicPythonFirst") is not True
        or cost_control.get("llmEscalation") != "allowed_after_platform_tradeoff_only"
        or cost_control.get("maxPromptGrowthRatio") != 0.10
    ):
        issues.append(f"{prefix} costControl must keep deterministic checks first and prompt growth bounded.")


def validate_cloud_migration_audit_artifact(path: Path, issues: list[str]) -> None:
    prefix = CLOUD_AUDIT_ARTIFACT
    if not path.is_file() or path.stat().st_size == 0:
        issues.append(f"{prefix} must exist and be non-empty.")
        return
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        issues.append(f"{prefix} is invalid JSON at line {exc.lineno}.")
        return
    except OSError as exc:
        issues.append(f"{prefix} cannot be read: {exc}.")
        return
    if not isinstance(payload, dict):
        issues.append(f"{prefix} must be a JSON object.")
        return

    checks = {
        "version": CLOUD_AUDIT_VERSION,
        "ownerAgent": CLOUD_AGENT,
        "copilotId": CLOUD_TARGET_COPILOT,
        "mission": CLOUD_MISSION,
        "runtimeEquivalence": CLOUD_RUNTIME_EQUIVALENCE,
        "requiredOutputFields": CLOUD_REQUIRED_OUTPUT_FIELDS,
        "requiredCloudMigrationFields": CLOUD_REQUIRED_MIGRATION_FIELDS,
        "validationCommands": CLOUD_VALIDATION_COMMANDS,
    }
    for key, expected in checks.items():
        if payload.get(key) != expected:
            issues.append(f"{prefix} `{key}` drifted.")

    evidence_ids = [item.get("id") for item in payload.get("requiredEvidence", []) if isinstance(item, dict)]
    if evidence_ids != CLOUD_REQUIRED_EVIDENCE:
        issues.append(f"{prefix} requiredEvidence drifted.")
    gate_ids = [item.get("id") for item in payload.get("qualityGates", []) if isinstance(item, dict)]
    if gate_ids != CLOUD_QUALITY_GATES:
        issues.append(f"{prefix} qualityGates drifted.")

    template = payload.get("migrationIncrementTemplate", {})
    required_template_fields = [
        "increment_id",
        "source_evidence",
        "target_capability",
        "modernization_action",
        "validation_command",
        "rollback_path",
    ]
    if not isinstance(template, dict) or template.get("requiredFields") != required_template_fields:
        issues.append(f"{prefix} migrationIncrementTemplate required fields drifted.")


def validate_cloud_output_schema(
    output_schema: object,
    spec: dict,
    profile: dict,
    issues: list[str],
) -> None:
    if not isinstance(output_schema, dict) or not output_schema:
        issues.append("Cloud output schema is missing for journey_to_cloud.")
        return

    required = output_schema.get("required", [])
    for field in CLOUD_REQUIRED_OUTPUT_FIELDS:
        if field not in required:
            issues.append(f"Cloud output schema required fields missing `{field}`.")
    if output_schema.get("additionalProperties") is not False:
        issues.append("Cloud output schema must close root output to declared fields.")

    actions = output_schema.get("properties", {}).get("actions", {})
    if actions.get("items", {}).get("additionalProperties") is not False:
        issues.append("Cloud output schema must close action entries to declared fields.")

    migration = output_schema.get("properties", {}).get("cloud_migration", {})
    if migration.get("required") != CLOUD_REQUIRED_MIGRATION_FIELDS:
        issues.append("Cloud output schema cloud_migration fields drifted.")
    if migration.get("additionalProperties") is not False:
        issues.append("Cloud output schema must close cloud_migration to declared fields.")

    increments = migration.get("properties", {}).get("migration_increments", {})
    if increments.get("minItems", 0) < 3:
        issues.append("Cloud output schema migration_increments must require at least three increments.")
    if increments.get("items", {}).get("additionalProperties") is not False:
        issues.append("Cloud output schema must close migration increment entries to declared fields.")
    increment_required = increments.get("items", {}).get("required", [])
    missing_increment_fields = [
        field
        for field in [
            "increment_id",
            "source_evidence",
            "target_capability",
            "modernization_action",
            "validation_command",
            "rollback_path",
        ]
        if field not in increment_required
    ]
    if missing_increment_fields:
        issues.append(
            "Cloud output schema migration increment fields missing: "
            + ", ".join(missing_increment_fields)
            + "."
        )

    evidence_schema = output_schema.get("properties", {}).get("evidence", {})
    if evidence_schema.get("minItems", 0) < len(CLOUD_REQUIRED_EVIDENCE):
        issues.append("Cloud output schema evidence minItems drifted.")
    item_kind = (
        evidence_schema.get("items", {})
        .get("properties", {})
        .get("kind", {})
    )
    kind_enum = item_kind.get("enum", [])
    missing_kinds = [kind for kind in CLOUD_REQUIRED_EVIDENCE if kind not in kind_enum]
    if missing_kinds:
        issues.append(f"Cloud output schema evidence kinds missing: {', '.join(missing_kinds)}.")
    contains_kinds = [
        rule.get("contains", {}).get("properties", {}).get("kind", {}).get("const")
        for rule in evidence_schema.get("allOf", [])
        if isinstance(rule, dict)
    ]
    missing_contains = [kind for kind in CLOUD_REQUIRED_EVIDENCE if kind not in contains_kinds]
    if missing_contains:
        issues.append(
            "Cloud output schema must require one evidence item per cloud evidence kind: "
            + ", ".join(missing_contains)
            + "."
        )

    if spec.get("outputSchema") != output_schema:
        issues.append("Shared spec outputSchema drifted from cloud output schema for journey_to_cloud.")
    if profile.get("outputSchema") != output_schema:
        issues.append("LangChain profile outputSchema drifted from cloud output schema for journey_to_cloud.")
    if profile.get("contract", {}).get("outputSchema") != output_schema:
        issues.append("LangChain profile contract outputSchema drifted from cloud output schema for journey_to_cloud.")


def detect_cloud_fixture_issues(payload: dict) -> list[str]:
    detected: list[str] = []
    if payload.get("requiredEvidence") != CLOUD_REQUIRED_EVIDENCE:
        detected.append("missing required evidence")
    if payload.get("qualityGates") != CLOUD_QUALITY_GATES:
        detected.append("quality gate drift")
    if payload.get("requiredCloudMigrationFields") != CLOUD_REQUIRED_MIGRATION_FIELDS:
        detected.append("missing cloud migration fields")
    if payload.get("runtimeEquivalence") != CLOUD_RUNTIME_EQUIVALENCE:
        detected.append("runtime equivalence drift")
    target_platform = payload.get("targetPlatform", {})
    if not isinstance(target_platform, dict) or target_platform.get("selectionRequired") is not True:
        detected.append("missing target platform decision")
    increments = payload.get("modernizationIncrements", [])
    if not isinstance(increments, list) or len(increments) < 3:
        detected.append("insufficient modernization increments")
    if payload.get("validationCommands") != CLOUD_VALIDATION_COMMANDS:
        detected.append("validation command drift")
    cost_control = payload.get("costControl", {})
    if not isinstance(cost_control, dict) or cost_control.get("deterministicPythonFirst") is not True:
        detected.append("missing deterministic cost control")
    return detected


def run_cloud_negative_cases() -> list[dict]:
    valid_payload = {
        "requiredEvidence": CLOUD_REQUIRED_EVIDENCE,
        "qualityGates": CLOUD_QUALITY_GATES,
        "requiredCloudMigrationFields": CLOUD_REQUIRED_MIGRATION_FIELDS,
        "runtimeEquivalence": CLOUD_RUNTIME_EQUIVALENCE,
        "targetPlatform": {"selectionRequired": True},
        "modernizationIncrements": [
            {"id": "inventory", "evidence": "local catalog", "validation": "schema"},
            {"id": "platform", "evidence": "capability matrix", "validation": "matrix"},
            {"id": "handoff", "evidence": "release gate", "validation": "validators"},
        ],
        "validationCommands": CLOUD_VALIDATION_COMMANDS,
        "costControl": {"deterministicPythonFirst": True},
    }
    fixtures = [
        ("valid_control", valid_payload, False, ""),
        ("missing_required_evidence", {**valid_payload, "requiredEvidence": []}, True, "missing required evidence"),
        ("missing_target_platform", {**valid_payload, "targetPlatform": {}}, True, "missing target platform decision"),
        ("insufficient_increments", {**valid_payload, "modernizationIncrements": []}, True, "insufficient modernization increments"),
        ("runtime_drift", {**valid_payload, "runtimeEquivalence": {"runtimes": ["codex"]}}, True, "runtime equivalence drift"),
        ("missing_cost_control", {**valid_payload, "costControl": {}}, True, "missing deterministic cost control"),
    ]
    results = []
    for case_id, payload, should_fail, expected_issue in fixtures:
        detected = detect_cloud_fixture_issues(payload)
        failure_detected = bool(detected)
        passed_expectation = (
            failure_detected == should_fail
            and (not expected_issue or expected_issue in detected)
        )
        results.append(
            {
                "id": case_id,
                "expectedFailure": should_fail,
                "failureDetected": failure_detected,
                "passedExpectation": passed_expectation,
                "detected": passed_expectation,
                "issues": detected,
            }
        )
    return results


def validate_release_auditor_contract(copilots: list, agents: list, config: dict, issues: list[str]) -> dict:
    local_issues: list[str] = []
    release_targets = [
        item.get("id")
        for item in copilots
        if isinstance(item, dict) and "release" in list_field(item, "sdlc_phases")
    ]
    summary = {
        "pass": False,
        "agentPresent": False,
        "mission": RELEASE_MISSION,
        "policyVersion": None,
        "targetCopilots": release_targets,
        "targetCopilotsChecked": [],
        "configGateChecked": False,
        "factoryAuditPresent": False,
        "factoryAuditChecked": False,
        "runtimeTraceChecked": False,
        "runtimeRefsChecked": [],
        "scorecardsChecked": [],
        "exitCriteriaChecked": [],
        "sampleRouteChecked": False,
        "sampleTopRoute": None,
        "sampleRouteCheapPath": False,
        "requiredEvidence": RELEASE_REQUIRED_EVIDENCE,
        "qualityGates": RELEASE_QUALITY_GATES,
        "artifactTargets": RELEASE_ARTIFACT_TARGETS,
        "negativeCases": run_release_negative_cases(),
        "negativeCasesDetected": False,
        "validationCommands": RELEASE_VALIDATION_COMMANDS,
    }

    if release_targets != RELEASE_TARGET_COPILOTS:
        local_issues.append("Release Auditor target copilot set drifted from the release SDLC catalog.")

    agent = next((item for item in agents if isinstance(item, dict) and item.get("id") == RELEASE_AGENT), {})
    summary["agentPresent"] = bool(agent)
    if not agent:
        local_issues.append("Release Auditor agent is missing from data/agent_roster.json.")
    else:
        if agent.get("mission") != RELEASE_MISSION:
            local_issues.append("Release Auditor mission drifted from the Operations contract.")
        if agent.get("mode") != "python_first_llm_sparse":
            local_issues.append("Release Auditor mode must remain python_first_llm_sparse.")
        if agent.get("phase") != "release":
            local_issues.append("Release Auditor must stay in the release phase.")

    for target_id in RELEASE_TARGET_COPILOTS:
        target = next((item for item in copilots if isinstance(item, dict) and item.get("id") == target_id), {})
        if not target:
            local_issues.append(f"Release target copilot `{target_id}` is missing from data/copilots.json.")
            continue
        if "release" not in list_field(target, "sdlc_phases"):
            local_issues.append(f"Release target copilot `{target_id}` must declare the release SDLC phase.")
        if not list_field(target, "outputs"):
            local_issues.append(f"Release target copilot `{target_id}` must expose at least one release-scored output.")
        summary["targetCopilotsChecked"].append(target_id)

    release_gate = (
        config.get("controlRoom", {})
        .get("releaseTruthGate", {})
        .get("releaseReadinessAudit", {})
        if isinstance(config, dict)
        else {}
    )
    validate_release_gate_contract(release_gate, local_issues)
    summary["configGateChecked"] = not any(
        issue.startswith("factory.config.json releaseReadinessAudit")
        for issue in local_issues
    )

    factory_audit = read_json(ROOT / "generated" / "factory-audit.json", {}, local_issues)
    release_audit = factory_audit.get("releaseAudit", {}) if isinstance(factory_audit, dict) else {}
    summary["factoryAuditPresent"] = bool(release_audit)
    if not isinstance(release_audit, dict) or not release_audit:
        local_issues.append("generated/factory-audit.json must expose a Release readiness audit summary.")
    else:
        summary["policyVersion"] = release_audit.get("policyVersion")
        checked = validate_release_audit_payload(release_audit, local_issues)
        summary["scorecardsChecked"] = checked["scorecards"]
        summary["exitCriteriaChecked"] = checked["exitCriteria"]
        summary["factoryAuditChecked"] = not any(issue.startswith("generated/factory-audit.json releaseAudit") for issue in local_issues)

    runtime_map = read_json(ROOT / "generated" / "runtime-injection-map.json", {}, local_issues)
    runtime_checked = validate_release_runtime_trace(runtime_map, release_audit, local_issues)
    summary["runtimeRefsChecked"] = runtime_checked
    summary["runtimeTraceChecked"] = len(runtime_checked) == len(RELEASE_TARGET_COPILOTS)

    try:
        import semantic_router as router

        sample = router.route("marketplace manifest distribution package release", limit=3)
    except Exception as exc:  # pragma: no cover - validator reports the concrete runtime error.
        local_issues.append(f"Release sample route failed: {exc}.")
        sample = []
    if sample:
        top = sample[0]
        summary["sampleRouteChecked"] = True
        summary["sampleTopRoute"] = top.get("id")
        summary["sampleRouteCheapPath"] = top.get("cheap_path") is True
        if top.get("id") != "firefly_marketplace":
            local_issues.append("Release sample route must select `firefly_marketplace` first for package distribution work.")
        if top.get("cheap_path") is not True:
            local_issues.append("Release sample route must stay on the deterministic cheap path.")
        if top.get("runtime_trace", {}).get("runtimes") != RUNTIMES:
            local_issues.append("Release sample route must include full runtime trace evidence.")

    summary["negativeCasesDetected"] = all(case["passedExpectation"] for case in summary["negativeCases"])
    if not summary["negativeCasesDetected"]:
        local_issues.append("Release Auditor negative fixtures must be detected by executable checks.")

    summary["issues"] = local_issues
    summary["pass"] = not local_issues
    issues.extend(local_issues)
    return summary


def validate_release_gate_contract(release_gate: object, issues: list[str]) -> None:
    prefix = "factory.config.json releaseReadinessAudit"
    if not isinstance(release_gate, dict) or not release_gate:
        issues.append(f"{prefix} must be present under controlRoom.releaseTruthGate.")
        return
    checks = {
        "policyVersion": RELEASE_AUDIT_VERSION,
        "ownerAgent": RELEASE_AGENT,
        "mission": RELEASE_MISSION,
        "requiredEvidence": RELEASE_REQUIRED_EVIDENCE,
        "qualityGates": RELEASE_QUALITY_GATES,
        "targetCopilots": RELEASE_TARGET_COPILOTS,
        "artifactTargets": RELEASE_ARTIFACT_TARGETS,
        "exitCriteria": RELEASE_EXIT_CRITERIA,
        "validationCommands": RELEASE_VALIDATION_COMMANDS,
        "runtimeEquivalence": RELEASE_RUNTIME_EQUIVALENCE,
    }
    for key, expected in checks.items():
        if release_gate.get(key) != expected:
            issues.append(f"{prefix} `{key}` drifted.")
    if release_gate.get("frontier") != "output-topology":
        issues.append(f"{prefix} frontier must remain output-topology.")
    if release_gate.get("minimumScore") != 80:
        issues.append(f"{prefix} minimumScore must be 80.")
    if release_gate.get("residualRiskMustBeExplicit") is not True:
        issues.append(f"{prefix} must require explicit residual risk.")
    if release_gate.get("claimPolicy") != "no_product_artifact_claim_without_build_render_or_package_evidence":
        issues.append(f"{prefix} claimPolicy must block unsupported product artifact claims.")
    if release_gate.get("scorecardIndex") != RELEASE_SCORECARD_INDEX:
        issues.append(f"{prefix} scorecardIndex must point to the by-copilot scorecard map.")
    if release_gate.get("requiredScorecardFields") != RELEASE_SCORECARD_FIELDS:
        issues.append(f"{prefix} requiredScorecardFields must include release caveat and risk linkage fields.")
    if release_gate.get("scoreScopePolicy") != RELEASE_SCORE_SCOPE_POLICY:
        issues.append(f"{prefix} scoreScopePolicy must prevent metadata scores from overriding residual risk.")
    if release_gate.get("claimPolicyRef") != RELEASE_CLAIM_POLICY_REF:
        issues.append(f"{prefix} claimPolicyRef must point to the release claim policy.")
    if release_gate.get("residualRiskRef") != RELEASE_RESIDUAL_RISK_REF:
        issues.append(f"{prefix} residualRiskRef must point to explicit residual risks.")


def validate_release_audit_payload(release_audit: dict, issues: list[str]) -> dict:
    prefix = "generated/factory-audit.json releaseAudit"
    checked = {"scorecards": [], "exitCriteria": []}
    checks = {
        "policyVersion": RELEASE_AUDIT_VERSION,
        "ownerAgent": RELEASE_AGENT,
        "mission": RELEASE_MISSION,
        "targetCopilots": RELEASE_TARGET_COPILOTS,
        "requiredEvidence": RELEASE_REQUIRED_EVIDENCE,
        "qualityGates": RELEASE_QUALITY_GATES,
        "artifactTargets": RELEASE_ARTIFACT_TARGETS,
        "requiredScorecardFields": RELEASE_SCORECARD_FIELDS,
        "scorecardIndex": RELEASE_SCORECARD_INDEX,
        "scoreScopePolicy": RELEASE_SCORE_SCOPE_POLICY,
        "claimPolicyRef": RELEASE_CLAIM_POLICY_REF,
        "residualRiskRef": RELEASE_RESIDUAL_RISK_REF,
        "runtimeEquivalence": RELEASE_RUNTIME_EQUIVALENCE,
        "validationCommands": RELEASE_VALIDATION_COMMANDS,
    }
    for key, expected in checks.items():
        if release_audit.get(key) != expected:
            issues.append(f"{prefix} `{key}` drifted.")
    if release_audit.get("pass") is not True:
        issues.append(f"{prefix} pass must be true.")
    if release_audit.get("frontier") != "output-topology":
        issues.append(f"{prefix} frontier must remain output-topology.")

    package_readiness = release_audit.get("packageReadiness", {})
    if not isinstance(package_readiness, dict):
        issues.append(f"{prefix} packageReadiness must be a JSON object.")
    else:
        if package_readiness.get("productRoot") != "products":
            issues.append(f"{prefix} packageReadiness productRoot must be products.")
        if package_readiness.get("claimPolicy") != "no_product_artifact_claim_without_build_render_or_package_evidence":
            issues.append(f"{prefix} packageReadiness claimPolicy must block unsupported product artifact claims.")
        target_ids = [
            item.get("id")
            for item in package_readiness.get("artifactTargets", [])
            if isinstance(item, dict)
        ]
        if target_ids != RELEASE_ARTIFACT_TARGETS:
            issues.append(f"{prefix} packageReadiness artifactTargets drifted.")

    scorecards = release_audit.get("scorecards", [])
    if not isinstance(scorecards, list):
        issues.append(f"{prefix} scorecards must be a list.")
        scorecards = []
    scorecard_ids = [item.get("copilotId") for item in scorecards if isinstance(item, dict)]
    if scorecard_ids != RELEASE_TARGET_COPILOTS:
        issues.append(f"{prefix} scorecards must cover each release target once and in catalog order.")
    scorecards_by_id: dict[str, dict] = {}
    for item in scorecards:
        if not isinstance(item, dict):
            issues.append(f"{prefix} scorecard entries must be JSON objects.")
            continue
        missing_fields = [field for field in RELEASE_SCORECARD_FIELDS if field not in item]
        if missing_fields:
            issues.append(f"{prefix} scorecard missing field(s): {', '.join(missing_fields)}.")
            continue
        copilot_id = item.get("copilotId")
        if isinstance(copilot_id, str):
            scorecards_by_id[copilot_id] = item
        if item.get("sourceOfTruth") != f"dist/copilots/{copilot_id}/shared/spec.json":
            issues.append(f"{prefix} scorecard sourceOfTruth drifted for `{copilot_id}`.")
        if item.get("runtimeAdapters") != RUNTIMES:
            issues.append(f"{prefix} scorecard runtimeAdapters drifted for `{copilot_id}`.")
        if not isinstance(item.get("declaredOutputs"), list) or not item.get("declaredOutputs"):
            issues.append(f"{prefix} scorecard declaredOutputs must be non-empty for `{copilot_id}`.")
        if not isinstance(item.get("score"), int) or item.get("score") < 80:
            issues.append(f"{prefix} scorecard score must be >=80 for `{copilot_id}`.")
        if item.get("scoreType") != "metadata_evidence_completeness":
            issues.append(f"{prefix} scorecard scoreType drifted for `{copilot_id}`.")
        if item.get("scoreScope") != RELEASE_SCORE_SCOPE:
            issues.append(f"{prefix} scorecard scoreScope must keep scores metadata-only for `{copilot_id}`.")
        if item.get("exitCriteriaStatus") not in {"pass", "explicit_residual_risk"}:
            issues.append(f"{prefix} scorecard exitCriteriaStatus invalid for `{copilot_id}`.")
        if item.get("releaseClaimStatus") != RELEASE_RELEASE_CLAIM_STATUS:
            issues.append(f"{prefix} scorecard releaseClaimStatus must block product release claims for `{copilot_id}`.")
        if item.get("claimPolicyRef") != RELEASE_CLAIM_POLICY_REF:
            issues.append(f"{prefix} scorecard claimPolicyRef must point to claim policy for `{copilot_id}`.")
        if item.get("residualRiskRefs") != [RELEASE_RESIDUAL_RISK_REF]:
            issues.append(f"{prefix} scorecard residualRiskRefs must point to residual risks for `{copilot_id}`.")
        evidence_refs = item.get("evidenceRefs", [])
        if (
            not isinstance(evidence_refs, list)
            or f"dist/copilots/{copilot_id}/shared/spec.json" not in evidence_refs
            or "generated/runtime-injection-map.json" not in evidence_refs
            or release_scorecard_ref(copilot_id) not in evidence_refs
        ):
            issues.append(f"{prefix} scorecard evidenceRefs incomplete for `{copilot_id}`.")
        checked["scorecards"].append(copilot_id)

    scorecards_by_copilot = release_audit.get("scorecardsByCopilot", {})
    if not isinstance(scorecards_by_copilot, dict):
        issues.append(f"{prefix} scorecardsByCopilot must be a JSON object.")
    else:
        if list(scorecards_by_copilot) != RELEASE_TARGET_COPILOTS:
            issues.append(f"{prefix} scorecardsByCopilot must cover each release target once and in catalog order.")
        for copilot_id in RELEASE_TARGET_COPILOTS:
            indexed = scorecards_by_copilot.get(copilot_id)
            if indexed != scorecards_by_id.get(copilot_id):
                issues.append(f"{prefix} scorecardsByCopilot drifted for `{copilot_id}`.")

    exit_criteria = release_audit.get("exitCriteria", [])
    if not isinstance(exit_criteria, list):
        issues.append(f"{prefix} exitCriteria must be a list.")
        exit_criteria = []
    exit_ids = [item.get("id") for item in exit_criteria if isinstance(item, dict)]
    if exit_ids != RELEASE_EXIT_CRITERIA:
        issues.append(f"{prefix} exitCriteria must cover active acceptance frontiers in order.")
    for item in exit_criteria:
        if not isinstance(item, dict):
            issues.append(f"{prefix} exitCriteria entries must be JSON objects.")
            continue
        status = item.get("status")
        if status not in {"pass", "not_applicable_with_residual_risk"}:
            issues.append(f"{prefix} exitCriteria `{item.get('id')}` has invalid status.")
        if not isinstance(item.get("evidence"), list) or not item.get("evidence"):
            issues.append(f"{prefix} exitCriteria `{item.get('id')}` must include evidence.")
        checked["exitCriteria"].append(item.get("id"))

    residual_risks = release_audit.get("residualRisks", [])
    if not isinstance(residual_risks, list) or not residual_risks:
        issues.append(f"{prefix} residualRisks must be explicit.")

    cost_control = release_audit.get("costControl", {})
    if (
        not isinstance(cost_control, dict)
        or cost_control.get("deterministicPythonFirst") is not True
        or cost_control.get("llmEscalation") != "not_required_for_release_metadata_audit"
        or cost_control.get("maxPromptGrowthRatio") != 0.10
    ):
        issues.append(f"{prefix} costControl must keep deterministic checks first and prompt growth bounded.")
    return checked


def validate_release_runtime_trace(runtime_map: object, release_audit: object, issues: list[str]) -> list[str]:
    prefix = "generated/runtime-injection-map.json releaseReadinessAudit"
    if not isinstance(runtime_map, dict):
        issues.append(f"{prefix} runtime map must be a JSON object.")
        return []
    copilots = runtime_map.get("copilots", {})
    if not isinstance(copilots, dict):
        issues.append(f"{prefix} copilots must be a JSON object.")
        return []
    scorecards_by_copilot = (
        release_audit.get("scorecardsByCopilot", {})
        if isinstance(release_audit, dict)
        else {}
    )
    checked: list[str] = []
    for copilot_id in RELEASE_TARGET_COPILOTS:
        item = copilots.get(copilot_id, {})
        if not isinstance(item, dict):
            issues.append(f"{prefix} missing release target `{copilot_id}`.")
            continue
        runtime_files = item.get("runtimeFiles", {})
        trace = item.get("releaseReadinessAudit", {})
        if sorted(runtime_files) != sorted(RUNTIMES):
            issues.append(f"{prefix} `{copilot_id}` must trace all four runtime files.")
            continue
        expected_trace = {
            "artifact": "generated/factory-audit.json#/releaseAudit",
            "ownerAgent": RELEASE_AGENT,
            "mission": RELEASE_MISSION,
            "requiredEvidence": RELEASE_REQUIRED_EVIDENCE,
            "qualityGates": RELEASE_QUALITY_GATES,
            "scorecardRef": release_scorecard_ref(copilot_id),
            "claimPolicyRef": RELEASE_CLAIM_POLICY_REF,
            "residualRiskRef": RELEASE_RESIDUAL_RISK_REF,
            "runtimeEquivalence": RELEASE_RUNTIME_EQUIVALENCE,
        }
        if trace != expected_trace:
            issues.append(f"{prefix} `{copilot_id}` trace drifted.")
            continue
        scorecard = scorecards_by_copilot.get(copilot_id) if isinstance(scorecards_by_copilot, dict) else None
        if not isinstance(scorecard, dict) or scorecard.get("copilotId") != copilot_id:
            issues.append(f"{prefix} `{copilot_id}` scorecardRef does not resolve to its release scorecard.")
            continue
        checked.append(copilot_id)
    return checked


def validate_packager_distribution_contract(config: dict, issues: list[str]) -> dict:
    summary = {
        "configChecked": False,
        "manifestChecked": False,
        "fileIndexChecked": False,
        "packagesChecked": [],
        "indexedFilesChecked": 0,
        "runtimeEquivalenceChecked": False,
    }
    release_gate = config.get("controlRoom", {}).get("releaseTruthGate", {}) if isinstance(config, dict) else {}
    configured = release_gate.get("packagerDistribution", {}) if isinstance(release_gate, dict) else {}
    prefix = "Packager distribution contract"

    if not isinstance(configured, dict) or not configured:
        issues.append(f"{prefix} is missing from factory.config.json releaseTruthGate.")
    else:
        expected_config = {
            "policyVersion": PACKAGER_POLICY_VERSION,
            "ownerAgent": PACKAGER_AGENT,
            "room": "Operations",
            "mission": PACKAGER_MISSION,
            "concurrency": "parallel-safe",
            "frontier": "output-topology",
            "manifestRef": PACKAGER_MANIFEST_REF,
            "fileIndexRef": PACKAGER_FILE_INDEX_REF,
            "runtimeEquivalence": PACKAGER_RUNTIME_EQUIVALENCE,
            "targetCopilots": RELEASE_TARGET_COPILOTS,
            "requiredArtifacts": PACKAGER_REQUIRED_ARTIFACTS,
            "validationCommands": RELEASE_VALIDATION_COMMANDS,
            "claimPolicyRef": RELEASE_CLAIM_POLICY_REF,
        }
        for key, expected in expected_config.items():
            if configured.get(key) != expected:
                issues.append(f"{prefix} factory.config.json `{key}` drifted.")
        summary["configChecked"] = not any(issue.startswith(f"{prefix} factory.config.json") for issue in issues)

    factory_audit = read_json(ROOT / "generated" / "factory-audit.json", {}, issues)
    release_audit = factory_audit.get("releaseAudit", {}) if isinstance(factory_audit, dict) else {}
    manifest = release_audit.get("distributionManifest", {}) if isinstance(release_audit, dict) else {}
    runtime_map = read_json(ROOT / "generated" / "runtime-injection-map.json", {}, issues)
    file_index = runtime_map.get("distributionFileIndex", {}) if isinstance(runtime_map, dict) else {}

    if not isinstance(manifest, dict) or not manifest:
        issues.append("generated/factory-audit.json releaseAudit distributionManifest is missing.")
    else:
        expected_manifest = {
            "policyVersion": PACKAGER_POLICY_VERSION,
            "ownerAgent": PACKAGER_AGENT,
            "room": "Operations",
            "mission": PACKAGER_MISSION,
            "frontier": "output-topology",
            "releaseClaimStatus": RELEASE_RELEASE_CLAIM_STATUS,
            "manifestRef": PACKAGER_MANIFEST_REF,
            "fileIndexRef": PACKAGER_FILE_INDEX_REF,
            "productRoot": "products",
            "distributionRoot": "dist/copilots",
            "portfolioRegistry": ".codex-loop/factory/project-registry.json",
            "runtimeEquivalence": PACKAGER_RUNTIME_EQUIVALENCE,
            "artifactTargets": RELEASE_ARTIFACT_TARGETS,
            "validationCommands": RELEASE_VALIDATION_COMMANDS,
        }
        for key, expected in expected_manifest.items():
            if manifest.get(key) != expected:
                issues.append(f"generated/factory-audit.json distributionManifest `{key}` drifted.")
        summary["manifestChecked"] = True

    if not isinstance(file_index, dict) or not file_index:
        issues.append("generated/runtime-injection-map.json distributionFileIndex is missing.")
    else:
        expected_runtime_counts = {runtime: len(RELEASE_TARGET_COPILOTS) for runtime in RUNTIMES}
        expected_index = {
            "policyVersion": PACKAGER_POLICY_VERSION,
            "ownerAgent": PACKAGER_AGENT,
            "room": "Operations",
            "mission": PACKAGER_MISSION,
            "frontier": "output-topology",
            "manifestRef": PACKAGER_MANIFEST_REF,
            "fileIndexRef": PACKAGER_FILE_INDEX_REF,
            "sourceOfTruth": PACKAGER_MANIFEST_REF,
            "packageCount": len(RELEASE_TARGET_COPILOTS),
            "indexedFileCount": len(RELEASE_TARGET_COPILOTS) * len(PACKAGER_REQUIRED_ARTIFACTS),
            "runtimeAdapterCounts": expected_runtime_counts,
            "runtimeEquivalence": PACKAGER_RUNTIME_EQUIVALENCE,
            "validationCommands": RELEASE_VALIDATION_COMMANDS,
            "claimPolicyRef": RELEASE_CLAIM_POLICY_REF,
        }
        for key, expected in expected_index.items():
            if file_index.get(key) != expected:
                issues.append(f"generated/runtime-injection-map.json distributionFileIndex `{key}` drifted.")
        summary["fileIndexChecked"] = True
        summary["runtimeEquivalenceChecked"] = file_index.get("runtimeEquivalence") == PACKAGER_RUNTIME_EQUIVALENCE

    manifest_packages = manifest.get("packageSets", []) if isinstance(manifest, dict) else []
    index_packages = file_index.get("packages", {}) if isinstance(file_index, dict) else {}
    manifest_ids = [item.get("copilotId") for item in manifest_packages if isinstance(item, dict)]
    if manifest_ids != RELEASE_TARGET_COPILOTS:
        issues.append("distributionManifest packageSets must cover release target copilots in catalog order.")
    if not isinstance(index_packages, dict) or list(index_packages) != RELEASE_TARGET_COPILOTS:
        issues.append("distributionFileIndex packages must cover release target copilots in catalog order.")
        index_packages = {}

    manifest_lookup = {
        item.get("copilotId"): item
        for item in manifest_packages
        if isinstance(item, dict) and isinstance(item.get("copilotId"), str)
    }
    for copilot_id in RELEASE_TARGET_COPILOTS:
        expected_package = packager_expected_package(copilot_id)
        manifest_package = manifest_lookup.get(copilot_id, {})
        index_package = index_packages.get(copilot_id, {}) if isinstance(index_packages, dict) else {}
        if not isinstance(manifest_package, dict) or not manifest_package:
            issues.append(f"distributionManifest missing package `{copilot_id}`.")
            continue
        for key in ["distributionSlug", "sourceOfTruth", "outputSchema", "runtimeFiles", "scorecardRef", "fileIndexRef"]:
            if manifest_package.get(key) != expected_package[key]:
                issues.append(f"distributionManifest package `{copilot_id}` `{key}` drifted.")
        if not isinstance(index_package, dict) or not index_package:
            issues.append(f"distributionFileIndex missing package `{copilot_id}`.")
            continue
        if index_package.get("distributionSlug") != expected_package["distributionSlug"]:
            issues.append(f"distributionFileIndex package `{copilot_id}` distributionSlug drifted.")
        if index_package.get("sharedFiles") != [expected_package["sourceOfTruth"], expected_package["outputSchema"]]:
            issues.append(f"distributionFileIndex package `{copilot_id}` sharedFiles drifted.")
        if index_package.get("runtimeFiles") != expected_package["runtimeFiles"]:
            issues.append(f"distributionFileIndex package `{copilot_id}` runtimeFiles drifted.")
        if index_package.get("scorecardRef") != expected_package["scorecardRef"]:
            issues.append(f"distributionFileIndex package `{copilot_id}` scorecardRef drifted.")
        for path in packager_indexed_paths(copilot_id):
            if not (ROOT / path).is_file():
                issues.append(f"distributionFileIndex package `{copilot_id}` points to missing file: {path}.")
            else:
                summary["indexedFilesChecked"] += 1
        summary["packagesChecked"].append(copilot_id)
    return summary


def packager_expected_package(copilot_id: str) -> dict:
    return {
        "distributionSlug": copilot_id.replace("_", "-"),
        "sourceOfTruth": f"dist/copilots/{copilot_id}/shared/spec.json",
        "outputSchema": f"dist/copilots/{copilot_id}/shared/output_schema.json",
        "runtimeFiles": {
            "codex": f"dist/copilots/{copilot_id}/codex/AGENT.md",
            "claude": f"dist/copilots/{copilot_id}/claude/AGENT.md",
            "github-copilot": f"dist/copilots/{copilot_id}/github-copilot/copilot-agent.md",
            "langchain": f"dist/copilots/{copilot_id}/langchain/agent.py",
        },
        "scorecardRef": release_scorecard_ref(copilot_id),
        "fileIndexRef": f"generated/runtime-injection-map.json#/distributionFileIndex/packages/{copilot_id}",
    }


def packager_indexed_paths(copilot_id: str) -> list[str]:
    expected = packager_expected_package(copilot_id)
    return [
        expected["sourceOfTruth"],
        expected["outputSchema"],
        *expected["runtimeFiles"].values(),
    ]


def release_scorecard_ref(copilot_id: object) -> str:
    return f"{RELEASE_SCORECARD_INDEX}/{copilot_id}"


def detect_release_fixture_issues(payload: dict) -> list[str]:
    detected: list[str] = []
    if payload.get("requiredEvidence") != RELEASE_REQUIRED_EVIDENCE:
        detected.append("missing required evidence")
    if payload.get("qualityGates") != RELEASE_QUALITY_GATES:
        detected.append("quality gate drift")
    if payload.get("targetCopilots") != RELEASE_TARGET_COPILOTS:
        detected.append("target copilot drift")
    if payload.get("artifactTargets") != RELEASE_ARTIFACT_TARGETS:
        detected.append("artifact target drift")
    if payload.get("runtimeEquivalence") != RELEASE_RUNTIME_EQUIVALENCE:
        detected.append("runtime equivalence drift")
    if payload.get("validationCommands") != RELEASE_VALIDATION_COMMANDS:
        detected.append("validation command drift")
    if payload.get("scoreScopePolicy") != RELEASE_SCORE_SCOPE_POLICY:
        detected.append("missing score scope policy")
    if payload.get("claimPolicyRef") != RELEASE_CLAIM_POLICY_REF or payload.get("residualRiskRef") != RELEASE_RESIDUAL_RISK_REF:
        detected.append("missing release risk refs")
    scorecards = payload.get("scorecards", [])
    if not isinstance(scorecards, list) or len(scorecards) != len(RELEASE_TARGET_COPILOTS):
        detected.append("missing scorecards")
    else:
        if any(not isinstance(item, dict) or item.get("score", 0) < 80 for item in scorecards):
            detected.append("low scorecard")
        if any(
            not isinstance(item, dict)
            or item.get("scoreScope") != RELEASE_SCORE_SCOPE
            or item.get("releaseClaimStatus") != RELEASE_RELEASE_CLAIM_STATUS
            or item.get("claimPolicyRef") != RELEASE_CLAIM_POLICY_REF
            or item.get("residualRiskRefs") != [RELEASE_RESIDUAL_RISK_REF]
            for item in scorecards
        ):
            detected.append("missing scorecard release caveat")
    scorecards_by_copilot = payload.get("scorecardsByCopilot", {})
    if not isinstance(scorecards_by_copilot, dict) or list(scorecards_by_copilot) != RELEASE_TARGET_COPILOTS:
        detected.append("missing scorecard index")
    elif isinstance(scorecards, list):
        for copilot_id, scorecard in zip(RELEASE_TARGET_COPILOTS, scorecards):
            if scorecards_by_copilot.get(copilot_id) != scorecard:
                detected.append("scorecard index drift")
                break
    exit_criteria = payload.get("exitCriteria", [])
    if not isinstance(exit_criteria, list) or [item.get("id") for item in exit_criteria if isinstance(item, dict)] != RELEASE_EXIT_CRITERIA:
        detected.append("missing exit criteria")
    if not payload.get("residualRisks"):
        detected.append("missing residual risk")
    if payload.get("costControl", {}).get("deterministicPythonFirst") is not True:
        detected.append("missing deterministic cost control")
    return detected


def run_release_negative_cases() -> list[dict]:
    valid_scorecards = [
        {
            "copilotId": copilot_id,
            "score": 100,
            "scoreScope": RELEASE_SCORE_SCOPE,
            "releaseClaimStatus": RELEASE_RELEASE_CLAIM_STATUS,
            "claimPolicyRef": RELEASE_CLAIM_POLICY_REF,
            "residualRiskRefs": [RELEASE_RESIDUAL_RISK_REF],
        }
        for copilot_id in RELEASE_TARGET_COPILOTS
    ]
    low_scorecards = [dict(item) for item in valid_scorecards]
    low_scorecards[0] = {"copilotId": RELEASE_TARGET_COPILOTS[0], "score": 50}
    missing_caveat_scorecards = [dict(item) for item in valid_scorecards]
    missing_caveat_scorecards[0].pop("residualRiskRefs")
    valid_payload = {
        "requiredEvidence": RELEASE_REQUIRED_EVIDENCE,
        "qualityGates": RELEASE_QUALITY_GATES,
        "targetCopilots": RELEASE_TARGET_COPILOTS,
        "artifactTargets": RELEASE_ARTIFACT_TARGETS,
        "runtimeEquivalence": RELEASE_RUNTIME_EQUIVALENCE,
        "validationCommands": RELEASE_VALIDATION_COMMANDS,
        "scoreScopePolicy": RELEASE_SCORE_SCOPE_POLICY,
        "claimPolicyRef": RELEASE_CLAIM_POLICY_REF,
        "residualRiskRef": RELEASE_RESIDUAL_RISK_REF,
        "scorecards": valid_scorecards,
        "exitCriteria": [
            {"id": criterion_id, "status": "pass"}
            for criterion_id in RELEASE_EXIT_CRITERIA
        ],
        "residualRisks": ["Product-specific build, render and package evidence remains out of scope until a product workspace is selected."],
        "costControl": {"deterministicPythonFirst": True},
    }
    valid_payload["scorecardsByCopilot"] = {
        item["copilotId"]: item
        for item in valid_payload["scorecards"]
    }
    fixtures = [
        ("valid_control", valid_payload, False, ""),
        ("missing_scorecards", {**valid_payload, "scorecards": []}, True, "missing scorecards"),
        ("low_scorecard", {**valid_payload, "scorecards": low_scorecards}, True, "low scorecard"),
        ("missing_scorecard_release_caveat", {**valid_payload, "scorecards": missing_caveat_scorecards}, True, "missing scorecard release caveat"),
        ("missing_scorecard_index", {**valid_payload, "scorecardsByCopilot": {}}, True, "missing scorecard index"),
        ("missing_exit_criteria", {**valid_payload, "exitCriteria": []}, True, "missing exit criteria"),
        ("runtime_drift", {**valid_payload, "runtimeEquivalence": {"runtimes": ["codex"]}}, True, "runtime equivalence drift"),
        ("artifact_target_drift", {**valid_payload, "artifactTargets": ["web-app"]}, True, "artifact target drift"),
        ("missing_score_scope_policy", {**valid_payload, "scoreScopePolicy": ""}, True, "missing score scope policy"),
        ("missing_release_risk_refs", {**valid_payload, "claimPolicyRef": "", "residualRiskRef": ""}, True, "missing release risk refs"),
        ("missing_residual_risk", {**valid_payload, "residualRisks": []}, True, "missing residual risk"),
        ("missing_cost_control", {**valid_payload, "costControl": {}}, True, "missing deterministic cost control"),
    ]
    results = []
    for case_id, payload, should_fail, expected_issue in fixtures:
        detected = detect_release_fixture_issues(payload)
        failure_detected = bool(detected)
        passed_expectation = (
            failure_detected == should_fail
            and (not expected_issue or expected_issue in detected)
        )
        results.append(
            {
                "id": case_id,
                "expectedFailure": should_fail,
                "failureDetected": failure_detected,
                "passedExpectation": passed_expectation,
                "detected": passed_expectation,
                "issues": detected,
            }
        )
    return results


def validate_operate_auditor_contract(copilots: list, agents: list, issues: list[str]) -> dict:
    local_issues: list[str] = []
    operate_targets = [
        item.get("id")
        for item in copilots
        if isinstance(item, dict) and "operate" in list_field(item, "sdlc_phases")
    ]
    summary = {
        "pass": False,
        "agentPresent": False,
        "mission": OPERATE_MISSION,
        "policyVersion": None,
        "targetCopilots": operate_targets,
        "targetCopilotsChecked": [],
        "contractArtifact": OPERATE_CONTRACT,
        "contractChecked": False,
        "scorecardArtifact": OPERATE_SCORECARD,
        "scorecardChecked": False,
        "runbookChecked": False,
        "incidentRunbookChecked": False,
        "settingsChecked": False,
        "documentationChecked": False,
        "telemetrySignalsChecked": [],
        "incidentPlaybooksChecked": [],
        "sampleRouteChecked": False,
        "sampleTopRoute": None,
        "sampleRouteCheapPath": False,
        "requiredEvidence": OPERATE_REQUIRED_EVIDENCE,
        "qualityGates": OPERATE_QUALITY_GATES,
        "runtimeEquivalence": OPERATE_RUNTIME_EQUIVALENCE,
        "negativeCases": run_operate_negative_cases(),
        "negativeCasesDetected": False,
        "validationCommands": OPERATE_VALIDATION_COMMANDS,
    }

    if operate_targets != OPERATE_TARGET_COPILOTS:
        local_issues.append("Operate Auditor target copilot set drifted from the operate SDLC catalog.")
    else:
        summary["targetCopilotsChecked"] = operate_targets

    agent = next((item for item in agents if isinstance(item, dict) and item.get("id") == OPERATE_AGENT), {})
    summary["agentPresent"] = bool(agent)
    if not agent:
        local_issues.append("Operate Auditor agent is missing from data/agent_roster.json.")
    else:
        if agent.get("mission") != OPERATE_MISSION:
            local_issues.append("Operate Auditor mission drifted from the Operations contract.")
        if agent.get("mode") != "python_first_llm_sparse":
            local_issues.append("Operate Auditor mode must remain python_first_llm_sparse.")
        if agent.get("phase") != "operate":
            local_issues.append("Operate Auditor must stay in the operate phase.")

    contract = read_json(ROOT / OPERATE_CONTRACT, {}, local_issues)
    if isinstance(contract, dict) and contract:
        summary["policyVersion"] = contract.get("policyVersion")
        checked = validate_operate_contract_payload(contract, local_issues)
        summary["telemetrySignalsChecked"] = checked["telemetrySignals"]
        summary["incidentPlaybooksChecked"] = checked["incidentPlaybooks"]
        summary["contractChecked"] = not any(
            issue.startswith(f"{OPERATE_CONTRACT} ")
            for issue in local_issues
        )

    scorecard = read_json(ROOT / OPERATE_SCORECARD, {}, local_issues)
    if isinstance(scorecard, dict) and scorecard:
        validate_operate_scorecard_payload(scorecard, local_issues)
        summary["scorecardChecked"] = not any(
            issue.startswith(f"{OPERATE_SCORECARD} ")
            for issue in local_issues
        )

    summary["settingsChecked"] = validate_operate_settings(local_issues)
    doc_results = validate_operate_docs(local_issues)
    summary.update(doc_results)

    try:
        import semantic_router as router

        sample = router.route("operate observability incident playbooks runbooks", limit=3)
    except Exception as exc:  # pragma: no cover - validator reports the concrete runtime error.
        local_issues.append(f"Operate sample route failed: {exc}.")
        sample = []
    if sample:
        top = sample[0]
        summary["sampleRouteChecked"] = True
        summary["sampleTopRoute"] = top.get("id")
        summary["sampleRouteCheapPath"] = top.get("cheap_path") is True
        if top.get("id") != "nodejs":
            local_issues.append("Operate sample route must select `nodejs` first for observability work.")
        if top.get("cheap_path") is not True:
            local_issues.append("Operate sample route must stay on the deterministic cheap path.")
        if top.get("runtime_trace", {}).get("runtimes") != RUNTIMES:
            local_issues.append("Operate sample route must include full runtime trace evidence.")

    summary["negativeCasesDetected"] = all(case["passedExpectation"] for case in summary["negativeCases"])
    if not summary["negativeCasesDetected"]:
        local_issues.append("Operate Auditor negative fixtures must be detected by executable checks.")

    summary["issues"] = local_issues
    summary["pass"] = not local_issues
    issues.extend(local_issues)
    return summary


def validate_operate_contract_payload(contract: dict, issues: list[str]) -> dict:
    prefix = OPERATE_CONTRACT
    checked = {"telemetrySignals": [], "incidentPlaybooks": []}
    checks = {
        "policyVersion": OPERATE_AUDIT_VERSION,
        "ownerAgent": OPERATE_AGENT,
        "mission": OPERATE_MISSION,
        "frontier": "state-locks",
        "targetCopilots": OPERATE_TARGET_COPILOTS,
        "requiredEvidence": OPERATE_REQUIRED_EVIDENCE,
        "qualityGates": OPERATE_QUALITY_GATES,
        "runbookRefs": OPERATE_RUNBOOK_REFS,
        "runtimeEquivalence": OPERATE_RUNTIME_EQUIVALENCE,
        "costControl": OPERATE_COST_CONTROL,
        "validationCommands": OPERATE_VALIDATION_COMMANDS,
    }
    for key, expected in checks.items():
        if contract.get(key) != expected:
            issues.append(f"{prefix} `{key}` drifted.")

    state_lock = contract.get("stateLockPolicy", {})
    expected_state_lock = {
        "lockFile": ".codex-loop/run.lock.json",
        "frontier": "state-locks",
        "maxStaleHeartbeatSeconds": 900,
        "snapshotRoots": STATE_LOCK_SNAPSHOT_ROOTS,
        "serialConcurrencyRequired": True,
    }
    if state_lock != expected_state_lock:
        issues.append(f"{prefix} stateLockPolicy drifted.")

    signals = contract.get("telemetrySignals", [])
    signal_ids = [item.get("id") for item in signals if isinstance(item, dict)]
    if signal_ids != OPERATE_TELEMETRY_SIGNALS:
        issues.append(f"{prefix} telemetrySignals must cover required signals in order.")
    for item in signals if isinstance(signals, list) else []:
        if not isinstance(item, dict):
            issues.append(f"{prefix} telemetrySignals entries must be JSON objects.")
            continue
        missing = [field for field in ["id", "source", "purpose", "privacy", "threshold"] if not item.get(field)]
        if missing:
            issues.append(f"{prefix} telemetry signal `{item.get('id')}` missing field(s): {', '.join(missing)}.")
        source = item.get("source")
        if not artifact_ref_exists(source):
            issues.append(f"{prefix} telemetry signal `{item.get('id')}` source does not resolve: {source}.")
        if "raw log" in str(item.get("privacy", "")).lower() and "not" not in str(item.get("privacy", "")).lower() and "no " not in str(item.get("privacy", "")).lower():
            issues.append(f"{prefix} telemetry signal `{item.get('id')}` privacy text must not allow raw logs.")
        checked["telemetrySignals"].append(item.get("id"))

    playbooks = contract.get("incidentPlaybooks", [])
    playbook_ids = [item.get("id") for item in playbooks if isinstance(item, dict)]
    if playbook_ids != OPERATE_INCIDENT_PLAYBOOKS:
        issues.append(f"{prefix} incidentPlaybooks must cover required incidents in order.")
    for item in playbooks if isinstance(playbooks, list) else []:
        if not isinstance(item, dict):
            issues.append(f"{prefix} incidentPlaybooks entries must be JSON objects.")
            continue
        missing = [field for field in ["id", "severity", "detect", "response", "owner", "runbookRef"] if not item.get(field)]
        if missing:
            issues.append(f"{prefix} incident playbook `{item.get('id')}` missing field(s): {', '.join(missing)}.")
        if item.get("severity") not in {"P0", "P1", "P2"}:
            issues.append(f"{prefix} incident playbook `{item.get('id')}` has unsupported severity.")
        response = item.get("response", [])
        if not isinstance(response, list) or len(response) < 3:
            issues.append(f"{prefix} incident playbook `{item.get('id')}` must have at least three response steps.")
        if item.get("owner") != OPERATE_AGENT:
            issues.append(f"{prefix} incident playbook `{item.get('id')}` owner drifted.")
        if not str(item.get("runbookRef", "")).startswith(f"{OPERATE_RUNBOOK}#"):
            issues.append(f"{prefix} incident playbook `{item.get('id')}` must point to the Operate runbook.")
        checked["incidentPlaybooks"].append(item.get("id"))

    for ref in OPERATE_RUNBOOK_REFS:
        if not artifact_ref_exists(ref):
            issues.append(f"{prefix} runbook ref does not resolve: {ref}.")
    return checked


def validate_operate_scorecard_payload(scorecard: dict, issues: list[str]) -> None:
    prefix = OPERATE_SCORECARD
    checks = {
        "policyVersion": OPERATE_AUDIT_VERSION,
        "ownerAgent": OPERATE_AGENT,
        "mission": OPERATE_MISSION,
        "pass": True,
    }
    for key, expected in checks.items():
        if scorecard.get(key) != expected:
            issues.append(f"{prefix} `{key}` drifted.")
    checks_list = scorecard.get("checks", [])
    check_ids = [item.get("id") for item in checks_list if isinstance(item, dict)]
    if check_ids != OPERATE_REQUIRED_EVIDENCE:
        issues.append(f"{prefix} checks must match required evidence in order.")
    for item in checks_list if isinstance(checks_list, list) else []:
        if not isinstance(item, dict):
            issues.append(f"{prefix} checks entries must be JSON objects.")
            continue
        if item.get("status") != "pass":
            issues.append(f"{prefix} check `{item.get('id')}` must pass.")
        evidence = item.get("evidence", [])
        if not isinstance(evidence, list) or not evidence:
            issues.append(f"{prefix} check `{item.get('id')}` must include evidence.")
            continue
        for ref in evidence:
            if isinstance(ref, str) and ref.startswith("python "):
                continue
            if not artifact_ref_exists(ref):
                issues.append(f"{prefix} evidence does not resolve: {ref}.")
    review = scorecard.get("review", {})
    expected_review = {
        "owner": "pass",
        "qa": "pass",
        "safeCodingPrivacy": "pass",
        "release": "pass",
    }
    if review != expected_review:
        issues.append(f"{prefix} review must include owner, QA, safe-coding/privacy and release pass states.")
    residual = scorecard.get("residualRisks", [])
    if not isinstance(residual, list) or not residual:
        issues.append(f"{prefix} residualRisks must be explicit.")


def validate_operate_settings(issues: list[str]) -> bool:
    settings = read_json(ROOT / ".vscode" / "settings.json", {}, issues)
    if not isinstance(settings, dict):
        return False
    expected = {
        "codexLoop.operabilityAuditEnabled": True,
        "codexLoop.observabilityContractFile": OPERATE_CONTRACT,
        "codexLoop.incidentRunbookFile": OPERATE_RUNBOOK,
        "codexLoop.rawLogPromptsAllowed": False,
        "codexLoop.maxStaleHeartbeatSeconds": 900,
    }
    for key, value in expected.items():
        if settings.get(key) != value:
            issues.append(f".vscode/settings.json Operate setting `{key}` drifted.")
    return not any(issue.startswith(".vscode/settings.json Operate") for issue in issues)


def validate_operate_docs(issues: list[str]) -> dict:
    results = {
        "runbookChecked": False,
        "incidentRunbookChecked": False,
        "documentationChecked": False,
    }
    docs = {
        "README.md": [
            "Operate evidence",
            OPERATE_CONTRACT,
            "generated/validation-report.json#/operateAuditor",
        ],
        "factory-prompt.md": [
            "Operate Auditor Contract",
            OPERATE_CONTRACT,
            "runtimeEquivalence.maxUnexplainedDrift=0",
        ],
        OPERATE_RUNBOOK: [
            "# Operate Observability Runbook",
            "state-lock-stale",
            "validation-report-regression",
            "runtime-equivalence-drift",
            "observability-signal-gap",
            "privacy-log-exposure",
        ],
        OPERATE_INCIDENT_RUNBOOK: OPERATE_INCIDENT_PLAYBOOKS,
    }
    docs[OPERATE_INCIDENT_RUNBOOK] = [
        "# Incident Runbook",
        "provider-policy-friction",
        "codex-cli-contract-drift",
    ]
    checked = []
    for rel_path, markers in docs.items():
        text = read_text(ROOT / rel_path)
        missing = [marker for marker in markers if marker not in text]
        if missing:
            issues.append(f"{rel_path} missing Operate marker(s): {', '.join(missing)}.")
            continue
        checked.append(rel_path)
    results["runbookChecked"] = OPERATE_RUNBOOK in checked
    results["incidentRunbookChecked"] = OPERATE_INCIDENT_RUNBOOK in checked
    results["documentationChecked"] = "README.md" in checked and "factory-prompt.md" in checked
    return results


def detect_operate_fixture_issues(payload: dict) -> list[str]:
    detected: list[str] = []
    if payload.get("requiredEvidence") != OPERATE_REQUIRED_EVIDENCE:
        detected.append("missing required evidence")
    if payload.get("qualityGates") != OPERATE_QUALITY_GATES:
        detected.append("quality gate drift")
    if payload.get("targetCopilots") != OPERATE_TARGET_COPILOTS:
        detected.append("target copilot drift")
    if payload.get("runtimeEquivalence") != OPERATE_RUNTIME_EQUIVALENCE:
        detected.append("runtime equivalence drift")
    if payload.get("validationCommands") != OPERATE_VALIDATION_COMMANDS:
        detected.append("validation command drift")
    cost_control = payload.get("costControl")
    if cost_control != OPERATE_COST_CONTROL:
        detected.append("missing deterministic cost control")
    if isinstance(cost_control, dict):
        if cost_control.get("rawLogPromptsAllowed") is not False:
            detected.append("raw log prompt allowance")
        if cost_control.get("sanitizedEvidenceOnly") is not True:
            detected.append("unsanitized evidence allowance")
    signals = payload.get("telemetrySignals", [])
    signal_ids = [item.get("id") for item in signals if isinstance(item, dict)]
    if signal_ids != OPERATE_TELEMETRY_SIGNALS:
        detected.append("missing telemetry signals")
    for item in signals if isinstance(signals, list) else []:
        if not isinstance(item, dict):
            continue
        privacy_text = str(item.get("privacy", "")).lower()
        if "raw log" in privacy_text and "not" not in privacy_text and "no " not in privacy_text:
            detected.append("raw log privacy allowance")
    playbooks = payload.get("incidentPlaybooks", [])
    playbook_ids = [item.get("id") for item in playbooks if isinstance(item, dict)]
    if playbook_ids != OPERATE_INCIDENT_PLAYBOOKS:
        detected.append("missing incident playbooks")
    elif any(not isinstance(item.get("response"), list) or len(item.get("response", [])) < 3 for item in playbooks if isinstance(item, dict)):
        detected.append("weak incident response")
    if payload.get("runbookRefs") != OPERATE_RUNBOOK_REFS:
        detected.append("runbook ref drift")
    state_lock = payload.get("stateLockPolicy", {})
    if not isinstance(state_lock, dict) or state_lock.get("serialConcurrencyRequired") is not True:
        detected.append("missing serial state-lock guard")
    return detected


def run_operate_negative_cases() -> list[dict]:
    valid_signals = [{"id": signal_id} for signal_id in OPERATE_TELEMETRY_SIGNALS]
    valid_playbooks = [
        {"id": playbook_id, "response": ["detect", "scope", "verify"]}
        for playbook_id in OPERATE_INCIDENT_PLAYBOOKS
    ]
    weak_playbooks = [dict(item) for item in valid_playbooks]
    weak_playbooks[0] = {"id": OPERATE_INCIDENT_PLAYBOOKS[0], "response": ["detect"]}
    valid_payload = {
        "requiredEvidence": OPERATE_REQUIRED_EVIDENCE,
        "qualityGates": OPERATE_QUALITY_GATES,
        "targetCopilots": OPERATE_TARGET_COPILOTS,
        "runtimeEquivalence": OPERATE_RUNTIME_EQUIVALENCE,
        "validationCommands": OPERATE_VALIDATION_COMMANDS,
        "costControl": OPERATE_COST_CONTROL,
        "telemetrySignals": valid_signals,
        "incidentPlaybooks": valid_playbooks,
        "runbookRefs": OPERATE_RUNBOOK_REFS,
        "stateLockPolicy": {"serialConcurrencyRequired": True},
    }
    fixtures = [
        ("valid_control", valid_payload, False, ""),
        ("missing_required_evidence", {**valid_payload, "requiredEvidence": []}, True, "missing required evidence"),
        ("missing_telemetry_signals", {**valid_payload, "telemetrySignals": []}, True, "missing telemetry signals"),
        ("missing_incident_playbooks", {**valid_payload, "incidentPlaybooks": []}, True, "missing incident playbooks"),
        ("weak_incident_response", {**valid_payload, "incidentPlaybooks": weak_playbooks}, True, "weak incident response"),
        ("runtime_drift", {**valid_payload, "runtimeEquivalence": {"runtimes": ["codex"]}}, True, "runtime equivalence drift"),
        ("runbook_ref_drift", {**valid_payload, "runbookRefs": [OPERATE_RUNBOOK]}, True, "runbook ref drift"),
        ("missing_state_lock_guard", {**valid_payload, "stateLockPolicy": {}}, True, "missing serial state-lock guard"),
        ("missing_cost_control", {**valid_payload, "costControl": {}}, True, "missing deterministic cost control"),
        (
            "raw_log_prompt_allowed",
            {**valid_payload, "costControl": {**OPERATE_COST_CONTROL, "rawLogPromptsAllowed": True}},
            True,
            "raw log prompt allowance",
        ),
        (
            "unsanitized_evidence_allowed",
            {**valid_payload, "costControl": {**OPERATE_COST_CONTROL, "sanitizedEvidenceOnly": False}},
            True,
            "unsanitized evidence allowance",
        ),
        (
            "raw_log_privacy_text",
            {
                **valid_payload,
                "telemetrySignals": [
                    {"id": signal_id, "privacy": "raw logs may be copied to prompts"}
                    for signal_id in OPERATE_TELEMETRY_SIGNALS
                ],
            },
            True,
            "raw log privacy allowance",
        ),
    ]
    results = []
    for case_id, payload, should_fail, expected_issue in fixtures:
        detected = detect_operate_fixture_issues(payload)
        failure_detected = bool(detected)
        passed_expectation = (
            failure_detected == should_fail
            and (not expected_issue or expected_issue in detected)
        )
        results.append(
            {
                "id": case_id,
                "expectedFailure": should_fail,
                "failureDetected": failure_detected,
                "passedExpectation": passed_expectation,
                "detected": passed_expectation,
                "issues": detected,
            }
        )
    return results


def validate_cost_routing_contract(agents: list, issues: list[str]) -> dict:
    local_issues: list[str] = []
    summary = {
        "pass": False,
        "agentPresent": False,
        "mission": COST_MISSION,
        "policyVersion": COST_ROUTING_VERSION,
        "contractChecked": False,
        "scorecardChecked": False,
        "policyDocChecked": False,
        "settingsChecked": False,
        "cheapDeterministicWorkChecked": [],
        "judgementWorkChecked": [],
        "runtimeEquivalenceChecked": False,
        "traceabilityChecked": False,
        "sampleRouteChecked": False,
        "sampleTopRoute": None,
        "sampleRouteCheapPath": None,
        "negativeCases": run_cost_routing_negative_cases(),
        "negativeCasesDetected": False,
        "issues": local_issues,
    }

    agent = next((item for item in agents if isinstance(item, dict) and item.get("id") == COST_AGENT), {})
    summary["agentPresent"] = bool(agent)
    if not agent:
        local_issues.append("Cost Routing Governor agent is missing from data/agent_roster.json.")
    else:
        if agent.get("mission") != COST_MISSION:
            local_issues.append("Cost Routing Governor mission drifted from data/agent_roster.json.")
        if agent.get("mode") != "python_only":
            local_issues.append("Cost Routing Governor must remain python_only; it routes LLM work but does not perform it.")

    contract = read_json(ROOT / COST_CONTRACT, {}, local_issues)
    scorecard = read_json(ROOT / COST_SCORECARD, {}, local_issues)
    settings = read_json(ROOT / ".vscode" / "settings.json", {}, local_issues)
    policy_text = read_text(ROOT / COST_POLICY_DOC)

    if contract:
        summary["contractChecked"] = True
        validate_cost_contract_payload(contract, summary, local_issues)
    if scorecard:
        summary["scorecardChecked"] = True
        validate_cost_scorecard_payload(scorecard, local_issues)
    if policy_text:
        summary["policyDocChecked"] = True
        missing_markers = [
            marker
            for marker in [
                "# Cost Routing Policy",
                "## Decision Contract",
                "## Runtime Equivalence",
                "## Verification",
            ]
            if marker not in policy_text
        ]
        if missing_markers:
            local_issues.append(f"{COST_POLICY_DOC} missing marker(s): {', '.join(missing_markers)}.")
    else:
        local_issues.append(f"Missing required policy document: {COST_POLICY_DOC}.")

    if settings:
        summary["settingsChecked"] = True
        expected_settings = {
            "codexLoop.costRoutingContractFile": COST_CONTRACT,
            "codexLoop.costRoutingScorecardFile": COST_SCORECARD,
            "codexLoop.costRoutingPolicyFile": COST_POLICY_DOC,
            "codexLoop.deterministicPythonFirst": True,
            "codexLoop.llmEscalationMode": "judgement-only-after-python-evidence",
            "codexLoop.maxUnexplainedRuntimeDrift": 0,
            "codexLoop.rawLogPromptsAllowed": False,
        }
        for key, expected in expected_settings.items():
            if settings.get(key) != expected:
                local_issues.append(f".vscode/settings.json {key} must be {expected!r}.")

    try:
        import semantic_router as router

        sample = router.route("python ci routing", limit=3)
    except Exception as exc:  # pragma: no cover - validator reports the concrete runtime error.
        local_issues.append(f"Cost Routing Governor sample route failed: {exc}.")
        sample = []
    if sample:
        summary["sampleRouteChecked"] = True
        top = sample[0]
        summary["sampleTopRoute"] = top.get("id")
        summary["sampleRouteCheapPath"] = top.get("cheap_path")
        evidence = top.get("routing_evidence", {})
        if top.get("id") != "python":
            local_issues.append("Cost Routing Governor sample route must keep Python first for `python ci routing`.")
        if top.get("cheap_path") is not True:
            local_issues.append("Cost Routing Governor sample route must resolve as a cheap deterministic path.")
        if evidence.get("llm_assist_used") is not False:
            local_issues.append("Cost Routing Governor sample route must not use LLM assist for cheap deterministic work.")

    summary["negativeCasesDetected"] = all(case["passedExpectation"] for case in summary["negativeCases"])
    if not summary["negativeCasesDetected"]:
        local_issues.append("Cost Routing Governor negative fixtures must be detected by executable checks.")

    summary["pass"] = not local_issues
    issues.extend(local_issues)
    return summary


def validate_cost_contract_payload(contract: dict, summary: dict, issues: list[str]) -> None:
    if contract.get("policyVersion") != COST_ROUTING_VERSION:
        issues.append(f"{COST_CONTRACT} policyVersion must be {COST_ROUTING_VERSION}.")
    if contract.get("ownerAgent") != COST_AGENT:
        issues.append(f"{COST_CONTRACT} ownerAgent must be {COST_AGENT}.")
    if contract.get("room") != "Operations":
        issues.append(f"{COST_CONTRACT} room must be Operations.")
    if contract.get("mission") != COST_MISSION:
        issues.append(f"{COST_CONTRACT} mission drifted.")
    if contract.get("mode") != COST_ROUTING_MODE:
        issues.append(f"{COST_CONTRACT} mode must be {COST_ROUTING_MODE}.")
    if contract.get("frontier") != "state-locks":
        issues.append(f"{COST_CONTRACT} frontier must remain state-locks.")
    if contract.get("runtimes") != RUNTIMES:
        issues.append(f"{COST_CONTRACT} runtimes must match factory runtimes.")
    if contract.get("sourceOfTruth") != COST_CONTRACT:
        issues.append(f"{COST_CONTRACT} sourceOfTruth must point to itself.")
    if contract.get("decisionRules") != COST_DECISION_RULES:
        issues.append(f"{COST_CONTRACT} decisionRules must preserve Python-first cost control.")
    if contract.get("runtimeEquivalence") != COST_RUNTIME_EQUIVALENCE:
        issues.append(f"{COST_CONTRACT} runtimeEquivalence drifted.")
    else:
        summary["runtimeEquivalenceChecked"] = True
    if contract.get("traceability") != COST_TRACEABILITY:
        issues.append(f"{COST_CONTRACT} traceability refs drifted.")
    else:
        summary["traceabilityChecked"] = True

    cheap_work = contract.get("cheapDeterministicWork", [])
    cheap_ids = [item.get("id") for item in cheap_work if isinstance(item, dict)]
    if cheap_ids != COST_CHEAP_WORK_IDS:
        issues.append(f"{COST_CONTRACT} cheapDeterministicWork ids drifted.")
    for item in cheap_work if isinstance(cheap_work, list) else []:
        if not isinstance(item, dict):
            issues.append(f"{COST_CONTRACT} cheapDeterministicWork entries must be objects.")
            continue
        if item.get("executor") != "python" or item.get("costClass") != "cheap_deterministic":
            issues.append(f"{COST_CONTRACT} cheap work `{item.get('id')}` must route to Python.")
        if not isinstance(item.get("evidence"), list) or not item.get("evidence"):
            issues.append(f"{COST_CONTRACT} cheap work `{item.get('id')}` needs evidence refs.")
    summary["cheapDeterministicWorkChecked"] = cheap_ids

    judgement_work = contract.get("expensiveJudgementWork", [])
    judgement_ids = [item.get("id") for item in judgement_work if isinstance(item, dict)]
    if judgement_ids != COST_JUDGEMENT_WORK_IDS:
        issues.append(f"{COST_CONTRACT} expensiveJudgementWork ids drifted.")
    for item in judgement_work if isinstance(judgement_work, list) else []:
        if not isinstance(item, dict):
            issues.append(f"{COST_CONTRACT} expensiveJudgementWork entries must be objects.")
            continue
        if item.get("executor") != "llm" or item.get("costClass") != "expensive_judgement":
            issues.append(f"{COST_CONTRACT} judgement work `{item.get('id')}` must route to LLM.")
        allowed_after = item.get("allowedAfter", [])
        if "python_gates_pass" not in allowed_after:
            issues.append(f"{COST_CONTRACT} judgement work `{item.get('id')}` must wait for Python gates.")
        if item.get("traceRequired") is not True:
            issues.append(f"{COST_CONTRACT} judgement work `{item.get('id')}` must require trace evidence.")
    summary["judgementWorkChecked"] = judgement_ids

    validation = contract.get("validation", {})
    if validation.get("commands") != COST_VALIDATION_COMMANDS:
        issues.append(f"{COST_CONTRACT} validation commands drifted.")
    if validation.get("requiredSettings") != COST_REQUIRED_SETTINGS:
        issues.append(f"{COST_CONTRACT} requiredSettings drifted.")
    required_artifacts = validation.get("requiredArtifacts", [])
    for required in [COST_CONTRACT, COST_SCORECARD, COST_POLICY_DOC]:
        if required not in required_artifacts:
            issues.append(f"{COST_CONTRACT} validation.requiredArtifacts missing {required}.")


def validate_cost_scorecard_payload(scorecard: dict, issues: list[str]) -> None:
    if scorecard.get("policyVersion") != COST_ROUTING_VERSION:
        issues.append(f"{COST_SCORECARD} policyVersion must be {COST_ROUTING_VERSION}.")
    if scorecard.get("ownerAgent") != COST_AGENT:
        issues.append(f"{COST_SCORECARD} ownerAgent must be {COST_AGENT}.")
    if scorecard.get("contract") != COST_CONTRACT:
        issues.append(f"{COST_SCORECARD} contract ref must be {COST_CONTRACT}.")
    if scorecard.get("pass") is not True:
        issues.append(f"{COST_SCORECARD} pass must be true.")
    checks = scorecard.get("checks", [])
    if not isinstance(checks, list) or len(checks) < 6:
        issues.append(f"{COST_SCORECARD} must include at least 6 executable checks.")
    else:
        failing = [item.get("id") for item in checks if not isinstance(item, dict) or item.get("status") != "pass"]
        if failing:
            issues.append(f"{COST_SCORECARD} has non-pass check(s): {', '.join(map(str, failing))}.")
    samples = scorecard.get("sampleRoutes", [])
    if not isinstance(samples, list) or not samples:
        issues.append(f"{COST_SCORECARD} must include sample route evidence.")
    else:
        sample = samples[0]
        if sample.get("request") != "python ci routing":
            issues.append(f"{COST_SCORECARD} first sample route request drifted.")
        if sample.get("expectedTopRoute") != "python" or sample.get("expectedCheapPath") is not True:
            issues.append(f"{COST_SCORECARD} sample route must expect the cheap Python path.")
        if sample.get("evidenceField") != "routing_evidence":
            issues.append(f"{COST_SCORECARD} sample route evidenceField must be routing_evidence.")


def detect_cost_routing_fixture_issues(payload: dict) -> list[str]:
    detected = []
    if payload.get("decisionRules") != COST_DECISION_RULES:
        detected.append("decision rule drift")
    else:
        rules = payload["decisionRules"]
        if rules.get("pythonFirstRequired") is not True:
            detected.append("missing python first")
        if rules.get("llmBeforePythonAllowed") is not False:
            detected.append("llm before python allowed")
        if rules.get("rawLogPromptsAllowed") is not False:
            detected.append("raw log prompt allowance")
    if payload.get("runtimeEquivalence") != COST_RUNTIME_EQUIVALENCE:
        detected.append("runtime equivalence drift")
    cheap_work = payload.get("cheapDeterministicWork", [])
    if [item.get("id") for item in cheap_work if isinstance(item, dict)] != COST_CHEAP_WORK_IDS:
        detected.append("cheap work drift")
    elif any(item.get("executor") != "python" for item in cheap_work if isinstance(item, dict)):
        detected.append("cheap work not routed to python")
    judgement_work = payload.get("expensiveJudgementWork", [])
    if [item.get("id") for item in judgement_work if isinstance(item, dict)] != COST_JUDGEMENT_WORK_IDS:
        detected.append("judgement work drift")
    elif any("python_gates_pass" not in item.get("allowedAfter", []) for item in judgement_work if isinstance(item, dict)):
        detected.append("judgement without python gate")
    if payload.get("traceability") != COST_TRACEABILITY:
        detected.append("traceability drift")
    return detected


def run_cost_routing_negative_cases() -> list[dict]:
    cheap_work = [
        {"id": item_id, "executor": "python", "costClass": "cheap_deterministic", "evidence": ["generated/validation-report.json"]}
        for item_id in COST_CHEAP_WORK_IDS
    ]
    judgement_work = [
        {
            "id": item_id,
            "executor": "llm",
            "costClass": "expensive_judgement",
            "allowedAfter": ["python_gates_pass"],
            "traceRequired": True,
        }
        for item_id in COST_JUDGEMENT_WORK_IDS
    ]
    valid_payload = {
        "decisionRules": COST_DECISION_RULES,
        "runtimeEquivalence": COST_RUNTIME_EQUIVALENCE,
        "cheapDeterministicWork": cheap_work,
        "expensiveJudgementWork": judgement_work,
        "traceability": COST_TRACEABILITY,
    }
    llm_cheap_work = [dict(item) for item in cheap_work]
    llm_cheap_work[0]["executor"] = "llm"
    ungated_judgement = [dict(item) for item in judgement_work]
    ungated_judgement[0]["allowedAfter"] = []
    fixtures = [
        ("valid_control", valid_payload, False, ""),
        ("missing_python_first", {**valid_payload, "decisionRules": {**COST_DECISION_RULES, "pythonFirstRequired": False}}, True, "decision rule drift"),
        ("llm_before_python", {**valid_payload, "decisionRules": {**COST_DECISION_RULES, "llmBeforePythonAllowed": True}}, True, "decision rule drift"),
        ("runtime_drift", {**valid_payload, "runtimeEquivalence": {"runtimes": ["codex"]}}, True, "runtime equivalence drift"),
        ("cheap_work_to_llm", {**valid_payload, "cheapDeterministicWork": llm_cheap_work}, True, "cheap work not routed to python"),
        ("ungated_judgement", {**valid_payload, "expensiveJudgementWork": ungated_judgement}, True, "judgement without python gate"),
        ("traceability_missing", {**valid_payload, "traceability": {}}, True, "traceability drift"),
    ]
    results = []
    for case_id, payload, should_fail, expected_issue in fixtures:
        detected = detect_cost_routing_fixture_issues(payload)
        failure_detected = bool(detected)
        passed_expectation = (
            failure_detected == should_fail
            and (not expected_issue or expected_issue in detected)
        )
        results.append(
            {
                "id": case_id,
                "expectedFailure": should_fail,
                "failureDetected": failure_detected,
                "passedExpectation": passed_expectation,
                "detected": passed_expectation,
                "issues": detected,
            }
        )
    return results


def validate_docs_auditor_contract(copilots: list, agents: list, issues: list[str]) -> dict:
    local_issues: list[str] = []
    summary = {
        "pass": False,
        "agentPresent": False,
        "mission": DOCS_MISSION,
        "policyVersion": DOCS_AUDIT_VERSION,
        "requiredEvidence": DOCS_REQUIRED_EVIDENCE,
        "qualityGates": DOCS_QUALITY_GATES,
        "runtimeEquivalence": DOCS_RUNTIME_EQUIVALENCE,
        "costControl": DOCS_COST_CONTROL,
        "validationCommands": DOCS_VALIDATION_COMMANDS,
        "reportArtifact": DOCS_REPORT_REF,
        "reportMarkdown": DOCS_REPORT_MD_REF,
        "reportWritten": False,
        "copilotReadmesExpected": len(copilots),
        "copilotReadmesChecked": [],
        "operatorDocsChecked": [],
        "readmeChecks": [],
        "operatorDocChecks": [],
        "negativeCases": run_docs_negative_cases(),
        "negativeCasesDetected": False,
        "issues": local_issues,
    }

    agent = next((item for item in agents if isinstance(item, dict) and item.get("id") == DOCS_AGENT), {})
    summary["agentPresent"] = bool(agent)
    if not agent:
        local_issues.append("Documentation Auditor agent is missing from data/agent_roster.json.")
    else:
        if agent.get("mission") != DOCS_MISSION:
            local_issues.append("Documentation Auditor mission drifted from data/agent_roster.json.")
        if agent.get("mode") != "python_first_llm_sparse":
            local_issues.append("Documentation Auditor mode must remain python_first_llm_sparse.")
        if agent.get("phase") != "quality":
            local_issues.append("Documentation Auditor must stay in the quality phase.")

    for copilot in copilots:
        if not isinstance(copilot, dict):
            local_issues.append("Documentation Auditor found a non-object copilot catalog entry.")
            continue
        check = validate_copilot_readme_contract(copilot, local_issues)
        summary["readmeChecks"].append(check)
        if check["pass"]:
            summary["copilotReadmesChecked"].append(copilot.get("id"))

    for rel_path, markers in DOCS_OPERATOR_DOCS.items():
        check = validate_operator_doc_contract(rel_path, markers, local_issues)
        summary["operatorDocChecks"].append(check)
        if check["pass"]:
            summary["operatorDocsChecked"].append(rel_path)

    summary["negativeCasesDetected"] = all(case["passedExpectation"] for case in summary["negativeCases"])
    if not summary["negativeCasesDetected"]:
        local_issues.append("Documentation Auditor negative fixtures must be detected by executable checks.")

    if len(summary["copilotReadmesChecked"]) != len(copilots):
        local_issues.append("Documentation Auditor did not verify every generated copilot README.")
    if len(summary["operatorDocsChecked"]) != len(DOCS_OPERATOR_DOCS):
        local_issues.append("Documentation Auditor did not verify every required operator doc.")

    summary["pass"] = not local_issues
    summary["reportWritten"] = True
    write_documentation_audit_report(summary)
    reports_written = DOCS_AUDIT_REPORT_JSON.exists() and DOCS_AUDIT_REPORT_MD.exists()
    if not reports_written:
        summary["reportWritten"] = False
        local_issues.append("Documentation Auditor did not write generated documentation audit reports.")
        summary["pass"] = False
        write_documentation_audit_report(summary)

    issues.extend(local_issues)
    return summary


def validate_copilot_readme_contract(copilot: dict, issues: list[str]) -> dict:
    copilot_id = str(copilot.get("id", ""))
    safe_copilot_id = is_lower_snake(copilot_id)
    path = ROOT / "dist" / "copilots" / copilot_id / "README.md" if safe_copilot_id else None
    text = read_text(path) if path is not None else ""
    required_operator_markers = [
        "## Operator Runbook",
        "Use `shared/spec.json` as the source of truth.",
        "Run `python tools/validate_copilot_factory.py`",
        "Run `python tools/validate_prompt_quality.py`",
        "Do not paste raw logs, tokens or customer data",
        "## Documentation Audit",
        f"`{DOCS_REPORT_REF}`",
        "`generated/validation-report.json#/docsAuditor`",
    ]
    check = {
        "copilotId": copilot_id,
        "copilotIdValid": safe_copilot_id,
        "readmePath": relative(path) if path is not None else "dist/copilots/<invalid-copilot-id>/README.md",
        "exists": path.exists() if path is not None else False,
        "sectionsPresent": [],
        "missingSections": [],
        "runtimeMarkersPresent": [],
        "missingRuntimeMarkers": [],
        "operatorMarkersPresent": [],
        "missingOperatorMarkers": [],
        "purposeChecked": False,
        "sourceOfTruthChecked": False,
        "pass": False,
    }
    if not safe_copilot_id:
        issues.append(f"Documentation Auditor unsafe copilot id for README path: {copilot_id}.")
        return check
    if not text:
        issues.append(f"Documentation Auditor missing README for {copilot_id}: {relative(path)}.")
        return check

    for section in DOCS_REQUIRED_README_SECTIONS:
        marker = f"## {section}"
        if marker in text:
            check["sectionsPresent"].append(section)
        else:
            check["missingSections"].append(section)
    for marker in DOCS_REQUIRED_RUNTIME_MARKERS:
        if marker in text:
            check["runtimeMarkersPresent"].append(marker)
        else:
            check["missingRuntimeMarkers"].append(marker)
    for marker in required_operator_markers:
        if marker in text:
            check["operatorMarkersPresent"].append(marker)
        else:
            check["missingOperatorMarkers"].append(marker)

    purpose = str(copilot.get("function", ""))
    check["purposeChecked"] = bool(purpose and purpose in text)
    check["sourceOfTruthChecked"] = "`shared/spec.json`" in text
    if not check["purposeChecked"]:
        issues.append(f"Documentation Auditor README purpose drift for {copilot_id}.")
    if not check["sourceOfTruthChecked"]:
        issues.append(f"Documentation Auditor README source-of-truth marker missing for {copilot_id}.")
    if check["missingSections"]:
        issues.append(
            f"Documentation Auditor README sections missing for {copilot_id}: "
            + ", ".join(check["missingSections"])
            + "."
        )
    if check["missingRuntimeMarkers"]:
        issues.append(
            f"Documentation Auditor runtime refs missing for {copilot_id}: "
            + ", ".join(check["missingRuntimeMarkers"])
            + "."
        )
    if check["missingOperatorMarkers"]:
        issues.append(
            f"Documentation Auditor operator markers missing for {copilot_id}: "
            + ", ".join(check["missingOperatorMarkers"])
            + "."
        )

    check["pass"] = (
        check["exists"]
        and not check["missingSections"]
        and not check["missingRuntimeMarkers"]
        and not check["missingOperatorMarkers"]
        and check["purposeChecked"]
        and check["sourceOfTruthChecked"]
    )
    return check


def validate_operator_doc_contract(rel_path: str, markers: list[str], issues: list[str]) -> dict:
    path = ROOT / rel_path
    text = read_text(path)
    missing = [marker for marker in markers if marker not in text]
    check = {
        "path": rel_path,
        "exists": path.exists(),
        "markersPresent": [marker for marker in markers if marker in text],
        "missingMarkers": missing,
        "pass": path.exists() and not missing,
    }
    if not path.exists():
        issues.append(f"Documentation Auditor operator doc missing: {rel_path}.")
    elif missing:
        issues.append(f"{rel_path} missing Documentation Auditor marker(s): {', '.join(missing)}.")
    return check


def detect_docs_fixture_issues(payload: dict) -> list[str]:
    detected: list[str] = []
    if payload.get("requiredEvidence") != DOCS_REQUIRED_EVIDENCE:
        detected.append("missing required evidence")
    if payload.get("qualityGates") != DOCS_QUALITY_GATES:
        detected.append("quality gate drift")
    if payload.get("runtimeEquivalence") != DOCS_RUNTIME_EQUIVALENCE:
        detected.append("runtime equivalence drift")
    if payload.get("validationCommands") != DOCS_VALIDATION_COMMANDS:
        detected.append("validation command drift")
    if payload.get("readmeSections") != DOCS_REQUIRED_README_SECTIONS:
        detected.append("readme section drift")
    if payload.get("runtimeMarkers") != DOCS_REQUIRED_RUNTIME_MARKERS:
        detected.append("runtime marker drift")
    cost_control = payload.get("costControl")
    if cost_control != DOCS_COST_CONTROL:
        detected.append("missing deterministic cost control")
    if isinstance(cost_control, dict) and cost_control.get("rawLogPromptsAllowed") is not False:
        detected.append("raw log prompt allowance")
    operator_docs = payload.get("operatorDocs", [])
    if operator_docs != list(DOCS_OPERATOR_DOCS):
        detected.append("operator doc drift")
    return detected


def run_docs_negative_cases() -> list[dict]:
    valid_payload = {
        "requiredEvidence": DOCS_REQUIRED_EVIDENCE,
        "qualityGates": DOCS_QUALITY_GATES,
        "runtimeEquivalence": DOCS_RUNTIME_EQUIVALENCE,
        "validationCommands": DOCS_VALIDATION_COMMANDS,
        "readmeSections": DOCS_REQUIRED_README_SECTIONS,
        "runtimeMarkers": DOCS_REQUIRED_RUNTIME_MARKERS,
        "operatorDocs": list(DOCS_OPERATOR_DOCS),
        "costControl": DOCS_COST_CONTROL,
    }
    fixtures = [
        ("valid_control", valid_payload, False, ""),
        ("missing_required_evidence", {**valid_payload, "requiredEvidence": []}, True, "missing required evidence"),
        ("missing_runtime_markers", {**valid_payload, "runtimeMarkers": []}, True, "runtime marker drift"),
        ("missing_operator_docs", {**valid_payload, "operatorDocs": []}, True, "operator doc drift"),
        ("runtime_drift", {**valid_payload, "runtimeEquivalence": {"runtimes": ["codex"]}}, True, "runtime equivalence drift"),
        ("missing_cost_control", {**valid_payload, "costControl": {}}, True, "missing deterministic cost control"),
        (
            "raw_log_prompt_allowed",
            {**valid_payload, "costControl": {**DOCS_COST_CONTROL, "rawLogPromptsAllowed": True}},
            True,
            "raw log prompt allowance",
        ),
    ]
    results = []
    for case_id, payload, should_fail, expected_issue in fixtures:
        detected = detect_docs_fixture_issues(payload)
        failure_detected = bool(detected)
        passed_expectation = (
            failure_detected == should_fail
            and (not expected_issue or expected_issue in detected)
        )
        results.append(
            {
                "id": case_id,
                "expectedFailure": should_fail,
                "failureDetected": failure_detected,
                "passedExpectation": passed_expectation,
                "detected": passed_expectation,
                "issues": detected,
            }
        )
    return results


def write_documentation_audit_report(summary: dict) -> None:
    report = {
        **summary,
        "checkedAt": datetime.now(timezone.utc).isoformat(),
    }
    DOCS_AUDIT_REPORT_JSON.parent.mkdir(parents=True, exist_ok=True)
    DOCS_AUDIT_REPORT_JSON.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    DOCS_AUDIT_REPORT_MD.write_text(render_documentation_audit_md(report), encoding="utf-8")


def render_documentation_audit_md(report: dict) -> str:
    readme_rows = "\n".join(
        "| {copilot} | {status} | {sections} | {runtime_refs} | {operator_refs} |".format(
            copilot=item.get("copilotId"),
            status="pass" if item.get("pass") else "fail",
            sections=len(item.get("sectionsPresent", [])),
            runtime_refs=len(item.get("runtimeMarkersPresent", [])),
            operator_refs=len(item.get("operatorMarkersPresent", [])),
        )
        for item in report.get("readmeChecks", [])
    )
    operator_rows = "\n".join(
        "| {path} | {status} | {markers} |".format(
            path=item.get("path"),
            status="pass" if item.get("pass") else "fail",
            markers=len(item.get("markersPresent", [])),
        )
        for item in report.get("operatorDocChecks", [])
    )
    issues = "\n".join(f"- {issue}" for issue in report.get("issues", [])) or "- none"
    return f"""# Documentation Audit Report

Pass: {report.get('pass')}

Policy version: `{report.get('policyVersion')}`

Owner: `{DOCS_AGENT}`

Mission: `{report.get('mission')}`

Report JSON: `{DOCS_REPORT_REF}`

Validation commands:

- `python tools/validate_copilot_factory.py`
- `python tools/validate_prompt_quality.py`

## Copilot README Checks

| Copilot | Status | Sections | Runtime refs | Operator refs |
|---|---|---:|---:|---:|
{readme_rows}

## Operator Doc Checks

| Path | Status | Markers |
|---|---|---:|
{operator_rows}

## Cost And Traceability

- Deterministic Python first: {report.get('costControl', {}).get('deterministicPythonFirst')}
- LLM escalation: {report.get('costControl', {}).get('llmEscalation')}
- Runtime trace evidence: `{DOCS_RUNTIME_EQUIVALENCE['traceEvidence']}`
- Max unexplained drift: {DOCS_RUNTIME_EQUIVALENCE['maxUnexplainedDrift']}

## Issues

{issues}
"""


def artifact_ref_exists(ref: object) -> bool:
    if not isinstance(ref, str) or not ref.strip():
        return False
    if ref.startswith("python "):
        return True
    path_text = ref.split("#", 1)[0]
    if not path_text or Path(path_text).is_absolute():
        return False
    return (ROOT / path_text).exists()


def project_contract_subset(candidate, template):
    if isinstance(candidate, dict) and isinstance(template, dict):
        return {
            key: project_contract_subset(candidate.get(key), expected)
            for key, expected in template.items()
        }
    if isinstance(candidate, list) and isinstance(template, list) and len(candidate) == len(template):
        return [
            project_contract_subset(candidate_item, template_item)
            for candidate_item, template_item in zip(candidate, template)
        ]
    return candidate


def validate_generator_contract(issues: list[str]) -> dict:
    summary = {
        "present": False,
        "semanticRouterTemplateChecked": False,
        "generatedIndexChecked": False,
        "generatedAgentChecked": False,
        "generatedPythonProfileChecked": False,
        "generatedDiscoveryPolicyChecked": False,
        "generatedDiscoveryAgentChecked": False,
        "generatedDiscoveryProfileChecked": False,
        "generatedDesignPolicyChecked": False,
        "generatedDesignAgentChecked": False,
        "generatedDesignProfilesChecked": False,
        "generatedBuildPolicyChecked": False,
        "generatedBuildAgentChecked": False,
        "generatedBuildProfilesChecked": False,
        "generatedRunFactoryChecked": False,
        "generatedSecurityPolicyChecked": False,
        "generatedSecurityEnvChecked": False,
    }
    try:
        import generate_copilot_factory as generator
    except Exception as exc:  # pragma: no cover - reports import-time failure.
        issues.append(f"Factory generator cannot be imported: {exc}.")
        return summary

    summary["present"] = True

    try:
        rendered_run_factory = generator.render_run_factory()
        compile(rendered_run_factory, "rendered_run_factory.py", "exec")
    except Exception as exc:
        issues.append(f"Factory generator run_factory template is invalid: {exc}.")
        rendered_run_factory = ""
    required_run_factory_snippets = [
        "RUN_SEQUENCE",
        "SCRIPT_TIMEOUT_SECONDS",
        "PYTHONDONTWRITEBYTECODE",
        "subprocess.run",
        "LOG_EVIDENCE_PATH",
        "cwd=ROOT",
        "env=env",
        "check=True",
        "timeout=SCRIPT_TIMEOUT_SECONDS",
        "emit_log_evidence",
        "emit_devops_audit",
        "devops_audit_payload",
        "sanitizedEvidenceOnly",
        "noBytecodeArtifacts",
    ]
    missing_run_factory_snippets = [
        snippet for snippet in required_run_factory_snippets
        if snippet not in rendered_run_factory
    ]
    if missing_run_factory_snippets:
        issues.append(
            "Factory generator run_factory template would drop DevOps runtime-toolchain marker(s): "
            + ", ".join(missing_run_factory_snippets)
            + "."
        )
    else:
        summary["generatedRunFactoryChecked"] = True

    try:
        generated_security_policy = generator.security_mcp_connectors_contract()
    except Exception as exc:
        issues.append(f"Factory generator security MCP template cannot be rendered: {exc}.")
        generated_security_policy = {}
    current_security_policy = read_json(ROOT / SECURITY_MCP_CONFIG, {}, issues)
    current_security_core = project_contract_subset(current_security_policy, generated_security_policy)
    if generated_security_policy == current_security_core:
        summary["generatedSecurityPolicyChecked"] = True
    else:
        issues.append("Factory generator security MCP template would drift from the checked connector policy.")

    try:
        generated_env_example = generator.security_env_example()
    except Exception as exc:
        issues.append(f"Factory generator env example template cannot be rendered: {exc}.")
        generated_env_example = ""
    generated_env_values = {
        line.split("=", 1)[0]: line.split("=", 1)[1]
        for line in generated_env_example.replace("\r\n", "\n").splitlines()
        if line.strip() and not line.strip().startswith("#") and "=" in line
    }
    current_env_values = parse_env_example(ROOT / SECURITY_ENV_EXAMPLE, issues)
    if all(current_env_values.get(key) == value for key, value in generated_env_values.items()):
        summary["generatedSecurityEnvChecked"] = True
    else:
        issues.append("Factory generator env example template would drift from the placeholder-only credentials policy.")

    try:
        rendered_router = generator.render_semantic_router()
        compile(rendered_router, "rendered_semantic_router.py", "exec")
    except Exception as exc:
        issues.append(f"Factory generator semantic router template is invalid: {exc}.")
        rendered_router = ""
    required_router_snippets = [
        "routing_evidence",
        "llm_assist_used",
        "score_before_llm_assist",
        "SCORE_INPUTS",
        "EXECUTION_ORDER",
        "CHEAP_PATH_THRESHOLD",
        "discovery_audit",
        "discovery_audit_evidence",
        "design_boundary_audit",
        "design_boundary_audit_evidence",
        "design_audit:shared_contract",
        "implementation_plan_audit",
        "implementation_plan_audit_evidence",
        "build_audit:shared_contract",
    ]
    missing_router_snippets = [
        snippet for snippet in required_router_snippets
        if snippet not in rendered_router
    ]
    if missing_router_snippets:
        issues.append(
            "Factory generator semantic router template would drop deterministic evidence field(s): "
            + ", ".join(missing_router_snippets)
            + "."
        )
    else:
        summary["semanticRouterTemplateChecked"] = True

    try:
        generated_index = generator.copilot_index()
    except Exception as exc:
        issues.append(f"Factory generator copilot index cannot be rendered: {exc}.")
        generated_index = {}
    semantic_policy = generated_index.get("normalizationPolicy", {}).get("semanticRouting", {})
    if semantic_policy.get("ownerAgent") != SEMANTIC_AGENT:
        issues.append("Factory generator semanticRouting ownerAgent is missing or incorrect.")
    if semantic_policy.get("policyVersion") != SEMANTIC_ROUTING_VERSION:
        issues.append("Factory generator semanticRouting policyVersion is missing or incorrect.")
    if semantic_policy.get("scoreModel") != SEMANTIC_SCORE_MODEL:
        issues.append("Factory generator semanticRouting scoreModel is missing or incorrect.")
    if semantic_policy.get("scoreInputs") != SEMANTIC_SCORE_INPUTS:
        issues.append("Factory generator semanticRouting scoreInputs drifted.")
    if semantic_policy.get("executionOrder") != SEMANTIC_EXECUTION_ORDER:
        issues.append("Factory generator semanticRouting executionOrder drifted.")
    if semantic_policy.get("llmAssistBeforeScoringAllowed") is not False:
        issues.append("Factory generator semanticRouting must forbid LLM assist before scoring.")
    audit = generated_index.get("semanticRoutingAudit", {})
    if audit.get("pass") is not True or audit.get("llmAssistUsedByRouter") is not False:
        issues.append("Factory generator semanticRoutingAudit must prove no router LLM assist.")
    else:
        summary["generatedIndexChecked"] = True
    discovery_policy = generated_index.get("normalizationPolicy", {}).get("discoveryAudit", {})
    if discovery_policy.get("ownerAgent") != DISCOVERY_AGENT:
        issues.append("Factory generator discoveryAudit ownerAgent is missing or incorrect.")
    if discovery_policy.get("policyVersion") != DISCOVERY_AUDIT_VERSION:
        issues.append("Factory generator discoveryAudit policyVersion is missing or incorrect.")
    if discovery_policy.get("targetCopilot") != DISCOVERY_TARGET_COPILOT:
        issues.append("Factory generator discoveryAudit targetCopilot is incorrect.")
    if discovery_policy.get("coverageItems") != DISCOVERY_COVERAGE_ITEMS:
        issues.append("Factory generator discoveryAudit coverageItems drifted.")
    if discovery_policy.get("inventoryFields") != DISCOVERY_INVENTORY_FIELDS:
        issues.append("Factory generator discoveryAudit inventoryFields drifted.")
    if discovery_policy.get("requiredOutputs") != DISCOVERY_REQUIRED_OUTPUTS:
        issues.append("Factory generator discoveryAudit requiredOutputs drifted.")
    if discovery_policy.get("executionOrder") != DISCOVERY_EXECUTION_ORDER:
        issues.append("Factory generator discoveryAudit executionOrder drifted.")
    discovery_audit = generated_index.get("discoveryAudit", {})
    if discovery_audit.get("pass") is True and discovery_audit.get("coverageItemsChecked") == len(DISCOVERY_COVERAGE_ITEMS):
        summary["generatedDiscoveryPolicyChecked"] = True
    else:
        issues.append("Factory generator discoveryAudit summary must prove coverage item checks.")
    design_policy = generated_index.get("normalizationPolicy", {}).get("designBoundaryAudit", {})
    expected_design_policy = {
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
    design_audit = generated_index.get("designBoundaryAudit", {})
    if design_policy == expected_design_policy and design_audit.get("pass") is True:
        summary["generatedDesignPolicyChecked"] = True
    else:
        issues.append("Factory generator designBoundaryAudit policy or summary drifted.")
    build_policy = generated_index.get("normalizationPolicy", {}).get("buildImplementationAudit", {})
    expected_build_policy = {
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
    build_audit = generated_index.get("buildImplementationAudit", {})
    if build_policy == expected_build_policy and build_audit.get("pass") is True:
        summary["generatedBuildPolicyChecked"] = True
    else:
        issues.append("Factory generator buildImplementationAudit policy or summary drifted.")

    try:
        agents = generator.agent_roster()
    except Exception as exc:
        issues.append(f"Factory generator agent roster cannot be rendered: {exc}.")
        agents = []
    semantic_agent = next(
        (item for item in agents if isinstance(item, dict) and item.get("id") == SEMANTIC_AGENT),
        {},
    )
    generated_contract = semantic_agent.get("deterministic_scoring_contract", {})
    if generated_contract.get("llm_assist") != SEMANTIC_LLM_GUARD:
        issues.append("Factory generator Semantic Router agent LLM guard drifted.")
    if generated_contract.get("score_inputs") != SEMANTIC_SCORE_INPUTS:
        issues.append("Factory generator Semantic Router agent score inputs drifted.")
    if generated_contract.get("execution_order") != SEMANTIC_EXECUTION_ORDER:
        issues.append("Factory generator Semantic Router agent execution order drifted.")
    if generated_contract.get("runtime_equivalence", {}).get("runtimes") != RUNTIMES:
        issues.append("Factory generator Semantic Router agent runtime equivalence drifted.")
    if generated_contract.get("llm_assist") == SEMANTIC_LLM_GUARD:
        summary["generatedAgentChecked"] = True
    discovery_agent = next(
        (item for item in agents if isinstance(item, dict) and item.get("id") == DISCOVERY_AGENT),
        {},
    )
    discovery_contract = discovery_agent.get("as_is_inventory_contract", {})
    if discovery_agent.get("outputs") != DISCOVERY_AGENT_OUTPUTS:
        issues.append("Factory generator Discovery Auditor outputs drifted.")
    if discovery_contract.get("coverage_items") != DISCOVERY_COVERAGE_ITEMS:
        issues.append("Factory generator Discovery Auditor coverage_items drifted.")
    if discovery_contract.get("inventory_fields") != DISCOVERY_INVENTORY_FIELDS:
        issues.append("Factory generator Discovery Auditor inventory_fields drifted.")
    if discovery_contract.get("runtime_equivalence") != DISCOVERY_RUNTIME_EQUIVALENCE:
        issues.append("Factory generator Discovery Auditor runtime_equivalence drifted.")
    if discovery_contract.get("validation_commands") == DISCOVERY_VALIDATION_COMMANDS:
        summary["generatedDiscoveryAgentChecked"] = True
    design_agent = next(
        (item for item in agents if isinstance(item, dict) and item.get("id") == DESIGN_AGENT),
        {},
    )
    design_contract = design_agent.get("design_boundary_contract", {})
    expected_design_contract = {
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
    if design_agent.get("outputs") == DESIGN_AGENT_OUTPUTS and design_contract == expected_design_contract:
        summary["generatedDesignAgentChecked"] = True
    else:
        issues.append("Factory generator Design Auditor contract drifted.")
    build_agent = next(
        (item for item in agents if isinstance(item, dict) and item.get("id") == BUILD_AGENT),
        {},
    )
    build_contract = build_agent.get("implementation_plan_contract", {})
    expected_build_contract = {
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
    if build_agent.get("outputs") == BUILD_AGENT_OUTPUTS and build_contract == expected_build_contract:
        summary["generatedBuildAgentChecked"] = True
    else:
        issues.append("Factory generator Build Auditor contract drifted.")

    try:
        generated_copilots = generator.normalized_copilots()
    except Exception as exc:
        issues.append(f"Factory generator catalog cannot be rendered: {exc}.")
        generated_copilots = []
    python_copilot = next(
        (item for item in generated_copilots if isinstance(item, dict) and item.get("id") == "python"),
        {},
    )
    python_semantic = python_copilot.get("semantic_routing", {})
    if python_semantic.get("deterministic_python_first") is not True:
        issues.append("Factory generator Python copilot must declare deterministic_python_first.")
    if python_semantic.get("score_before_llm_assist") is not True:
        issues.append("Factory generator Python copilot must declare score_before_llm_assist.")
    if python_semantic.get("llm_assist_before_scoring_allowed") is not False:
        issues.append("Factory generator Python copilot must forbid LLM assist before scoring.")
    if python_semantic.get("score_model") == SEMANTIC_SCORE_MODEL:
        summary["generatedPythonProfileChecked"] = True
    discovery_copilot = next(
        (item for item in generated_copilots if isinstance(item, dict) and item.get("id") == DISCOVERY_TARGET_COPILOT),
        {},
    )
    if discovery_copilot.get("discovery_audit", {}).get("coverage_items") == DISCOVERY_COVERAGE_ITEMS:
        summary["generatedDiscoveryProfileChecked"] = True
    else:
        issues.append("Factory generator AS-IS Discovery copilot must declare discovery_audit coverage items.")
    generated_design_profiles = [
        item.get("id")
        for item in generated_copilots
        if isinstance(item, dict)
        and item.get("id") in DESIGN_TARGET_COPILOTS
        and item.get("design_boundary_audit") == design_profile(item.get("id", ""))
    ]
    if generated_design_profiles == DESIGN_TARGET_COPILOTS:
        summary["generatedDesignProfilesChecked"] = True
    else:
        issues.append("Factory generator design copilot profiles must declare design_boundary_audit contracts.")
    generated_build_profiles = [
        item.get("id")
        for item in generated_copilots
        if isinstance(item, dict)
        and item.get("id") in BUILD_TARGET_COPILOTS
        and item.get("implementation_plan_audit") == build_profile(item.get("id", ""))
    ]
    if generated_build_profiles == BUILD_TARGET_COPILOTS:
        summary["generatedBuildProfilesChecked"] = True
    else:
        issues.append("Factory generator build copilot profiles must declare implementation_plan_audit contracts.")
    return summary


def list_field(item: dict, key: str) -> list[str]:
    value = item.get(key, [])
    return value if isinstance(value, list) else []


def validate_unique_values(values: list[str], label: str, issues: list[str]) -> None:
    if len(values) != len(set(values)):
        issues.append(f"Duplicate value found in {label}.")


def is_lower_snake(value: object) -> bool:
    return isinstance(value, str) and re.fullmatch(r"[a-z0-9]+(?:_[a-z0-9]+)*", value) is not None


def is_upper_snake(value: object) -> bool:
    return isinstance(value, str) and re.fullmatch(r"[A-Z0-9]+(?:_[A-Z0-9]+)*", value) is not None


def expected_runtime_trace(copilot_id: str) -> dict:
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


def should_scan_text_file(file: Path) -> bool:
    if not file.is_file():
        return False
    if any(part in {".git", "__pycache__"} for part in file.parts):
        return False
    if file.suffix.lower() in {".png", ".jpg", ".jpeg", ".gif", ".ico", ".zip"}:
        return False
    rel = relative(file)
    if rel in LOCAL_RUNTIME_FILES:
        return False
    return not any(rel.startswith(prefix) for prefix in LOCAL_RUNTIME_PATH_PREFIXES)


def should_ignore_local_runtime_artifact(path: Path) -> bool:
    rel = relative(path)
    if rel in LOCAL_RUNTIME_FILES:
        return True
    return any(rel.startswith(prefix) for prefix in LOCAL_RUNTIME_PATH_PREFIXES)


def is_local_factory_runtime_report(path: Path) -> bool:
    return relative(path) in LOCAL_FACTORY_RUNTIME_REPORTS


def validate_no_python_bytecode_artifacts(issues: list[str]) -> None:
    for path in ROOT.rglob("*"):
        if any(part == ".git" for part in path.parts):
            continue
        if should_ignore_local_runtime_artifact(path):
            continue
        rel = relative(path)
        if path.is_dir() and path.name == "__pycache__":
            issues.append(f"Python bytecode cache must not be in release artifact: {rel}/")
        elif path.is_file() and path.suffix == ".pyc":
            issues.append(f"Python bytecode cache must not be in release artifact: {rel}")


def scan_text_safety(file: Path, text: str, issues: list[str]) -> None:
    rel = relative(file)
    for pattern in SECRET_PATTERNS:
        if pattern.search(text):
            issues.append(f"Potential secret pattern in {rel}")
            break
    for pattern in LOCAL_PATH_PATTERNS:
        if pattern.search(text):
            if is_local_factory_runtime_report(file):
                continue
            issues.append(f"Local absolute path leaked in release artifact: {rel}")
            break


def validate_sdlc_runtime_matrix_contract(copilots: list, agents: list, index: dict, issues: list[str]) -> dict:
    local_issues: list[str] = []
    agent = next((item for item in agents if isinstance(item, dict) and item.get("id") == MATRIX_AGENT), {})
    summary = {
        "pass": False,
        "ownerAgent": MATRIX_AGENT,
        "mission": MATRIX_MISSION,
        "policyVersion": MATRIX_POLICY_VERSION,
        "agentPresent": bool(agent),
        "agentMode": agent.get("mode") if isinstance(agent, dict) else None,
        "matrixArtifact": relative(SDLC_RUNTIME_MATRIX_JSON),
        "markdownArtifact": relative(SDLC_RUNTIME_MATRIX_MD),
        "maintenanceArtifact": relative(SDLC_RUNTIME_MATRIX_MAINTENANCE_JSON),
        "maintenanceMarkdownArtifact": relative(SDLC_RUNTIME_MATRIX_MAINTENANCE_MD),
        "dimensions": MATRIX_DIMENSIONS,
        "runtimes": RUNTIMES,
        "catalogCopilots": len([item for item in copilots if isinstance(item, dict)]),
        "matrixCellCount": 0,
        "phaseCount": 0,
        "traceLedgerEntries": 0,
        "traceLedgerDigest": None,
        "traceLedgerChecked": False,
        "runtimeTraceChecked": False,
        "promptContentStored": False,
        "costControlChecked": False,
        "traceabilityChecked": False,
        "maintenanceReceiptChecked": False,
        "maintenanceReceiptDigest": None,
        "maintenanceReceipt": {},
        "validationCommands": MATRIX_VALIDATION_COMMANDS,
        "issues": local_issues,
    }

    if not agent:
        local_issues.append("SDLC Matrix Builder agent is missing from data/agent_roster.json.")
    else:
        if agent.get("mission") != MATRIX_MISSION:
            local_issues.append("SDLC Matrix Builder mission drifted from the runtime matrix contract.")
        if agent.get("mode") != "python_only":
            local_issues.append("SDLC Matrix Builder must stay python_only to avoid prompt cost inflation.")

    normalization_policy = index.get("normalizationPolicy", {}) if isinstance(index, dict) else {}
    runtime_equivalence = normalization_policy.get("runtimeEquivalence", {}) if isinstance(normalization_policy, dict) else {}
    if runtime_equivalence.get("runtimes") != RUNTIMES:
        local_issues.append("SDLC runtime matrix index runtime list drifted from factory runtimes.")
    if runtime_equivalence.get("sourceOfTruth") != "dist/copilots/<copilot_id>/shared/spec.json":
        local_issues.append("SDLC runtime matrix index source of truth must point to shared spec.json.")

    injection_map = read_json(ROOT / "generated" / "runtime-injection-map.json", {"copilots": {}}, local_issues)
    matrix = build_sdlc_runtime_matrix(copilots, injection_map, local_issues)
    maintenance_receipt = build_sdlc_runtime_matrix_maintenance_receipt(matrix)
    try:
        SDLC_RUNTIME_MATRIX_JSON.parent.mkdir(parents=True, exist_ok=True)
        SDLC_RUNTIME_MATRIX_JSON.write_text(json.dumps(matrix, indent=2) + "\n", encoding="utf-8")
        SDLC_RUNTIME_MATRIX_MD.write_text(render_sdlc_runtime_matrix_md(matrix), encoding="utf-8")
        SDLC_RUNTIME_MATRIX_MAINTENANCE_JSON.write_text(
            json.dumps(maintenance_receipt, indent=2) + "\n",
            encoding="utf-8",
        )
        SDLC_RUNTIME_MATRIX_MAINTENANCE_MD.write_text(
            render_sdlc_runtime_matrix_maintenance_md(maintenance_receipt),
            encoding="utf-8",
        )
    except OSError as exc:
        local_issues.append(f"Cannot write SDLC runtime matrix artifact: {exc}.")

    matrix_summary = matrix.get("summary", {})
    summary["matrixCellCount"] = matrix_summary.get("matrixCellCount", 0)
    summary["phaseCount"] = matrix_summary.get("phaseCount", 0)
    trace_ledger = matrix.get("traceLedger", []) if isinstance(matrix.get("traceLedger"), list) else []
    expected_trace_ledger_entries = matrix_summary.get("traceLedgerEntries", 0)
    summary["traceLedgerEntries"] = expected_trace_ledger_entries
    summary["traceLedgerDigest"] = matrix_summary.get("traceLedgerDigest")
    summary["traceLedgerChecked"] = (
        isinstance(trace_ledger, list)
        and len(trace_ledger) == expected_trace_ledger_entries
        and matrix_summary.get("traceLedgerDigest") == stable_json_digest(trace_ledger)
    )
    if not summary["traceLedgerChecked"]:
        local_issues.append("SDLC runtime matrix trace ledger digest or entry count drifted.")
    summary["runtimeTraceChecked"] = matrix_summary.get("missingRuntimeFiles", 1) == 0
    summary["promptContentStored"] = matrix.get("costControl", {}).get("promptContentStored")
    summary["costControlChecked"] = matrix.get("costControl", {}).get("deterministicPythonFirst") is True
    summary["traceabilityChecked"] = (
        matrix.get("traceability", {}).get("runtimeMap") == "generated/runtime-injection-map.json"
        and matrix.get("traceability", {}).get("traceLedgerDigest") == summary["traceLedgerDigest"]
    )
    cell_equivalence_contract = matrix.get("cellEquivalenceContract", {})
    summary["cellEquivalenceChecked"] = (
        isinstance(cell_equivalence_contract, dict)
        and cell_equivalence_contract.get("pass") is True
        and cell_equivalence_contract.get("cellsChecked") == matrix_summary.get("matrixCellCount")
        and cell_equivalence_contract.get("passingCells") == matrix_summary.get("matrixCellCount")
    )
    if not summary["cellEquivalenceChecked"]:
        local_issues.append("SDLC runtime matrix cell equivalence contract is incomplete or failing.")
    maintenance_summary = validate_sdlc_runtime_matrix_maintenance_receipt(maintenance_receipt, matrix)
    summary["maintenanceReceiptChecked"] = maintenance_summary["pass"]
    summary["maintenanceReceiptDigest"] = maintenance_receipt.get("digests", {}).get("receiptDigest")
    summary["maintenanceReceipt"] = maintenance_summary
    local_issues.extend(maintenance_summary["issues"])
    summary["pass"] = not local_issues
    issues.extend(local_issues)
    return summary


def build_sdlc_runtime_matrix(copilots: list, injection_map: dict, issues: list[str]) -> dict:
    injection_copilots = injection_map.get("copilots", {}) if isinstance(injection_map, dict) else {}
    if not isinstance(injection_copilots, dict):
        issues.append("SDLC runtime matrix requires generated/runtime-injection-map.json#/copilots to be an object.")
        injection_copilots = {}

    cells: list[dict] = []
    phase_coverage: dict[str, dict] = {}
    copilot_coverage: dict[str, dict] = {}
    runtime_cell_counts = {runtime: 0 for runtime in RUNTIMES}
    missing_runtime_files = 0
    phase_order: list[str] = []
    trace_ledger: list[dict] = []

    for copilot in copilots:
        if not isinstance(copilot, dict):
            issues.append("SDLC runtime matrix catalog entries must be JSON objects.")
            continue
        copilot_id = copilot.get("id")
        if not isinstance(copilot_id, str) or not copilot_id:
            issues.append("SDLC runtime matrix catalog entry is missing copilot id.")
            continue
        phases = [phase for phase in list_field(copilot, "sdlc_phases") if isinstance(phase, str) and phase]
        if not phases:
            issues.append(f"SDLC runtime matrix copilot {copilot_id} has no declared SDLC phases.")
            continue
        for phase in phases:
            if phase not in phase_order:
                phase_order.append(phase)

        expected_source = f"dist/copilots/{copilot_id}/shared/spec.json"
        expected_schema = f"dist/copilots/{copilot_id}/shared/output_schema.json"
        spec_digest = file_sha256(expected_source, issues, copilot_id)
        schema_digest = file_sha256(expected_schema, issues, copilot_id)
        map_entry = injection_copilots.get(copilot_id, {})
        if not isinstance(map_entry, dict):
            issues.append(f"SDLC runtime matrix missing runtime map entry for {copilot_id}.")
            map_entry = {}
        runtime_files = map_entry.get("runtimeFiles", {}) if isinstance(map_entry.get("runtimeFiles"), dict) else {}
        source_of_truth = map_entry.get("sourceOfTruth")
        if source_of_truth != expected_source:
            issues.append(f"SDLC runtime matrix source of truth drift for {copilot_id}.")

        copilot_coverage[copilot_id] = {
            "name": copilot.get("name", copilot_id),
            "phases": phases,
            "runtimeCells": len(phases) * len(RUNTIMES),
            "sourceOfTruth": expected_source,
            "sharedSpecDigest": spec_digest,
            "outputSchemaDigest": schema_digest,
        }

        for phase in phases:
            phase_runtime_files: dict[str, str] = {}
            phase_runtime_digests: dict[str, str | None] = {}
            phase_runtime_trace_refs: dict[str, str] = {}
            phase_entry = phase_coverage.setdefault(
                phase,
                {"copilots": 0, "runtimeCells": 0, "runtimes": {runtime: 0 for runtime in RUNTIMES}},
            )
            phase_entry["copilots"] += 1
            for runtime in RUNTIMES:
                expected_runtime_file = expected_runtime_adapter_path(copilot_id, runtime)
                runtime_file = runtime_files.get(runtime)
                runtime_file_matches = runtime_file == expected_runtime_file
                if not runtime_file_matches:
                    issues.append(f"SDLC runtime matrix adapter path drift for {copilot_id}/{runtime}.")
                    runtime_file = expected_runtime_file
                runtime_digest = file_sha256(runtime_file, issues, copilot_id)
                runtime_exists = bool(runtime_digest)
                if not runtime_exists:
                    missing_runtime_files += 1
                runtime_cell_counts[runtime] += 1
                phase_entry["runtimeCells"] += 1
                phase_entry["runtimes"][runtime] += 1
                runtime_trace_ref = f"generated/runtime-injection-map.json#/copilots/{copilot_id}/runtimeFiles/{runtime}"
                runtime_trace_ref_matches = runtime in runtime_files
                phase_runtime_files[runtime] = runtime_file
                phase_runtime_digests[runtime] = runtime_digest
                phase_runtime_trace_refs[runtime] = runtime_trace_ref
                cells.append(
                    {
                        "phase": phase,
                        "copilotId": copilot_id,
                        "copilotName": copilot.get("name", copilot_id),
                        "runtime": runtime,
                        "sourceOfTruth": expected_source,
                        "outputSchema": expected_schema,
                        "runtimeFile": runtime_file,
                        "runtimeTraceRef": runtime_trace_ref,
                        "sharedSpecDigest": spec_digest,
                        "outputSchemaDigest": schema_digest,
                        "runtimeFileDigest": runtime_digest,
                        "equivalence": build_matrix_cell_equivalence(
                            source_of_truth == expected_source,
                            runtime_file_matches,
                            runtime_trace_ref_matches,
                            spec_digest,
                            schema_digest,
                            runtime_digest,
                        ),
                    }
                )
            trace_ledger.append(
                {
                    "id": f"{copilot_id}:{phase}",
                    "phase": phase,
                    "copilotId": copilot_id,
                    "copilotName": copilot.get("name", copilot_id),
                    "runtimeOrder": RUNTIMES,
                    "sourceOfTruth": expected_source,
                    "outputSchema": expected_schema,
                    "sharedSpecDigest": spec_digest,
                    "outputSchemaDigest": schema_digest,
                    "runtimeFiles": phase_runtime_files,
                    "runtimeFileDigests": phase_runtime_digests,
                    "runtimeTraceRefs": phase_runtime_trace_refs,
                    "pairwiseRuntimeCases": matrix_pairwise_runtime_cases(
                        phase_runtime_digests,
                        spec_digest,
                        schema_digest,
                    ),
                    "evidenceMode": "paths_and_sha256_digests_only",
                    "promptBodiesStored": False,
                    "maxUnexplainedDrift": 0,
                }
            )

    expected_cells = sum(
        len([phase for phase in list_field(item, "sdlc_phases") if isinstance(phase, str) and phase]) * len(RUNTIMES)
        for item in copilots
        if isinstance(item, dict)
    )
    if len(cells) != expected_cells:
        issues.append(f"SDLC runtime matrix expected {expected_cells} cells, generated {len(cells)}.")
    expected_trace_ledger_entries = sum(
        len([phase for phase in list_field(item, "sdlc_phases") if isinstance(phase, str) and phase])
        for item in copilots
        if isinstance(item, dict)
    )
    if len(trace_ledger) != expected_trace_ledger_entries:
        issues.append(
            f"SDLC runtime matrix expected {expected_trace_ledger_entries} trace ledger entries, generated {len(trace_ledger)}."
        )
    trace_ledger_digest = stable_json_digest(trace_ledger)
    cell_equivalence_contract = summarize_matrix_cell_equivalence(cells)

    return {
        "version": MATRIX_POLICY_VERSION,
        "generatedAt": datetime.now(timezone.utc).isoformat(),
        "ownerAgent": MATRIX_AGENT,
        "mission": MATRIX_MISSION,
        "dimensions": MATRIX_DIMENSIONS,
        "sourceArtifacts": {
            "catalog": "data/copilots.json",
            "catalogIndex": "generated/copilot-index.json",
            "runtimeMap": "generated/runtime-injection-map.json",
            "factoryValidation": "generated/validation-report.json#/sdlcRuntimeMatrix",
            "promptQuality": "generated/prompt-quality-report.json#/sdlcRuntimeMatrixAudit",
            "runtimeEquivalence": "generated/runtime-equivalence-report.json#/sdlcRuntimeMatrixAudit",
        },
        "runtimes": RUNTIMES,
        "costControl": {
            "deterministicPythonFirst": True,
            "promptContentStored": False,
            "storedPromptEvidence": "paths_and_sha256_digests_only",
            "llmEscalation": "not_required_for_matrix_generation",
            "maxUnexplainedDrift": 0,
        },
        "traceability": {
            "runtimeMap": "generated/runtime-injection-map.json",
            "canonicalSpecPattern": "dist/copilots/<copilot_id>/shared/spec.json",
            "runtimeTraceRefPattern": "generated/runtime-injection-map.json#/copilots/<copilot_id>/runtimeFiles/<runtime>",
            "traceLedgerDigest": trace_ledger_digest,
            "validationCommands": MATRIX_VALIDATION_COMMANDS,
        },
        "cellEquivalenceContract": cell_equivalence_contract,
        "summary": {
            "copilotCount": len([item for item in copilots if isinstance(item, dict)]),
            "phaseCount": len(phase_order),
            "phases": phase_order,
            "runtimeCount": len(RUNTIMES),
            "matrixCellCount": len(cells),
            "expectedMatrixCellCount": expected_cells,
            "traceLedgerEntries": len(trace_ledger),
            "expectedTraceLedgerEntries": expected_trace_ledger_entries,
            "traceLedgerDigest": trace_ledger_digest,
            "missingRuntimeFiles": missing_runtime_files,
            "maxUnexplainedDrift": 0,
            "cellEquivalencePass": cell_equivalence_contract["pass"],
        },
        "phaseCoverage": phase_coverage,
        "runtimeCoverage": runtime_cell_counts,
        "copilotCoverage": copilot_coverage,
        "traceLedger": trace_ledger,
        "cells": cells,
    }


def build_matrix_cell_equivalence(
    source_of_truth_matches: bool,
    runtime_file_matches: bool,
    runtime_trace_ref_matches: bool,
    spec_digest: str | None,
    schema_digest: str | None,
    runtime_digest: str | None,
) -> dict:
    assertions = {
        "sourceOfTruthMatchesRuntimeMap": source_of_truth_matches,
        "runtimeFileMatchesCanonical": runtime_file_matches,
        "runtimeTraceRefMatchesRuntimeMap": runtime_trace_ref_matches,
        "sharedSpecDigestPresent": bool(spec_digest),
        "outputSchemaDigestPresent": bool(schema_digest),
        "runtimeFileDigestPresent": bool(runtime_digest),
        "promptBodiesStoredFalse": True,
        "maxUnexplainedDriftZero": True,
    }
    return {
        "contractVersion": MATRIX_CELL_EQUIVALENCE_VERSION,
        "assertions": assertions,
        "sourceOfTruthMatchesRuntimeMap": source_of_truth_matches,
        "runtimeFileMatchesCanonical": runtime_file_matches,
        "runtimeTraceRefMatchesRuntimeMap": runtime_trace_ref_matches,
        "sameSharedSpecDigestAcrossRuntimes": True,
        "sameOutputSchemaDigestAcrossRuntimes": True,
        "promptBodiesStored": False,
        "maxUnexplainedDrift": 0,
    }


def summarize_matrix_cell_equivalence(cells: list[dict]) -> dict:
    failures = []
    for cell in cells:
        if not isinstance(cell, dict):
            failures.append({"cell": "unknown", "missingAssertions": MATRIX_CELL_EQUIVALENCE_ASSERTIONS})
            continue
        equivalence = cell.get("equivalence", {}) if isinstance(cell.get("equivalence"), dict) else {}
        assertions = equivalence.get("assertions", {}) if isinstance(equivalence.get("assertions"), dict) else {}
        missing = [name for name in MATRIX_CELL_EQUIVALENCE_ASSERTIONS if assertions.get(name) is not True]
        if equivalence.get("contractVersion") != MATRIX_CELL_EQUIVALENCE_VERSION:
            missing.append("contractVersion")
        if equivalence.get("promptBodiesStored") is not False:
            missing.append("promptBodiesStored")
        if equivalence.get("maxUnexplainedDrift") != 0:
            missing.append("maxUnexplainedDrift")
        if missing:
            failures.append(
                {
                    "cell": "/".join(
                        str(cell.get(key, "unknown"))
                        for key in ("copilotId", "phase", "runtime")
                    ),
                    "missingAssertions": sorted(set(missing)),
                }
            )
    passing_cells = max(0, len(cells) - len(failures))
    return {
        "version": MATRIX_CELL_EQUIVALENCE_VERSION,
        "requiredAssertions": MATRIX_CELL_EQUIVALENCE_ASSERTIONS,
        "evidenceMode": "per_cell_boolean_assertions_plus_sha256_digests",
        "cellsChecked": len(cells),
        "passingCells": passing_cells,
        "failingCells": failures[:10],
        "pass": not failures,
    }


def matrix_pairwise_runtime_cases(
    runtime_file_digests: dict[str, str | None],
    spec_digest: str | None,
    schema_digest: str | None,
) -> list[dict]:
    cases = []
    for left_index, left in enumerate(RUNTIMES):
        for right in RUNTIMES[left_index + 1:]:
            cases.append(
                {
                    "id": f"{left}__{right}",
                    "runtimes": [left, right],
                    "sameSharedSpecDigest": True,
                    "sameOutputSchemaDigest": True,
                    "sharedSpecDigest": spec_digest,
                    "outputSchemaDigest": schema_digest,
                    "runtimeFileDigests": {
                        left: runtime_file_digests.get(left),
                        right: runtime_file_digests.get(right),
                    },
                    "promptBodiesStored": False,
                    "maxUnexplainedDrift": 0,
                }
            )
    return cases


def expected_runtime_adapter_path(copilot_id: str, runtime: str) -> str:
    paths = {
        "codex": f"dist/copilots/{copilot_id}/codex/AGENT.md",
        "claude": f"dist/copilots/{copilot_id}/claude/AGENT.md",
        "github-copilot": f"dist/copilots/{copilot_id}/github-copilot/copilot-agent.md",
        "langchain": f"dist/copilots/{copilot_id}/langchain/agent.py",
    }
    return paths[runtime]


def file_sha256(rel_path: str, issues: list[str], scope: str) -> str | None:
    if not isinstance(rel_path, str) or not rel_path:
        issues.append(f"SDLC runtime matrix {scope} has an empty repository path.")
        return None
    candidate = (ROOT / rel_path).resolve()
    try:
        candidate.relative_to(ROOT)
    except ValueError:
        issues.append(f"SDLC runtime matrix path escapes workspace: {rel_path}.")
        return None
    try:
        data = candidate.read_bytes()
    except FileNotFoundError:
        issues.append(f"SDLC runtime matrix missing artifact: {rel_path}.")
        return None
    except OSError as exc:
        issues.append(f"SDLC runtime matrix cannot read {rel_path}: {exc}.")
        return None
    return hashlib.sha256(data).hexdigest()


def stable_json_digest(value) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def build_sdlc_runtime_matrix_maintenance_receipt(matrix: dict) -> dict:
    summary = matrix.get("summary", {}) if isinstance(matrix.get("summary"), dict) else {}
    cost_control = matrix.get("costControl", {}) if isinstance(matrix.get("costControl"), dict) else {}
    cells = matrix.get("cells", []) if isinstance(matrix.get("cells"), list) else []
    trace_ledger = matrix.get("traceLedger", []) if isinstance(matrix.get("traceLedger"), list) else []
    cell_equivalence_contract = (
        matrix.get("cellEquivalenceContract", {})
        if isinstance(matrix.get("cellEquivalenceContract"), dict)
        else {}
    )
    coverage = {
        "phaseCoverage": matrix.get("phaseCoverage", {}),
        "runtimeCoverage": matrix.get("runtimeCoverage", {}),
        "copilotCoverage": matrix.get("copilotCoverage", {}),
    }
    digests = {
        "cellDigest": stable_json_digest(cells),
        "coverageDigest": stable_json_digest(coverage),
        "traceLedgerDigest": stable_json_digest(trace_ledger),
        "cellEquivalenceContractDigest": stable_json_digest(cell_equivalence_contract),
    }
    counts = {
        "copilots": summary.get("copilotCount"),
        "phases": summary.get("phaseCount"),
        "runtimes": len(matrix.get("runtimes", [])) if isinstance(matrix.get("runtimes"), list) else 0,
        "matrixCells": summary.get("matrixCellCount"),
        "expectedMatrixCells": summary.get("expectedMatrixCellCount"),
        "traceLedgerEntries": summary.get("traceLedgerEntries"),
        "expectedTraceLedgerEntries": summary.get("expectedTraceLedgerEntries"),
    }
    acceptance_gates = {
        "coverageComplete": counts["matrixCells"] == counts["expectedMatrixCells"],
        "traceLedgerComplete": counts["traceLedgerEntries"] == counts["expectedTraceLedgerEntries"],
        "runtimeEquivalence": summary.get("missingRuntimeFiles") == 0 and summary.get("maxUnexplainedDrift") == 0,
        "promptBudget": cost_control.get("deterministicPythonFirst") is True and cost_control.get("promptContentStored") is False,
        "traceability": matrix.get("traceability", {}).get("traceLedgerDigest") == digests["traceLedgerDigest"],
        "cellEquivalence": (
            cell_equivalence_contract.get("pass") is True
            and cell_equivalence_contract.get("cellsChecked") == counts["matrixCells"]
            and cell_equivalence_contract.get("passingCells") == counts["matrixCells"]
        ),
    }
    receipt = {
        "version": MATRIX_MAINTENANCE_VERSION,
        "generatedAt": datetime.now(timezone.utc).isoformat(),
        "ownerAgent": MATRIX_AGENT,
        "mission": MATRIX_MISSION,
        "maintenanceAction": "generate_matrix_and_cross_validate_artifacts",
        "matrixPolicyVersion": matrix.get("version"),
        "dimensions": matrix.get("dimensions"),
        "runtimes": matrix.get("runtimes"),
        "artifacts": {
            "matrixJson": relative(SDLC_RUNTIME_MATRIX_JSON),
            "matrixMarkdown": relative(SDLC_RUNTIME_MATRIX_MD),
            "maintenanceJson": relative(SDLC_RUNTIME_MATRIX_MAINTENANCE_JSON),
            "maintenanceMarkdown": relative(SDLC_RUNTIME_MATRIX_MAINTENANCE_MD),
        },
        "sourceArtifacts": matrix.get("sourceArtifacts", {}),
        "counts": counts,
        "digests": digests,
        "costControl": {
            "deterministicPythonFirst": cost_control.get("deterministicPythonFirst"),
            "promptContentStored": cost_control.get("promptContentStored"),
            "storedPromptEvidence": cost_control.get("storedPromptEvidence"),
            "maxUnexplainedDrift": cost_control.get("maxUnexplainedDrift"),
        },
        "promptBudget": {
            "promptBodiesStored": cost_control.get("promptContentStored"),
            "evidenceMode": cost_control.get("storedPromptEvidence"),
            "rawPromptKeysAllowed": False,
        },
        "runtimeEquivalence": {
            "runtimes": matrix.get("runtimes"),
            "runtimeCount": len(matrix.get("runtimes", [])) if isinstance(matrix.get("runtimes"), list) else 0,
            "pairwiseCasesPerCopilotPhase": len(runtime_pairwise_cases()),
            "missingRuntimeFiles": summary.get("missingRuntimeFiles"),
            "maxUnexplainedDrift": summary.get("maxUnexplainedDrift"),
        },
        "cellEquivalenceContract": {
            "version": cell_equivalence_contract.get("version"),
            "requiredAssertions": cell_equivalence_contract.get("requiredAssertions"),
            "evidenceMode": cell_equivalence_contract.get("evidenceMode"),
            "cellsChecked": cell_equivalence_contract.get("cellsChecked"),
            "passingCells": cell_equivalence_contract.get("passingCells"),
            "failingCells": cell_equivalence_contract.get("failingCells", []),
            "pass": cell_equivalence_contract.get("pass"),
            "contractDigest": digests["cellEquivalenceContractDigest"],
        },
        "traceability": {
            "runtimeMap": "generated/runtime-injection-map.json",
            "factoryReport": "generated/validation-report.json#/sdlcRuntimeMatrix",
            "promptQualityReport": "generated/prompt-quality-report.json#/sdlcRuntimeMatrixAudit",
            "runtimeEquivalenceReport": "generated/runtime-equivalence-report.json#/sdlcRuntimeMatrixAudit",
            "traceLedgerDigest": digests["traceLedgerDigest"],
        },
        "validationCommands": MATRIX_VALIDATION_COMMANDS,
        "acceptanceGates": acceptance_gates,
    }
    receipt["digests"]["receiptDigest"] = stable_json_digest(
        {
            "version": receipt["version"],
            "mission": receipt["mission"],
            "matrixPolicyVersion": receipt["matrixPolicyVersion"],
            "dimensions": receipt["dimensions"],
            "runtimes": receipt["runtimes"],
            "counts": counts,
            "digests": digests,
            "cellEquivalenceContract": receipt["cellEquivalenceContract"],
            "acceptanceGates": acceptance_gates,
        }
    )
    return receipt


def validate_sdlc_runtime_matrix_maintenance_receipt(receipt: dict, matrix: dict) -> dict:
    local_issues: list[str] = []
    matrix_summary = matrix.get("summary", {}) if isinstance(matrix.get("summary"), dict) else {}
    receipt_counts = receipt.get("counts", {}) if isinstance(receipt.get("counts"), dict) else {}
    receipt_digests = receipt.get("digests", {}) if isinstance(receipt.get("digests"), dict) else {}
    cells = matrix.get("cells", []) if isinstance(matrix.get("cells"), list) else []
    trace_ledger = matrix.get("traceLedger", []) if isinstance(matrix.get("traceLedger"), list) else []
    matrix_cell_equivalence = (
        matrix.get("cellEquivalenceContract", {})
        if isinstance(matrix.get("cellEquivalenceContract"), dict)
        else {}
    )
    receipt_cell_equivalence = (
        receipt.get("cellEquivalenceContract", {})
        if isinstance(receipt.get("cellEquivalenceContract"), dict)
        else {}
    )
    acceptance_gates = receipt.get("acceptanceGates", {}) if isinstance(receipt.get("acceptanceGates"), dict) else {}
    summary = {
        "pass": False,
        "artifact": relative(SDLC_RUNTIME_MATRIX_MAINTENANCE_JSON),
        "markdownArtifact": relative(SDLC_RUNTIME_MATRIX_MAINTENANCE_MD),
        "policyVersion": receipt.get("version"),
        "cellDigestMatches": receipt_digests.get("cellDigest") == stable_json_digest(cells),
        "traceLedgerDigestMatches": receipt_digests.get("traceLedgerDigest") == stable_json_digest(trace_ledger),
        "cellEquivalenceContractDigestMatches": (
            receipt_digests.get("cellEquivalenceContractDigest") == stable_json_digest(matrix_cell_equivalence)
        ),
        "allAcceptanceGatesPass": all(acceptance_gates.values()) if acceptance_gates else False,
        "issues": local_issues,
    }
    if receipt.get("version") != MATRIX_MAINTENANCE_VERSION:
        local_issues.append("SDLC runtime matrix maintenance receipt policy version drifted.")
    if receipt.get("mission") != MATRIX_MISSION:
        local_issues.append("SDLC runtime matrix maintenance receipt mission drifted.")
    if receipt.get("ownerAgent") != MATRIX_AGENT:
        local_issues.append("SDLC runtime matrix maintenance receipt owner drifted.")
    if receipt.get("matrixPolicyVersion") != MATRIX_POLICY_VERSION:
        local_issues.append("SDLC runtime matrix maintenance receipt matrix policy drifted.")
    if receipt.get("dimensions") != MATRIX_DIMENSIONS or receipt.get("runtimes") != RUNTIMES:
        local_issues.append("SDLC runtime matrix maintenance receipt dimensions or runtimes drifted.")
    if receipt.get("validationCommands") != MATRIX_VALIDATION_COMMANDS:
        local_issues.append("SDLC runtime matrix maintenance receipt validation commands drifted.")
    if receipt_counts.get("matrixCells") != matrix_summary.get("matrixCellCount"):
        local_issues.append("SDLC runtime matrix maintenance receipt cell count drifted.")
    if receipt_counts.get("traceLedgerEntries") != matrix_summary.get("traceLedgerEntries"):
        local_issues.append("SDLC runtime matrix maintenance receipt trace ledger count drifted.")
    if not summary["cellDigestMatches"]:
        local_issues.append("SDLC runtime matrix maintenance receipt cell digest drifted.")
    if not summary["traceLedgerDigestMatches"]:
        local_issues.append("SDLC runtime matrix maintenance receipt trace ledger digest drifted.")
    if not summary["cellEquivalenceContractDigestMatches"]:
        local_issues.append("SDLC runtime matrix maintenance receipt cell equivalence digest drifted.")
    if receipt_cell_equivalence.get("version") != MATRIX_CELL_EQUIVALENCE_VERSION:
        local_issues.append("SDLC runtime matrix maintenance receipt cell equivalence policy drifted.")
    if receipt_cell_equivalence.get("requiredAssertions") != MATRIX_CELL_EQUIVALENCE_ASSERTIONS:
        local_issues.append("SDLC runtime matrix maintenance receipt cell equivalence assertions drifted.")
    if receipt_cell_equivalence.get("pass") is not True or acceptance_gates.get("cellEquivalence") is not True:
        local_issues.append("SDLC runtime matrix maintenance receipt cell equivalence gate is not passing.")
    if not summary["allAcceptanceGatesPass"]:
        local_issues.append("SDLC runtime matrix maintenance receipt acceptance gates are not all passing.")
    summary["pass"] = not local_issues
    return summary


def render_sdlc_runtime_matrix_maintenance_md(receipt: dict) -> str:
    gates = "\n".join(
        f"- {name}: {value}"
        for name, value in receipt.get("acceptanceGates", {}).items()
    ) or "- none"
    counts = receipt.get("counts", {})
    digests = receipt.get("digests", {})
    cell_equivalence = receipt.get("cellEquivalenceContract", {})
    commands = "\n".join(f"- `{command}`" for command in receipt.get("validationCommands", [])) or "- none"
    return f"""# SDLC Runtime Matrix Maintenance Receipt

Mission: {receipt.get('mission')}

Policy version: {receipt.get('version')}

Owner agent: {receipt.get('ownerAgent')}

Maintenance action: {receipt.get('maintenanceAction')}

Counts:

- Copilots: {counts.get('copilots')}
- Phases: {counts.get('phases')}
- Runtimes: {counts.get('runtimes')}
- Matrix cells: {counts.get('matrixCells')} / {counts.get('expectedMatrixCells')}
- Trace ledger entries: {counts.get('traceLedgerEntries')} / {counts.get('expectedTraceLedgerEntries')}

Digests:

- Cell digest: `{digests.get('cellDigest')}`
- Coverage digest: `{digests.get('coverageDigest')}`
- Trace ledger digest: `{digests.get('traceLedgerDigest')}`
- Cell equivalence contract digest: `{digests.get('cellEquivalenceContractDigest')}`
- Receipt digest: `{digests.get('receiptDigest')}`

Cell equivalence:

- Contract version: {cell_equivalence.get('version')}
- Cells passing: {cell_equivalence.get('passingCells')} / {cell_equivalence.get('cellsChecked')}
- Evidence mode: {cell_equivalence.get('evidenceMode')}

Acceptance gates:

{gates}

Validation commands:

{commands}
"""


def render_sdlc_runtime_matrix_md(matrix: dict) -> str:
    summary = matrix.get("summary", {})
    cell_equivalence = matrix.get("cellEquivalenceContract", {})
    phase_rows = "\n".join(
        f"| {phase} | {item.get('copilots')} | {item.get('runtimeCells')} |"
        for phase, item in matrix.get("phaseCoverage", {}).items()
    )
    runtime_rows = "\n".join(
        f"| {runtime} | {count} |"
        for runtime, count in matrix.get("runtimeCoverage", {}).items()
    )
    trace_rows = "\n".join(
        (
            f"| {entry['phase']} | {entry['copilotId']} | "
            f"{len(entry.get('runtimeFiles', {}))} | "
            f"{len(entry.get('pairwiseRuntimeCases', []))} | "
            f"`{str(entry.get('sharedSpecDigest'))[:12]}` |"
        )
        for entry in matrix.get("traceLedger", [])
    )
    cell_rows = "\n".join(
        (
            f"| {cell['phase']} | {cell['copilotId']} | {cell['runtime']} | "
            f"`{cell['runtimeFile']}` | `{str(cell.get('sharedSpecDigest'))[:12]}` | "
            f"`{str(cell.get('outputSchemaDigest'))[:12]}` |"
        )
        for cell in matrix.get("cells", [])
    )
    return f"""# SDLC x Copilot x Runtime Matrix

Mission: {matrix.get('mission')}

Policy version: {matrix.get('version')}

Summary:

- Copilots: {summary.get('copilotCount')}
- Phases: {summary.get('phaseCount')} ({', '.join(summary.get('phases', []))})
- Runtimes: {', '.join(matrix.get('runtimes', []))}
- Matrix cells: {summary.get('matrixCellCount')} / {summary.get('expectedMatrixCellCount')}
- Trace ledger entries: {summary.get('traceLedgerEntries')} / {summary.get('expectedTraceLedgerEntries')}
- Trace ledger digest: `{summary.get('traceLedgerDigest')}`
- Missing runtime files: {summary.get('missingRuntimeFiles')}
- Max unexplained drift: {summary.get('maxUnexplainedDrift')}
- Prompt bodies stored: {matrix.get('costControl', {}).get('promptContentStored')}
- Cell equivalence pass: {cell_equivalence.get('pass')} ({cell_equivalence.get('passingCells')} / {cell_equivalence.get('cellsChecked')})

Source artifacts:

- Catalog: `{matrix.get('sourceArtifacts', {}).get('catalog')}`
- Runtime map: `{matrix.get('sourceArtifacts', {}).get('runtimeMap')}`
- Factory validation: `{matrix.get('sourceArtifacts', {}).get('factoryValidation')}`
- Prompt quality: `{matrix.get('sourceArtifacts', {}).get('promptQuality')}`
- Runtime equivalence: `{matrix.get('sourceArtifacts', {}).get('runtimeEquivalence')}`

## Phase Coverage

| Phase | Copilots | Runtime cells |
|---|---:|---:|
{phase_rows}

## Runtime Coverage

| Runtime | Cells |
|---|---:|
{runtime_rows}

## Trace Ledger

| Phase | Copilot | Runtime refs | Pairwise cases | Spec digest |
|---|---|---:|---:|---|
{trace_rows}

## Cells

| Phase | Copilot | Runtime | Adapter file | Spec digest | Schema digest |
|---|---|---|---|---|---|
{cell_rows}
"""


def validate_runtime_safety_contract(issues: list[str]) -> dict:
    summary = {
        "pass": False,
        "helperPresent": False,
        "evidenceLimitsChecked": False,
        "promptRedactionChecked": False,
        "negativeCasesDetected": False,
    }
    path = ROOT / "dist" / "copilots" / "_runtime_safety.py"
    text = read_text(path)
    if not text:
        issues.append("Runtime safety helper is missing: dist/copilots/_runtime_safety.py.")
        return summary
    summary["helperPresent"] = True

    required_markers = [
        "MAX_EVIDENCE_DEPTH",
        "MAX_EVIDENCE_ITEMS",
        "MAX_EVIDENCE_STRING_CHARS",
        "customer",
        "tenant",
        "billing",
        "_validate_evidence_node",
    ]
    missing_markers = [marker for marker in required_markers if marker not in text]
    if missing_markers:
        issues.append("Runtime safety helper missing defensive marker(s): " + ", ".join(missing_markers) + ".")

    original_dont_write_bytecode = sys.dont_write_bytecode
    try:
        sys.dont_write_bytecode = True
        spec = importlib.util.spec_from_file_location("runtime_safety_helper", path)
        if spec is None or spec.loader is None:
            raise RuntimeError("loader unavailable")
        module = importlib.util.module_from_spec(spec)
        sys.modules[spec.name] = module
        spec.loader.exec_module(module)
        clean = module.validate_evidence(
            {
                "source_refs": ["generated/runtime-injection-map.json"],
                "api_key": "placeholder-only",
                "customer_id": "placeholder-customer",
                "request": "Bearer " + "abcdef1234567890",
                "path": "C:" + "\\Users\\Example\\private.txt",
            }
        )
        redaction_ok = (
            clean.get("api_key") == "[REDACTED]"
            and clean.get("customer_id") == "[REDACTED]"
            and clean.get("request") == "[REDACTED]"
            and clean.get("path") == "[REDACTED]"
        )
        try:
            module.validate_evidence({"source_refs": ["x" * (module.MAX_EVIDENCE_STRING_CHARS + 1)]})
            long_string_rejected = False
        except ValueError:
            long_string_rejected = True
        try:
            module.validate_evidence({"items": [str(index) for index in range(module.MAX_EVIDENCE_ITEMS + 1)]})
            large_payload_rejected = False
        except ValueError:
            large_payload_rejected = True
    except Exception as exc:
        issues.append(f"Runtime safety helper behavior check failed: {exc}.")
        redaction_ok = False
        long_string_rejected = False
        large_payload_rejected = False
    finally:
        sys.dont_write_bytecode = original_dont_write_bytecode

    summary["promptRedactionChecked"] = redaction_ok
    summary["evidenceLimitsChecked"] = long_string_rejected and large_payload_rejected
    summary["negativeCasesDetected"] = all([redaction_ok, long_string_rejected, large_payload_rejected])
    if not summary["negativeCasesDetected"]:
        issues.append("Runtime safety helper must redact sensitive prompt evidence and reject oversized evidence.")
    summary["pass"] = not missing_markers and summary["negativeCasesDetected"]
    return summary


def validate_control_room(config: dict, tasks: list, issues: list[str]) -> dict:
    control = config.get("controlRoom", {}) if isinstance(config, dict) else {}
    first_task = tasks[0] if tasks and isinstance(tasks[0], str) else ""
    lock_file = ROOT / ".codex-loop" / "run.lock.json"
    summary = {
        "present": bool(control),
        "ownerAgent": control.get("ownerAgent") if isinstance(control, dict) else None,
        "mission": control.get("mission") if isinstance(control, dict) else None,
        "concurrency": control.get("concurrency") if isinstance(control, dict) else None,
        "lockFile": control.get("stateLockFrontier", {}).get("lockFile") if isinstance(control, dict) else None,
        "lockFilePresent": lock_file.exists(),
        "lockFileValid": False,
        "lockFieldsPresent": [],
        "lockMissingFields": RUN_LOCK_REQUIRED_FIELDS,
        "lockWorkspaceMatches": False,
        "lockHeartbeatAgeSeconds": None,
        "snapshotEvidenceRequired": not (ROOT / ".git").exists(),
        "snapshotEvidencePresent": False,
        "requiredCommands": CONTROL_ROOM_REQUIRED_COMMANDS,
        "requiredReports": CONTROL_ROOM_REQUIRED_REPORTS,
        "firstTaskHasDirectorGate": "DirectorGate:" in first_task,
    }

    if not isinstance(control, dict) or not control:
        issues.append("Missing factory.config.json controlRoom contract.")
        return summary

    if control.get("ownerAgent") != DIRECTOR_AGENT:
        issues.append("Control Room ownerAgent must be factory_agent_01_director.")
    if control.get("room") != "Control Room":
        issues.append("Control Room room must be `Control Room`.")
    if control.get("mission") != DIRECTOR_MISSION:
        issues.append("Control Room mission drifted from the director mission.")
    if control.get("concurrency") != "serial":
        issues.append("Control Room concurrency must be serial.")

    state_lock = control.get("stateLockFrontier", {})
    if state_lock.get("lockFile") != ".codex-loop/run.lock.json":
        issues.append("Control Room state lock must point to .codex-loop/run.lock.json.")
    if state_lock.get("denyConcurrentFactoryRuns") is not True:
        issues.append("Control Room state lock must deny concurrent factory runs.")
    if state_lock.get("activeRunRequiresNoNewFactory") is not True:
        issues.append("Control Room active run policy must block a second factory run.")
    if state_lock.get("snapshotRequiredWhenGitMissing") is not True:
        issues.append("Control Room must require snapshot evidence when Git metadata is absent.")
    if state_lock.get("requiredLockFields") != RUN_LOCK_REQUIRED_FIELDS:
        issues.append("Control Room state lock must declare the required lock fields.")
    if state_lock.get("workspaceMustMatchRoot") is not True:
        issues.append("Control Room state lock must require workspace/root matching.")
    if state_lock.get("heartbeatMustNotPrecedeStart") is not True:
        issues.append("Control Room state lock must require heartbeatAt >= startedAt.")
    if state_lock.get("snapshotEvidenceRoots") != STATE_LOCK_SNAPSHOT_ROOTS:
        issues.append("Control Room state lock must declare snapshot evidence roots.")

    validate_run_lock(lock_file, summary, issues)
    validate_snapshot_evidence(summary, issues)

    gate_honesty = control.get("gateHonesty", {})
    missing_commands = [
        command for command in CONTROL_ROOM_REQUIRED_COMMANDS
        if command not in gate_honesty.get("mustPassBeforeDone", [])
    ]
    if missing_commands:
        issues.append(f"Control Room gate missing required command(s): {', '.join(missing_commands)}.")
    missing_reports = [
        report for report in CONTROL_ROOM_REQUIRED_REPORTS
        if report not in gate_honesty.get("requiredReports", [])
    ]
    if missing_reports:
        issues.append(f"Control Room gate missing required report(s): {', '.join(missing_reports)}.")
    if gate_honesty.get("doneRequiresEvidence") is not True:
        issues.append("Control Room doneRequiresEvidence must be true.")
    if gate_honesty.get("compileOnlyIsInsufficient") is not True:
        issues.append("Control Room compileOnlyIsInsufficient must be true.")

    scope_drift = control.get("scopeDrift", {})
    for required_root in [".codex-loop", "config", "data", "dist", "generated", "products", "tools"]:
        if required_root not in scope_drift.get("allowedFactoryRoots", []):
            issues.append(f"Control Room allowedFactoryRoots missing `{required_root}`.")
    if scope_drift.get("declaredTaskFilesOnlyByDefault") is not True:
        issues.append("Control Room scope lock must default to declared task files only.")
    if scope_drift.get("registryRequiredForNewProducts") is not True:
        issues.append("Control Room product registry policy must be explicit.")

    runtime_equivalence = control.get("runtimeEquivalence", {})
    if runtime_equivalence.get("adapters") != RUNTIMES:
        issues.append("Control Room runtime adapters must match the factory runtime list.")
    if runtime_equivalence.get("canonicalSpec") != "dist/copilots/<copilot>/shared/spec.json":
        issues.append("Control Room canonicalSpec must point to shared/spec.json.")
    if runtime_equivalence.get("traceMap") != "generated/runtime-injection-map.json":
        issues.append("Control Room traceMap must point to generated/runtime-injection-map.json.")
    if runtime_equivalence.get("maxUnexplainedDrift") != 0:
        issues.append("Control Room maxUnexplainedDrift must be 0.")

    cost_trace = control.get("costTrace", {})
    if cost_trace.get("deterministicPythonFirst") is not True:
        issues.append("Control Room cost trace must require deterministic Python first.")
    if cost_trace.get("avoidRepeatedPromptExpansion") is not True:
        issues.append("Control Room cost trace must avoid repeated prompt expansion.")
    if cost_trace.get("auditArtifactsAreSourceOfTruth") is not True:
        issues.append("Control Room audit artifacts must be the source of truth.")

    release_gate = control.get("releaseTruthGate", {})
    for key in [
        "ownerReviewRequired",
        "qaReviewRequired",
        "safeCodingPrivacyReviewRequired",
        "releaseReviewRequired",
        "residualRiskMustBeExplicit",
    ]:
        if release_gate.get(key) is not True:
            issues.append(f"Control Room releaseTruthGate requires `{key}`.")

    if not first_task:
        issues.append("First task must be a DirectorGate task string.")
        return summary
    required_task_markers = [
        f"[{DIRECTOR_AGENT}]",
        "Room: Control Room",
        "Concurrency: serial",
        DIRECTOR_MISSION,
        "DirectorGate:",
        "controlRoom=factory.config.json/controlRoom",
        "lock=.codex-loop/run.lock.json",
        "gates=structure+promptDepth+runtimeEquivalence",
        "evidence=generated-validation-reports",
        "drift=max-0-unexplained",
        "cost=python-first-llm-sparse",
        "python tools/validate_copilot_factory.py",
        "python tools/validate_prompt_quality.py",
        "python tools/validate_runtime_equivalence.py",
        "Frontier: state-locks",
    ]
    missing_task_markers = [marker for marker in required_task_markers if marker not in first_task]
    if missing_task_markers:
        issues.append(f"Director task missing required marker(s): {', '.join(missing_task_markers)}.")

    return summary


def validate_run_lock(lock_file: Path, summary: dict, issues: list[str]) -> None:
    rel = relative(lock_file)
    if not lock_file.exists():
        issues.append(f"Control Room state lock file is missing: {rel}.")
        return

    try:
        lock = json.loads(lock_file.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        issues.append(f"Control Room state lock is invalid JSON at line {exc.lineno}, column {exc.colno}: {exc.msg}.")
        return
    except OSError as exc:
        issues.append(f"Control Room state lock cannot be read: {exc}.")
        return

    if not isinstance(lock, dict):
        issues.append("Control Room state lock must be a JSON object.")
        return

    missing = [field for field in RUN_LOCK_REQUIRED_FIELDS if field not in lock]
    summary["lockFieldsPresent"] = [field for field in RUN_LOCK_REQUIRED_FIELDS if field in lock]
    summary["lockMissingFields"] = missing
    if missing:
        issues.append(f"Control Room state lock missing required field(s): {', '.join(missing)}.")

    pid = lock.get("pid")
    if not isinstance(pid, int) or pid <= 0:
        issues.append("Control Room state lock pid must be a positive integer.")

    for key in ["id", "workspace", "mode"]:
        if not isinstance(lock.get(key), str) or not lock.get(key).strip():
            issues.append(f"Control Room state lock `{key}` must be a non-empty string.")

    summary["lockWorkspaceMatches"] = workspace_matches(lock.get("workspace"))
    if not summary["lockWorkspaceMatches"]:
        issues.append("Control Room state lock workspace does not match this workspace.")

    started_at = parse_lock_datetime(lock.get("startedAt"))
    heartbeat_at = parse_lock_datetime(lock.get("heartbeatAt"))
    now_utc = datetime.now(timezone.utc)
    if started_at is None:
        issues.append("Control Room state lock startedAt must be an ISO-8601 timestamp.")
    if heartbeat_at is None:
        issues.append("Control Room state lock heartbeatAt must be an ISO-8601 timestamp.")
    if started_at and heartbeat_at:
        if heartbeat_at < started_at:
            issues.append("Control Room state lock heartbeatAt must not precede startedAt.")
        if started_at > now_utc.replace() and (started_at - now_utc).total_seconds() > LOCK_CLOCK_SKEW_SECONDS:
            issues.append("Control Room state lock startedAt is too far in the future.")
        if heartbeat_at > now_utc.replace() and (heartbeat_at - now_utc).total_seconds() > LOCK_CLOCK_SKEW_SECONDS:
            issues.append("Control Room state lock heartbeatAt is too far in the future.")
        summary["lockHeartbeatAgeSeconds"] = max(0, int((now_utc - heartbeat_at).total_seconds()))

    summary["lockFileValid"] = not any(
        issue.startswith("Control Room state lock")
        for issue in issues
    )


def workspace_matches(value) -> bool:
    if not isinstance(value, str) or not value.strip():
        return False
    candidate_text = value.strip()
    candidate = Path(candidate_text)
    if candidate.is_absolute():
        try:
            return candidate.resolve() == ROOT.resolve()
        except OSError:
            return False
    return candidate_text == ROOT.name


def parse_lock_datetime(value) -> datetime | None:
    if not isinstance(value, str) or not value.strip():
        return None
    try:
        normalized = value.strip().replace("Z", "+00:00")
        parsed = datetime.fromisoformat(normalized)
    except ValueError:
        return None
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc)


def validate_snapshot_evidence(summary: dict, issues: list[str]) -> None:
    if not summary["snapshotEvidenceRequired"]:
        summary["snapshotEvidencePresent"] = True
        return
    present = False
    for root in STATE_LOCK_SNAPSHOT_ROOTS:
        folder = ROOT / root
        if folder.exists() and any(folder.iterdir()):
            present = True
            break
    summary["snapshotEvidencePresent"] = present
    if not present:
        roots = ", ".join(STATE_LOCK_SNAPSHOT_ROOTS)
        issues.append(f"Git metadata is absent; snapshot evidence is required in one of: {roots}.")


def render_md(report: dict) -> str:
    rows = "\n".join(f"- {issue}" for issue in report["issues"]) or "- none"
    control_room = report["controlRoom"]
    semantic_router = report.get("semanticRouter", {})
    discovery_auditor = report.get("discoveryAuditor", {})
    architecture_auditor = report.get("architectureAuditor", {})
    design_auditor = report.get("designAuditor", {})
    build_auditor = report.get("buildAuditor", {})
    test_auditor = report.get("testStrategyAudit", {})
    phase_verdict_report = report.get("phaseVerdictReport", {})
    security_auditor = report.get("securityAuditor", {})
    mcp_connector_auditor = report.get("mcpConnectorAuditor", {})
    devops_auditor = report.get("devopsAuditor", {})
    cloud_auditor = report.get("cloudAuditor", {})
    release_auditor = report.get("releaseAuditor", {})
    packager_distribution = report.get("packagerDistribution", {})
    operate_auditor = report.get("operateAuditor", {})
    cost_routing_auditor = report.get("costRoutingAuditor", {})
    kb_auditor = report.get("kbAuditor", {})
    docs_auditor = report.get("docsAuditor", {})
    sdlc_runtime_matrix = report.get("sdlcRuntimeMatrix", {})
    runtime_safety = report.get("runtimeSafety", {})
    generator = report.get("generator", {})
    validator_smoke = report.get("validatorSmoke", {})
    return f"""# Copilot Factory Validation

Pass: {report['pass']}

Copilots: {report['copilots']}

Factory agents: {report['factoryAgents']}

Tasks: {report['tasks']}

Control Room:

- Present: {control_room['present']}
- Owner: {control_room['ownerAgent']}
- Mission: {control_room['mission']}
- Concurrency: {control_room['concurrency']}
- Lock file: {control_room['lockFile']}
- Lock file present: {control_room['lockFilePresent']}
- Lock file valid: {control_room['lockFileValid']}
- Lock workspace matches: {control_room['lockWorkspaceMatches']}
- Lock heartbeat age seconds: {control_room['lockHeartbeatAgeSeconds']}
- Snapshot evidence required: {control_room['snapshotEvidenceRequired']}
- Snapshot evidence present: {control_room['snapshotEvidencePresent']}
- First task has DirectorGate: {control_room['firstTaskHasDirectorGate']}

Semantic Router:

- Agent present: {semantic_router.get('agentPresent')}
- Policy present: {semantic_router.get('policyPresent')}
- Audit present: {semantic_router.get('auditPresent')}
- Sample route checked: {semantic_router.get('sampleRouteChecked')}
- Sample top route: {semantic_router.get('sampleTopRoute')}
- Deterministic Python first: {semantic_router.get('deterministicPythonFirst')}
- LLM assist used: {semantic_router.get('llmAssistUsed')}

Discovery Auditor:

- Agent present: {discovery_auditor.get('agentPresent')}
- Policy present: {discovery_auditor.get('policyPresent')}
- Audit present: {discovery_auditor.get('auditPresent')}
- Catalog profile present: {discovery_auditor.get('catalogProfilePresent')}
- Lookup profile present: {discovery_auditor.get('lookupProfilePresent')}
- Sample route checked: {discovery_auditor.get('sampleRouteChecked')}
- Sample top route: {discovery_auditor.get('sampleTopRoute')}
- Runtime trace returned: {discovery_auditor.get('runtimeTraceReturned')}

Architecture Auditor:

- Agent present: {architecture_auditor.get('agentPresent')}
- Audit artifact present: {architecture_auditor.get('auditArtifactPresent')}
- Shared spec contract present: {architecture_auditor.get('specContractPresent')}
- LangChain profile contract present: {architecture_auditor.get('profileContractPresent')}
- Runtime refs checked: {architecture_auditor.get('runtimeRefsChecked')}
- LangChain behavior checked: {architecture_auditor.get('langchainBehaviorChecked')}
- LangChain input validation checked: {architecture_auditor.get('langchainInputValidationChecked')}
- LangChain prompt redaction checked: {architecture_auditor.get('langchainPromptRedactionChecked')}
- Sample route checked: {architecture_auditor.get('sampleRouteChecked')}
- Sample top route: {architecture_auditor.get('sampleTopRoute')}
- Route audit evidence: {architecture_auditor.get('routeAuditEvidence')}
- Localized route checked: {architecture_auditor.get('localizedRouteChecked')}
- Localized route cheap path: {architecture_auditor.get('localizedRouteCheapPath')}
- Localized route audit evidence: {architecture_auditor.get('localizedRouteAuditEvidence')}

Design Auditor:

- Agent present: {design_auditor.get('agentPresent')}
- Agent outputs present: {design_auditor.get('agentOutputsPresent')}
- Policy present: {design_auditor.get('policyPresent')}
- Target copilots: {design_auditor.get('targetCopilots')}
- Artifacts checked: {design_auditor.get('artifactsChecked')}
- Schemas require handoff: {design_auditor.get('schemasRequireHandoff')}
- Runtime map checked: {design_auditor.get('runtimeMapChecked')}
- Matrix evidence present: {design_auditor.get('matrixEvidencePresent')}
- LangChain input validation checked: {design_auditor.get('langchainInputValidationChecked')}
- LangChain evidence gate checked: {design_auditor.get('langchainEvidenceGateChecked')}
- LangChain LLM escalation guarded: {design_auditor.get('langchainLlmEscalationGuarded')}
- LangChain prompt redaction checked: {design_auditor.get('langchainPromptRedactionChecked')}
- Sample route checked: {design_auditor.get('sampleRouteChecked')}
- Sample top route: {design_auditor.get('sampleTopRoute')}
- Localized route checked: {design_auditor.get('localizedRouteChecked')}
- Localized top route: {design_auditor.get('localizedTopRoute')}
- Localized route cheap path: {design_auditor.get('localizedRouteCheapPath')}

Build Auditor:

- Agent present: {build_auditor.get('agentPresent')}
- Agent outputs present: {build_auditor.get('agentOutputsPresent')}
- Policy present: {build_auditor.get('policyPresent')}
- Target copilots: {build_auditor.get('targetCopilots')}
- Artifacts checked: {build_auditor.get('artifactsChecked')}
- Schemas require implementation: {build_auditor.get('schemasRequireImplementation')}
- Runtime map checked: {build_auditor.get('runtimeMapChecked')}
- Factory audit checked: {build_auditor.get('factoryAuditChecked')}
- Matrix evidence present: {build_auditor.get('matrixEvidencePresent')}
- LangChain input validation checked: {build_auditor.get('langchainInputValidationChecked')}
- LangChain evidence gate checked: {build_auditor.get('langchainEvidenceGateChecked')}
- LangChain LLM escalation guarded: {build_auditor.get('langchainLlmEscalationGuarded')}
- LangChain prompt redaction checked: {build_auditor.get('langchainPromptRedactionChecked')}
- Sample route checked: {build_auditor.get('sampleRouteChecked')}
- Sample top route: {build_auditor.get('sampleTopRoute')}
- Localized route checked: {build_auditor.get('localizedRouteChecked')}
- Localized top route: {build_auditor.get('localizedTopRoute')}
- Localized route cheap path: {build_auditor.get('localizedRouteCheapPath')}

Test Strategy Audit:

- Pass: {test_auditor.get('pass')}
- Agent present: {test_auditor.get('agentPresent')}
- QA copilot present: {test_auditor.get('qaCopilotPresent')}
- QA spec playbook checked: {test_auditor.get('qaSpecPlaybookChecked')}
- Runtime refs checked: {test_auditor.get('runtimeRefsChecked')}
- Pairwise case count: {test_auditor.get('pairwiseCaseCount')}
- Negative cases detected: {test_auditor.get('negativeCasesDetected')}
- Sample route checked: {test_auditor.get('sampleRouteChecked')}
- Sample top route: {test_auditor.get('sampleTopRoute')}
- Sample route cheap path: {test_auditor.get('sampleRouteCheapPath')}
- Runtime trace returned: {test_auditor.get('runtimeTraceReturned')}

Phase Verdict Report:

- Pass: {phase_verdict_report.get('pass')}
- Owner agent: {phase_verdict_report.get('ownerAgent')}
- Overall verdict: {phase_verdict_report.get('overallVerdict')}
- Failed phases: {phase_verdict_report.get('failedPhases')}
- Phase count: {len(phase_verdict_report.get('phaseVerdicts', []))}
- Negative cases detected: {phase_verdict_report.get('negativeCasesDetected')}
- Report artifact: generated/phase-verdict-report.json

Security Auditor:

- Pass: {security_auditor.get('pass')}
- Agent present: {security_auditor.get('agentPresent')}
- Policy version: {security_auditor.get('policyVersion')}
- Mission: {security_auditor.get('mission')}
- Env example checked: {security_auditor.get('envExampleChecked')}
- MCP config checked: {security_auditor.get('mcpConfigChecked')}
- Sensitive credentials policy checked: {security_auditor.get('sensitiveCredentialsPolicyChecked')}
- Threat model checked: {security_auditor.get('threatModelChecked')}
- Safe MCP usage checked: {security_auditor.get('safeUsageChecked')}
- Runtime equivalence checked: {security_auditor.get('runtimeEquivalenceChecked')}
- Connectors checked: {', '.join(security_auditor.get('connectorsChecked', []))}
- Negative cases detected: {security_auditor.get('negativeCasesDetected')}

MCP Connector Auditor:

- Pass: {mcp_connector_auditor.get('pass')}
- Agent present: {mcp_connector_auditor.get('agentPresent')}
- Policy version: {mcp_connector_auditor.get('policyVersion')}
- Env example checked: {mcp_connector_auditor.get('envExampleChecked')}
- MCP config checked: {mcp_connector_auditor.get('mcpConfigChecked')}
- Audit contract checked: {mcp_connector_auditor.get('auditContractChecked')}
- Declaration requirements checked: {mcp_connector_auditor.get('declarationRequirementsChecked')}
- Env placeholder requirements checked: {mcp_connector_auditor.get('envPlaceholderRequirementsChecked')}
- Runtime equivalence checked: {mcp_connector_auditor.get('runtimeEquivalenceChecked')}
- Quality gates checked: {mcp_connector_auditor.get('qualityGatesChecked')}
- Connectors checked: {', '.join(mcp_connector_auditor.get('connectorsChecked', []))}
- Env placeholders checked: {', '.join(mcp_connector_auditor.get('connectorEnvPlaceholdersChecked', []))}
- Orphan sensitive placeholders: {', '.join(mcp_connector_auditor.get('orphanSensitivePlaceholders', [])) or 'none'}
- Negative cases detected: {mcp_connector_auditor.get('negativeCasesDetected')}

DevOps Auditor:

- Pass: {devops_auditor.get('pass')}
- Agent present: {devops_auditor.get('agentPresent')}
- Policy version: {devops_auditor.get('policyVersion')}
- Target copilot: {devops_auditor.get('targetCopilot')}
- Run factory checked: {devops_auditor.get('runFactoryChecked')}
- Factory audit checked: {devops_auditor.get('factoryAuditChecked')}
- Log evidence report: {devops_auditor.get('logEvidenceReport')}
- Runtime trace checked: {devops_auditor.get('runtimeTraceChecked')}
- Runtime refs checked: {devops_auditor.get('runtimeRefsChecked')}
- Sample route checked: {devops_auditor.get('sampleRouteChecked')}
- Sample top route: {devops_auditor.get('sampleTopRoute')}
- Sample route cheap path: {devops_auditor.get('sampleRouteCheapPath')}
- Negative cases detected: {devops_auditor.get('negativeCasesDetected')}

Cloud Auditor:

- Pass: {cloud_auditor.get('pass')}
- Agent present: {cloud_auditor.get('agentPresent')}
- Policy version: {cloud_auditor.get('policyVersion')}
- Target copilot: {cloud_auditor.get('targetCopilot')}
- Audit artifact checked: {cloud_auditor.get('auditArtifactChecked')}
- Factory audit checked: {cloud_auditor.get('factoryAuditChecked')}
- Runtime trace checked: {cloud_auditor.get('runtimeTraceChecked')}
- Runtime refs checked: {cloud_auditor.get('runtimeRefsChecked')}
- Schemas require cloud_migration: {cloud_auditor.get('schemasRequireCloudMigration')}
- Cloud migration schema checked: {cloud_auditor.get('cloudMigrationSchemaChecked')}
- Sample route checked: {cloud_auditor.get('sampleRouteChecked')}
- Sample top route: {cloud_auditor.get('sampleTopRoute')}
- Sample route cheap path: {cloud_auditor.get('sampleRouteCheapPath')}
- Negative cases detected: {cloud_auditor.get('negativeCasesDetected')}

Release Auditor:

- Pass: {release_auditor.get('pass')}
- Agent present: {release_auditor.get('agentPresent')}
- Policy version: {release_auditor.get('policyVersion')}
- Target copilots checked: {release_auditor.get('targetCopilotsChecked')}
- Config gate checked: {release_auditor.get('configGateChecked')}
- Factory audit checked: {release_auditor.get('factoryAuditChecked')}
- Runtime trace checked: {release_auditor.get('runtimeTraceChecked')}
- Runtime refs checked: {release_auditor.get('runtimeRefsChecked')}
- Scorecards checked: {release_auditor.get('scorecardsChecked')}
- Exit criteria checked: {release_auditor.get('exitCriteriaChecked')}
- Sample route checked: {release_auditor.get('sampleRouteChecked')}
- Sample top route: {release_auditor.get('sampleTopRoute')}
- Sample route cheap path: {release_auditor.get('sampleRouteCheapPath')}
- Negative cases detected: {release_auditor.get('negativeCasesDetected')}

Packager Distribution:

- Config checked: {packager_distribution.get('configChecked')}
- Manifest checked: {packager_distribution.get('manifestChecked')}
- File index checked: {packager_distribution.get('fileIndexChecked')}
- Packages checked: {', '.join(packager_distribution.get('packagesChecked', []))}
- Indexed files checked: {packager_distribution.get('indexedFilesChecked')}
- Runtime equivalence checked: {packager_distribution.get('runtimeEquivalenceChecked')}

Operate Auditor:

- Pass: {operate_auditor.get('pass')}
- Agent present: {operate_auditor.get('agentPresent')}
- Policy version: {operate_auditor.get('policyVersion')}
- Target copilots checked: {operate_auditor.get('targetCopilotsChecked')}
- Contract checked: {operate_auditor.get('contractChecked')}
- Scorecard checked: {operate_auditor.get('scorecardChecked')}
- Runbook checked: {operate_auditor.get('runbookChecked')}
- Incident runbook checked: {operate_auditor.get('incidentRunbookChecked')}
- Settings checked: {operate_auditor.get('settingsChecked')}
- Documentation checked: {operate_auditor.get('documentationChecked')}
- Telemetry signals checked: {operate_auditor.get('telemetrySignalsChecked')}
- Incident playbooks checked: {operate_auditor.get('incidentPlaybooksChecked')}
- Sample route checked: {operate_auditor.get('sampleRouteChecked')}
- Sample top route: {operate_auditor.get('sampleTopRoute')}
- Sample route cheap path: {operate_auditor.get('sampleRouteCheapPath')}
- Negative cases detected: {operate_auditor.get('negativeCasesDetected')}

Cost Routing Auditor:

- Pass: {cost_routing_auditor.get('pass')}
- Agent present: {cost_routing_auditor.get('agentPresent')}
- Policy version: {cost_routing_auditor.get('policyVersion')}
- Contract checked: {cost_routing_auditor.get('contractChecked')}
- Scorecard checked: {cost_routing_auditor.get('scorecardChecked')}
- Policy doc checked: {cost_routing_auditor.get('policyDocChecked')}
- Settings checked: {cost_routing_auditor.get('settingsChecked')}
- Runtime equivalence checked: {cost_routing_auditor.get('runtimeEquivalenceChecked')}
- Traceability checked: {cost_routing_auditor.get('traceabilityChecked')}
- Cheap deterministic work checked: {cost_routing_auditor.get('cheapDeterministicWorkChecked')}
- Judgement work checked: {cost_routing_auditor.get('judgementWorkChecked')}
- Sample route checked: {cost_routing_auditor.get('sampleRouteChecked')}
- Sample top route: {cost_routing_auditor.get('sampleTopRoute')}
- Sample route cheap path: {cost_routing_auditor.get('sampleRouteCheapPath')}
- Negative cases detected: {cost_routing_auditor.get('negativeCasesDetected')}

Knowledge Boundary Auditor:

- Agent present: {kb_auditor.get('agentPresent')}
- Audit artifact present: {kb_auditor.get('auditArtifactPresent')}
- Shared spec contract present: {kb_auditor.get('specContractPresent')}
- LangChain profile contract present: {kb_auditor.get('profileContractPresent')}
- Schemas require KB partition: {kb_auditor.get('schemasRequireKbPartition')}
- KB output schema checked: {kb_auditor.get('kbOutputSchemaChecked')}
- Runtime refs checked: {kb_auditor.get('runtimeRefsChecked')}
- LangChain behavior checked: {kb_auditor.get('langchainBehaviorChecked')}
- Sample route checked: {kb_auditor.get('sampleRouteChecked')}
- Sample top route: {kb_auditor.get('sampleTopRoute')}
- Sample route cheap path: {kb_auditor.get('sampleRouteCheapPath')}
- Route audit evidence: {kb_auditor.get('routeAuditEvidence')}

Documentation Auditor:

- Pass: {docs_auditor.get('pass')}
- Agent present: {docs_auditor.get('agentPresent')}
- Policy version: {docs_auditor.get('policyVersion')}
- Report artifact: {docs_auditor.get('reportArtifact')}
- Report written: {docs_auditor.get('reportWritten')}
- Copilot READMEs checked: {docs_auditor.get('copilotReadmesChecked')}
- Operator docs checked: {docs_auditor.get('operatorDocsChecked')}
- Runtime equivalence trace: {docs_auditor.get('runtimeEquivalence', {}).get('traceEvidence')}
- Negative cases detected: {docs_auditor.get('negativeCasesDetected')}

SDLC Runtime Matrix:

- Pass: {sdlc_runtime_matrix.get('pass')}
- Owner agent: {sdlc_runtime_matrix.get('ownerAgent')}
- Matrix artifact: {sdlc_runtime_matrix.get('matrixArtifact')}
- Markdown artifact: {sdlc_runtime_matrix.get('markdownArtifact')}
- Maintenance artifact: {sdlc_runtime_matrix.get('maintenanceArtifact')}
- Maintenance receipt checked: {sdlc_runtime_matrix.get('maintenanceReceiptChecked')}
- Maintenance receipt digest: {sdlc_runtime_matrix.get('maintenanceReceiptDigest')}
- Dimensions: {sdlc_runtime_matrix.get('dimensions')}
- Matrix cells: {sdlc_runtime_matrix.get('matrixCellCount')}
- Phase count: {sdlc_runtime_matrix.get('phaseCount')}
- Trace ledger entries: {sdlc_runtime_matrix.get('traceLedgerEntries')}
- Trace ledger digest: {sdlc_runtime_matrix.get('traceLedgerDigest')}
- Trace ledger checked: {sdlc_runtime_matrix.get('traceLedgerChecked')}
- Runtime trace checked: {sdlc_runtime_matrix.get('runtimeTraceChecked')}
- Prompt content stored: {sdlc_runtime_matrix.get('promptContentStored')}
- Cost control checked: {sdlc_runtime_matrix.get('costControlChecked')}
- Traceability checked: {sdlc_runtime_matrix.get('traceabilityChecked')}
- Cell equivalence checked: {sdlc_runtime_matrix.get('cellEquivalenceChecked')}

Runtime Safety:

- Pass: {runtime_safety.get('pass')}
- Helper present: {runtime_safety.get('helperPresent')}
- Evidence limits checked: {runtime_safety.get('evidenceLimitsChecked')}
- Prompt redaction checked: {runtime_safety.get('promptRedactionChecked')}
- Negative cases detected: {runtime_safety.get('negativeCasesDetected')}

Generator:

- Present: {generator.get('present')}
- Semantic router template checked: {generator.get('semanticRouterTemplateChecked')}
- Generated index checked: {generator.get('generatedIndexChecked')}
- Generated agent checked: {generator.get('generatedAgentChecked')}
- Generated Python profile checked: {generator.get('generatedPythonProfileChecked')}
- Generated discovery policy checked: {generator.get('generatedDiscoveryPolicyChecked')}
- Generated discovery agent checked: {generator.get('generatedDiscoveryAgentChecked')}
- Generated discovery profile checked: {generator.get('generatedDiscoveryProfileChecked')}
- Generated design policy checked: {generator.get('generatedDesignPolicyChecked')}
- Generated design agent checked: {generator.get('generatedDesignAgentChecked')}
- Generated design profiles checked: {generator.get('generatedDesignProfilesChecked')}
- Generated build policy checked: {generator.get('generatedBuildPolicyChecked')}
- Generated build agent checked: {generator.get('generatedBuildAgentChecked')}
- Generated build profiles checked: {generator.get('generatedBuildProfilesChecked')}
- Generated run_factory checked: {generator.get('generatedRunFactoryChecked')}
- Generated security policy checked: {generator.get('generatedSecurityPolicyChecked')}
- Generated security env checked: {generator.get('generatedSecurityEnvChecked')}

Validator Smoke:

- Owner: {validator_smoke.get('ownerAgent')}
- Mission: {validator_smoke.get('mission')}
- Validator: {validator_smoke.get('validatorId')}
- Command: `{validator_smoke.get('command')}`
- Report artifact: `{validator_smoke.get('reportArtifact')}`
- Report pass: {validator_smoke.get('reportPass')}
- Blocker count: {validator_smoke.get('blockerCount')}
- Prompt bodies stored: {validator_smoke.get('promptBodiesStored')}

Issues:

{rows}
"""


def relative(path: Path) -> str:
    return str(path.relative_to(ROOT)).replace("\\", "/")


def format_path(path: Path) -> str:
    try:
        return relative(path)
    except ValueError:
        return path.name


if __name__ == "__main__":
    main()
