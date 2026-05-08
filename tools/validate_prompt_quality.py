from __future__ import annotations

import hashlib
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPORT_JSON = ROOT / "generated" / "prompt-quality-report.json"
REPORT_MD = ROOT / "generated" / "prompt-quality-report.md"
VALIDATOR_SMOKE_REPORT_JSON = ROOT / "generated" / "validator-smoke-report.json"
VALIDATOR_SMOKE_REPORT_MD = ROOT / "generated" / "validator-smoke-report.md"
BASELINE_JSON = ROOT / "generated" / "prompt-size-baseline.json"
SDLC_RUNTIME_MATRIX_JSON = ROOT / "generated" / "sdlc-runtime-matrix.json"
SDLC_RUNTIME_MATRIX_MD = ROOT / "generated" / "sdlc-runtime-matrix.md"
SDLC_RUNTIME_MATRIX_MAINTENANCE_JSON = ROOT / "generated" / "sdlc-runtime-matrix-maintenance.json"
SDLC_RUNTIME_MATRIX_MAINTENANCE_MD = ROOT / "generated" / "sdlc-runtime-matrix-maintenance.md"

EXPECTED_COPILOTS = 18
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
MATRIX_FORBIDDEN_PROMPT_KEYS = {
    "adapterPrompt",
    "developerPrompt",
    "promptText",
    "rawPrompt",
    "runtimePrompt",
    "systemPrompt",
}
SAFE_COPILOT_ID_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_-]*$")
MIN_MARKDOWN_CHARS = 6500
MIN_LANGCHAIN_CHARS = 4500
MIN_SYSTEM_PROMPT_CHARS = 1300
MIN_DEVELOPER_PROMPT_CHARS = 1500
MAX_COST_GROWTH_RATIO = 0.10

BASELINE_KEYS = {
    "codex": "codexChars",
    "claude": "claudeChars",
    "github-copilot": "githubChars",
    "langchain": "langchainChars",
    "systemPrompt": "systemPromptChars",
    "developerPrompt": "developerPromptChars",
}

REQUIRED_MARKDOWN_SECTIONS = [
    "Runtime Injection",
    "System Prompt",
    "Developer Prompt",
    "Execution Protocol",
    "Python Brain Contract",
    "SDLC Playbook",
    "Evidence Gates",
    "Outputs",
    "Quality Rubric",
    "Escalation",
]

REQUIRED_SPEC_KEYS = [
    "systemPrompt",
    "developerPrompt",
    "runtimeInjection",
    "sdlcPlaybook",
    "outputSchema",
    "qualityRubric",
    "pythonBrain",
    "committee",
]

