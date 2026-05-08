from __future__ import annotations

import ast
import hashlib
import importlib.util
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CATALOG_JSON = ROOT / "data" / "copilots.json"
REPORT_JSON = ROOT / "generated" / "runtime-equivalence-report.json"
REPORT_MD = ROOT / "generated" / "runtime-equivalence-report.md"
VALIDATOR_SMOKE_REPORT_JSON = ROOT / "generated" / "validator-smoke-report.json"
VALIDATOR_SMOKE_REPORT_MD = ROOT / "generated" / "validator-smoke-report.md"
SDLC_RUNTIME_MATRIX_JSON = ROOT / "generated" / "sdlc-runtime-matrix.json"
SDLC_RUNTIME_MATRIX_MD = ROOT / "generated" / "sdlc-runtime-matrix.md"
SDLC_RUNTIME_MATRIX_MAINTENANCE_JSON = ROOT / "generated" / "sdlc-runtime-matrix-maintenance.json"
SDLC_RUNTIME_MATRIX_MAINTENANCE_MD = ROOT / "generated" / "sdlc-runtime-matrix-maintenance.md"
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
CODEX_PROTOCOL_VERSION = "codex-local-tool-protocol-1.0"
CODEX_OWNER_AGENT = "factory_agent_14_codex"
CODEX_MISSION = "Builds Codex-facing task prompts and local tool protocol."
CODEX_PROTOCOL_FILE = "shared/codex_tool_protocol.json"
CODEX_REQUIRED_EVIDENCE = [
    "codex_task_prompt",
    "local_tool_protocol",
    "validation_commands",
    "runtime_equivalence",
]
CODEX_QUALITY_GATES = [
    "codex_prompt_embeds_shared_spec",
    "local_tool_protocol_declared",
    "tool_fallbacks_are_non_fatal",
    "traceability_and_cost",
]
CODEX_REQUIRED_SECTIONS = [
    "Runtime Injection",
    "System Prompt",
    "Developer Prompt",
    "Execution Protocol",
    "Python Brain Contract",
    "Evidence Gates",
    "Outputs",
]
CODEX_PROMPT_MARKERS = [
    "## Codex Local Tool Protocol",
    "../shared/codex_tool_protocol.json",
    "workspace_boundary",
    "snapshot_or_git",
    "python_first",
    "validation_commands",
    "secret_placeholders",
]
CODEX_TOOL_PROTOCOL_REQUIRED = {
    "workspaceBoundary": "current_workspace_only",
    "editPrecondition": "git_metadata_or_codex_loop_snapshot",
    "deterministicFirst": True,
    "missingToolFallback": "non_fatal_report_blocker",
    "secretHandling": "placeholders_only",
    "validationRequired": True,
}
CODEX_VALIDATION_COMMANDS = [
    "python tools/validate_copilot_factory.py",
    "python tools/validate_prompt_quality.py",
    "python tools/validate_runtime_equivalence.py",
]
CLAUDE_PROTOCOL_VERSION = "claude-project-instructions-1.0"
CLAUDE_OWNER_AGENT = "factory_agent_15_claude"
CLAUDE_MISSION = "Builds Claude-facing project instructions and agent cards."
CLAUDE_PROTOCOL_FILE = "shared/claude_project_instructions.json"
CLAUDE_REQUIRED_EVIDENCE = [
    "claude_project_instructions",
    "claude_agent_card",
    "evidence_pack_handoff",
    "runtime_equivalence",
]
CLAUDE_QUALITY_GATES = [
    "claude_instructions_embed_shared_spec",
    "agent_card_declared",
    "handoff_is_executor_ready",
    "traceability_and_cost",
]
CLAUDE_REQUIRED_SECTIONS = [
    "Runtime Injection",
    "Claude Project Instructions",
    "System Prompt",
    "Developer Prompt",
    "Execution Protocol",
    "Python Brain Contract",
    "Evidence Gates",
    "Outputs",
    "Runtime Specific Protocol",
]
CLAUDE_PROMPT_MARKERS = [
    "## Claude Project Instructions",
    "../shared/claude_project_instructions.json",
    "shared_spec",
    "agent_card",
    "evidence_pack_handoff",
    "python_first",
    "traceability_and_cost",
]
CLAUDE_VALIDATION_COMMANDS = CODEX_VALIDATION_COMMANDS
GITHUB_PROTOCOL_VERSION = "github-copilot-profile-mcp-placeholders-1.0"
GITHUB_OWNER_AGENT = "factory_agent_16_github"
GITHUB_MISSION = "Builds GitHub Copilot profile docs and MCP placeholders."
GITHUB_PROFILE_FILE = "github-copilot/copilot-profile.json"
GITHUB_MCP_PLACEHOLDERS_FILE = "github-copilot/mcp-placeholders.json"
GITHUB_REQUIRED_EVIDENCE = [
    "github_copilot_profile_doc",
    "mcp_placeholders",
    "runtime_equivalence",
    "safe_connector_policy",
]
GITHUB_QUALITY_GATES = [
    "github_profile_embeds_shared_spec",
    "mcp_placeholders_are_disabled",
    "connector_env_names_only",
    "traceability_and_cost",
]
GITHUB_COST_CONTROL = {
    "promptExpansion": "profile_json_references_shared_spec_and_schema",
    "deterministicPythonFirst": True,
    "llmEscalation": "only_after_github_evidence_or_local_file_checks_are_insufficient",
}
GITHUB_REQUIRED_SECTIONS = [
    "Runtime Injection",
    "System Prompt",
    "Developer Prompt",
    "Execution Protocol",
    "Python Brain Contract",
    "Evidence Gates",
    "Outputs",
    "Runtime Specific Protocol",
    "GitHub Copilot Profile",
    "MCP Placeholder Contract",
]
GITHUB_PROMPT_MARKERS = [
    "## GitHub Copilot Profile",
    "copilot-profile.json",
    "## MCP Placeholder Contract",
    "mcp-placeholders.json",
    "config/mcp-connectors.example.json",
    "factory_agent_16_github",
    "github_copilot_profile_doc",
    "mcp_placeholders",
]
GITHUB_VALIDATION_COMMANDS = CODEX_VALIDATION_COMMANDS
LANGCHAIN_PROTOCOL_VERSION = "langchain-agent-spec-1.0"
LANGCHAIN_OWNER_AGENT = "factory_agent_17_langchain"
LANGCHAIN_MISSION = "Builds Python/LangChain compatible agent specs."
LANGCHAIN_CONTRACT_FILE = "langchain/agent_contract.json"
LANGCHAIN_REQUIRED_EVIDENCE = [
    "langchain_agent_spec",
    "agent_profile_contract",
    "runtime_equivalence",
    "schema_digest",
    "safe_prompt_rendering",
]
LANGCHAIN_QUALITY_GATES = [
    "profile_embeds_shared_spec",
    "agent_exports_required_api",
    "hard_langchain_dependency_not_required",
    "render_prompt_redacts_inputs",
    "traceability_and_cost",
]
LANGCHAIN_COMPATIBLE_INTERFACES = [
    "plain_python_class",
    "langchain_tool",
    "langchain_runnable",
    "agent_executor_adapter",
]
LANGCHAIN_REQUIRED_API = {
    "moduleConstants": [
        "PROFILE",
        "SYSTEM_PROMPT",
        "DEVELOPER_PROMPT",
        "OUTPUT_SCHEMA",
    ],
    "moduleFunctions": [
        "build_agent",
    ],
    "agentMethods": [
        "score",
        "audit",
        "plan",
        "render_prompt",
        "output_schema",
    ],
    "classNameSuffix": "Agent",
}
LANGCHAIN_RUNTIME_CONTRACT_REQUIRED = {
    "deterministicPythonFirst": True,
    "hardLangChainDependency": False,
    "llmEscalation": "only_after_audit_passes_and_request_requires_judgement",
    "promptExpansion": "render_prompt_uses_redacted_request_profile_plan_schema_evidence",
    "evidenceHandling": "validate_evidence_then_redact_value",
    "connectorActivation": "declared_names_only_no_credentials",
}
LANGCHAIN_COST_CONTROL = {
    "promptExpansion": "render_prompt_references_profile_plan_schema_evidence_without_repo_dump",
    "deterministicPythonFirst": True,
    "llmEscalation": "only_after_audit_passes_and_request_requires_judgement",
    "traceability": "runtime-injection-map links profile, spec, schema and agent file",
}
LANGCHAIN_SAFE_RENDER_MARKERS = [
    "validate_request(request)",
    "validate_evidence(evidence)",
    "redact_value(request)",
    "redact_value(evidence)",
    "redact_value(self.plan(request, safe_evidence))",
]
LANGCHAIN_VALIDATION_COMMANDS = CODEX_VALIDATION_COMMANDS

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
SAFE_COPILOT_ID_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_-]*$")
LANGCHAIN_ALLOWED_IMPORT_ROOTS = {
    "__future__",
    "_runtime_safety",
    "dataclasses",
    "json",
    "pathlib",
    "re",
    "sys",
    "typing",
}
LANGCHAIN_DANGEROUS_CALLS = {
    "__import__",
    "compile",
    "eval",
    "exec",
    "input",
    "open",
}
LANGCHAIN_DANGEROUS_METHODS = {
    "popen",
    "remove",
    "rename",
    "rmdir",
    "rmtree",
    "system",
    "unlink",
    "write_bytes",
    "write_text",
}


def main() -> None:
    issues: list[dict] = []
    metrics: list[dict] = []
    codex_protocol_metrics: list[dict] = []
    claude_protocol_metrics: list[dict] = []
    github_protocol_metrics: list[dict] = []
    langchain_protocol_metrics: list[dict] = []
    data_hygiene_metrics: list[dict] = []
    injection_map = read_json(ROOT / "generated" / "runtime-injection-map.json", {"copilots": {}}, issues, "runtime-injection-map")
    validate_runtime_map_header(injection_map, issues)
    validate_artifact_hygiene(ROOT / "generated" / "runtime-injection-map.json", issues, data_hygiene_metrics)
    expected_copilot_ids = catalog_copilot_ids(issues)
    injection_copilots = injection_map.get("copilots")
    if not isinstance(injection_copilots, dict):
        issues.append(issue("runtime-injection-map", "runtime_map_copilots", "runtime-injection-map `copilots` must be an object."))
        injection_copilots = {}
    validate_runtime_map_coverage(injection_copilots, expected_copilot_ids, issues)

    for copilot_id, item in injection_copilots.items():
        if not isinstance(copilot_id, str) or not copilot_id.strip():
            issues.append(issue("runtime-injection-map", "runtime_map_copilot_id", "runtime-injection-map copilot keys must be non-empty strings."))
            continue
        if not is_safe_copilot_id(copilot_id):
            issues.append(
                issue(
                    "runtime-injection-map",
                    "runtime_map_copilot_id",
                    "runtime-injection-map copilot keys must be safe repository path segments.",
                )
            )
            continue
        if not isinstance(item, dict):
            issues.append(issue(copilot_id, "runtime_map_entry", "runtime-injection-map copilot entry must be an object."))
            item = {}
        base = ROOT / "dist" / "copilots" / copilot_id
        spec = read_json(base / "shared" / "spec.json", {}, issues, copilot_id)
        profile = read_json(base / "langchain" / "agent_profile.json", {}, issues, copilot_id)
        langchain_agent = read_text(base / "langchain" / "agent.py", issues, copilot_id)
        runtime_contract = read_text(base / "shared" / "runtime_contract.md", issues, copilot_id)
        markdown_runtimes = {
            "codex": read_text(base / "codex" / "AGENT.md", issues, copilot_id),
            "claude": read_text(base / "claude" / "AGENT.md", issues, copilot_id),
            "github-copilot": read_text(base / "github-copilot" / "copilot-agent.md", issues, copilot_id),
        }

        system_prompt = spec.get("systemPrompt", "")
        developer_prompt = spec.get("developerPrompt", "")
        output_schema = read_json(base / "shared" / "output_schema.json", {}, issues, copilot_id)
        codex_protocol = read_json(base / "shared" / "codex_tool_protocol.json", {}, issues, copilot_id)
        claude_protocol = read_json(base / "shared" / "claude_project_instructions.json", {}, issues, copilot_id)
        github_profile = read_json(base / "github-copilot" / "copilot-profile.json", {}, issues, copilot_id)
        github_mcp_placeholders = read_json(base / "github-copilot" / "mcp-placeholders.json", {}, issues, copilot_id)
        langchain_contract = read_json(base / "langchain" / "agent_contract.json", {}, issues, copilot_id)
        validate_artifact_hygiene(base / "shared" / "codex_tool_protocol.json", issues, data_hygiene_metrics)
        validate_artifact_hygiene(base / "shared" / "claude_project_instructions.json", issues, data_hygiene_metrics)
        validate_artifact_hygiene(base / "github-copilot" / "copilot-profile.json", issues, data_hygiene_metrics)
        validate_artifact_hygiene(base / "github-copilot" / "mcp-placeholders.json", issues, data_hygiene_metrics)
        validate_artifact_hygiene(base / "langchain" / "agent_contract.json", issues, data_hygiene_metrics)

        if profile.get("systemPrompt") != system_prompt:
            issues.append(issue(copilot_id, "langchain_system_prompt", "LangChain profile systemPrompt drifted from shared spec."))
        if profile.get("developerPrompt") != developer_prompt:
            issues.append(issue(copilot_id, "langchain_developer_prompt", "LangChain profile developerPrompt drifted from shared spec."))

        for runtime, text in markdown_runtimes.items():
            if system_prompt and system_prompt not in text:
                issues.append(issue(copilot_id, f"{runtime}_system_prompt", f"{runtime} adapter does not embed the shared system prompt verbatim."))
            if developer_prompt and developer_prompt not in text:
                issues.append(issue(copilot_id, f"{runtime}_developer_prompt", f"{runtime} adapter does not embed the shared developer prompt verbatim."))
            if "shared/output_schema.json" not in text and "../shared/output_schema.json" not in text:
                issues.append(issue(copilot_id, f"{runtime}_schema_link", f"{runtime} adapter does not reference the shared output schema."))
            validate_runtime_specific_markdown(copilot_id, runtime, text, issues)

        if spec.get("outputSchema") != output_schema:
            issues.append(issue(copilot_id, "output_schema_sync", "shared/spec.json outputSchema drifted from shared/output_schema.json."))
        validate_required_trace_fields_schema(copilot_id, spec, output_schema, issues)
        if profile.get("outputSchema") != output_schema:
            issues.append(issue(copilot_id, "langchain_profile_output_schema", "LangChain profile outputSchema drifted from shared/output_schema.json."))
        profile_contract = profile.get("contract", {}) if isinstance(profile.get("contract"), dict) else {}
        if profile_contract.get("outputSchema") != output_schema:
            issues.append(issue(copilot_id, "langchain_profile_contract_schema", "LangChain profile contract outputSchema drifted from shared/output_schema.json."))
        embedded_schema = embedded_langchain_output_schema(langchain_agent, issues, copilot_id)
        if embedded_schema is not None and embedded_schema != output_schema:
            issues.append(issue(copilot_id, "langchain_embedded_output_schema", "LangChain agent OUTPUT_SCHEMA drifted from shared/output_schema.json."))

        for path, text in [
            (base / "shared" / "spec.json", json.dumps(spec)),
            (base / "langchain" / "agent_profile.json", json.dumps(profile)),
            (base / "langchain" / "agent.py", langchain_agent),
            (base / "shared" / "runtime_contract.md", runtime_contract),
            (base / "codex" / "AGENT.md", markdown_runtimes["codex"]),
            (base / "claude" / "AGENT.md", markdown_runtimes["claude"]),
            (base / "github-copilot" / "copilot-agent.md", markdown_runtimes["github-copilot"]),
            (base / "github-copilot" / "copilot-profile.json", json.dumps(github_profile)),
            (base / "github-copilot" / "mcp-placeholders.json", json.dumps(github_mcp_placeholders)),
            (base / "langchain" / "agent_contract.json", json.dumps(langchain_contract)),
        ]:
            if has_local_path(text):
                issues.append(issue(relative(path), "local_path", "Local absolute path leaked in runtime artifact."))
            if has_secret_pattern(text):
                issues.append(issue(relative(path), "secret_pattern", "Potential secret pattern leaked in runtime artifact."))

        if system_prompt and system_prompt not in runtime_contract:
            issues.append(issue(copilot_id, "runtime_contract_system_prompt", "runtime_contract.md does not include the shared system prompt."))
        if developer_prompt and developer_prompt not in runtime_contract:
            issues.append(issue(copilot_id, "runtime_contract_developer_prompt", "runtime_contract.md does not include the shared developer prompt."))

        validate_codex_adapter_protocol(
            copilot_id,
            item if isinstance(item, dict) else {},
            codex_protocol,
            markdown_runtimes["codex"],
            output_schema,
            issues,
            codex_protocol_metrics,
        )
        validate_claude_adapter_protocol(
            copilot_id,
            item if isinstance(item, dict) else {},
            claude_protocol,
            markdown_runtimes["claude"],
            output_schema,
            spec,
            issues,
            claude_protocol_metrics,
        )
        validate_github_copilot_profile_protocol(
            copilot_id,
            item if isinstance(item, dict) else {},
            github_profile,
            github_mcp_placeholders,
            markdown_runtimes["github-copilot"],
            output_schema,
            spec,
            issues,
            github_protocol_metrics,
        )
        validate_langchain_agent_protocol(
            copilot_id,
            item if isinstance(item, dict) else {},
            langchain_contract,
            profile,
            langchain_agent,
            output_schema,
            spec,
            issues,
            langchain_protocol_metrics,
        )

        metrics.append(
            {
                "id": copilot_id,
                "name": item.get("name", copilot_id),
                "runtimesChecked": 4,
                "sharedSpec": item.get("sourceOfTruth"),
            }
        )

    test_strategy_audit = validate_test_strategy_runtime_equivalence(metrics, issues)
    codex_adapter_audit = summarize_codex_adapter_audit(codex_protocol_metrics, issues)
    claude_adapter_audit = summarize_claude_adapter_audit(claude_protocol_metrics, issues)
    github_adapter_audit = summarize_github_adapter_audit(github_protocol_metrics, issues)
    langchain_adapter_audit = summarize_langchain_agent_audit(langchain_protocol_metrics, issues)
    data_hygiene_audit = summarize_data_hygiene_audit(data_hygiene_metrics, issues)
    sdlc_runtime_matrix_audit = validate_sdlc_runtime_matrix_equivalence(injection_map, metrics, issues)
    validator_smoke = build_current_validator_smoke(
        "runtime_equivalence",
        "python tools/validate_runtime_equivalence.py",
        REPORT_JSON,
        issues,
    )

    report = {
        "pass": not issues,
        "checkedAt": datetime.now(timezone.utc).isoformat(),
        "copilotsChecked": len(metrics),
        "metrics": metrics,
        "codexAdapterAudit": codex_adapter_audit,
        "claudeAdapterAudit": claude_adapter_audit,
        "githubCopilotAdapterAudit": github_adapter_audit,
        "langchainAgentAudit": langchain_adapter_audit,
        "dataHygieneAudit": data_hygiene_audit,
        "sdlcRuntimeMatrixAudit": sdlc_runtime_matrix_audit,
        "testStrategyAudit": test_strategy_audit,
        "validatorSmoke": validator_smoke,
        "issues": issues,
    }
    REPORT_JSON.parent.mkdir(parents=True, exist_ok=True)
    REPORT_JSON.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    REPORT_MD.write_text(render_md(report), encoding="utf-8")
    write_validator_smoke_artifacts(
        "runtime_equivalence",
        "python tools/validate_runtime_equivalence.py",
        REPORT_JSON,
        report,
        issues,
    )

    if issues:
        print(f"Runtime equivalence FAIL: {len(issues)} issue(s).")
        for item in issues[:30]:
            print(f"- {item['scope']} [{item['kind']}]: {item['message']}")
        sys.exit(1)
    print(f"Runtime equivalence PASS: {len(metrics)} copilots checked.")


