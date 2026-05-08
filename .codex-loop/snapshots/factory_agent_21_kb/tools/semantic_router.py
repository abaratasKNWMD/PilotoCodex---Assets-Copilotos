from __future__ import annotations

import json
import math
import re
import unicodedata
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
ARCHITECTURE_AUDIT_COPILOT = "aida_architecture"
ARCHITECTURE_AUDIT_SOURCE = "dist/copilots/aida_architecture/shared/architecture_decision_audit.json"
ARCHITECTURE_AUDIT_BOOST = CHEAP_PATH_THRESHOLD
ARCHITECTURE_AUDIT_SCOPE = {"architecture", "arquitectura"}
ARCHITECTURE_AUDIT_REQUIRED = {
    "adr",
    "calidad",
    "decision",
    "principios",
    "principles",
    "quality",
    "technical",
    "tecnica",
    "tecnico",
}
DESIGN_AUDIT_VERSION = "domain-boundary-handoff-audit-1.0"
DESIGN_AUDIT_SCOPE = {"design", "diseno"}
DESIGN_AUDIT_REQUIRED = {
    "acceptance",
    "api",
    "boundaries",
    "boundary",
    "contract",
    "contracts",
    "contratos",
    "criteria",
    "data",
    "domain",
    "dominio",
    "handoff",
    "limites",
    "modules",
    "traspaso",
}
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
BUILD_AUDIT_VERSION = "implementation-plan-stack-rules-audit-1.0"
BUILD_AUDIT_SCOPE = {"build", "implementation", "implementacion", "patch"}
BUILD_AUDIT_REQUIRED = {
    "affected",
    "archivos",
    "files",
    "plan",
    "reglas",
    "rollback",
    "rules",
    "stack",
    "tests",
    "validation",
}
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


def ascii_fold(text: object) -> str:
    return unicodedata.normalize("NFKD", str(text or "")).encode("ascii", "ignore").decode("ascii")


def normalize(text: str) -> set[str]:
    clean = re.sub(r"[^a-zA-Z0-9_ -]+", " ", ascii_fold(text).lower())
    return set(clean.replace("-", " ").replace("_", " ").split())


def request_chunks(text: str) -> list[str]:
    return [chunk for chunk in re.split(r"[^A-Za-z0-9_-]+", ascii_fold(text)) if chunk]


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
    if architecture_audit_applies(copilot, words):
        score += ARCHITECTURE_AUDIT_BOOST
        reasons.append("architecture_audit:shared_contract")
    if design_audit_applies(copilot, words):
        score += CHEAP_PATH_THRESHOLD
        reasons.append("design_audit:shared_contract")
    if build_audit_applies(copilot, words):
        score += CHEAP_PATH_THRESHOLD
        reasons.append("build_audit:shared_contract")
    return score, reasons


def architecture_audit_applies(copilot: dict, words: set[str]) -> bool:
    if copilot.get("id") != ARCHITECTURE_AUDIT_COPILOT:
        return False
    if not words & ARCHITECTURE_AUDIT_SCOPE:
        return False
    return bool(words & ARCHITECTURE_AUDIT_REQUIRED)


def design_audit_applies(copilot: dict, words: set[str]) -> bool:
    if "design" not in list_values(copilot.get("sdlc_phases")):
        return False
    if not words & DESIGN_AUDIT_SCOPE:
        return False
    return bool(words & DESIGN_AUDIT_REQUIRED)


def build_audit_applies(copilot: dict, words: set[str]) -> bool:
    if "build" not in list_values(copilot.get("sdlc_phases")):
        return False
    if not words & BUILD_AUDIT_SCOPE:
        return False
    return bool(words & BUILD_AUDIT_REQUIRED)


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
    if item["id"] == ARCHITECTURE_AUDIT_COPILOT:
        payload["architecture_decision_audit"] = architecture_decision_audit_evidence()
    if "design" in item.get("sdlc_phases", []):
        payload["design_boundary_audit"] = design_boundary_audit_evidence(item["id"])
    if "build" in item.get("sdlc_phases", []):
        payload["implementation_plan_audit"] = implementation_plan_audit_evidence(item["id"])
    return payload


def architecture_decision_audit_evidence() -> dict:
    return {
        "mission": "Audits principles, ADRs and technical decision quality.",
        "source_of_truth": ARCHITECTURE_AUDIT_SOURCE,
        "required_evidence": [
            "principles",
            "adr",
            "technical_decision_quality",
            "validation",
        ],
        "quality_gates": [
            "principle_alignment",
            "adr_completeness",
            "decision_quality",
            "traceability_and_cost",
        ],
        "runtime_equivalence": {
            "runtimes": list(RUNTIMES),
            "max_unexplained_drift": 0,
        },
    }


def design_boundary_audit_evidence(copilot_id: str) -> dict:
    return {
        "mission": "Audits domain boundaries, contracts and handoff clarity.",
        "source_of_truth": f"dist/copilots/{copilot_id}/shared/design_boundary_audit.json",
        "policy_version": DESIGN_AUDIT_VERSION,
        "required_evidence": DESIGN_REQUIRED_EVIDENCE,
        "quality_gates": DESIGN_QUALITY_GATES,
        "required_output_fields": [
            "copilot_id",
            "decision",
            "evidence",
            "actions",
            "validation",
            "risks",
            "handoff",
        ],
        "required_handoff_fields": DESIGN_REQUIRED_HANDOFF_FIELDS,
        "runtime_equivalence": {
            "runtimes": list(RUNTIMES),
            "max_unexplained_drift": 0,
        },
    }


def implementation_plan_audit_evidence(copilot_id: str) -> dict:
    return {
        "mission": "Audits implementation plans and stack-specific rules.",
        "source_of_truth": f"dist/copilots/{copilot_id}/shared/implementation_plan_audit.json",
        "policy_version": BUILD_AUDIT_VERSION,
        "required_evidence": BUILD_REQUIRED_EVIDENCE,
        "quality_gates": BUILD_QUALITY_GATES,
        "required_output_fields": [
            "copilot_id",
            "decision",
            "evidence",
            "actions",
            "validation",
            "risks",
            "implementation",
        ],
        "required_implementation_fields": BUILD_REQUIRED_IMPLEMENTATION_FIELDS,
        "runtime_equivalence": {
            "runtimes": list(RUNTIMES),
            "max_unexplained_drift": 0,
        },
    }


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