REQUIRED_LANGCHAIN_SNIPPETS = [
    "class ",
    "def score(",
    "def audit(",
    "def plan(",
    "def render_prompt(",
    "def output_schema(",
    "SYSTEM_PROMPT",
    "DEVELOPER_PROMPT",
    "OUTPUT_SCHEMA",
]

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
    issues: list[dict] = []
    metrics: list[dict] = []
    cost_metrics: list[dict] = []
    copilots = read_json(ROOT / "data" / "copilots.json", [], issues, "catalog")
    prompt_baseline = read_prompt_baseline(issues)

    if len(copilots) != EXPECTED_COPILOTS:
        issues.append(issue("catalog", "copilot_count", f"Expected {EXPECTED_COPILOTS}, found {len(copilots)}."))

    for index, copilot in enumerate(copilots):
        if not isinstance(copilot, dict):
            issues.append(issue("catalog", "catalog_entry", f"data/copilots.json item {index} must be an object."))
            continue
        cid = copilot.get("id", "")
        if not is_safe_copilot_id(cid):
            issues.append(issue("catalog", "catalog_entry_id", f"data/copilots.json item {index} id must be a safe repository path segment."))
            continue
        base = ROOT / "dist" / "copilots" / cid
        spec = read_json(base / "shared" / "spec.json", {}, issues, cid)
        for key in REQUIRED_SPEC_KEYS:
            if key not in spec:
                issues.append(issue(cid, "spec_key", f"Missing shared spec key: {key}."))

        system_prompt = spec.get("systemPrompt", "")
        developer_prompt = spec.get("developerPrompt", "")
        if len(system_prompt) < MIN_SYSTEM_PROMPT_CHARS:
            issues.append(issue(cid, "system_prompt_depth", f"System prompt too short: {len(system_prompt)} chars."))
        if len(developer_prompt) < MIN_DEVELOPER_PROMPT_CHARS:
            issues.append(issue(cid, "developer_prompt_depth", f"Developer prompt too short: {len(developer_prompt)} chars."))
        record_cost_metric(cost_metrics, prompt_baseline, cid, "systemPrompt", len(system_prompt), issues)
        record_cost_metric(cost_metrics, prompt_baseline, cid, "developerPrompt", len(developer_prompt), issues)
        if len(spec.get("sdlcPlaybook", [])) < max(1, len(copilot.get("sdlc_phases", []))):
            issues.append(issue(cid, "sdlc_playbook", "SDLC playbook does not cover all declared phases."))
        if len(spec.get("qualityRubric", [])) < 5:
            issues.append(issue(cid, "quality_rubric", "Quality rubric needs at least 5 criteria."))

        for runtime, path in {
            "codex": base / "codex" / "AGENT.md",
            "claude": base / "claude" / "AGENT.md",
            "github-copilot": base / "github-copilot" / "copilot-agent.md",
        }.items():
            text = read_text(path)
            if len(text) < MIN_MARKDOWN_CHARS:
                issues.append(issue(cid, "runtime_prompt_depth", f"{runtime} prompt too short: {len(text)} chars."))
            for section in REQUIRED_MARKDOWN_SECTIONS:
                if f"## {section}" not in text:
                    issues.append(issue(cid, "runtime_section", f"{runtime} missing section: {section}."))
            metrics.append({"id": cid, "runtime": runtime, "chars": len(text)})
            record_cost_metric(cost_metrics, prompt_baseline, cid, runtime, len(text), issues)

        langchain = read_text(base / "langchain" / "agent.py")
        langchain_path = base / "langchain" / "agent.py"
        if len(langchain) < MIN_LANGCHAIN_CHARS:
            issues.append(issue(cid, "langchain_depth", f"LangChain/Python adapter too short: {len(langchain)} chars."))
        for snippet in REQUIRED_LANGCHAIN_SNIPPETS:
            if snippet not in langchain:
                issues.append(issue(cid, "langchain_snippet", f"LangChain adapter missing `{snippet}`."))
        try:
            compile(langchain, str(langchain_path), "exec")
        except SyntaxError as exc:
            issues.append(issue(cid, "langchain_compile", f"LangChain adapter does not compile: {exc.msg}"))
        metrics.append({"id": cid, "runtime": "langchain", "chars": len(langchain)})
        record_cost_metric(cost_metrics, prompt_baseline, cid, "langchain", len(langchain), issues)

        schema = read_json(base / "shared" / "output_schema.json", {}, issues, cid)
        required = set(schema.get("required", []))
        for key in ["copilot_id", "decision", "evidence", "actions", "validation", "risks"]:
            if key not in required:
                issues.append(issue(cid, "output_schema", f"Output schema missing required key: {key}."))

    for file in ROOT.rglob("*"):
        if not should_scan_text_file(file):
            continue
        text = read_text(file, allow_missing=True)
        scan_text_safety(file, text, issues)

    test_strategy_audit = validate_test_strategy_prompt_quality(metrics, cost_metrics, issues)
    sdlc_runtime_matrix_audit = validate_sdlc_runtime_matrix_prompt_quality(copilots, metrics, issues)
    validator_smoke = build_current_validator_smoke(
        "prompt_quality",
        "python tools/validate_prompt_quality.py",
        REPORT_JSON,
        issues,
    )

    report = {
        "pass": not issues,
        "checkedAt": datetime.now(timezone.utc).isoformat(),
        "copilots": len(copilots),
        "minimumDepthThresholds": {
            "markdownChars": MIN_MARKDOWN_CHARS,
            "langchainChars": MIN_LANGCHAIN_CHARS,
            "systemPromptChars": MIN_SYSTEM_PROMPT_CHARS,
            "developerPromptChars": MIN_DEVELOPER_PROMPT_CHARS,
        },
        "thresholds": {
            "markdownChars": MIN_MARKDOWN_CHARS,
            "langchainChars": MIN_LANGCHAIN_CHARS,
            "systemPromptChars": MIN_SYSTEM_PROMPT_CHARS,
            "developerPromptChars": MIN_DEVELOPER_PROMPT_CHARS,
        },
        "costBudget": {
            "baseline": "generated/prompt-size-baseline.json",
            "maxGrowthRatio": MAX_COST_GROWTH_RATIO,
            "metrics": cost_metrics,
        },
        "metrics": metrics,
        "testStrategyAudit": test_strategy_audit,
        "sdlcRuntimeMatrixAudit": sdlc_runtime_matrix_audit,
        "validatorSmoke": validator_smoke,
        "issues": issues,
    }
    REPORT_JSON.parent.mkdir(parents=True, exist_ok=True)
    REPORT_JSON.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    REPORT_MD.write_text(render_md(report), encoding="utf-8")
    write_validator_smoke_artifacts(
        "prompt_quality",
        "python tools/validate_prompt_quality.py",
        REPORT_JSON,
        report,
        issues,
    )

    if issues:
        print(f"Prompt quality validation FAIL: {len(issues)} issue(s).")
        for item in issues[:30]:
            print(f"- {item['scope']} [{item['kind']}]: {item['message']}")
        sys.exit(1)
    print(f"Prompt quality validation PASS: {len(copilots)} copilots, {len(metrics)} runtime prompts.")


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