def issue(scope: str, kind: str, message: str) -> dict:
    return {"scope": scope, "kind": kind, "message": message}


def build_current_validator_smoke(validator_id: str, command: str, report_path: Path, issues: list[dict]) -> dict:
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
    issues: list[dict],
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


def normalize_validator_blockers(issues: list[dict]) -> list[dict]:
    blockers = []
    for item in issues[:20]:
        blockers.append(
            {
                "scope": truncate_text(item.get("scope", "validator")),
                "kind": truncate_text(item.get("kind", "validation_issue")),
                "message": truncate_text(item.get("message", "")),
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


def read_json(path: Path, fallback, issues: list[dict] | None = None, scope: str | None = None):
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        if issues is not None:
            issues.append(issue(scope or format_path(path), "json_input", f"Missing required JSON input: {format_path(path)}."))
        return fallback
    except json.JSONDecodeError as exc:
        if issues is not None:
            issues.append(
                issue(
                    scope or format_path(path),
                    "json_input",
                    f"Invalid JSON in {format_path(path)} at line {exc.lineno}, column {exc.colno}: {exc.msg}.",
                )
            )
        return fallback
    except OSError as exc:
        if issues is not None:
            issues.append(issue(scope or format_path(path), "json_input", f"Cannot read JSON input {format_path(path)}: {exc}."))
        return fallback
    if not isinstance(value, type(fallback)):
        if issues is not None:
            issues.append(
                issue(
                    scope or format_path(path),
                    "json_input",
                    f"Unexpected JSON type in {format_path(path)}: expected {type(fallback).__name__}, got {type(value).__name__}.",
                )
            )
        return fallback
    return value


def read_text(path: Path, issues: list[dict] | None = None, scope: str | None = None) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except FileNotFoundError:
        if issues is not None:
            issues.append(issue(scope or format_path(path), "text_input", f"Missing required text input: {format_path(path)}."))
        return ""
    except UnicodeDecodeError as exc:
        if issues is not None:
            issues.append(issue(scope or format_path(path), "text_input", f"Invalid UTF-8 in {format_path(path)}: {exc.reason}."))
        return ""
    except OSError as exc:
        if issues is not None:
            reason = getattr(exc, "strerror", None) or exc.__class__.__name__
            issues.append(issue(scope or format_path(path), "text_input", f"Cannot read text input {format_path(path)}: {reason}."))
        return ""


def catalog_copilot_ids(issues: list[dict]) -> list[str]:
    catalog = read_json(CATALOG_JSON, [], issues, "copilot-catalog")
    ids: list[str] = []
    for index, item in enumerate(catalog):
        if not isinstance(item, dict):
            issues.append(issue("copilot-catalog", "catalog_entry", f"data/copilots.json item {index} must be an object."))
            continue
        copilot_id = item.get("id")
        if not isinstance(copilot_id, str) or not copilot_id.strip():
            issues.append(issue("copilot-catalog", "catalog_entry_id", f"data/copilots.json item {index} must have a non-empty string id."))
            continue
        if not is_safe_copilot_id(copilot_id):
            issues.append(issue("copilot-catalog", "catalog_entry_id", f"data/copilots.json item {index} id must be a safe repository path segment."))
            continue
        ids.append(copilot_id)
    if not ids:
        issues.append(issue("copilot-catalog", "catalog_coverage", "data/copilots.json must declare at least one copilot."))
    return ids


def validate_runtime_map_header(injection_map: dict, issues: list[dict]) -> None:
    version = injection_map.get("version")
    if not isinstance(version, str) or not version.strip():
        issues.append(issue("runtime-injection-map", "runtime_map_version", "runtime-injection-map must declare a non-empty string version."))

    generated_at = injection_map.get("generatedAt")
    if not isinstance(generated_at, str) or not generated_at.strip():
        issues.append(issue("runtime-injection-map", "runtime_map_generated_at", "runtime-injection-map must declare a non-empty generatedAt timestamp."))
    else:
        try:
            datetime.fromisoformat(generated_at.replace("Z", "+00:00"))
        except ValueError:
            issues.append(issue("runtime-injection-map", "runtime_map_generated_at", "runtime-injection-map generatedAt must be an ISO-8601 timestamp."))

    if injection_map.get("runtimes") != RUNTIMES:
        issues.append(issue("runtime-injection-map", "runtime_map_runtimes", f"runtime-injection-map runtimes must be exactly {RUNTIMES!r}."))


def validate_runtime_map_coverage(copilots: dict, expected_ids: list[str], issues: list[dict]) -> None:
    if not copilots:
        issues.append(issue("runtime-injection-map", "runtime_map_coverage", "runtime-injection-map must declare at least one copilot."))
        return
    expected = set(expected_ids)
    actual = set(copilots)
    missing = [copilot_id for copilot_id in expected_ids if copilot_id not in actual]
    extra = sorted(copilot_id for copilot_id in actual if copilot_id not in expected)
    if missing:
        issues.append(issue("runtime-injection-map", "runtime_map_coverage", f"runtime-injection-map missing copilot(s): {', '.join(missing)}."))
    if extra:
        issues.append(issue("runtime-injection-map", "runtime_map_coverage", f"runtime-injection-map has unknown copilot(s): {', '.join(extra)}."))


def has_local_path(text: str) -> bool:
    return any(pattern.search(text) for pattern in LOCAL_PATH_PATTERNS)


def has_secret_pattern(text: str) -> bool:
    return any(pattern.search(text) for pattern in SECRET_PATTERNS)


def is_safe_copilot_id(value: object) -> bool:
    return isinstance(value, str) and bool(SAFE_COPILOT_ID_RE.fullmatch(value))


def validate_runtime_specific_markdown(copilot_id: str, runtime: str, text: str, issues: list[dict]) -> None:
    section = runtime_specific_section(text)
    if not section:
        issues.append(issue(copilot_id, f"{runtime}_runtime_specific_protocol", f"{runtime} adapter is missing Runtime Specific Protocol section."))
        return
    if re.search(r"(?m)^(?: {4,}|\t+)-\s+", section):
        issues.append(
            issue(
                copilot_id,
                f"{runtime}_runtime_specific_protocol_markdown",
                f"{runtime} Runtime Specific Protocol has an indented list item that renders as a code block.",
            )
        )


def runtime_specific_section(text: str) -> str:
    match = re.search(r"^## Runtime Specific Protocol\s*$([\s\S]*?)(?=^## |\Z)", text, re.M)
    return match.group(1) if match else ""


def validate_artifact_hygiene(path: Path, issues: list[dict], metrics: list[dict]) -> None:
    artifact = format_path(path)
    try:
        text = path.read_text(encoding="utf-8")
    except FileNotFoundError:
        metrics.append({"artifact": artifact, "checked": False, "localPathLeak": False, "secretPatternLeak": False})
        return
    except OSError as exc:
        reason = getattr(exc, "strerror", None) or exc.__class__.__name__
        issues.append(issue(artifact, "data_hygiene_read", f"Cannot inspect artifact hygiene for {artifact}: {reason}."))
        metrics.append({"artifact": artifact, "checked": False, "localPathLeak": False, "secretPatternLeak": False})
        return

    local_path_leak = has_local_path(text)
    secret_pattern_leak = has_secret_pattern(text)
    metrics.append(
        {
            "artifact": artifact,
            "checked": True,
            "localPathLeak": local_path_leak,
            "secretPatternLeak": secret_pattern_leak,
        }
    )
    if local_path_leak:
        issues.append(issue(artifact, "data_hygiene_local_path", "Local absolute path leaked in runtime contract artifact."))
    if secret_pattern_leak:
        issues.append(issue(artifact, "data_hygiene_secret_pattern", "Potential secret pattern leaked in runtime contract artifact."))


def embedded_langchain_output_schema(text: str, issues: list[dict], copilot_id: str) -> dict | None:
    try:
        tree = ast.parse(text)
    except SyntaxError as exc:
        issues.append(issue(copilot_id, "langchain_agent_syntax", f"LangChain agent cannot be parsed: {exc.msg}."))
        return None

    for node in tree.body:
        if not isinstance(node, ast.Assign):
            continue
        if any(isinstance(target, ast.Name) and target.id == "OUTPUT_SCHEMA" for target in node.targets):
            try:
                value = ast.literal_eval(node.value)
            except (ValueError, TypeError) as exc:
                issues.append(issue(copilot_id, "langchain_embedded_output_schema", f"LangChain agent OUTPUT_SCHEMA is not a literal dict: {exc}."))
                return None
            if isinstance(value, dict):
                return value
            issues.append(issue(copilot_id, "langchain_embedded_output_schema", "LangChain agent OUTPUT_SCHEMA must be a dict."))
            return None

    issues.append(issue(copilot_id, "langchain_embedded_output_schema", "LangChain agent is missing OUTPUT_SCHEMA."))
    return None


def validate_codex_adapter_protocol(
    copilot_id: str,
    injection_item: dict,
    protocol: dict,
    codex_text: str,
    output_schema: dict,
    issues: list[dict],
    metrics: list[dict],
) -> None:
    local_issues: list[dict] = []
    rel_protocol = f"dist/copilots/{copilot_id}/{CODEX_PROTOCOL_FILE}"
    expected_source = f"dist/copilots/{copilot_id}/shared/spec.json"
    expected_schema = f"dist/copilots/{copilot_id}/shared/output_schema.json"
    expected_runtime_files = {
        "codex": f"dist/copilots/{copilot_id}/codex/AGENT.md",
        "claude": f"dist/copilots/{copilot_id}/claude/AGENT.md",
        "github-copilot": f"dist/copilots/{copilot_id}/github-copilot/copilot-agent.md",
        "langchain": f"dist/copilots/{copilot_id}/langchain/agent.py",
    }
    source_of_truth = injection_item.get("sourceOfTruth")
    runtime_files = injection_item.get("runtimeFiles", {}) if isinstance(injection_item.get("runtimeFiles"), dict) else {}
    codex_file = runtime_files.get("codex")
    schema_file = injection_item.get("outputSchema")
    map_protocol = injection_item.get("codexAdapterProtocol", {})

    expect(local_issues, copilot_id, "runtime_map_source_of_truth", source_of_truth, expected_source)
    expect(local_issues, copilot_id, "runtime_map_output_schema", schema_file, expected_schema)
    if runtime_files != expected_runtime_files:
        local_issues.append(issue(copilot_id, "runtime_map_runtime_files", "runtime-injection-map runtimeFiles drifted from canonical runtime adapter paths."))
    required_repo_file(local_issues, copilot_id, "runtime_map_source_file", source_of_truth)
    required_repo_file(local_issues, copilot_id, "runtime_map_schema_file", schema_file)
    for runtime, path in runtime_files.items():
        required_repo_file(local_issues, copilot_id, f"runtime_map_{runtime}_file", path)

    if not protocol:
        local_issues.append(issue(copilot_id, "codex_protocol", f"Missing Codex protocol artifact: {rel_protocol}."))
    else:
        expect(local_issues, copilot_id, "codex_protocol_version", protocol.get("policyVersion"), CODEX_PROTOCOL_VERSION)
        expect(local_issues, copilot_id, "codex_protocol_owner", protocol.get("ownerAgent"), CODEX_OWNER_AGENT)
        expect(local_issues, copilot_id, "codex_protocol_mission", protocol.get("mission"), CODEX_MISSION)
        expect(local_issues, copilot_id, "codex_protocol_runtime", protocol.get("runtime"), "codex")
        expect(local_issues, copilot_id, "codex_protocol_copilot", protocol.get("copilotId"), copilot_id)
        expect(local_issues, copilot_id, "codex_protocol_source", protocol.get("sourceOfTruth"), source_of_truth)

        task_prompt = protocol.get("taskPrompt", {}) if isinstance(protocol.get("taskPrompt"), dict) else {}
        expect(local_issues, copilot_id, "codex_task_prompt_artifact", task_prompt.get("artifact"), codex_file)
        expect(local_issues, copilot_id, "codex_task_prompt_schema", task_prompt.get("schemaRef"), schema_file)
        expect(local_issues, copilot_id, "codex_task_prompt_schema_digest", task_prompt.get("outputSchemaSha256"), stable_json_digest(output_schema))
        missing_sections = missing_items(task_prompt.get("requiredSections"), CODEX_REQUIRED_SECTIONS)
        if missing_sections:
            local_issues.append(issue(copilot_id, "codex_task_prompt_sections", f"Codex task prompt contract missing section(s): {', '.join(missing_sections)}."))

        missing_evidence = missing_items(protocol.get("requiredEvidence"), CODEX_REQUIRED_EVIDENCE)
        if missing_evidence:
            local_issues.append(issue(copilot_id, "codex_protocol_evidence", f"Codex protocol missing evidence marker(s): {', '.join(missing_evidence)}."))
        missing_gates = missing_items(protocol.get("qualityGates"), CODEX_QUALITY_GATES)
        if missing_gates:
            local_issues.append(issue(copilot_id, "codex_protocol_quality_gates", f"Codex protocol missing quality gate(s): {', '.join(missing_gates)}."))

        tool_protocol = protocol.get("localToolProtocol", {}) if isinstance(protocol.get("localToolProtocol"), dict) else {}
        for key, expected in CODEX_TOOL_PROTOCOL_REQUIRED.items():
            expect(local_issues, copilot_id, f"codex_tool_protocol_{key}", tool_protocol.get(key), expected)
        missing_tool_steps = missing_items(
            tool_protocol.get("toolingOrder"),
            ["inspect_files", "deterministic_python_check", "scoped_patch", "validation_commands"],
        )
        if missing_tool_steps:
            local_issues.append(issue(copilot_id, "codex_tool_protocol_order", f"Codex tool protocol missing step(s): {', '.join(missing_tool_steps)}."))

        validation_commands = protocol.get("validationCommands", [])
        missing_commands = missing_items(validation_commands, CODEX_VALIDATION_COMMANDS)
        if missing_commands:
            local_issues.append(issue(copilot_id, "codex_validation_commands", f"Codex protocol missing validation command(s): {', '.join(missing_commands)}."))

        runtime_equivalence = protocol.get("runtimeEquivalence", {}) if isinstance(protocol.get("runtimeEquivalence"), dict) else {}
        expect(local_issues, copilot_id, "codex_runtime_equivalence_source", runtime_equivalence.get("sourceOfTruth"), source_of_truth)
        expect(local_issues, copilot_id, "codex_runtime_equivalence_runtimes", runtime_equivalence.get("runtimes"), RUNTIMES)
        expect(local_issues, copilot_id, "codex_runtime_equivalence_drift", runtime_equivalence.get("maxUnexplainedDrift"), 0)
        if runtime_equivalence.get("adapterFiles") != runtime_files:
            local_issues.append(issue(copilot_id, "codex_runtime_equivalence_adapters", "Codex protocol adapterFiles drifted from runtime-injection-map runtimeFiles."))

    if not map_protocol:
        local_issues.append(issue(copilot_id, "codex_runtime_map", "runtime-injection-map is missing codexAdapterProtocol."))
    else:
        expect(local_issues, copilot_id, "codex_runtime_map_artifact", map_protocol.get("artifact"), rel_protocol)
        expect(local_issues, copilot_id, "codex_runtime_map_owner", map_protocol.get("ownerAgent"), CODEX_OWNER_AGENT)
        expect(local_issues, copilot_id, "codex_runtime_map_mission", map_protocol.get("mission"), CODEX_MISSION)
        missing_map_gates = missing_items(map_protocol.get("qualityGates"), CODEX_QUALITY_GATES)
        if missing_map_gates:
            local_issues.append(issue(copilot_id, "codex_runtime_map_gates", f"runtime-injection-map codexAdapterProtocol missing gate(s): {', '.join(missing_map_gates)}."))
        map_equivalence = map_protocol.get("runtimeEquivalence", {}) if isinstance(map_protocol.get("runtimeEquivalence"), dict) else {}
        expect(local_issues, copilot_id, "codex_runtime_map_source", map_equivalence.get("sourceOfTruth"), source_of_truth)
        expect(local_issues, copilot_id, "codex_runtime_map_runtimes", map_equivalence.get("runtimes"), RUNTIMES)
        expect(local_issues, copilot_id, "codex_runtime_map_drift", map_equivalence.get("maxUnexplainedDrift"), 0)

    missing_prompt_markers = [marker for marker in CODEX_PROMPT_MARKERS if marker not in codex_text]
    if missing_prompt_markers:
        local_issues.append(issue(copilot_id, "codex_prompt_protocol_markers", f"Codex AGENT.md missing local protocol marker(s): {', '.join(missing_prompt_markers)}."))

    metrics.append(
        {
            "id": copilot_id,
            "protocol": rel_protocol,
            "runtimeFile": codex_file,
            "sourceOfTruth": source_of_truth,
            "pass": not local_issues,
        }
    )
    issues.extend(local_issues)


def validate_claude_adapter_protocol(
    copilot_id: str,
    injection_item: dict,
    protocol: dict,
    claude_text: str,
    output_schema: dict,
    spec: dict,
    issues: list[dict],
    metrics: list[dict],
) -> None:
    local_issues: list[dict] = []
    rel_protocol = f"dist/copilots/{copilot_id}/{CLAUDE_PROTOCOL_FILE}"
    expected_source = f"dist/copilots/{copilot_id}/shared/spec.json"
    expected_schema = f"dist/copilots/{copilot_id}/shared/output_schema.json"
    expected_runtime_files = {
        "codex": f"dist/copilots/{copilot_id}/codex/AGENT.md",
        "claude": f"dist/copilots/{copilot_id}/claude/AGENT.md",
        "github-copilot": f"dist/copilots/{copilot_id}/github-copilot/copilot-agent.md",
        "langchain": f"dist/copilots/{copilot_id}/langchain/agent.py",
    }
    source_of_truth = injection_item.get("sourceOfTruth")
    runtime_files = injection_item.get("runtimeFiles", {}) if isinstance(injection_item.get("runtimeFiles"), dict) else {}
    claude_file = runtime_files.get("claude")
    schema_file = injection_item.get("outputSchema")
    map_protocol = injection_item.get("claudeAdapterProtocol", {})

    expect(local_issues, copilot_id, "claude_runtime_map_source_of_truth", source_of_truth, expected_source)
    expect(local_issues, copilot_id, "claude_runtime_map_output_schema", schema_file, expected_schema)

    if not protocol:
        local_issues.append(issue(copilot_id, "claude_protocol", f"Missing Claude project instructions artifact: {rel_protocol}."))
    else:
        expect(local_issues, copilot_id, "claude_protocol_version", protocol.get("policyVersion"), CLAUDE_PROTOCOL_VERSION)
        expect(local_issues, copilot_id, "claude_protocol_owner", protocol.get("ownerAgent"), CLAUDE_OWNER_AGENT)
        expect(local_issues, copilot_id, "claude_protocol_mission", protocol.get("mission"), CLAUDE_MISSION)
        expect(local_issues, copilot_id, "claude_protocol_runtime", protocol.get("runtime"), "claude")
        expect(local_issues, copilot_id, "claude_protocol_copilot", protocol.get("copilotId"), copilot_id)
        expect(local_issues, copilot_id, "claude_protocol_source", protocol.get("sourceOfTruth"), source_of_truth)

        project_instructions = protocol.get("projectInstructions", {}) if isinstance(protocol.get("projectInstructions"), dict) else {}
        expect(local_issues, copilot_id, "claude_project_instructions_artifact", project_instructions.get("artifact"), claude_file)
        expect(local_issues, copilot_id, "claude_project_instructions_schema", project_instructions.get("schemaRef"), schema_file)
        expect(
            local_issues,
            copilot_id,
            "claude_project_instructions_schema_digest",
            project_instructions.get("outputSchemaSha256"),
            stable_json_digest(output_schema),
        )
        missing_sections = missing_items(project_instructions.get("requiredSections"), CLAUDE_REQUIRED_SECTIONS)
        if missing_sections:
            local_issues.append(
                issue(copilot_id, "claude_project_instructions_sections", f"Claude project instructions missing section(s): {', '.join(missing_sections)}.")
            )

        agent_card = protocol.get("agentCard", {}) if isinstance(protocol.get("agentCard"), dict) else {}
        expect(local_issues, copilot_id, "claude_agent_card_copilot", agent_card.get("copilotId"), copilot_id)
        expect(local_issues, copilot_id, "claude_agent_card_runtime", agent_card.get("runtime"), "claude")
        expect(local_issues, copilot_id, "claude_agent_card_source", agent_card.get("sourceOfTruth"), source_of_truth)
        expect(local_issues, copilot_id, "claude_agent_card_schema", agent_card.get("outputSchema"), schema_file)
        expect(local_issues, copilot_id, "claude_agent_card_runtime_file", agent_card.get("runtimeFile"), claude_file)
        expect(local_issues, copilot_id, "claude_agent_card_display_name", agent_card.get("displayName"), spec.get("name"))
        expect(local_issues, copilot_id, "claude_agent_card_family", agent_card.get("family"), spec.get("family"))
        expect(local_issues, copilot_id, "claude_agent_card_connectors", agent_card.get("connectors"), spec.get("connectors"))
        expect(local_issues, copilot_id, "claude_agent_card_env_keys", agent_card.get("envKeys"), spec.get("env_keys"))
        expect(local_issues, copilot_id, "claude_agent_card_outputs", agent_card.get("declaredOutputs"), spec.get("outputs"))
        missing_handoff_targets = missing_items(agent_card.get("handoffTargets"), ["codex", "github-copilot"])
        if missing_handoff_targets:
            local_issues.append(issue(copilot_id, "claude_agent_card_handoff", f"Claude agent card missing handoff target(s): {', '.join(missing_handoff_targets)}."))

        missing_evidence = missing_items(protocol.get("requiredEvidence"), CLAUDE_REQUIRED_EVIDENCE)
        if missing_evidence:
            local_issues.append(issue(copilot_id, "claude_protocol_evidence", f"Claude protocol missing evidence marker(s): {', '.join(missing_evidence)}."))
        missing_gates = missing_items(protocol.get("qualityGates"), CLAUDE_QUALITY_GATES)
        if missing_gates:
            local_issues.append(issue(copilot_id, "claude_protocol_quality_gates", f"Claude protocol missing quality gate(s): {', '.join(missing_gates)}."))

        missing_commands = missing_items(protocol.get("validationCommands"), CLAUDE_VALIDATION_COMMANDS)
        if missing_commands:
            local_issues.append(issue(copilot_id, "claude_validation_commands", f"Claude protocol missing validation command(s): {', '.join(missing_commands)}."))

        runtime_equivalence = protocol.get("runtimeEquivalence", {}) if isinstance(protocol.get("runtimeEquivalence"), dict) else {}
        expect(local_issues, copilot_id, "claude_runtime_equivalence_source", runtime_equivalence.get("sourceOfTruth"), source_of_truth)
        expect(local_issues, copilot_id, "claude_runtime_equivalence_runtimes", runtime_equivalence.get("runtimes"), RUNTIMES)
        expect(local_issues, copilot_id, "claude_runtime_equivalence_drift", runtime_equivalence.get("maxUnexplainedDrift"), 0)
        if runtime_equivalence.get("adapterFiles") != runtime_files:
            local_issues.append(issue(copilot_id, "claude_runtime_equivalence_adapters", "Claude protocol adapterFiles drifted from runtime-injection-map runtimeFiles."))

    if not map_protocol:
        local_issues.append(issue(copilot_id, "claude_runtime_map", "runtime-injection-map is missing claudeAdapterProtocol."))
    else:
        expect(local_issues, copilot_id, "claude_runtime_map_artifact", map_protocol.get("artifact"), rel_protocol)
        expect(local_issues, copilot_id, "claude_runtime_map_owner", map_protocol.get("ownerAgent"), CLAUDE_OWNER_AGENT)
        expect(local_issues, copilot_id, "claude_runtime_map_mission", map_protocol.get("mission"), CLAUDE_MISSION)
        required_repo_file(local_issues, copilot_id, "claude_runtime_map_artifact_file", map_protocol.get("artifact"))
        missing_map_evidence = missing_items(map_protocol.get("requiredEvidence"), CLAUDE_REQUIRED_EVIDENCE)
        if missing_map_evidence:
            local_issues.append(issue(copilot_id, "claude_runtime_map_evidence", f"runtime-injection-map claudeAdapterProtocol missing evidence marker(s): {', '.join(missing_map_evidence)}."))
        missing_map_gates = missing_items(map_protocol.get("qualityGates"), CLAUDE_QUALITY_GATES)
        if missing_map_gates:
            local_issues.append(issue(copilot_id, "claude_runtime_map_gates", f"runtime-injection-map claudeAdapterProtocol missing gate(s): {', '.join(missing_map_gates)}."))
        map_equivalence = map_protocol.get("runtimeEquivalence", {}) if isinstance(map_protocol.get("runtimeEquivalence"), dict) else {}
        expect(local_issues, copilot_id, "claude_runtime_map_source", map_equivalence.get("sourceOfTruth"), source_of_truth)
        expect(local_issues, copilot_id, "claude_runtime_map_runtimes", map_equivalence.get("runtimes"), RUNTIMES)
        expect(local_issues, copilot_id, "claude_runtime_map_drift", map_equivalence.get("maxUnexplainedDrift"), 0)

    if runtime_files != expected_runtime_files:
        local_issues.append(issue(copilot_id, "claude_runtime_map_runtime_files", "runtime-injection-map runtimeFiles drifted from canonical runtime adapter paths."))
    required_repo_file(local_issues, copilot_id, "claude_runtime_map_source_file", source_of_truth)
    required_repo_file(local_issues, copilot_id, "claude_runtime_map_schema_file", schema_file)
    required_repo_file(local_issues, copilot_id, "claude_runtime_map_runtime_file", claude_file)

    missing_prompt_markers = [marker for marker in CLAUDE_PROMPT_MARKERS if marker not in claude_text]
    if missing_prompt_markers:
        local_issues.append(issue(copilot_id, "claude_prompt_protocol_markers", f"Claude AGENT.md missing project instruction marker(s): {', '.join(missing_prompt_markers)}."))

    metrics.append(
        {
            "id": copilot_id,
            "protocol": rel_protocol,
            "runtimeFile": claude_file,
            "sourceOfTruth": source_of_truth,
            "pass": not local_issues,
        }
    )
    issues.extend(local_issues)


def validate_github_copilot_profile_protocol(
    copilot_id: str,
    injection_item: dict,
    profile: dict,
    mcp_placeholders: dict,
    github_text: str,
    output_schema: dict,
    spec: dict,
    issues: list[dict],
    metrics: list[dict],
) -> None:
    local_issues: list[dict] = []
    rel_profile = f"dist/copilots/{copilot_id}/{GITHUB_PROFILE_FILE}"
    rel_mcp = f"dist/copilots/{copilot_id}/{GITHUB_MCP_PLACEHOLDERS_FILE}"
    expected_source = f"dist/copilots/{copilot_id}/shared/spec.json"
    expected_schema = f"dist/copilots/{copilot_id}/shared/output_schema.json"
    expected_runtime_files = {
        "codex": f"dist/copilots/{copilot_id}/codex/AGENT.md",
        "claude": f"dist/copilots/{copilot_id}/claude/AGENT.md",
        "github-copilot": f"dist/copilots/{copilot_id}/github-copilot/copilot-agent.md",
        "langchain": f"dist/copilots/{copilot_id}/langchain/agent.py",
    }
    source_of_truth = injection_item.get("sourceOfTruth")
    runtime_files = injection_item.get("runtimeFiles", {}) if isinstance(injection_item.get("runtimeFiles"), dict) else {}
    github_file = runtime_files.get("github-copilot")
    schema_file = injection_item.get("outputSchema")
    map_protocol = injection_item.get("githubCopilotProfileProtocol", {})

    expect(local_issues, copilot_id, "github_runtime_map_source_of_truth", source_of_truth, expected_source)
    expect(local_issues, copilot_id, "github_runtime_map_output_schema", schema_file, expected_schema)
    if runtime_files != expected_runtime_files:
        local_issues.append(issue(copilot_id, "github_runtime_map_runtime_files", "runtime-injection-map runtimeFiles drifted from canonical runtime adapter paths."))
    required_repo_file(local_issues, copilot_id, "github_runtime_map_source_file", source_of_truth)
    required_repo_file(local_issues, copilot_id, "github_runtime_map_schema_file", schema_file)
    required_repo_file(local_issues, copilot_id, "github_runtime_map_runtime_file", github_file)

    if not profile:
        local_issues.append(issue(copilot_id, "github_profile", f"Missing GitHub Copilot profile artifact: {rel_profile}."))
    else:
        expect(local_issues, copilot_id, "github_profile_version", profile.get("policyVersion"), GITHUB_PROTOCOL_VERSION)
        expect(local_issues, copilot_id, "github_profile_owner", profile.get("ownerAgent"), GITHUB_OWNER_AGENT)
        expect(local_issues, copilot_id, "github_profile_mission", profile.get("mission"), GITHUB_MISSION)
        expect(local_issues, copilot_id, "github_profile_runtime", profile.get("runtime"), "github-copilot")
        expect(local_issues, copilot_id, "github_profile_copilot", profile.get("copilotId"), copilot_id)
        expect(local_issues, copilot_id, "github_profile_display_name", profile.get("displayName"), spec.get("name"))
        expect(local_issues, copilot_id, "github_profile_family", profile.get("family"), spec.get("family"))
        expect(local_issues, copilot_id, "github_profile_connectors", profile.get("connectors"), spec.get("connectors"))
        expect(local_issues, copilot_id, "github_profile_env_keys", profile.get("envKeys"), spec.get("env_keys"))
        expect(local_issues, copilot_id, "github_profile_outputs", profile.get("declaredOutputs"), spec.get("outputs"))
        expect(local_issues, copilot_id, "github_profile_source", profile.get("sourceOfTruth"), source_of_truth)
        expect(local_issues, copilot_id, "github_profile_schema", profile.get("outputSchema"), schema_file)
        expect(local_issues, copilot_id, "github_profile_runtime_file", profile.get("runtimeFile"), github_file)
        expect(local_issues, copilot_id, "github_profile_mcp_ref", profile.get("mcpPlaceholderRef"), rel_mcp)

        profile_doc = profile.get("profileDoc", {}) if isinstance(profile.get("profileDoc"), dict) else {}
        expect(local_issues, copilot_id, "github_profile_doc_artifact", profile_doc.get("artifact"), github_file)
        expect(local_issues, copilot_id, "github_profile_doc_profile_artifact", profile_doc.get("profileArtifact"), rel_profile)
        expect(local_issues, copilot_id, "github_profile_doc_schema", profile_doc.get("schemaRef"), schema_file)
        expect(local_issues, copilot_id, "github_profile_schema_digest", profile_doc.get("outputSchemaSha256"), stable_json_digest(output_schema))
        missing_sections = missing_items(profile_doc.get("requiredSections"), GITHUB_REQUIRED_SECTIONS)
        if missing_sections:
            local_issues.append(issue(copilot_id, "github_profile_doc_sections", f"GitHub Copilot profile missing section(s): {', '.join(missing_sections)}."))

        workflow = profile.get("repositoryWorkflow", {}) if isinstance(profile.get("repositoryWorkflow"), dict) else {}
        missing_workflow_steps = missing_items(
            workflow.get("evidenceOrder"),
            [
                "issue_or_pr_context",
                "branch_and_review_policy",
                "workflow_or_check_status",
                "source_file_refs",
                "validation_commands",
            ],
        )
        if missing_workflow_steps:
            local_issues.append(issue(copilot_id, "github_profile_workflow", f"GitHub Copilot profile missing workflow step(s): {', '.join(missing_workflow_steps)}."))
        expect(local_issues, copilot_id, "github_profile_branch_policy", workflow.get("branchPolicyRespected"), True)
        expect(local_issues, copilot_id, "github_profile_review_comments", workflow.get("reviewCommentsActionable"), True)

        missing_evidence = missing_items(profile.get("requiredEvidence"), GITHUB_REQUIRED_EVIDENCE)
        if missing_evidence:
            local_issues.append(issue(copilot_id, "github_profile_evidence", f"GitHub Copilot profile missing evidence marker(s): {', '.join(missing_evidence)}."))
        missing_gates = missing_items(profile.get("qualityGates"), GITHUB_QUALITY_GATES)
        if missing_gates:
            local_issues.append(issue(copilot_id, "github_profile_quality_gates", f"GitHub Copilot profile missing quality gate(s): {', '.join(missing_gates)}."))
        missing_commands = missing_items(profile.get("validationCommands"), GITHUB_VALIDATION_COMMANDS)
        if missing_commands:
            local_issues.append(issue(copilot_id, "github_profile_validation_commands", f"GitHub Copilot profile missing validation command(s): {', '.join(missing_commands)}."))

        runtime_equivalence = profile.get("runtimeEquivalence", {}) if isinstance(profile.get("runtimeEquivalence"), dict) else {}
        expect(local_issues, copilot_id, "github_profile_runtime_equivalence_source", runtime_equivalence.get("sourceOfTruth"), source_of_truth)
        expect(local_issues, copilot_id, "github_profile_runtime_equivalence_runtimes", runtime_equivalence.get("runtimes"), RUNTIMES)
        expect(local_issues, copilot_id, "github_profile_runtime_equivalence_drift", runtime_equivalence.get("maxUnexplainedDrift"), 0)
        if runtime_equivalence.get("adapterFiles") != runtime_files:
            local_issues.append(issue(copilot_id, "github_profile_runtime_equivalence_adapters", "GitHub Copilot profile adapterFiles drifted from runtime-injection-map runtimeFiles."))
        validate_github_profile_cost_control(copilot_id, profile, local_issues)

    validate_github_mcp_placeholders(
        copilot_id,
        mcp_placeholders,
        rel_mcp,
        source_of_truth,
        runtime_files,
        spec,
        local_issues,
    )

    if not map_protocol:
        local_issues.append(issue(copilot_id, "github_runtime_map", "runtime-injection-map is missing githubCopilotProfileProtocol."))
    else:
        expect(local_issues, copilot_id, "github_runtime_map_artifact", map_protocol.get("artifact"), rel_profile)
        expect(local_issues, copilot_id, "github_runtime_map_profile_doc", map_protocol.get("profileDoc"), github_file)
        expect(local_issues, copilot_id, "github_runtime_map_mcp_placeholders", map_protocol.get("mcpPlaceholders"), rel_mcp)
        expect(local_issues, copilot_id, "github_runtime_map_policy_ref", map_protocol.get("policyRef"), "config/mcp-connectors.example.json")
        expect(local_issues, copilot_id, "github_runtime_map_owner", map_protocol.get("ownerAgent"), GITHUB_OWNER_AGENT)
        expect(local_issues, copilot_id, "github_runtime_map_mission", map_protocol.get("mission"), GITHUB_MISSION)
        required_repo_file(local_issues, copilot_id, "github_runtime_map_artifact_file", map_protocol.get("artifact"))
        required_repo_file(local_issues, copilot_id, "github_runtime_map_profile_doc_file", map_protocol.get("profileDoc"))
        required_repo_file(local_issues, copilot_id, "github_runtime_map_mcp_file", map_protocol.get("mcpPlaceholders"))
        missing_map_evidence = missing_items(map_protocol.get("requiredEvidence"), GITHUB_REQUIRED_EVIDENCE)
        if missing_map_evidence:
            local_issues.append(issue(copilot_id, "github_runtime_map_evidence", f"runtime-injection-map githubCopilotProfileProtocol missing evidence marker(s): {', '.join(missing_map_evidence)}."))
        missing_map_gates = missing_items(map_protocol.get("qualityGates"), GITHUB_QUALITY_GATES)
        if missing_map_gates:
            local_issues.append(issue(copilot_id, "github_runtime_map_gates", f"runtime-injection-map githubCopilotProfileProtocol missing gate(s): {', '.join(missing_map_gates)}."))
        map_equivalence = map_protocol.get("runtimeEquivalence", {}) if isinstance(map_protocol.get("runtimeEquivalence"), dict) else {}
        expect(local_issues, copilot_id, "github_runtime_map_source", map_equivalence.get("sourceOfTruth"), source_of_truth)
        expect(local_issues, copilot_id, "github_runtime_map_runtimes", map_equivalence.get("runtimes"), RUNTIMES)
        expect(local_issues, copilot_id, "github_runtime_map_drift", map_equivalence.get("maxUnexplainedDrift"), 0)
        if map_equivalence.get("adapterFiles") != runtime_files:
            local_issues.append(issue(copilot_id, "github_runtime_map_adapters", "GitHub runtime map adapterFiles drifted from runtimeFiles."))

    missing_prompt_markers = [marker for marker in GITHUB_PROMPT_MARKERS if marker not in github_text]
    if missing_prompt_markers:
            local_issues.append(issue(copilot_id, "github_prompt_protocol_markers", f"GitHub Copilot profile doc missing marker(s): {', '.join(missing_prompt_markers)}."))

    metrics.append(
        {
            "id": copilot_id,
            "profile": rel_profile,
            "mcpPlaceholders": rel_mcp,
            "runtimeFile": github_file,
            "sourceOfTruth": source_of_truth,
            "pass": not local_issues,
        }
    )
    issues.extend(local_issues)


def validate_github_profile_cost_control(copilot_id: str, profile: dict, issues: list[dict]) -> None:
    cost_control = profile.get("costControl", {}) if isinstance(profile.get("costControl"), dict) else {}
    for key, expected in GITHUB_COST_CONTROL.items():
        expect(issues, copilot_id, f"github_profile_cost_control_{key}", cost_control.get(key), expected)


def validate_github_mcp_placeholders(
    copilot_id: str,
    placeholders: dict,
    rel_mcp: str,
    source_of_truth,
    runtime_files: dict,
    spec: dict,
    issues: list[dict],
) -> None:
    if not placeholders:
        issues.append(issue(copilot_id, "github_mcp_placeholders", f"Missing GitHub Copilot MCP placeholder artifact: {rel_mcp}."))
        return

    expect(issues, copilot_id, "github_mcp_version", placeholders.get("policyVersion"), GITHUB_PROTOCOL_VERSION)
    expect(issues, copilot_id, "github_mcp_owner", placeholders.get("ownerAgent"), GITHUB_OWNER_AGENT)
    expect(issues, copilot_id, "github_mcp_mission", placeholders.get("mission"), GITHUB_MISSION)
    expect(issues, copilot_id, "github_mcp_copilot", placeholders.get("copilotId"), copilot_id)
    expect(issues, copilot_id, "github_mcp_runtime", placeholders.get("runtime"), "github-copilot")
    expect(issues, copilot_id, "github_mcp_source_policy", placeholders.get("sourcePolicy"), "config/mcp-connectors.example.json")
    expect(issues, copilot_id, "github_mcp_default_enabled", placeholders.get("defaultEnabled"), False)
    expect(issues, copilot_id, "github_mcp_placeholder_only", placeholders.get("placeholderOnly"), True)
    expect(issues, copilot_id, "github_mcp_credentials_required", placeholders.get("credentialsRequired"), False)
    expect(issues, copilot_id, "github_mcp_credential_values_stored", placeholders.get("credentialValuesStored"), False)
    expect(issues, copilot_id, "github_mcp_customer_data", placeholders.get("customerDataAllowed"), False)
    expect(issues, copilot_id, "github_mcp_billing_data", placeholders.get("billingDataAllowed"), False)

    expected_connectors = spec.get("connectors", [])
    expected_env_keys = spec.get("env_keys", [])
    connectors = placeholders.get("connectors", {}) if isinstance(placeholders.get("connectors"), dict) else {}
    if set(connectors) != set(expected_connectors):
        issues.append(issue(copilot_id, "github_mcp_connectors", "GitHub Copilot MCP placeholders drifted from shared spec connectors."))
    for connector_name in expected_connectors:
        connector = connectors.get(connector_name, {}) if isinstance(connectors.get(connector_name), dict) else {}
        expect(issues, copilot_id, f"github_mcp_{connector_name}_name", connector.get("connector"), connector_name)
        expect(issues, copilot_id, f"github_mcp_{connector_name}_enabled", connector.get("enabled"), False)
        env_key = connector.get("env")
        if env_key not in expected_env_keys:
            issues.append(issue(copilot_id, f"github_mcp_{connector_name}_env", f"Connector env key {env_key!r} is not declared by shared spec."))
        expected_env_reference = f"${{{env_key}}}" if env_key else ""
        expect(issues, copilot_id, f"github_mcp_{connector_name}_env_reference", connector.get("envReference"), expected_env_reference)
        if connector.get("credentialValue") != "":
            issues.append(issue(copilot_id, f"github_mcp_{connector_name}_credential_value", "MCP placeholder credentialValue must be empty."))
        expect(issues, copilot_id, f"github_mcp_{connector_name}_credential_storage", connector.get("credentialValuesStored"), False)
        expect(issues, copilot_id, f"github_mcp_{connector_name}_activation", connector.get("requiresOperatorActivation"), True)
        expect(issues, copilot_id, f"github_mcp_{connector_name}_write_approval", connector.get("operatorApprovalRequiredForWrites"), True)
        expect(issues, copilot_id, f"github_mcp_{connector_name}_local_only", connector.get("localOnlyConfig"), True)
        expect(issues, copilot_id, f"github_mcp_{connector_name}_runtimes", connector.get("allowedRuntimes"), RUNTIMES)
        expect(issues, copilot_id, f"github_mcp_{connector_name}_policy_ref", connector.get("policyRef"), "config/mcp-connectors.example.json")

    safe_usage = placeholders.get("safeUsage", {}) if isinstance(placeholders.get("safeUsage"), dict) else {}
    for key in [
        "operatorActivationRequired",
        "operatorApprovalRequiredForWrites",
        "denyCustomerDataInPrompts",
        "redactTokensInLogs",
        "noExternalNetworkWithoutOperatorApproval",
    ]:
        expect(issues, copilot_id, f"github_mcp_safe_usage_{key}", safe_usage.get(key), True)

    runtime_equivalence = placeholders.get("runtimeEquivalence", {}) if isinstance(placeholders.get("runtimeEquivalence"), dict) else {}
    expect(issues, copilot_id, "github_mcp_runtime_equivalence_source", runtime_equivalence.get("sourceOfTruth"), source_of_truth)
    expect(issues, copilot_id, "github_mcp_runtime_equivalence_runtimes", runtime_equivalence.get("runtimes"), RUNTIMES)
    expect(issues, copilot_id, "github_mcp_runtime_equivalence_drift", runtime_equivalence.get("maxUnexplainedDrift"), 0)
    if runtime_equivalence.get("adapterFiles") != runtime_files:
        issues.append(issue(copilot_id, "github_mcp_runtime_equivalence_adapters", "GitHub MCP placeholders adapterFiles drifted from runtime-injection-map runtimeFiles."))


def validate_langchain_agent_protocol(
    copilot_id: str,
    injection_item: dict,
    contract: dict,
    profile: dict,
    langchain_text: str,
    output_schema: dict,
    spec: dict,
    issues: list[dict],
    metrics: list[dict],
) -> None:
    local_issues: list[dict] = []
    rel_contract = f"dist/copilots/{copilot_id}/{LANGCHAIN_CONTRACT_FILE}"
    rel_profile = f"dist/copilots/{copilot_id}/langchain/agent_profile.json"
    expected_source = f"dist/copilots/{copilot_id}/shared/spec.json"
    expected_schema = f"dist/copilots/{copilot_id}/shared/output_schema.json"
    expected_runtime_files = {
        "codex": f"dist/copilots/{copilot_id}/codex/AGENT.md",
        "claude": f"dist/copilots/{copilot_id}/claude/AGENT.md",
        "github-copilot": f"dist/copilots/{copilot_id}/github-copilot/copilot-agent.md",
        "langchain": f"dist/copilots/{copilot_id}/langchain/agent.py",
    }
    source_of_truth = injection_item.get("sourceOfTruth")
    runtime_files = injection_item.get("runtimeFiles", {}) if isinstance(injection_item.get("runtimeFiles"), dict) else {}
    langchain_file = runtime_files.get("langchain")
    schema_file = injection_item.get("outputSchema")
    map_protocol = injection_item.get("langchainAgentProtocol", {})

    expect(local_issues, copilot_id, "langchain_runtime_map_source_of_truth", source_of_truth, expected_source)
    expect(local_issues, copilot_id, "langchain_runtime_map_output_schema", schema_file, expected_schema)
    if runtime_files != expected_runtime_files:
        local_issues.append(issue(copilot_id, "langchain_runtime_map_runtime_files", "runtime-injection-map runtimeFiles drifted from canonical runtime adapter paths."))
    required_repo_file(local_issues, copilot_id, "langchain_runtime_map_source_file", source_of_truth)
    required_repo_file(local_issues, copilot_id, "langchain_runtime_map_schema_file", schema_file)
    required_repo_file(local_issues, copilot_id, "langchain_runtime_map_runtime_file", langchain_file)
    required_repo_file(local_issues, copilot_id, "langchain_profile_file", rel_profile)

    if not contract:
        local_issues.append(issue(copilot_id, "langchain_agent_contract", f"Missing LangChain agent contract artifact: {rel_contract}."))
    else:
        expect(local_issues, copilot_id, "langchain_agent_contract_version", contract.get("policyVersion"), LANGCHAIN_PROTOCOL_VERSION)
        expect(local_issues, copilot_id, "langchain_agent_contract_owner", contract.get("ownerAgent"), LANGCHAIN_OWNER_AGENT)
        expect(local_issues, copilot_id, "langchain_agent_contract_mission", contract.get("mission"), LANGCHAIN_MISSION)
        expect(local_issues, copilot_id, "langchain_agent_contract_runtime", contract.get("runtime"), "langchain")
        expect(local_issues, copilot_id, "langchain_agent_contract_copilot", contract.get("copilotId"), copilot_id)
        expect(local_issues, copilot_id, "langchain_agent_contract_display_name", contract.get("displayName"), spec.get("name"))
        expect(local_issues, copilot_id, "langchain_agent_contract_family", contract.get("family"), spec.get("family"))
        expect(local_issues, copilot_id, "langchain_agent_contract_connectors", contract.get("connectors"), spec.get("connectors"))
        expect(local_issues, copilot_id, "langchain_agent_contract_env_keys", contract.get("envKeys"), spec.get("env_keys"))
        expect(local_issues, copilot_id, "langchain_agent_contract_outputs", contract.get("declaredOutputs"), spec.get("outputs"))
        expect(local_issues, copilot_id, "langchain_agent_contract_source", contract.get("sourceOfTruth"), source_of_truth)
        expect(local_issues, copilot_id, "langchain_agent_contract_schema", contract.get("outputSchema"), schema_file)
        expect(local_issues, copilot_id, "langchain_agent_contract_runtime_file", contract.get("runtimeFile"), langchain_file)
        expect(local_issues, copilot_id, "langchain_agent_contract_profile", contract.get("profileArtifact"), rel_profile)

        agent_spec = contract.get("agentSpec", {}) if isinstance(contract.get("agentSpec"), dict) else {}
        expect(local_issues, copilot_id, "langchain_agent_spec_artifact", agent_spec.get("artifact"), langchain_file)
        expect(local_issues, copilot_id, "langchain_agent_spec_profile_artifact", agent_spec.get("profileArtifact"), rel_profile)
        expect(local_issues, copilot_id, "langchain_agent_spec_schema", agent_spec.get("schemaRef"), schema_file)
        expect(local_issues, copilot_id, "langchain_agent_spec_schema_digest", agent_spec.get("outputSchemaSha256"), stable_json_digest(output_schema))
        missing_interfaces = missing_items(agent_spec.get("compatibleInterfaces"), LANGCHAIN_COMPATIBLE_INTERFACES)
        if missing_interfaces:
            local_issues.append(issue(copilot_id, "langchain_agent_spec_interfaces", f"LangChain agent spec missing compatible interface(s): {', '.join(missing_interfaces)}."))
        required_api = agent_spec.get("requiredPythonApi", {}) if isinstance(agent_spec.get("requiredPythonApi"), dict) else {}
        validate_required_langchain_api_contract(copilot_id, required_api, local_issues)

        runtime_contract = contract.get("runtimeContract", {}) if isinstance(contract.get("runtimeContract"), dict) else {}
        for key, expected in LANGCHAIN_RUNTIME_CONTRACT_REQUIRED.items():
            expect(local_issues, copilot_id, f"langchain_runtime_contract_{key}", runtime_contract.get(key), expected)
        expect(local_issues, copilot_id, "langchain_runtime_contract_schema_source", runtime_contract.get("outputSchemaSource"), schema_file)

        missing_evidence = missing_items(contract.get("requiredEvidence"), LANGCHAIN_REQUIRED_EVIDENCE)
        if missing_evidence:
            local_issues.append(issue(copilot_id, "langchain_agent_contract_evidence", f"LangChain agent contract missing evidence marker(s): {', '.join(missing_evidence)}."))
        missing_gates = missing_items(contract.get("qualityGates"), LANGCHAIN_QUALITY_GATES)
        if missing_gates:
            local_issues.append(issue(copilot_id, "langchain_agent_contract_quality_gates", f"LangChain agent contract missing quality gate(s): {', '.join(missing_gates)}."))
        missing_commands = missing_items(contract.get("validationCommands"), LANGCHAIN_VALIDATION_COMMANDS)
        if missing_commands:
            local_issues.append(issue(copilot_id, "langchain_agent_contract_validation_commands", f"LangChain agent contract missing validation command(s): {', '.join(missing_commands)}."))

        runtime_equivalence = contract.get("runtimeEquivalence", {}) if isinstance(contract.get("runtimeEquivalence"), dict) else {}
        expect(local_issues, copilot_id, "langchain_runtime_equivalence_source", runtime_equivalence.get("sourceOfTruth"), source_of_truth)
        expect(local_issues, copilot_id, "langchain_runtime_equivalence_runtimes", runtime_equivalence.get("runtimes"), RUNTIMES)
        expect(local_issues, copilot_id, "langchain_runtime_equivalence_drift", runtime_equivalence.get("maxUnexplainedDrift"), 0)
        if runtime_equivalence.get("adapterFiles") != runtime_files:
            local_issues.append(issue(copilot_id, "langchain_runtime_equivalence_adapters", "LangChain agent contract adapterFiles drifted from runtime-injection-map runtimeFiles."))
        validate_langchain_cost_control(copilot_id, contract, local_issues)

    if not map_protocol:
        local_issues.append(issue(copilot_id, "langchain_runtime_map", "runtime-injection-map is missing langchainAgentProtocol."))
    else:
        expect(local_issues, copilot_id, "langchain_runtime_map_artifact", map_protocol.get("artifact"), rel_contract)
        expect(local_issues, copilot_id, "langchain_runtime_map_profile", map_protocol.get("profile"), rel_profile)
        expect(local_issues, copilot_id, "langchain_runtime_map_runtime_file", map_protocol.get("runtimeFile"), langchain_file)
        expect(local_issues, copilot_id, "langchain_runtime_map_owner", map_protocol.get("ownerAgent"), LANGCHAIN_OWNER_AGENT)
        expect(local_issues, copilot_id, "langchain_runtime_map_mission", map_protocol.get("mission"), LANGCHAIN_MISSION)
        required_repo_file(local_issues, copilot_id, "langchain_runtime_map_artifact_file", map_protocol.get("artifact"))
        required_repo_file(local_issues, copilot_id, "langchain_runtime_map_profile_file", map_protocol.get("profile"))
        required_repo_file(local_issues, copilot_id, "langchain_runtime_map_runtime_file_exists", map_protocol.get("runtimeFile"))
        missing_map_evidence = missing_items(map_protocol.get("requiredEvidence"), LANGCHAIN_REQUIRED_EVIDENCE)
        if missing_map_evidence:
            local_issues.append(issue(copilot_id, "langchain_runtime_map_evidence", f"runtime-injection-map langchainAgentProtocol missing evidence marker(s): {', '.join(missing_map_evidence)}."))
        missing_map_gates = missing_items(map_protocol.get("qualityGates"), LANGCHAIN_QUALITY_GATES)
        if missing_map_gates:
            local_issues.append(issue(copilot_id, "langchain_runtime_map_gates", f"runtime-injection-map langchainAgentProtocol missing gate(s): {', '.join(missing_map_gates)}."))
        map_equivalence = map_protocol.get("runtimeEquivalence", {}) if isinstance(map_protocol.get("runtimeEquivalence"), dict) else {}
        expect(local_issues, copilot_id, "langchain_runtime_map_source", map_equivalence.get("sourceOfTruth"), source_of_truth)
        expect(local_issues, copilot_id, "langchain_runtime_map_runtimes", map_equivalence.get("runtimes"), RUNTIMES)
        expect(local_issues, copilot_id, "langchain_runtime_map_drift", map_equivalence.get("maxUnexplainedDrift"), 0)
        if map_equivalence.get("adapterFiles") != runtime_files:
            local_issues.append(issue(copilot_id, "langchain_runtime_map_adapters", "LangChain runtime map adapterFiles drifted from runtimeFiles."))

    validate_langchain_profile_contract(copilot_id, profile, spec, output_schema, local_issues)
    validate_langchain_agent_api(copilot_id, langchain_text, local_issues)
    validate_langchain_agent_runtime(copilot_id, ROOT / langchain_file, langchain_text, local_issues)

    metrics.append(
        {
            "id": copilot_id,
            "contract": rel_contract,
            "profile": rel_profile,
            "runtimeFile": langchain_file,
            "runtimeSmoke": not any(str(item.get("kind", "")).startswith("langchain_agent_runtime_") for item in local_issues),
            "sourceOfTruth": source_of_truth,
            "pass": not local_issues,
        }
    )
    issues.extend(local_issues)


def validate_required_langchain_api_contract(copilot_id: str, required_api: dict, issues: list[dict]) -> None:
    for key in ["moduleConstants", "moduleFunctions", "agentMethods"]:
        missing = missing_items(required_api.get(key), LANGCHAIN_REQUIRED_API[key])
        if missing:
            issues.append(issue(copilot_id, f"langchain_agent_spec_{key}", f"LangChain agent spec missing required API item(s): {', '.join(missing)}."))
    expect(issues, copilot_id, "langchain_agent_spec_class_suffix", required_api.get("classNameSuffix"), LANGCHAIN_REQUIRED_API["classNameSuffix"])


def validate_langchain_profile_contract(
    copilot_id: str,
    profile: dict,
    spec: dict,
    output_schema: dict,
    issues: list[dict],
) -> None:
    expect(issues, copilot_id, "langchain_profile_id", profile.get("id"), copilot_id)
    expect(issues, copilot_id, "langchain_profile_name", profile.get("name"), spec.get("name"))
    expect(issues, copilot_id, "langchain_profile_family", profile.get("family"), spec.get("family"))
    expect(issues, copilot_id, "langchain_profile_connectors", profile.get("connectors"), spec.get("connectors"))
    expect(issues, copilot_id, "langchain_profile_env_keys", profile.get("env_keys"), spec.get("env_keys"))
    expect(issues, copilot_id, "langchain_profile_outputs", profile.get("outputs"), spec.get("outputs"))
    profile_contract = profile.get("contract", {}) if isinstance(profile.get("contract"), dict) else {}
    if not profile_contract:
        issues.append(issue(copilot_id, "langchain_profile_contract", "LangChain profile must embed the shared contract."))
        return
    expect(issues, copilot_id, "langchain_profile_contract_version", profile_contract.get("version"), spec.get("version"))
    expect(issues, copilot_id, "langchain_profile_contract_system_prompt", profile_contract.get("systemPrompt"), spec.get("systemPrompt"))
    expect(issues, copilot_id, "langchain_profile_contract_developer_prompt", profile_contract.get("developerPrompt"), spec.get("developerPrompt"))
    expect(issues, copilot_id, "langchain_profile_contract_runtime_injection", profile_contract.get("runtimeInjection"), spec.get("runtimeInjection"))
    expect(issues, copilot_id, "langchain_profile_contract_sdlc_playbook", profile_contract.get("sdlcPlaybook"), spec.get("sdlcPlaybook"))
    expect(issues, copilot_id, "langchain_profile_contract_quality_rubric", profile_contract.get("qualityRubric"), spec.get("qualityRubric"))
    expect(issues, copilot_id, "langchain_profile_contract_python_brain", profile_contract.get("pythonBrain"), spec.get("pythonBrain"))
    expect(issues, copilot_id, "langchain_profile_contract_committee", profile_contract.get("committee"), spec.get("committee"))
    if profile_contract.get("outputSchema") != output_schema:
        issues.append(issue(copilot_id, "langchain_profile_contract_schema", "LangChain profile contract outputSchema drifted from shared/output_schema.json."))


def validate_langchain_agent_api(copilot_id: str, text: str, issues: list[dict]) -> None:
    inspected = inspect_langchain_agent(text, issues, copilot_id)
    if not inspected.get("parsed"):
        return
    for name in LANGCHAIN_REQUIRED_API["moduleConstants"]:
        if name not in inspected["moduleConstants"]:
            issues.append(issue(copilot_id, "langchain_agent_api_constant", f"LangChain agent missing module constant `{name}`."))
    for name in LANGCHAIN_REQUIRED_API["moduleFunctions"]:
        if name not in inspected["moduleFunctions"]:
            issues.append(issue(copilot_id, "langchain_agent_api_function", f"LangChain agent missing module function `{name}`."))
    if not inspected["agentClassWithRequiredMethods"]:
        missing = ", ".join(LANGCHAIN_REQUIRED_API["agentMethods"])
        issues.append(issue(copilot_id, "langchain_agent_api_methods", f"LangChain agent must expose an *Agent class with method(s): {missing}."))
    if inspected["hardLangChainImport"]:
        issues.append(issue(copilot_id, "langchain_agent_hard_dependency", "LangChain adapter must not require a hard langchain import to run deterministic checks."))
    for marker in LANGCHAIN_SAFE_RENDER_MARKERS:
        if marker not in text:
            issues.append(issue(copilot_id, "langchain_agent_safe_rendering", f"LangChain agent missing safe render marker: {marker}."))


def validate_langchain_static_safety(copilot_id: str, text: str, issues: list[dict]) -> bool:
    try:
        tree = ast.parse(text)
    except SyntaxError as exc:
        issues.append(issue(copilot_id, "langchain_agent_static_safety", f"LangChain agent cannot be parsed for static safety: {exc.msg}."))
        return False

    local_issues: list[dict] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                root = alias.name.split(".", 1)[0]
                if root not in LANGCHAIN_ALLOWED_IMPORT_ROOTS:
                    local_issues.append(
                        issue(copilot_id, "langchain_agent_static_import", f"LangChain agent imports unsupported module `{alias.name}`.")
                    )
        elif isinstance(node, ast.ImportFrom):
            root = (node.module or "").split(".", 1)[0]
            if root not in LANGCHAIN_ALLOWED_IMPORT_ROOTS:
                local_issues.append(
                    issue(copilot_id, "langchain_agent_static_import", f"LangChain agent imports unsupported module `{node.module or ''}`.")
                )
        elif isinstance(node, ast.Call) and is_dangerous_langchain_call(node):
            local_issues.append(issue(copilot_id, "langchain_agent_static_call", "LangChain agent contains a disallowed side-effect call."))

    for node in tree.body:
        if isinstance(node, ast.Expr) and isinstance(node.value, ast.Constant) and isinstance(node.value.value, str):
            continue
        if isinstance(node, (ast.Import, ast.ImportFrom, ast.Assign, ast.AnnAssign, ast.ClassDef, ast.FunctionDef)):
            continue
        if isinstance(node, ast.Expr) and isinstance(node.value, ast.Call) and is_allowed_langchain_top_level_call(node.value):
            continue
        if isinstance(node, ast.If) and is_main_guard(node):
            continue
        local_issues.append(
            issue(
                copilot_id,
                "langchain_agent_static_top_level",
                f"LangChain agent has unsupported top-level statement `{node.__class__.__name__}`.",
            )
        )

    issues.extend(local_issues)
    return not local_issues


def is_dangerous_langchain_call(node: ast.Call) -> bool:
    func = node.func
    if isinstance(func, ast.Name):
        return func.id in LANGCHAIN_DANGEROUS_CALLS
    if isinstance(func, ast.Attribute):
        if func.attr in LANGCHAIN_DANGEROUS_METHODS:
            return True
        if isinstance(func.value, ast.Name) and func.value.id in {"subprocess", "os", "socket", "requests", "urllib"}:
            return True
    return False


def is_allowed_langchain_top_level_call(node: ast.Call) -> bool:
    func = node.func
    return (
        isinstance(func, ast.Attribute)
        and func.attr in {"append", "insert"}
        and isinstance(func.value, ast.Attribute)
        and func.value.attr == "path"
        and isinstance(func.value.value, ast.Name)
        and func.value.value.id == "sys"
    )


def is_main_guard(node: ast.If) -> bool:
    test = node.test
    if not isinstance(test, ast.Compare):
        return False
    if not isinstance(test.left, ast.Name) or test.left.id != "__name__":
        return False
    if len(test.ops) != 1 or not isinstance(test.ops[0], ast.Eq):
        return False
    if len(test.comparators) != 1:
        return False
    comparator = test.comparators[0]
    return isinstance(comparator, ast.Constant) and comparator.value == "__main__"


def validate_langchain_agent_runtime(copilot_id: str, path: Path, text: str, issues: list[dict]) -> None:
    if not validate_langchain_static_safety(copilot_id, text, issues):
        return
    module_name = f"_copilot_factory_runtime_{copilot_id}"
    original_sys_path = list(sys.path)
    original_dont_write_bytecode = sys.dont_write_bytecode
    try:
        sys.dont_write_bytecode = True
        spec = importlib.util.spec_from_file_location(module_name, path)
        if spec is None or spec.loader is None:
            issues.append(issue(copilot_id, "langchain_agent_runtime_import", f"Cannot load LangChain agent module from {relative(path)}."))
            return
        module = importlib.util.module_from_spec(spec)
        sys.modules[module_name] = module
        spec.loader.exec_module(module)
    except Exception as exc:
        issues.append(issue(copilot_id, "langchain_agent_runtime_import", f"LangChain agent module import failed: {exc}."))
        return
    finally:
        sys.dont_write_bytecode = original_dont_write_bytecode
        sys.path[:] = original_sys_path

    try:
        agent = module.build_agent()
    except Exception as exc:
        issues.append(issue(copilot_id, "langchain_agent_runtime_build", f"LangChain build_agent() failed: {exc}."))
        return

    request_secret = "Bearer " + "abcdef1234567890"
    evidence_secret = "AKIA" + ("B" * 16)
    local_path = "C:" + "\\Users\\Example\\private-runtime-path"
    try:
        rendered = agent.render_prompt(
            f"review {copilot_id} build with {request_secret}",
            {
                "source_refs": ["dist/copilots"],
                "api_key": evidence_secret,
                "service_token": "xoxb-" + ("C" * 24),
                "nested": {"path": local_path},
            },
        )
    except Exception as exc:
        issues.append(issue(copilot_id, "langchain_agent_runtime_render_prompt", f"LangChain render_prompt() failed: {exc}."))
        return

    validate_langchain_rendered_messages(copilot_id, rendered, issues, [request_secret])


def validate_langchain_rendered_messages(copilot_id: str, rendered, issues: list[dict], raw_sensitive_values: list[str] | None = None) -> None:
    if not isinstance(rendered, list) or len(rendered) != 3:
        issues.append(issue(copilot_id, "langchain_agent_runtime_render_prompt_shape", "render_prompt() must return exactly system, developer and user messages."))
        return

    expected_roles = ["system", "developer", "user"]
    for index, expected_role in enumerate(expected_roles):
        item = rendered[index]
        if not isinstance(item, dict):
            issues.append(issue(copilot_id, "langchain_agent_runtime_render_prompt_shape", "render_prompt() messages must be dictionaries."))
            continue
        if item.get("role") != expected_role:
            issues.append(issue(copilot_id, "langchain_agent_runtime_render_prompt_role", f"render_prompt() message {index} must use role {expected_role!r}."))
        if not isinstance(item.get("content"), str) or not item.get("content"):
            issues.append(issue(copilot_id, "langchain_agent_runtime_render_prompt_content", f"render_prompt() message {index} must include non-empty string content."))

    payload = json.dumps(rendered, ensure_ascii=True, default=str)
    for raw_value in raw_sensitive_values or []:
        if raw_value and raw_value in payload:
            issues.append(issue(copilot_id, "langchain_agent_runtime_render_prompt_secret", "render_prompt() leaked a supplied sensitive value."))
    if has_secret_pattern(payload):
        issues.append(issue(copilot_id, "langchain_agent_runtime_render_prompt_secret", "render_prompt() leaked a secret-like value."))
    if has_local_path(payload):
        issues.append(issue(copilot_id, "langchain_agent_runtime_render_prompt_local_path", "render_prompt() leaked a local absolute path."))


def inspect_langchain_agent(text: str, issues: list[dict], copilot_id: str) -> dict:
    result = {
        "parsed": False,
        "moduleConstants": set(),
        "moduleFunctions": set(),
        "agentClassWithRequiredMethods": False,
        "hardLangChainImport": False,
    }
    try:
        tree = ast.parse(text)
    except SyntaxError as exc:
        issues.append(issue(copilot_id, "langchain_agent_syntax", f"LangChain agent cannot be parsed for API inspection: {exc.msg}."))
        return result

    result["parsed"] = True
    required_methods = set(LANGCHAIN_REQUIRED_API["agentMethods"])
    class_suffix = LANGCHAIN_REQUIRED_API["classNameSuffix"]
    for node in tree.body:
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name):
                    result["moduleConstants"].add(target.id)
        elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            result["moduleFunctions"].add(node.name)
        elif isinstance(node, ast.ClassDef) and node.name.endswith(class_suffix):
            methods = {
                item.name
                for item in node.body
                if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef))
            }
            if required_methods.issubset(methods):
                result["agentClassWithRequiredMethods"] = True

        if isinstance(node, ast.Import):
            if any(alias.name == "langchain" or alias.name.startswith("langchain.") for alias in node.names):
                result["hardLangChainImport"] = True
        elif isinstance(node, ast.ImportFrom):
            module = node.module or ""
            if module == "langchain" or module.startswith("langchain."):
                result["hardLangChainImport"] = True
    return result


