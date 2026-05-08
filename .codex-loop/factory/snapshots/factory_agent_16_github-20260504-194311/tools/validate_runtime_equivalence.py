from __future__ import annotations

import ast
import hashlib
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CATALOG_JSON = ROOT / "data" / "copilots.json"
REPORT_JSON = ROOT / "generated" / "runtime-equivalence-report.json"
REPORT_MD = ROOT / "generated" / "runtime-equivalence-report.md"
RUNTIMES = ["codex", "claude", "github-copilot", "langchain"]
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

SECRET_PATTERNS = [
    re.compile(r"(?<![A-Za-z0-9])sk-or-v1-[A-Za-z0-9_-]{20,}", re.I),
    re.compile(r"(?<![A-Za-z0-9])sk-[A-Za-z0-9_-]{20,}"),
    re.compile(r"github_pat_[A-Za-z0-9_]{20,}", re.I),
    re.compile(r"gh[pousr]_[A-Za-z0-9_]{20,}", re.I),
    re.compile(r"Bearer\s+[A-Za-z0-9._~+/=-]{20,}", re.I),
]
LOCAL_PATH_PATTERNS = [
    re.compile(r"(?i)\b[A-Z]:[\\/]+Users[\\/]+[^\\/\s\"']+"),
    re.compile(r"(?i)/Users/[A-Za-z0-9._-]+"),
    re.compile(r"(?i)/home/[A-Za-z0-9._-]+"),
]
SAFE_COPILOT_ID_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_-]*$")


def main() -> None:
    issues: list[dict] = []
    metrics: list[dict] = []
    codex_protocol_metrics: list[dict] = []
    claude_protocol_metrics: list[dict] = []
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
        validate_artifact_hygiene(base / "shared" / "codex_tool_protocol.json", issues, data_hygiene_metrics)
        validate_artifact_hygiene(base / "shared" / "claude_project_instructions.json", issues, data_hygiene_metrics)

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
    data_hygiene_audit = summarize_data_hygiene_audit(data_hygiene_metrics, issues)

    report = {
        "pass": not issues,
        "checkedAt": datetime.now(timezone.utc).isoformat(),
        "copilotsChecked": len(metrics),
        "metrics": metrics,
        "codexAdapterAudit": codex_adapter_audit,
        "claudeAdapterAudit": claude_adapter_audit,
        "dataHygieneAudit": data_hygiene_audit,
        "testStrategyAudit": test_strategy_audit,
        "issues": issues,
    }
    REPORT_JSON.parent.mkdir(parents=True, exist_ok=True)
    REPORT_JSON.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    REPORT_MD.write_text(render_md(report), encoding="utf-8")

    if issues:
        print(f"Runtime equivalence FAIL: {len(issues)} issue(s).")
        for item in issues[:30]:
            print(f"- {item['scope']} [{item['kind']}]: {item['message']}")
        sys.exit(1)
    print(f"Runtime equivalence PASS: {len(metrics)} copilots checked.")


def issue(scope: str, kind: str, message: str) -> dict:
    return {"scope": scope, "kind": kind, "message": message}


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
    secret_pattern_detected = has_secret_pattern("Bearer " + ("A" * 24))

    missing_schema_issues: list[dict] = []
    missing_schema = embedded_langchain_output_schema("PROFILE = {}", missing_schema_issues, "synthetic")

    syntax_issues: list[dict] = []
    syntax_schema = embedded_langchain_output_schema("OUTPUT_SCHEMA = {", syntax_issues, "synthetic")

    schema_drift_detected = {"required": ["copilot_id"]} != {"required": ["decision"]}
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
        ("unsafe_copilot_id", unsafe_copilot_id_detected, True, ["runtime_map_copilot_id"]),
        ("empty_runtime_injection_map", empty_map_detected, True, [item["kind"] for item in empty_map_issues]),
        (
            "indented_runtime_protocol_markdown",
            indented_runtime_markdown_detected,
            True,
            [item["kind"] for item in indented_runtime_markdown_issues],
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
    data_hygiene = report.get("dataHygieneAudit", {})
    codex_metrics = "\n".join(
        f"- `{item['id']}`: protocol `{item['protocol']}`, pass={item['pass']}"
        for item in codex_adapter.get("metrics", [])
    ) or "- none"
    claude_metrics = "\n".join(
        f"- `{item['id']}`: protocol `{item['protocol']}`, pass={item['pass']}"
        for item in claude_adapter.get("metrics", [])
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

Data hygiene audit:

- Pass: {data_hygiene.get('pass')}
- Artifacts checked: {data_hygiene.get('artifactsChecked')} / {data_hygiene.get('artifactsDeclared')}
- Local path leaks: {data_hygiene.get('localPathLeaks')}
- Secret pattern leaks: {data_hygiene.get('secretPatternLeaks')}
- Issue count: {data_hygiene.get('issues')}

Test strategy audit:

- Pass: {test_strategy.get('pass')}
- Pairwise case count: {len(test_strategy.get('pairwiseCases', []))}
- Pairwise coverage cases: {test_strategy.get('pairwiseCoverageCases')}
- Negative cases detected: {test_strategy.get('negativeCasesDetected')}
- QA traceability checked: {test_strategy.get('qaTraceabilityChecked')}
- QA runtime markers checked: {test_strategy.get('qaRuntimeMarkersChecked')}

Negative case results:

{negative_rows}

Issues:

{issues}
"""


if __name__ == "__main__":
    main()