def read_prompt_baseline(issues: list[dict]) -> dict[str, dict]:
    raw = read_json(BASELINE_JSON, {}, issues, "prompt_cost_baseline")
    stats = raw.get("stats", []) if isinstance(raw, dict) else []
    if not isinstance(stats, list):
        issues.append(issue("prompt_cost_baseline", "json_input", "Prompt size baseline stats must be an array."))
        return {}
    baseline: dict[str, dict] = {}
    for item in stats:
        if not isinstance(item, dict):
            issues.append(issue("prompt_cost_baseline", "json_input", "Prompt size baseline entries must be objects."))
            continue
        cid = item.get("id")
        if not isinstance(cid, str) or not cid:
            issues.append(issue("prompt_cost_baseline", "json_input", "Prompt size baseline entry is missing id."))
            continue
        baseline[cid] = item
    return baseline


def record_cost_metric(
    metrics: list[dict],
    baseline: dict[str, dict],
    cid: str,
    surface: str,
    chars: int,
    issues: list[dict],
) -> None:
    baseline_key = BASELINE_KEYS[surface]
    baseline_entry = baseline.get(cid)
    baseline_chars = baseline_entry.get(baseline_key) if isinstance(baseline_entry, dict) else None
    metric = {
        "id": cid,
        "surface": surface,
        "chars": chars,
        "baselineChars": baseline_chars,
        "deltaChars": None,
        "growthRatio": None,
        "maxAllowedGrowthRatio": MAX_COST_GROWTH_RATIO,
        "status": "unchecked",
    }
    if not isinstance(baseline_chars, int) or baseline_chars <= 0:
        metric["status"] = "missing_baseline"
        metrics.append(metric)
        issues.append(issue(cid, "cost_budget", f"Missing prompt-size baseline for {surface}."))
        return

    delta = chars - baseline_chars
    growth_ratio = delta / baseline_chars
    metric.update(
        {
            "deltaChars": delta,
            "growthRatio": round(growth_ratio, 4),
            "status": "pass" if growth_ratio <= MAX_COST_GROWTH_RATIO else "fail",
        }
    )
    metrics.append(metric)
    if growth_ratio > MAX_COST_GROWTH_RATIO:
        limit = int(MAX_COST_GROWTH_RATIO * 100)
        issues.append(
            issue(
                cid,
                "cost_budget",
                f"{surface} grew {delta} chars over baseline ({growth_ratio:.1%}); max allowed growth is {limit}%.",
            )
        )


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


def read_text(path: Path, allow_missing: bool = False) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except Exception:
        if allow_missing:
            return ""
        return ""


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


def scan_text_safety(file: Path, text: str, issues: list[dict]) -> None:
    rel = relative(file)
    for pattern in SECRET_PATTERNS:
        if pattern.search(text):
            issues.append(issue(rel, "secret_pattern", "Potential secret pattern found."))
            break
    for pattern in LOCAL_PATH_PATTERNS:
        if pattern.search(text):
            if rel in LOCAL_FACTORY_RUNTIME_REPORTS:
                continue
            issues.append(issue(rel, "local_path", "Local absolute path leaked in release artifact."))
            break


def is_safe_copilot_id(value: object) -> bool:
    return isinstance(value, str) and bool(SAFE_COPILOT_ID_RE.fullmatch(value))