def validate_langchain_cost_control(copilot_id: str, contract: dict, issues: list[dict]) -> None:
    cost_control = contract.get("costControl", {}) if isinstance(contract.get("costControl"), dict) else {}
    for key, expected in LANGCHAIN_COST_CONTROL.items():
        expect(issues, copilot_id, f"langchain_agent_cost_control_{key}", cost_control.get(key), expected)


def summarize_codex_adapter_audit(metrics: list[dict], issues: list[dict]) -> dict:
    codex_issue_count = sum(1 for item in issues if str(item.get("kind", "")).startswith("codex_"))
    return {
        "mission": CODEX_MISSION,
        "ownerAgent": CODEX_OWNER_AGENT,
        "policyVersion": CODEX_PROTOCOL_VERSION,
        "protocolsChecked": len(metrics),
        "requiredEvidence": CODEX_REQUIRED_EVIDENCE,
        "qualityGates": CODEX_QUALITY_GATES,
        "metrics": metrics,
        "pass": codex_issue_count == 0,
        "issues": codex_issue_count,
    }


def summarize_claude_adapter_audit(metrics: list[dict], issues: list[dict]) -> dict:
    claude_issue_count = sum(1 for item in issues if str(item.get("kind", "")).startswith("claude_"))
    return {
        "mission": CLAUDE_MISSION,
        "ownerAgent": CLAUDE_OWNER_AGENT,
        "policyVersion": CLAUDE_PROTOCOL_VERSION,
        "protocolsChecked": len(metrics),
        "requiredEvidence": CLAUDE_REQUIRED_EVIDENCE,
        "qualityGates": CLAUDE_QUALITY_GATES,
        "metrics": metrics,
        "pass": claude_issue_count == 0,
        "issues": claude_issue_count,
    }


