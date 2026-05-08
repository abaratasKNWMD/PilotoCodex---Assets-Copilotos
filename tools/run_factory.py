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
    re.compile(r"Bearer\s+[A-Za-z0-9._~+/=-]{20,}", re.I),
]
LOCAL_PATH_PATTERNS = [
    re.compile(r"(?i)\b[A-Z]:[\\/]+Users[\\/]+[^\\/\s\"']+"),
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

    report["lineCount"] = text.count("\n") + (0 if not text or text.endswith("\n") else 1)
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
    LOG_EVIDENCE_PATH.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
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
    AUDIT_PATH.write_text(json.dumps(audit, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    run(RUN_SEQUENCE[0])
    emit_devops_audit()
    for script in RUN_SEQUENCE[1:]:
        run(script)