def validate_sdlc_runtime_matrix_prompt_quality(copilots: list, metrics: list[dict], issues: list[dict]) -> dict:
    local_issues: list[dict] = []
    matrix = read_json(SDLC_RUNTIME_MATRIX_JSON, {}, local_issues, "sdlc_runtime_matrix")
    maintenance = read_json(SDLC_RUNTIME_MATRIX_MAINTENANCE_JSON, {}, local_issues, "sdlc_runtime_matrix_maintenance")
    cells = matrix.get("cells", []) if isinstance(matrix.get("cells"), list) else []
    expected_cells = expected_sdlc_runtime_cells(copilots)
    actual_cells = {
        (cell.get("copilotId"), cell.get("phase"), cell.get("runtime"))
        for cell in cells
        if isinstance(cell, dict)
    }
    runtime_metric_pairs = {
        (item.get("id"), item.get("runtime"))
        for item in metrics
        if item.get("runtime") in RUNTIMES
    }
    matrix_runtime_pairs = {
        (cell.get("copilotId"), cell.get("runtime"))
        for cell in cells
        if isinstance(cell, dict)
    }
    trace_ledger_audit = validate_matrix_trace_ledger_prompt_budget(matrix, expected_cells, local_issues)
    cell_equivalence_audit = validate_matrix_cell_equivalence_contract(matrix, expected_cells, local_issues)
    prompt_budget_detections = matrix_prompt_budget_detections(matrix)
    negative_matrix = {
        "costControl": {"promptContentStored": True},
        "traceLedger": [{"copilotId": "synthetic", "phase": "test", "runtimePrompt": "do not store prompt bodies"}],
        "cells": [{"copilotId": "synthetic", "runtime": "codex", "rawPrompt": "do not store prompt bodies"}],
    }
    negative_detections = matrix_prompt_budget_detections(negative_matrix)
    maintenance_audit = validate_sdlc_runtime_matrix_maintenance_prompt_budget(
        maintenance,
        matrix,
        expected_cells,
        local_issues,
    )
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
        "actualCells": len(actual_cells),
        "runtimePromptPairsCovered": len(runtime_metric_pairs - (runtime_metric_pairs - matrix_runtime_pairs)),
        "promptContentStored": matrix.get("costControl", {}).get("promptContentStored") if isinstance(matrix.get("costControl"), dict) else None,
        "promptBudgetDetections": prompt_budget_detections,
        "negativePromptStorageDetected": bool(negative_detections),
        "traceLedgerAudit": trace_ledger_audit,
        "cellEquivalenceAudit": cell_equivalence_audit,
        "maintenanceAudit": maintenance_audit,
        "issues": local_issues,
    }

    if matrix.get("mission") != MATRIX_MISSION:
        local_issues.append(issue("sdlc_runtime_matrix", "matrix_mission", "SDLC runtime matrix mission drifted."))
    if matrix.get("version") != MATRIX_POLICY_VERSION:
        local_issues.append(issue("sdlc_runtime_matrix", "matrix_policy_version", "SDLC runtime matrix policy version drifted."))
    if matrix.get("dimensions") != MATRIX_DIMENSIONS:
        local_issues.append(issue("sdlc_runtime_matrix", "matrix_dimensions", "SDLC runtime matrix dimensions must be phase, copilot and runtime."))
    if matrix.get("runtimes") != RUNTIMES:
        local_issues.append(issue("sdlc_runtime_matrix", "matrix_runtimes", "SDLC runtime matrix runtimes drifted from prompt quality runtimes."))
    if len(actual_cells) != len(expected_cells):
        local_issues.append(
            issue(
                "sdlc_runtime_matrix",
                "matrix_cell_count",
                f"Expected {len(expected_cells)} SDLC runtime cells, found {len(actual_cells)}.",
            )
        )
    missing_cells = sorted(expected_cells - actual_cells)
    if missing_cells:
        local_issues.append(
            issue(
                "sdlc_runtime_matrix",
                "matrix_cell_coverage",
                f"Missing SDLC runtime cell(s): {', '.join('/'.join(item) for item in missing_cells[:10])}.",
            )
        )
    missing_prompt_pairs = sorted(runtime_metric_pairs - matrix_runtime_pairs)
    if missing_prompt_pairs:
        local_issues.append(
            issue(
                "sdlc_runtime_matrix",
                "matrix_prompt_surface_coverage",
                f"Missing runtime prompt pair(s): {', '.join('/'.join(item) for item in missing_prompt_pairs[:10])}.",
            )
        )
    if prompt_budget_detections:
        local_issues.append(
            issue(
                "sdlc_runtime_matrix",
                "matrix_prompt_budget",
                f"Matrix stores raw prompt content or permits prompt storage: {', '.join(prompt_budget_detections)}.",
            )
        )
    if not negative_detections:
        local_issues.append(issue("sdlc_runtime_matrix", "matrix_prompt_negative_case", "Synthetic raw prompt matrix was not detected."))

    summary["pass"] = not local_issues
    issues.extend(local_issues)
    return summary