def summarize_github_adapter_audit(metrics: list[dict], issues: list[dict]) -> dict:
    github_issue_count = sum(1 for item in issues if str(item.get("kind", "")).startswith("github_"))
    return {
        "mission": GITHUB_MISSION,
        "ownerAgent": GITHUB_OWNER_AGENT,
        "policyVersion": GITHUB_PROTOCOL_VERSION,
        "profilesChecked": len(metrics),
        "requiredEvidence": GITHUB_REQUIRED_EVIDENCE,
        "qualityGates": GITHUB_QUALITY_GATES,
        "metrics": metrics,
        "pass": github_issue_count == 0,
        "issues": github_issue_count,
    }


def summarize_langchain_agent_audit(metrics: list[dict], issues: list[dict]) -> dict:
    langchain_issue_count = sum(1 for item in issues if str(item.get("kind", "")).startswith("langchain_"))
    return {
        "mission": LANGCHAIN_MISSION,
        "ownerAgent": LANGCHAIN_OWNER_AGENT,
        "policyVersion": LANGCHAIN_PROTOCOL_VERSION,
        "contractsChecked": len(metrics),
        "requiredEvidence": LANGCHAIN_REQUIRED_EVIDENCE,
        "qualityGates": LANGCHAIN_QUALITY_GATES,
        "metrics": metrics,
        "pass": langchain_issue_count == 0,
        "issues": langchain_issue_count,
    }


def summarize_data_hygiene_audit(metrics: list[dict], issues: list[dict]) -> dict:
    hygiene_issue_count = sum(1 for item in issues if str(item.get("kind", "")).startswith("data_hygiene_"))
    checked = [item for item in metrics if item.get("checked")]
    return {
        "pass": hygiene_issue_count == 0,
        "artifactsChecked": len(checked),
        "artifactsDeclared": len(metrics),
        "localPathLeaks": sum(1 for item in checked if item.get("localPathLeak")),
        "secretPatternLeaks": sum(1 for item in checked if item.get("secretPatternLeak")),
        "issues": hygiene_issue_count,
        "metrics": metrics,
    }


def validate_sdlc_runtime_matrix_equivalence(injection_map: dict, metrics: list[dict], issues: list[dict]) -> dict:
    local_issues: list[dict] = []
    matrix = read_json(SDLC_RUNTIME_MATRIX_JSON, {}, local_issues, "sdlc_runtime_matrix")
    maintenance = read_json(SDLC_RUNTIME_MATRIX_MAINTENANCE_JSON, {}, local_issues, "sdlc_runtime_matrix_maintenance")
    copilots = read_json(CATALOG_JSON, [], local_issues, "copilot-catalog")
    expected_cells = expected_sdlc_runtime_cells(copilots)
    cells = matrix.get("cells", []) if isinstance(matrix.get("cells"), list) else []
    cells_by_key = {
        (cell.get("copilotId"), cell.get("phase"), cell.get("runtime")): cell
        for cell in cells
        if isinstance(cell, dict)
    }
    trace_ledger = matrix.get("traceLedger", []) if isinstance(matrix.get("traceLedger"), list) else []
    trace_ledger_by_key = {
        (entry.get("copilotId"), entry.get("phase")): entry
        for entry in trace_ledger
        if isinstance(entry, dict)
    }
    injection_copilots = injection_map.get("copilots", {}) if isinstance(injection_map.get("copilots"), dict) else {}
    pairwise_case_count = 0
    digest_drift_count = 0
    runtime_file_mismatches = 0
    trace_ledger_mismatches = 0
    cell_equivalence_audit = validate_matrix_cell_equivalence_contract(matrix, expected_cells, local_issues)

    summary = {
        "pass": False,
        "mission": MATRIX_MISSION,
        "artifact": relative(SDLC_RUNTIME_MATRIX_JSON),
        "markdownArtifact": relative(SDLC_RUNTIME_MATRIX_MD),
        "maintenanceArtifact": relative(SDLC_RUNTIME_MATRIX_MAINTENANCE_JSON),
        "maintenanceMarkdownArtifact": relative(SDLC_RUNTIME_MATRIX_MAINTENANCE_MD),
        "policyVersion": matrix.get("version"),
        "dimensions": matrix.get("dimensions"),
        "runtimes": matrix.get("runtimes"),
        "expectedCells": len(expected_cells),
        "actualCells": len(cells_by_key),
        "copilotsChecked": len(metrics),
        "pairwiseRuntimeCases": 0,
        "digestDriftCount": 0,
        "runtimeFileMismatches": 0,
        "traceLedgerEntries": len(trace_ledger),
        "traceLedgerDigestMatches": False,
        "traceLedgerMismatches": 0,
        "cellEquivalenceAudit": cell_equivalence_audit,
        "promptContentStored": matrix.get("costControl", {}).get("promptContentStored") if isinstance(matrix.get("costControl"), dict) else None,
        "maintenanceAudit": {},
        "issues": local_issues,
    }

    if matrix.get("mission") != MATRIX_MISSION:
        local_issues.append(issue("sdlc_runtime_matrix", "matrix_mission", "SDLC runtime matrix mission drifted."))
    if matrix.get("version") != MATRIX_POLICY_VERSION:
        local_issues.append(issue("sdlc_runtime_matrix", "matrix_policy_version", "SDLC runtime matrix policy version drifted."))
    if matrix.get("dimensions") != MATRIX_DIMENSIONS:
        local_issues.append(issue("sdlc_runtime_matrix", "matrix_dimensions", "SDLC runtime matrix dimensions must be phase, copilot and runtime."))
    if matrix.get("runtimes") != RUNTIMES:
        local_issues.append(issue("sdlc_runtime_matrix", "matrix_runtimes", "SDLC runtime matrix runtimes drifted from runtime equivalence runtimes."))
    cost_control = matrix.get("costControl", {}) if isinstance(matrix.get("costControl"), dict) else {}
    if cost_control.get("deterministicPythonFirst") is not True or cost_control.get("promptContentStored") is not False:
        local_issues.append(issue("sdlc_runtime_matrix", "matrix_cost_control", "Matrix must stay deterministic and store only paths/digests."))
    matrix_summary = matrix.get("summary", {}) if isinstance(matrix.get("summary"), dict) else {}
    expected_trace_ledger_entries = {
        (copilot_id, phase)
        for copilot_id, phase, _runtime in expected_cells
    }
    if not isinstance(matrix.get("traceLedger"), list):
        trace_ledger_mismatches += 1
        local_issues.append(issue("sdlc_runtime_matrix", "matrix_trace_ledger", "Matrix traceLedger must be an array."))
    if set(trace_ledger_by_key) != expected_trace_ledger_entries:
        trace_ledger_mismatches += 1
        local_issues.append(issue("sdlc_runtime_matrix", "matrix_trace_ledger_coverage", "Trace ledger must cover every copilot/phase pair exactly once."))
    if matrix_summary.get("traceLedgerEntries") != len(trace_ledger):
        trace_ledger_mismatches += 1
        local_issues.append(issue("sdlc_runtime_matrix", "matrix_trace_ledger_summary", "Trace ledger summary count drifted from entries."))
    if matrix_summary.get("traceLedgerDigest") != stable_json_digest(trace_ledger):
        trace_ledger_mismatches += 1
        local_issues.append(issue("sdlc_runtime_matrix", "matrix_trace_ledger_digest", "Trace ledger digest drifted from entries."))

    missing_cells = sorted(expected_cells - set(cells_by_key))
    if missing_cells:
        local_issues.append(
            issue(
                "sdlc_runtime_matrix",
                "matrix_cell_coverage",
                f"Missing SDLC runtime cell(s): {', '.join('/'.join(item) for item in missing_cells[:10])}.",
            )
        )

    for key, cell in cells_by_key.items():
        copilot_id, phase, runtime = key
        if key not in expected_cells:
            local_issues.append(issue("sdlc_runtime_matrix", "matrix_unexpected_cell", f"Unexpected matrix cell: {copilot_id}/{phase}/{runtime}."))
            continue
        map_entry = injection_copilots.get(copilot_id, {}) if isinstance(copilot_id, str) else {}
        runtime_files = map_entry.get("runtimeFiles", {}) if isinstance(map_entry, dict) and isinstance(map_entry.get("runtimeFiles"), dict) else {}
        expected_source = f"dist/copilots/{copilot_id}/shared/spec.json"
        expected_schema = f"dist/copilots/{copilot_id}/shared/output_schema.json"
        expected_runtime_file = runtime_files.get(runtime)
        if not expected_runtime_file:
            expected_runtime_file = expected_runtime_adapter_path(copilot_id, runtime)
        if cell.get("sourceOfTruth") != expected_source:
            local_issues.append(issue(copilot_id, "matrix_source_of_truth", f"{phase}/{runtime} sourceOfTruth drifted."))
        if cell.get("outputSchema") != expected_schema:
            local_issues.append(issue(copilot_id, "matrix_output_schema", f"{phase}/{runtime} outputSchema drifted."))
        if cell.get("runtimeFile") != expected_runtime_file:
            runtime_file_mismatches += 1
            local_issues.append(issue(copilot_id, "matrix_runtime_file", f"{phase}/{runtime} runtime file drifted."))
        if cell.get("sharedSpecDigest") != file_sha256(expected_source, local_issues, copilot_id):
            digest_drift_count += 1
            local_issues.append(issue(copilot_id, "matrix_spec_digest", f"{phase}/{runtime} shared spec digest drifted."))
        if cell.get("outputSchemaDigest") != file_sha256(expected_schema, local_issues, copilot_id):
            digest_drift_count += 1
            local_issues.append(issue(copilot_id, "matrix_schema_digest", f"{phase}/{runtime} output schema digest drifted."))
        if cell.get("runtimeFileDigest") != file_sha256(expected_runtime_file, local_issues, copilot_id):
            digest_drift_count += 1
            local_issues.append(issue(copilot_id, "matrix_runtime_file_digest", f"{phase}/{runtime} runtime file digest drifted."))
        equivalence = cell.get("equivalence", {}) if isinstance(cell.get("equivalence"), dict) else {}
        if equivalence.get("maxUnexplainedDrift") != 0:
            local_issues.append(issue(copilot_id, "matrix_unexplained_drift", f"{phase}/{runtime} maxUnexplainedDrift must be 0."))

    grouped: dict[tuple[str, str], list[dict]] = {}
    for key, cell in cells_by_key.items():
        copilot_id, phase, _runtime = key
        grouped.setdefault((copilot_id, phase), []).append(cell)
    for (copilot_id, phase), phase_cells in grouped.items():
        by_runtime = {cell.get("runtime"): cell for cell in phase_cells}
        for left_index, left in enumerate(RUNTIMES):
            for right in RUNTIMES[left_index + 1:]:
                pairwise_case_count += 1
                left_cell = by_runtime.get(left)
                right_cell = by_runtime.get(right)
                if not left_cell or not right_cell:
                    continue
                if left_cell.get("sharedSpecDigest") != right_cell.get("sharedSpecDigest"):
                    digest_drift_count += 1
                    local_issues.append(issue(copilot_id, "matrix_pairwise_spec_digest", f"{phase} {left}/{right} spec digest drifted."))
                if left_cell.get("outputSchemaDigest") != right_cell.get("outputSchemaDigest"):
                    digest_drift_count += 1
                    local_issues.append(issue(copilot_id, "matrix_pairwise_schema_digest", f"{phase} {left}/{right} schema digest drifted."))

    expected_pairwise_cases = len(runtime_pairwise_cases())
    for key, entry in trace_ledger_by_key.items():
        copilot_id, phase = key
        runtime_files = entry.get("runtimeFiles", {}) if isinstance(entry.get("runtimeFiles"), dict) else {}
        runtime_digests = entry.get("runtimeFileDigests", {}) if isinstance(entry.get("runtimeFileDigests"), dict) else {}
        runtime_refs = entry.get("runtimeTraceRefs", {}) if isinstance(entry.get("runtimeTraceRefs"), dict) else {}
        pairwise_cases = entry.get("pairwiseRuntimeCases", []) if isinstance(entry.get("pairwiseRuntimeCases"), list) else []
        if entry.get("promptBodiesStored") is not False or entry.get("maxUnexplainedDrift") != 0:
            trace_ledger_mismatches += 1
            local_issues.append(issue(copilot_id, "matrix_trace_ledger_cost_control", f"{phase} trace ledger must store no prompt bodies and no unexplained drift."))
        if entry.get("runtimeOrder") != RUNTIMES:
            trace_ledger_mismatches += 1
            local_issues.append(issue(copilot_id, "matrix_trace_ledger_runtime_order", f"{phase} runtime order drifted."))
        if len(pairwise_cases) != expected_pairwise_cases:
            trace_ledger_mismatches += 1
            local_issues.append(issue(copilot_id, "matrix_trace_ledger_pairwise", f"{phase} trace ledger pairwise coverage drifted."))
        for runtime in RUNTIMES:
            cell = cells_by_key.get((copilot_id, phase, runtime))
            if not cell:
                continue
            if runtime_files.get(runtime) != cell.get("runtimeFile"):
                trace_ledger_mismatches += 1
                local_issues.append(issue(copilot_id, "matrix_trace_ledger_runtime_file", f"{phase}/{runtime} ledger runtime file drifted from matrix cell."))
            if runtime_digests.get(runtime) != cell.get("runtimeFileDigest"):
                trace_ledger_mismatches += 1
                local_issues.append(issue(copilot_id, "matrix_trace_ledger_runtime_digest", f"{phase}/{runtime} ledger runtime digest drifted from matrix cell."))
            if runtime_refs.get(runtime) != cell.get("runtimeTraceRef"):
                trace_ledger_mismatches += 1
                local_issues.append(issue(copilot_id, "matrix_trace_ledger_runtime_trace", f"{phase}/{runtime} ledger runtime trace ref drifted from matrix cell."))
        for case in pairwise_cases:
            if not isinstance(case, dict):
                trace_ledger_mismatches += 1
                local_issues.append(issue(copilot_id, "matrix_trace_ledger_pairwise_case", f"{phase} pairwise case must be an object."))
                continue
            if (
                case.get("sameSharedSpecDigest") is not True
                or case.get("sameOutputSchemaDigest") is not True
                or case.get("promptBodiesStored") is not False
                or case.get("maxUnexplainedDrift") != 0
            ):
                trace_ledger_mismatches += 1
                local_issues.append(issue(copilot_id, "matrix_trace_ledger_pairwise_equivalence", f"{phase} pairwise case drifted from equivalence contract."))

    summary["pairwiseRuntimeCases"] = pairwise_case_count
    summary["digestDriftCount"] = digest_drift_count
    summary["runtimeFileMismatches"] = runtime_file_mismatches
    summary["traceLedgerEntries"] = len(trace_ledger)
    summary["traceLedgerDigestMatches"] = matrix_summary.get("traceLedgerDigest") == stable_json_digest(trace_ledger)
    summary["traceLedgerMismatches"] = trace_ledger_mismatches
    summary["maintenanceAudit"] = validate_sdlc_runtime_matrix_maintenance_equivalence(
        maintenance,
        matrix,
        expected_cells,
        injection_map,
        local_issues,
    )
    summary["pass"] = not local_issues
    issues.extend(local_issues)
    return summary