def validate_sdlc_runtime_matrix_maintenance_prompt_budget(
    receipt: dict,
    matrix: dict,
    expected_cells: set[tuple[str, str, str]],
    issues: list[dict],
) -> dict:
    matrix_summary = matrix.get("summary", {}) if isinstance(matrix.get("summary"), dict) else {}
    receipt_counts = receipt.get("counts", {}) if isinstance(receipt.get("counts"), dict) else {}
    receipt_digests = receipt.get("digests", {}) if isinstance(receipt.get("digests"), dict) else {}
    receipt_gates = receipt.get("acceptanceGates", {}) if isinstance(receipt.get("acceptanceGates"), dict) else {}
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
    prompt_budget_detections = matrix_prompt_budget_detections(receipt)
    negative_receipt = {
        "costControl": {"promptContentStored": True},
        "rawPrompt": "do not store prompt bodies in maintenance receipts",
    }
    negative_detections = matrix_prompt_budget_detections(negative_receipt)
    audit = {
        "pass": False,
        "artifact": relative(SDLC_RUNTIME_MATRIX_MAINTENANCE_JSON),
        "policyVersion": receipt.get("version"),
        "mission": receipt.get("mission"),
        "cellDigestMatches": receipt_digests.get("cellDigest") == stable_json_digest(cells),
        "traceLedgerDigestMatches": receipt_digests.get("traceLedgerDigest") == stable_json_digest(trace_ledger),
        "cellEquivalenceContractDigestMatches": (
            receipt_digests.get("cellEquivalenceContractDigest") == stable_json_digest(matrix_cell_equivalence)
        ),
        "promptBudgetDetections": prompt_budget_detections,
        "negativePromptStorageDetected": bool(negative_detections),
        "allAcceptanceGatesPass": all(receipt_gates.values()) if receipt_gates else False,
        "cellEquivalenceGatePass": receipt_gates.get("cellEquivalence") is True,
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
    if prompt_budget_detections:
        issues.append(
            issue(
                "sdlc_runtime_matrix_maintenance",
                "maintenance_prompt_budget",
                f"Maintenance receipt stores raw prompt content or permits prompt storage: {', '.join(prompt_budget_detections)}.",
            )
        )
    if not negative_detections:
        issues.append(issue("sdlc_runtime_matrix_maintenance", "maintenance_prompt_negative_case", "Synthetic raw prompt maintenance receipt was not detected."))
    if not audit["allAcceptanceGatesPass"]:
        issues.append(issue("sdlc_runtime_matrix_maintenance", "maintenance_acceptance_gates", "Maintenance receipt acceptance gates are not all passing."))

    audit["pass"] = not any(item.get("scope") == "sdlc_runtime_matrix_maintenance" for item in issues)
    return audit


def validate_matrix_trace_ledger_prompt_budget(matrix: dict, expected_cells: set[tuple[str, str, str]], issues: list[dict]) -> dict:
    ledger = matrix.get("traceLedger", []) if isinstance(matrix.get("traceLedger"), list) else []
    expected_entries = {(copilot_id, phase) for copilot_id, phase, _runtime in expected_cells}
    actual_entries = {
        (entry.get("copilotId"), entry.get("phase"))
        for entry in ledger
        if isinstance(entry, dict)
    }
    summary_block = matrix.get("summary", {}) if isinstance(matrix.get("summary"), dict) else {}
    expected_pairwise_count = len(runtime_pairwise_cases())
    trace_ledger_digest = stable_json_digest(ledger)
    runtime_coverage_checked = 0
    pairwise_cases_checked = 0
    prompt_safe_entries = 0

    audit = {
        "expectedEntries": len(expected_entries),
        "actualEntries": len(ledger),
        "entryCoverageMatches": actual_entries == expected_entries,
        "summaryEntryCountMatches": summary_block.get("traceLedgerEntries") == len(ledger),
        "digestMatches": summary_block.get("traceLedgerDigest") == trace_ledger_digest,
        "runtimeCoverageChecked": 0,
        "pairwiseCasesChecked": 0,
        "promptSafeEntries": 0,
        "evidenceMode": "paths_and_sha256_digests_only",
    }

    if not isinstance(matrix.get("traceLedger"), list):
        issues.append(issue("sdlc_runtime_matrix", "matrix_trace_ledger", "Matrix traceLedger must be an array."))
        return audit
    if len(ledger) != len(expected_entries):
        issues.append(
            issue(
                "sdlc_runtime_matrix",
                "matrix_trace_ledger_count",
                f"Expected {len(expected_entries)} trace ledger entries, found {len(ledger)}.",
            )
        )
    if actual_entries != expected_entries:
        missing = sorted(expected_entries - actual_entries)
        extra = sorted(actual_entries - expected_entries)
        details = []
        if missing:
            details.append("missing " + ", ".join("/".join(item) for item in missing[:10]))
        if extra:
            details.append("unexpected " + ", ".join("/".join(str(part) for part in item) for item in extra[:10]))
        issues.append(issue("sdlc_runtime_matrix", "matrix_trace_ledger_coverage", "; ".join(details) or "Trace ledger coverage drifted."))
    if summary_block.get("traceLedgerEntries") != len(ledger):
        issues.append(issue("sdlc_runtime_matrix", "matrix_trace_ledger_summary", "Trace ledger summary count drifted from ledger entries."))
    if summary_block.get("traceLedgerDigest") != trace_ledger_digest:
        issues.append(issue("sdlc_runtime_matrix", "matrix_trace_ledger_digest", "Trace ledger digest drifted from ledger entries."))

    for entry in ledger:
        if not isinstance(entry, dict):
            issues.append(issue("sdlc_runtime_matrix", "matrix_trace_ledger_entry", "Trace ledger entries must be objects."))
            continue
        scope = f"{entry.get('copilotId', 'unknown')}/{entry.get('phase', 'unknown')}"
        runtime_files = entry.get("runtimeFiles", {}) if isinstance(entry.get("runtimeFiles"), dict) else {}
        runtime_digests = entry.get("runtimeFileDigests", {}) if isinstance(entry.get("runtimeFileDigests"), dict) else {}
        runtime_refs = entry.get("runtimeTraceRefs", {}) if isinstance(entry.get("runtimeTraceRefs"), dict) else {}
        pairwise_cases = entry.get("pairwiseRuntimeCases", []) if isinstance(entry.get("pairwiseRuntimeCases"), list) else []
        if entry.get("promptBodiesStored") is False and entry.get("evidenceMode") == "paths_and_sha256_digests_only":
            prompt_safe_entries += 1
        else:
            issues.append(issue(scope, "matrix_trace_ledger_prompt_budget", "Trace ledger must store paths/digests only and no prompt bodies."))
        if (
            set(runtime_files) == set(RUNTIMES)
            and set(runtime_digests) == set(RUNTIMES)
            and set(runtime_refs) == set(RUNTIMES)
            and entry.get("runtimeOrder") == RUNTIMES
        ):
            runtime_coverage_checked += 1
        else:
            issues.append(issue(scope, "matrix_trace_ledger_runtimes", "Trace ledger runtime refs must cover every runtime exactly once."))
        if len(pairwise_cases) == expected_pairwise_count and all(case.get("promptBodiesStored") is False for case in pairwise_cases if isinstance(case, dict)):
            pairwise_cases_checked += len(pairwise_cases)
        else:
            issues.append(issue(scope, "matrix_trace_ledger_pairwise", "Trace ledger pairwise cases must cover all runtime pairs without prompt bodies."))

    audit["runtimeCoverageChecked"] = runtime_coverage_checked
    audit["pairwiseCasesChecked"] = pairwise_cases_checked
    audit["promptSafeEntries"] = prompt_safe_entries
    return audit


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


def matrix_prompt_budget_detections(value) -> list[str]:
    detections: list[str] = []
    cost_control = value.get("costControl", {}) if isinstance(value, dict) else {}
    if not isinstance(cost_control, dict) or cost_control.get("promptContentStored") is not False:
        detections.append("prompt_content_stored")
    detections.extend(find_forbidden_prompt_keys(value))
    return sorted(set(detections))


def find_forbidden_prompt_keys(value, path: str = "$") -> list[str]:
    detections: list[str] = []
    if isinstance(value, dict):
        for key, child in value.items():
            child_path = f"{path}.{key}"
            if key in MATRIX_FORBIDDEN_PROMPT_KEYS:
                detections.append(f"raw_prompt_key:{child_path}")
            detections.extend(find_forbidden_prompt_keys(child, child_path))
    elif isinstance(value, list):
        for index, child in enumerate(value):
            detections.extend(find_forbidden_prompt_keys(child, f"{path}[{index}]"))
    return detections


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
                        "prompt_depth",
                        "shared_schema_reference",
                        "cost_budget",
                        "traceability",
                    ],
                }
            )
    return cases