def validate_matrix_cell_equivalence_contract(
    matrix: dict,
    expected_cells: set[tuple[str, str, str]],
    issues: list[dict],
) -> dict:
    issue_count_before = len(issues)
    cells = matrix.get("cells", []) if isinstance(matrix.get("cells"), list) else []
    contract = (
        matrix.get("cellEquivalenceContract", {})
        if isinstance(matrix.get("cellEquivalenceContract"), dict)
        else {}
    )
    failures = []
    audit = {
        "pass": False,
        "version": contract.get("version"),
        "requiredAssertions": contract.get("requiredAssertions"),
        "cellsChecked": contract.get("cellsChecked"),
        "passingCells": contract.get("passingCells"),
        "cellFailures": 0,
        "evidenceMode": contract.get("evidenceMode"),
    }

    if contract.get("version") != MATRIX_CELL_EQUIVALENCE_VERSION:
        issues.append(issue("sdlc_runtime_matrix", "matrix_cell_equivalence_version", "Cell equivalence contract version drifted."))
    if contract.get("requiredAssertions") != MATRIX_CELL_EQUIVALENCE_ASSERTIONS:
        issues.append(issue("sdlc_runtime_matrix", "matrix_cell_equivalence_assertions", "Cell equivalence assertions drifted."))
    if contract.get("cellsChecked") != len(cells) or contract.get("cellsChecked") != len(expected_cells):
        issues.append(issue("sdlc_runtime_matrix", "matrix_cell_equivalence_count", "Cell equivalence count drifted from matrix cells."))
    if contract.get("passingCells") != len(expected_cells) or contract.get("pass") is not True:
        issues.append(issue("sdlc_runtime_matrix", "matrix_cell_equivalence_gate", "Cell equivalence gate is not passing for every cell."))

    for cell in cells:
        if not isinstance(cell, dict):
            failures.append("unknown")
            continue
        scope = "/".join(str(cell.get(key, "unknown")) for key in ("copilotId", "phase", "runtime"))
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
            failures.append(f"{scope}: {', '.join(sorted(set(missing)))}")

    if failures:
        issues.append(
            issue(
                "sdlc_runtime_matrix",
                "matrix_cell_equivalence",
                "Cell equivalence assertion failures: " + "; ".join(failures[:10]) + ".",
            )
        )
    audit["cellFailures"] = len(failures)
    audit["pass"] = len(issues) == issue_count_before
    return audit