def run_prompt_quality_negative_cases() -> list[dict]:
    clean_issues: list[dict] = []
    scan_text_safety(ROOT / "generated" / "synthetic-clean.txt", "placeholder value only", clean_issues)

    secret_issues: list[dict] = []
    scan_text_safety(ROOT / "generated" / "synthetic-secret.txt", "sk-" + ("A" * 24), secret_issues)

    expanded_secret_issues: list[dict] = []
    private_key_fixture = "".join(["-----", "BE", "GIN ", "PRI", "VATE ", "KEY", "-----"])
    scan_text_safety(
        ROOT / "generated" / "synthetic-expanded-secret.txt",
        "AKIA" + ("B" * 16) + "\n" + private_key_fixture,
        expanded_secret_issues,
    )

    path_issues: list[dict] = []
    scan_text_safety(ROOT / "generated" / "synthetic-path.txt", "C:" + "\\Users\\Example\\private", path_issues)

    cost_issues: list[dict] = []
    cost_metrics: list[dict] = []
    record_cost_metric(cost_metrics, {"qa_general": {"codexChars": 100}}, "qa_general", "codex", 115, cost_issues)

    fixtures = [
        ("valid_control", clean_issues, False, ""),
        ("secret_pattern", secret_issues, True, "secret_pattern"),
        ("expanded_secret_patterns", expanded_secret_issues, True, "secret_pattern"),
        ("local_path", path_issues, True, "local_path"),
        ("cost_growth", cost_issues, True, "cost_budget"),
    ]
    results = []
    for case_id, detected_issues, should_fail, expected_kind in fixtures:
        kinds = [item.get("kind") for item in detected_issues]
        failure_detected = bool(detected_issues)
        passed_expectation = (
            failure_detected == should_fail
            and (not expected_kind or expected_kind in kinds)
        )
        results.append(
            {
                "id": case_id,
                "expectedFailure": should_fail,
                "failureDetected": failure_detected,
                "passedExpectation": passed_expectation,
                "detected": passed_expectation,
                "detectors": kinds,
            }
        )
    return results


def validate_test_strategy_prompt_quality(metrics: list[dict], cost_metrics: list[dict], issues: list[dict]) -> dict:
    local_issues: list[dict] = []
    pairwise_cases = runtime_pairwise_cases()
    negative_cases = run_prompt_quality_negative_cases()
    qa_metrics = {
        item.get("runtime")
        for item in metrics
        if item.get("id") == "qa_general"
    }
    qa_cost_statuses = {
        item.get("surface"): item.get("status")
        for item in cost_metrics
        if item.get("id") == "qa_general"
    }
    summary = {
        "mission": "Audits test strategy, pairwise cases and negative cases.",
        "targetCopilot": "qa_general",
        "pairwiseCases": pairwise_cases,
        "pairwiseCaseCount": len(pairwise_cases),
        "negativeCases": negative_cases,
        "negativeCasesDetected": all(case["passedExpectation"] for case in negative_cases),
        "qaRuntimeMetricsPresent": sorted(qa_metrics),
        "qaCostStatuses": qa_cost_statuses,
        "runtimeMarkersChecked": [],
    }

    missing_metrics = [runtime for runtime in RUNTIMES if runtime not in qa_metrics]
    if missing_metrics:
        local_issues.append(issue("qa_general", "test_strategy_prompt_quality", f"Missing QA runtime metrics: {', '.join(missing_metrics)}."))

    required_surfaces = [*RUNTIMES, "systemPrompt", "developerPrompt"]
    failing_cost_surfaces = [
        surface
        for surface in required_surfaces
        if qa_cost_statuses.get(surface) != "pass"
    ]
    if failing_cost_surfaces:
        local_issues.append(
            issue(
                "qa_general",
                "test_strategy_cost_budget",
                f"QA prompt surfaces must stay within cost budget: {', '.join(failing_cost_surfaces)}.",
            )
        )

    runtime_files = {
        "codex": ROOT / "dist" / "copilots" / "qa_general" / "codex" / "AGENT.md",
        "claude": ROOT / "dist" / "copilots" / "qa_general" / "claude" / "AGENT.md",
        "github-copilot": ROOT / "dist" / "copilots" / "qa_general" / "github-copilot" / "copilot-agent.md",
        "langchain": ROOT / "dist" / "copilots" / "qa_general" / "langchain" / "agent.py",
    }
    for runtime, path in runtime_files.items():
        text = read_text(path, allow_missing=True)
        missing = [marker for marker in ["qa_strategy", "test_matrix", "pairwise", "negative"] if marker not in text]
        if missing:
            local_issues.append(
                issue(
                    "qa_general",
                    "test_strategy_prompt_markers",
                    f"{runtime} prompt missing test strategy markers: {', '.join(missing)}.",
                )
            )
        else:
            summary["runtimeMarkersChecked"].append(runtime)

    if not summary["negativeCasesDetected"]:
        local_issues.append(issue("qa_general", "test_strategy_negative_cases", "Prompt quality negative fixtures were not all detected."))

    summary["pass"] = not local_issues
    summary["issues"] = local_issues
    issues.extend(local_issues)
    return summary