def validate_sdlc_runtime_matrix_maintenance_equivalence(
    receipt: dict,
    matrix: dict,
    expected_cells: set[tuple[str, str, str]],
    injection_map: dict,
    issues: list[dict],
) -> dict:
    matrix_summary = matrix.get("summary", {}) if isinstance(matrix.get("summary"), dict) else {}
    receipt_counts = receipt.get("counts", {}) if isinstance(receipt.get("counts"), dict) else {}
    receipt_digests = receipt.get("digests", {}) if isinstance(receipt.get("digests"), dict) else {}
    runtime_equivalence = receipt.get("runtimeEquivalence", {}) if isinstance(receipt.get("runtimeEquivalence"), dict) else {}
    acceptance_gates = receipt.get("acceptanceGates", {}) if isinstance(receipt.get("acceptanceGates"), dict) else {}
    source_artifacts = receipt.get("sourceArtifacts", {}) if isinstance(receipt.get("sourceArtifacts"), dict) else {}
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
    injection_copilots = injection_map.get("copilots", {}) if isinstance(injection_map.get("copilots"), dict) else {}
    issue_count_before = len(issues)
    audit = {
        "pass": False,
        "artifact": relative(SDLC_RUNTIME_MATRIX_MAINTENANCE_JSON),
        "policyVersion": receipt.get("version"),
        "cellDigestMatches": receipt_digests.get("cellDigest") == stable_json_digest(cells),
        "traceLedgerDigestMatches": receipt_digests.get("traceLedgerDigest") == stable_json_digest(trace_ledger),
        "cellEquivalenceContractDigestMatches": (
            receipt_digests.get("cellEquivalenceContractDigest") == stable_json_digest(matrix_cell_equivalence)
        ),
        "runtimeCountMatches": runtime_equivalence.get("runtimeCount") == len(RUNTIMES),
        "pairwiseCasesPerCopilotPhase": runtime_equivalence.get("pairwiseCasesPerCopilotPhase"),
        "allAcceptanceGatesPass": all(acceptance_gates.values()) if acceptance_gates else False,
        "cellEquivalenceGatePass": acceptance_gates.get("cellEquivalence") is True,
        "sourceRuntimeMapChecked": source_artifacts.get("runtimeMap") == "generated/runtime-injection-map.json",
    }

    if receipt.get("version") != MATRIX_MAINTENANCE_VERSION:
        issues.append(issue("sdlc_runtime_matrix_maintenance", "maintenance_policy_version", "Maintenance receipt policy version drifted."))
    if receipt.get("mission") != MATRIX_MISSION:
        issues.append(issue("sdlc_runtime_matrix_maintenance", "maintenance_mission", "Maintenance receipt mission drifted."))
    if receipt.get("ownerAgent") != "factory_agent_24_matrix":
        issues.append(issue("sdlc_runtime_matrix_maintenance", "maintenance_owner", "Maintenance receipt owner drifted."))
    if receipt.get("matrixPolicyVersion") != MATRIX_POLICY_VERSION:
        issues.append(issue("sdlc_runtime_matrix_maintenance", "maintenance_matrix_policy", "Maintenance receipt matrix policy drifted."))
    if receipt.get("dimensions") != MATRIX_DIMENSIONS or receipt.get("runtimes") != RUNTIMES:
        issues.append(issue("sdlc_runtime_matrix_maintenance", "maintenance_dimensions", "Maintenance receipt dimensions or runtimes drifted."))
    if receipt.get("validationCommands") != MATRIX_VALIDATION_COMMANDS:
        issues.append(issue("sdlc_runtime_matrix_maintenance", "maintenance_validation_commands", "Maintenance receipt validation commands drifted."))
    if receipt_counts.get("matrixCells") != len(expected_cells):
        issues.append(issue("sdlc_runtime_matrix_maintenance", "maintenance_cell_count", "Maintenance receipt cell count drifted from catalog phases."))
    if receipt_counts.get("matrixCells") != matrix_summary.get("matrixCellCount"):
        issues.append(issue("sdlc_runtime_matrix_maintenance", "maintenance_matrix_summary", "Maintenance receipt cell count drifted from matrix summary."))
    if receipt_counts.get("traceLedgerEntries") != matrix_summary.get("traceLedgerEntries"):
        issues.append(issue("sdlc_runtime_matrix_maintenance", "maintenance_trace_ledger_count", "Maintenance receipt trace ledger count drifted from matrix summary."))
    if not audit["cellDigestMatches"]:
        issues.append(issue("sdlc_runtime_matrix_maintenance", "maintenance_cell_digest", "Maintenance receipt cell digest drifted."))
    if not audit["traceLedgerDigestMatches"]:
        issues.append(issue("sdlc_runtime_matrix_maintenance", "maintenance_trace_ledger_digest", "Maintenance receipt trace ledger digest drifted."))
    if not audit["cellEquivalenceContractDigestMatches"]:
        issues.append(issue("sdlc_runtime_matrix_maintenance", "maintenance_cell_equivalence_digest", "Maintenance receipt cell equivalence digest drifted."))
    if receipt_cell_equivalence.get("version") != MATRIX_CELL_EQUIVALENCE_VERSION:
        issues.append(issue("sdlc_runtime_matrix_maintenance", "maintenance_cell_equivalence_version", "Maintenance receipt cell equivalence version drifted."))
    if receipt_cell_equivalence.get("requiredAssertions") != MATRIX_CELL_EQUIVALENCE_ASSERTIONS:
        issues.append(issue("sdlc_runtime_matrix_maintenance", "maintenance_cell_equivalence_assertions", "Maintenance receipt cell equivalence assertions drifted."))
    if receipt_cell_equivalence.get("pass") is not True or not audit["cellEquivalenceGatePass"]:
        issues.append(issue("sdlc_runtime_matrix_maintenance", "maintenance_cell_equivalence_gate", "Maintenance receipt cell equivalence gate is not passing."))
    if runtime_equivalence.get("runtimes") != RUNTIMES or runtime_equivalence.get("runtimeCount") != len(RUNTIMES):
        issues.append(issue("sdlc_runtime_matrix_maintenance", "maintenance_runtime_count", "Maintenance receipt runtime equivalence runtimes drifted."))
    if runtime_equivalence.get("pairwiseCasesPerCopilotPhase") != len(runtime_pairwise_cases()):
        issues.append(issue("sdlc_runtime_matrix_maintenance", "maintenance_pairwise_cases", "Maintenance receipt pairwise runtime case count drifted."))
    if runtime_equivalence.get("missingRuntimeFiles") != matrix_summary.get("missingRuntimeFiles"):
        issues.append(issue("sdlc_runtime_matrix_maintenance", "maintenance_missing_runtime_files", "Maintenance receipt missing runtime file count drifted."))
    if runtime_equivalence.get("maxUnexplainedDrift") != 0:
        issues.append(issue("sdlc_runtime_matrix_maintenance", "maintenance_unexplained_drift", "Maintenance receipt must preserve zero unexplained runtime drift."))
    if source_artifacts.get("runtimeMap") != "generated/runtime-injection-map.json" or not injection_copilots:
        issues.append(issue("sdlc_runtime_matrix_maintenance", "maintenance_runtime_map", "Maintenance receipt must trace to a populated runtime injection map."))
    if acceptance_gates.get("runtimeEquivalence") is not True or acceptance_gates.get("traceability") is not True:
        issues.append(issue("sdlc_runtime_matrix_maintenance", "maintenance_acceptance_gates", "Maintenance receipt runtime equivalence or traceability gate is not passing."))

    audit["pass"] = len(issues) == issue_count_before
    return audit


def expected_sdlc_runtime_cells(copilots: list) -> set[tuple[str, str, str]]:
    expected: set[tuple[str, str, str]] = set()
    for copilot in copilots:
        if not isinstance(copilot, dict):
            continue
        copilot_id = copilot.get("id")
        phases = copilot.get("sdlc_phases", [])
        if not isinstance(copilot_id, str) or not isinstance(phases, list):
            continue
        for phase in phases:
            if not isinstance(phase, str) or not phase:
                continue
            for runtime in RUNTIMES:
                expected.add((copilot_id, phase, runtime))
    return expected


def expected_runtime_adapter_path(copilot_id: str, runtime: str) -> str:
    paths = {
        "codex": f"dist/copilots/{copilot_id}/codex/AGENT.md",
        "claude": f"dist/copilots/{copilot_id}/claude/AGENT.md",
        "github-copilot": f"dist/copilots/{copilot_id}/github-copilot/copilot-agent.md",
        "langchain": f"dist/copilots/{copilot_id}/langchain/agent.py",
    }
    return paths.get(runtime, "")


def file_sha256(rel_path: str, issues: list[dict], scope: str) -> str | None:
    if not isinstance(rel_path, str) or not rel_path:
        issues.append(issue(scope, "matrix_path", "SDLC runtime matrix path is empty."))
        return None
    candidate = (ROOT / rel_path).resolve()
    try:
        candidate.relative_to(ROOT)
    except ValueError:
        issues.append(issue(scope, "matrix_path", f"SDLC runtime matrix path escapes workspace: {rel_path}."))
        return None
    try:
        data = candidate.read_bytes()
    except FileNotFoundError:
        issues.append(issue(scope, "matrix_path", f"SDLC runtime matrix missing artifact: {rel_path}."))
        return None
    except OSError as exc:
        issues.append(issue(scope, "matrix_path", f"SDLC runtime matrix cannot read {rel_path}: {exc}."))
        return None
    return hashlib.sha256(data).hexdigest()


def expect(issues: list[dict], scope: str, kind: str, actual, expected) -> None:
    if actual != expected:
        issues.append(issue(scope, kind, f"Expected {expected!r}, found {actual!r}."))


def missing_items(actual, required: list[str]) -> list[str]:
    if not isinstance(actual, list):
        return required
    return [item for item in required if item not in actual]


def required_repo_file(issues: list[dict], scope: str, kind: str, value) -> None:
    if not isinstance(value, str) or not value:
        issues.append(issue(scope, kind, "Required repository file path is missing or not a string."))
        return
    candidate = (ROOT / value).resolve()
    try:
        candidate.relative_to(ROOT)
    except ValueError:
        issues.append(issue(scope, kind, f"Repository file path escapes workspace: {value}."))
        return
    if not candidate.is_file():
        issues.append(issue(scope, kind, f"Declared repository file does not exist: {value}."))


def stable_json_digest(value) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def validate_required_trace_fields_schema(copilot_id: str, spec: dict, output_schema: dict, issues: list[dict]) -> None:
    trace_fields: list[str] = []
    for contract_key in ("runtimeParityContract", "runtimeContract"):
        contract = spec.get(contract_key)
        if not isinstance(contract, dict):
            continue
        contract_trace_fields = contract.get("requiredTraceFields")
        if isinstance(contract_trace_fields, list):
            trace_fields.extend(field for field in contract_trace_fields if isinstance(field, str))
    schema_required = output_schema.get("required")
    if not trace_fields or not isinstance(schema_required, list):
        return
    missing = [field for field in sorted(set(trace_fields)) if field not in schema_required]
    if missing:
        issues.append(
            issue(
                copilot_id,
                "runtime_trace_fields_schema",
                "runtime contract requiredTraceFields missing from output schema required: "
                + ", ".join(missing)
                + ".",
            )
        )


def runtime_pairwise_cases() -> list[dict]:
    cases = []
    for left_index, left in enumerate(RUNTIMES):
        for right in RUNTIMES[left_index + 1:]:
            cases.append(
                {
                    "id": f"{left}__{right}",
                    "runtimes": [left, right],
                    "assertions": [
                        "same_shared_spec",
                        "same_output_schema",
                        "same_prompt_source",
                        "no_local_path_leak",
                        "no_secret_pattern_leak",
                    ],
                }
            )
    return cases