def render_md(report: dict) -> str:
    top_metrics = "\n".join(
        f"- `{item['id']}` / `{item['runtime']}`: {item['chars']} chars"
        for item in report["metrics"][:20]
    )
    top_cost_metrics = "\n".join(
        (
            f"- `{item['id']}` / `{item['surface']}`: {item['chars']} chars "
            f"(baseline {item['baselineChars']}, delta {item['deltaChars']}, growth {item['growthRatio']})"
        )
        for item in report["costBudget"]["metrics"][:20]
    )
    issues = "\n".join(
        f"- `{item['scope']}` [{item['kind']}]: {item['message']}"
        for item in report["issues"]
    ) or "- none"
    test_strategy = report.get("testStrategyAudit", {})
    matrix_audit = report.get("sdlcRuntimeMatrixAudit", {})
    validator_smoke = report.get("validatorSmoke", {})
    trace_ledger_audit = matrix_audit.get("traceLedgerAudit", {}) if isinstance(matrix_audit, dict) else {}
    cell_equivalence_audit = matrix_audit.get("cellEquivalenceAudit", {}) if isinstance(matrix_audit, dict) else {}
    maintenance_audit = matrix_audit.get("maintenanceAudit", {}) if isinstance(matrix_audit, dict) else {}
    negative_rows = "\n".join(
        (
            f"- `{case['id']}`: passedExpectation={case.get('passedExpectation', case['detected'])}, "
            f"expectedFailure={case['expectedFailure']}, failureDetected={case.get('failureDetected')}"
        )
        for case in test_strategy.get("negativeCases", [])
    ) or "- none"
    return f"""# Prompt Quality Report

Pass: {report['pass']}

Copilots: {report['copilots']}

Minimum depth thresholds:

- Markdown runtime prompt chars: {report['minimumDepthThresholds']['markdownChars']}
- LangChain/Python adapter chars: {report['minimumDepthThresholds']['langchainChars']}
- System prompt chars: {report['minimumDepthThresholds']['systemPromptChars']}
- Developer prompt chars: {report['minimumDepthThresholds']['developerPromptChars']}

Cost budget:

- Baseline: `{report['costBudget']['baseline']}`
- Max growth ratio: {report['costBudget']['maxGrowthRatio']}

Sample metrics:

{top_metrics}

Sample cost metrics:

{top_cost_metrics}

Test strategy audit:

- Pass: {test_strategy.get('pass')}
- Pairwise case count: {test_strategy.get('pairwiseCaseCount')}
- Negative cases detected: {test_strategy.get('negativeCasesDetected')}
- QA runtime metrics present: {test_strategy.get('qaRuntimeMetricsPresent')}
- Runtime markers checked: {test_strategy.get('runtimeMarkersChecked')}

SDLC runtime matrix audit:

- Pass: {matrix_audit.get('pass')}
- Artifact: `{matrix_audit.get('artifact')}`
- Policy version: {matrix_audit.get('policyVersion')}
- Expected cells: {matrix_audit.get('expectedCells')}
- Actual cells: {matrix_audit.get('actualCells')}
- Runtime prompt pairs covered: {matrix_audit.get('runtimePromptPairsCovered')}
- Prompt content stored: {matrix_audit.get('promptContentStored')}
- Prompt budget detections: {matrix_audit.get('promptBudgetDetections')}
- Negative prompt storage detected: {matrix_audit.get('negativePromptStorageDetected')}
- Trace ledger entries: {trace_ledger_audit.get('actualEntries')} / {trace_ledger_audit.get('expectedEntries')}
- Trace ledger digest matches: {trace_ledger_audit.get('digestMatches')}
- Trace ledger runtime coverage checked: {trace_ledger_audit.get('runtimeCoverageChecked')}
- Trace ledger pairwise cases checked: {trace_ledger_audit.get('pairwiseCasesChecked')}
- Cell equivalence pass: {cell_equivalence_audit.get('pass')}
- Cell equivalence cells passing: {cell_equivalence_audit.get('passingCells')} / {cell_equivalence_audit.get('cellsChecked')}
- Maintenance artifact: `{matrix_audit.get('maintenanceArtifact')}`
- Maintenance receipt pass: {maintenance_audit.get('pass')}
- Maintenance prompt budget detections: {maintenance_audit.get('promptBudgetDetections')}
- Maintenance cell digest matches: {maintenance_audit.get('cellDigestMatches')}
- Maintenance cell equivalence gate: {maintenance_audit.get('cellEquivalenceGatePass')}

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


def relative(path: Path) -> str:
    return str(path.relative_to(ROOT)).replace("\\", "/")


def format_path(path: Path) -> str:
    try:
        return relative(path)
    except ValueError:
        return path.name


if __name__ == "__main__":
    main()