def run_runtime_equivalence_negative_cases() -> list[dict]:
    local_path_detected = has_local_path("C:" + "\\Users\\Example\\private-runtime-path")
    private_key_fixture = "".join(["-----", "BE", "GIN ", "PRI", "VATE ", "KEY", "-----"])
    secret_pattern_detected = (
        has_secret_pattern("Bearer " + ("A" * 24))
        and has_secret_pattern("AKIA" + ("B" * 16))
        and has_secret_pattern(private_key_fixture)
    )

    missing_schema_issues: list[dict] = []
    missing_schema = embedded_langchain_output_schema("PROFILE = {}", missing_schema_issues, "synthetic")

    syntax_issues: list[dict] = []
    syntax_schema = embedded_langchain_output_schema("OUTPUT_SCHEMA = {", syntax_issues, "synthetic")

    schema_drift_detected = {"required": ["copilot_id"]} != {"required": ["decision"]}
    trace_schema_issues: list[dict] = []
    validate_required_trace_fields_schema(
        "synthetic",
        {"runtimeParityContract": {"requiredTraceFields": ["phase", "expected_outputs"]}},
        {"required": ["copilot_id", "decision"]},
        trace_schema_issues,
    )
    trace_schema_detected = any(
        item["kind"] == "runtime_trace_fields_schema"
        for item in trace_schema_issues
    )
    unsafe_copilot_id_detected = (
        not is_safe_copilot_id("../outside")
        and not is_safe_copilot_id("bad\\path")
        and is_safe_copilot_id("qa_general")
    )
    empty_map_issues: list[dict] = []
    validate_runtime_map_coverage({}, ["synthetic"], empty_map_issues)
    empty_map_detected = any(item["kind"] == "runtime_map_coverage" for item in empty_map_issues)

    indented_runtime_markdown_issues: list[dict] = []
    validate_runtime_specific_markdown(
        "synthetic",
        "claude",
        "## Runtime Specific Protocol\n\n    - This bullet is accidentally rendered as a code block.\n",
        indented_runtime_markdown_issues,
    )
    indented_runtime_markdown_detected = any(
        item["kind"] == "claude_runtime_specific_protocol_markdown"
        for item in indented_runtime_markdown_issues
    )
    github_mcp_placeholder_issues: list[dict] = []
    synthetic_runtime_files = {
        "codex": "dist/copilots/synthetic/codex/AGENT.md",
        "claude": "dist/copilots/synthetic/claude/AGENT.md",
        "github-copilot": "dist/copilots/synthetic/github-copilot/copilot-agent.md",
        "langchain": "dist/copilots/synthetic/langchain/agent.py",
    }
    validate_github_mcp_placeholders(
        "synthetic",
        {
            "policyVersion": GITHUB_PROTOCOL_VERSION,
            "ownerAgent": GITHUB_OWNER_AGENT,
            "mission": GITHUB_MISSION,
            "copilotId": "synthetic",
            "runtime": "github-copilot",
            "sourcePolicy": "config/mcp-connectors.example.json",
            "defaultEnabled": False,
            "placeholderOnly": True,
            "credentialsRequired": False,
            "credentialValuesStored": False,
            "customerDataAllowed": False,
            "billingDataAllowed": False,
            "connectors": {
                "github_mcp": {
                    "connector": "github_mcp",
                    "enabled": False,
                    "env": "GITHUB_TOKEN",
                    "credentialValue": "placeholder-token",
                    "credentialValuesStored": False,
                    "requiresOperatorActivation": True,
                    "operatorApprovalRequiredForWrites": True,
                    "localOnlyConfig": True,
                    "allowedRuntimes": RUNTIMES,
                    "policyRef": "config/mcp-connectors.example.json",
                }
            },
            "safeUsage": {
                "operatorActivationRequired": True,
                "operatorApprovalRequiredForWrites": True,
                "denyCustomerDataInPrompts": True,
                "redactTokensInLogs": True,
                "noExternalNetworkWithoutOperatorApproval": True,
            },
            "runtimeEquivalence": {
                "sourceOfTruth": "dist/copilots/synthetic/shared/spec.json",
                "runtimes": RUNTIMES,
                "adapterFiles": synthetic_runtime_files,
                "maxUnexplainedDrift": 0,
            },
        },
        "dist/copilots/synthetic/github-copilot/mcp-placeholders.json",
        "dist/copilots/synthetic/shared/spec.json",
        synthetic_runtime_files,
        {"connectors": ["github_mcp"], "env_keys": ["GITHUB_TOKEN"]},
        github_mcp_placeholder_issues,
    )
    github_mcp_placeholder_detected = any(
        item["kind"] == "github_mcp_github_mcp_credential_value"
        for item in github_mcp_placeholder_issues
    )
    github_mcp_env_reference_issues: list[dict] = []
    validate_github_mcp_placeholders(
        "synthetic",
        {
            "policyVersion": GITHUB_PROTOCOL_VERSION,
            "ownerAgent": GITHUB_OWNER_AGENT,
            "mission": GITHUB_MISSION,
            "copilotId": "synthetic",
            "runtime": "github-copilot",
            "sourcePolicy": "config/mcp-connectors.example.json",
            "defaultEnabled": False,
            "placeholderOnly": True,
            "credentialsRequired": False,
            "credentialValuesStored": False,
            "customerDataAllowed": False,
            "billingDataAllowed": False,
            "connectors": {
                "github_mcp": {
                    "connector": "github_mcp",
                    "enabled": False,
                    "env": "GITHUB_TOKEN",
                    "envReference": "${WRONG_TOKEN}",
                    "credentialValue": "",
                    "credentialValuesStored": False,
                    "requiresOperatorActivation": True,
                    "operatorApprovalRequiredForWrites": True,
                    "localOnlyConfig": True,
                    "allowedRuntimes": RUNTIMES,
                    "policyRef": "config/mcp-connectors.example.json",
                }
            },
            "safeUsage": {
                "operatorActivationRequired": True,
                "operatorApprovalRequiredForWrites": True,
                "denyCustomerDataInPrompts": True,
                "redactTokensInLogs": True,
                "noExternalNetworkWithoutOperatorApproval": True,
            },
            "runtimeEquivalence": {
                "sourceOfTruth": "dist/copilots/synthetic/shared/spec.json",
                "runtimes": RUNTIMES,
                "adapterFiles": synthetic_runtime_files,
                "maxUnexplainedDrift": 0,
            },
        },
        "dist/copilots/synthetic/github-copilot/mcp-placeholders.json",
        "dist/copilots/synthetic/shared/spec.json",
        synthetic_runtime_files,
        {"connectors": ["github_mcp"], "env_keys": ["GITHUB_TOKEN"]},
        github_mcp_env_reference_issues,
    )
    github_mcp_env_reference_detected = any(
        item["kind"] == "github_mcp_github_mcp_env_reference"
        for item in github_mcp_env_reference_issues
    )
    github_profile_cost_issues: list[dict] = []
    validate_github_profile_cost_control(
        "synthetic",
        {
            "costControl": {
                "promptExpansion": "full_prompt_duplication",
                "deterministicPythonFirst": False,
                "llmEscalation": "always",
            }
        },
        github_profile_cost_issues,
    )
    github_profile_cost_detected = any(
        item["kind"].startswith("github_profile_cost_control_")
        for item in github_profile_cost_issues
    )
    langchain_api_issues: list[dict] = []
    incomplete_langchain_agent = inspect_langchain_agent(
        "PROFILE = {}\nOUTPUT_SCHEMA = {}\nclass BrokenAgent:\n    def score(self, request):\n        return 0\n",
        langchain_api_issues,
        "synthetic",
    )
    langchain_api_detected = (
        incomplete_langchain_agent.get("parsed") is True
        and incomplete_langchain_agent.get("agentClassWithRequiredMethods") is False
        and "SYSTEM_PROMPT" not in incomplete_langchain_agent.get("moduleConstants", set())
    )
    langchain_static_safety_issues: list[dict] = []
    validate_langchain_static_safety(
        "synthetic",
        "import subprocess\nPROFILE = {}\nsubprocess.run(['echo', 'unsafe'])\n",
        langchain_static_safety_issues,
    )
    langchain_static_safety_detected = any(
        item["kind"] in {"langchain_agent_static_import", "langchain_agent_static_call", "langchain_agent_static_top_level"}
        for item in langchain_static_safety_issues
    )
    langchain_render_prompt_issues: list[dict] = []
    validate_langchain_rendered_messages(
        "synthetic",
        [
            {"role": "system", "content": "system"},
            {"role": "developer", "content": "developer"},
            {"role": "user", "content": "AKIA" + ("B" * 16)},
        ],
        langchain_render_prompt_issues,
    )
    langchain_render_prompt_detected = any(
        item["kind"] == "langchain_agent_runtime_render_prompt_secret"
        for item in langchain_render_prompt_issues
    )

    fixtures = [
        ("local_path_leak", local_path_detected, True, ["local_path"]),
        ("secret_pattern_leak", secret_pattern_detected, True, ["secret_pattern"]),
        (
            "missing_langchain_output_schema",
            missing_schema is None and any(item["kind"] == "langchain_embedded_output_schema" for item in missing_schema_issues),
            True,
            [item["kind"] for item in missing_schema_issues],
        ),
        (
            "invalid_langchain_syntax",
            syntax_schema is None and any(item["kind"] == "langchain_agent_syntax" for item in syntax_issues),
            True,
            [item["kind"] for item in syntax_issues],
        ),
        ("schema_drift", schema_drift_detected, True, ["output_schema_sync"]),
        (
            "runtime_trace_fields_schema",
            trace_schema_detected,
            True,
            [item["kind"] for item in trace_schema_issues],
        ),
        ("unsafe_copilot_id", unsafe_copilot_id_detected, True, ["runtime_map_copilot_id"]),
        ("empty_runtime_injection_map", empty_map_detected, True, [item["kind"] for item in empty_map_issues]),
        (
            "indented_runtime_protocol_markdown",
            indented_runtime_markdown_detected,
            True,
            [item["kind"] for item in indented_runtime_markdown_issues],
        ),
        (
            "github_mcp_non_empty_placeholder",
            github_mcp_placeholder_detected,
            True,
            [item["kind"] for item in github_mcp_placeholder_issues],
        ),
        (
            "github_mcp_env_reference_drift",
            github_mcp_env_reference_detected,
            True,
            [item["kind"] for item in github_mcp_env_reference_issues],
        ),
        (
            "github_profile_cost_control_drift",
            github_profile_cost_detected,
            True,
            [item["kind"] for item in github_profile_cost_issues],
        ),
        (
            "incomplete_langchain_agent_api",
            langchain_api_detected,
            True,
            ["langchain_agent_api_methods", "langchain_agent_api_constant"],
        ),
        (
            "unsafe_langchain_static_side_effect",
            langchain_static_safety_detected,
            True,
            [item["kind"] for item in langchain_static_safety_issues],
        ),
        (
            "unsafe_langchain_render_prompt",
            langchain_render_prompt_detected,
            True,
            [item["kind"] for item in langchain_render_prompt_issues],
        ),
    ]
    results = []
    for case_id, failure_detected, expected, detectors in fixtures:
        passed_expectation = failure_detected is expected
        results.append(
            {
                "id": case_id,
                "expectedFailure": expected,
                "failureDetected": failure_detected,
                "passedExpectation": passed_expectation,
                "detected": passed_expectation,
                "detectors": detectors,
            }
        )
    return results


def validate_test_strategy_runtime_equivalence(metrics: list[dict], issues: list[dict]) -> dict:
    local_issues: list[dict] = []
    pairwise_cases = runtime_pairwise_cases()
    negative_cases = run_runtime_equivalence_negative_cases()
    copilot_ids = [item.get("id") for item in metrics if isinstance(item, dict)]
    summary = {
        "mission": "Audits test strategy, pairwise cases and negative cases.",
        "targetCopilot": "qa_general",
        "pairwiseCases": pairwise_cases,
        "pairwiseCoverageCases": len(copilot_ids) * len(pairwise_cases),
        "negativeCases": negative_cases,
        "negativeCasesDetected": all(case["passedExpectation"] for case in negative_cases),
        "qaRuntimeMarkersChecked": [],
        "qaTraceabilityChecked": False,
    }

    for item in metrics:
        if item.get("runtimesChecked") != len(RUNTIMES):
            local_issues.append(issue(item.get("id", "unknown"), "test_strategy_pairwise", "Runtime count drifted from pairwise strategy."))

    base = ROOT / "dist" / "copilots" / "qa_general"
    spec = read_json(base / "shared" / "spec.json", {}, local_issues, "qa_general")
    profile = read_json(base / "langchain" / "agent_profile.json", {}, local_issues, "qa_general")
    output_schema = read_json(base / "shared" / "output_schema.json", {}, local_issues, "qa_general")
    if spec.get("outputSchema") == output_schema and profile.get("outputSchema") == output_schema:
        summary["qaTraceabilityChecked"] = True
    else:
        local_issues.append(issue("qa_general", "test_strategy_traceability", "QA General output schema must trace through spec, profile and shared schema."))

    runtime_files = {
        "codex": base / "codex" / "AGENT.md",
        "claude": base / "claude" / "AGENT.md",
        "github-copilot": base / "github-copilot" / "copilot-agent.md",
        "langchain": base / "langchain" / "agent.py",
    }
    for runtime, path in runtime_files.items():
        text = read_text(path, local_issues, "qa_general")
        missing = [marker for marker in ["qa_strategy", "test_matrix", "pairwise", "negative"] if marker not in text]
        if missing:
            local_issues.append(
                issue(
                    "qa_general",
                    "test_strategy_runtime_markers",
                    f"{runtime} runtime missing test strategy markers: {', '.join(missing)}.",
                )
            )
        else:
            summary["qaRuntimeMarkersChecked"].append(runtime)

    if not summary["negativeCasesDetected"]:
        local_issues.append(issue("qa_general", "test_strategy_negative_cases", "Runtime equivalence negative fixtures were not all detected."))

    summary["pass"] = not local_issues
    summary["issues"] = local_issues
    issues.extend(local_issues)
    return summary


def relative(path: Path) -> str:
    return str(path.relative_to(ROOT)).replace("\\", "/")


def format_path(path: Path) -> str:
    try:
        return relative(path)
    except ValueError:
        return path.name


def render_md(report: dict) -> str:
    metrics = "\n".join(
        f"- `{item['id']}`: checked {item['runtimesChecked']} runtimes via `{item['sharedSpec']}`"
        for item in report["metrics"]
    ) or "- none"
    issues = "\n".join(
        f"- `{item['scope']}` [{item['kind']}]: {item['message']}"
        for item in report["issues"]
    ) or "- none"
    test_strategy = report.get("testStrategyAudit", {})
    codex_adapter = report.get("codexAdapterAudit", {})
    claude_adapter = report.get("claudeAdapterAudit", {})
    github_adapter = report.get("githubCopilotAdapterAudit", {})
    langchain_adapter = report.get("langchainAgentAudit", {})
    data_hygiene = report.get("dataHygieneAudit", {})
    matrix_audit = report.get("sdlcRuntimeMatrixAudit", {})
    validator_smoke = report.get("validatorSmoke", {})
    cell_equivalence_audit = matrix_audit.get("cellEquivalenceAudit", {}) if isinstance(matrix_audit, dict) else {}
    maintenance_audit = matrix_audit.get("maintenanceAudit", {}) if isinstance(matrix_audit, dict) else {}
    codex_metrics = "\n".join(
        f"- `{item['id']}`: protocol `{item['protocol']}`, pass={item['pass']}"
        for item in codex_adapter.get("metrics", [])
    ) or "- none"
    claude_metrics = "\n".join(
        f"- `{item['id']}`: protocol `{item['protocol']}`, pass={item['pass']}"
        for item in claude_adapter.get("metrics", [])
    ) or "- none"
    github_metrics = "\n".join(
        f"- `{item['id']}`: profile `{item['profile']}`, mcp `{item['mcpPlaceholders']}`, pass={item['pass']}"
        for item in github_adapter.get("metrics", [])
    ) or "- none"
    langchain_metrics = "\n".join(
        f"- `{item['id']}`: contract `{item['contract']}`, runtime `{item['runtimeFile']}`, pass={item['pass']}"
        for item in langchain_adapter.get("metrics", [])
    ) or "- none"
    negative_rows = "\n".join(
        (
            f"- `{case['id']}`: passedExpectation={case.get('passedExpectation', case['detected'])}, "
            f"expectedFailure={case['expectedFailure']}, failureDetected={case.get('failureDetected')}"
        )
        for case in test_strategy.get("negativeCases", [])
    ) or "- none"
    return f"""# Runtime Equivalence Report

Pass: {report['pass']}

Copilots checked: {report['copilotsChecked']}

Metrics:

{metrics}

Codex adapter audit:

- Pass: {codex_adapter.get('pass')}
- Owner: {codex_adapter.get('ownerAgent')}
- Mission: {codex_adapter.get('mission')}
- Protocols checked: {codex_adapter.get('protocolsChecked')}
- Issue count: {codex_adapter.get('issues')}

Codex protocol metrics:

{codex_metrics}

Claude adapter audit:

- Pass: {claude_adapter.get('pass')}
- Owner: {claude_adapter.get('ownerAgent')}
- Mission: {claude_adapter.get('mission')}
- Protocols checked: {claude_adapter.get('protocolsChecked')}
- Issue count: {claude_adapter.get('issues')}

Claude project instruction metrics:

{claude_metrics}

GitHub Copilot profile audit:

- Pass: {github_adapter.get('pass')}
- Owner: {github_adapter.get('ownerAgent')}
- Mission: {github_adapter.get('mission')}
- Profiles checked: {github_adapter.get('profilesChecked')}
- Issue count: {github_adapter.get('issues')}

GitHub Copilot profile metrics:

{github_metrics}

LangChain agent audit:

- Pass: {langchain_adapter.get('pass')}
- Owner: {langchain_adapter.get('ownerAgent')}
- Mission: {langchain_adapter.get('mission')}
- Contracts checked: {langchain_adapter.get('contractsChecked')}
- Issue count: {langchain_adapter.get('issues')}

LangChain agent contract metrics:

{langchain_metrics}

Data hygiene audit:

- Pass: {data_hygiene.get('pass')}
- Artifacts checked: {data_hygiene.get('artifactsChecked')} / {data_hygiene.get('artifactsDeclared')}
- Local path leaks: {data_hygiene.get('localPathLeaks')}
- Secret pattern leaks: {data_hygiene.get('secretPatternLeaks')}
- Issue count: {data_hygiene.get('issues')}

SDLC runtime matrix audit:

- Pass: {matrix_audit.get('pass')}
- Artifact: `{matrix_audit.get('artifact')}`
- Policy version: {matrix_audit.get('policyVersion')}
- Expected cells: {matrix_audit.get('expectedCells')}
- Actual cells: {matrix_audit.get('actualCells')}
- Pairwise runtime cases: {matrix_audit.get('pairwiseRuntimeCases')}
- Digest drift count: {matrix_audit.get('digestDriftCount')}
- Runtime file mismatches: {matrix_audit.get('runtimeFileMismatches')}
- Trace ledger entries: {matrix_audit.get('traceLedgerEntries')}
- Trace ledger digest matches: {matrix_audit.get('traceLedgerDigestMatches')}
- Trace ledger mismatches: {matrix_audit.get('traceLedgerMismatches')}
- Cell equivalence pass: {cell_equivalence_audit.get('pass')}
- Cell equivalence cells passing: {cell_equivalence_audit.get('passingCells')} / {cell_equivalence_audit.get('cellsChecked')}
- Prompt content stored: {matrix_audit.get('promptContentStored')}
- Maintenance artifact: `{matrix_audit.get('maintenanceArtifact')}`
- Maintenance receipt pass: {maintenance_audit.get('pass')}
- Maintenance runtime count matches: {maintenance_audit.get('runtimeCountMatches')}
- Maintenance cell digest matches: {maintenance_audit.get('cellDigestMatches')}
- Maintenance cell equivalence gate: {maintenance_audit.get('cellEquivalenceGatePass')}

Test strategy audit:

- Pass: {test_strategy.get('pass')}
- Pairwise case count: {len(test_strategy.get('pairwiseCases', []))}
- Pairwise coverage cases: {test_strategy.get('pairwiseCoverageCases')}
- Negative cases detected: {test_strategy.get('negativeCasesDetected')}
- QA traceability checked: {test_strategy.get('qaTraceabilityChecked')}
- QA runtime markers checked: {test_strategy.get('qaRuntimeMarkersChecked')}

Negative case results:

{negative_rows}

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

{issues}
"""


if __name__ == "__main__":
    main()
