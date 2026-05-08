from __future__ import annotations

import re
from typing import Any

MAX_REQUEST_CHARS = 2000
MAX_EVIDENCE_DEPTH = 6
MAX_EVIDENCE_ITEMS = 200
MAX_EVIDENCE_KEY_CHARS = 120
MAX_EVIDENCE_STRING_CHARS = 4000
SECRET_KEY_PARTS = {
    "token",
    "secret",
    "password",
    "credential",
    "authorization",
    "pat",
    "customer",
    "tenant",
    "billing",
}
SECRET_KEY_NAMES = {"api_key", "apikey", "private_key", "access_token", "client_secret", "bearer"}
PRIVATE_KEY_BLOCK_RE = (
    r"-{5}"
    r"BE" r"GIN "
    r"(?:RSA |DSA |EC |OPENSSH |PGP )?"
    r"PRI" r"VATE " r"KEY"
    r"-{5}"
)
SECRET_RE = re.compile(
    (
        r"sk-[\w-]{20,}|github_pat_\w{20,}|gh[pousr]_\w{20,}|glpat-[\w-]{20,}|"
        r"(?:AKIA|ASIA)[0-9A-Z]{16}|AIza[0-9A-Za-z_-]{35}|xox[baprs]-[A-Za-z0-9-]{20,}|"
        r"eyJ[A-Za-z0-9_-]{20,}\.[A-Za-z0-9_-]{20,}\.[A-Za-z0-9_-]{20,}|"
        + PRIVATE_KEY_BLOCK_RE
        + r"|Bearer\s+[\w.~+/=-]{8,}|"
        r"([A-Z0-9_]*(token|secret|password|credential|authorization|pat)|"
        r"api[_-]?key|private[_-]?key|access[_-]?token|client[_-]?secret|"
        r"customer[_-]?(data|id)?|tenant[_-]?id|billing[_-]?data)\s*[:=]\s*\S+|"
        r"\b[A-Z]:[\\/]+Users[\\/]+[^\\/\s\"']+(?:[\\/][^\\/\s\"']+)*|"
        r"/Users/[^/\s\"']+(?:/[^/\s\"']+)*|/home/[^/\s\"']+(?:/[^/\s\"']+)*"
    ),
    re.I,
)


def validate_request(request: object, label: str = "LangChain request") -> str:
    if not isinstance(request, str):
        raise ValueError(f"{label} must be a string.")
    normalized = " ".join(request.split())
    if not normalized:
        raise ValueError(f"{label} cannot be empty.")
    if len(normalized) > MAX_REQUEST_CHARS:
        raise ValueError(f"{label} must be {MAX_REQUEST_CHARS} characters or fewer.")
    return normalized


def validate_evidence(evidence: object | None, label: str = "LangChain evidence") -> dict[str, Any]:
    if evidence is None:
        return {}
    if not isinstance(evidence, dict):
        raise ValueError(f"{label} must be a dictionary.")
    return _validate_evidence_node(evidence, label, "$", 0, {"items": 0})


def _validate_evidence_node(
    value: Any,
    label: str,
    path: str,
    depth: int,
    counter: dict[str, int],
) -> Any:
    counter["items"] += 1
    if counter["items"] > MAX_EVIDENCE_ITEMS:
        raise ValueError(f"{label} must contain {MAX_EVIDENCE_ITEMS} nested items or fewer.")
    if depth > MAX_EVIDENCE_DEPTH:
        raise ValueError(f"{label} is too deeply nested at {path}.")

    if isinstance(value, dict):
        normalized: dict[str, Any] = {}
        for key, item in value.items():
            key_str = str(key).strip()
            if not key_str:
                raise ValueError(f"{label} contains an empty key at {path}.")
            if len(key_str) > MAX_EVIDENCE_KEY_CHARS:
                raise ValueError(f"{label} key at {path} must be {MAX_EVIDENCE_KEY_CHARS} characters or fewer.")
            child_path = f"{path}.{key_str}"
            if is_secret_key(key_str):
                normalized[key_str] = "[REDACTED]"
            else:
                normalized[key_str] = _validate_evidence_node(item, label, child_path, depth + 1, counter)
        return normalized

    if isinstance(value, list):
        return [
            _validate_evidence_node(item, label, f"{path}[{index}]", depth + 1, counter)
            for index, item in enumerate(value)
        ]

    if isinstance(value, str):
        if len(value) > MAX_EVIDENCE_STRING_CHARS:
            raise ValueError(f"{label} string at {path} must be {MAX_EVIDENCE_STRING_CHARS} characters or fewer.")
        return redact_value(value.strip())

    if isinstance(value, (int, float, bool)) or value is None:
        return value

    raise ValueError(
        f"{label} contains unsupported value at {path}; use strings, numbers, booleans, lists or dictionaries."
    )


def is_secret_key(key: object) -> bool:
    normalized = re.sub(r"[^a-z0-9]+", "_", str(key).strip().lower()).strip("_")
    parts = set(normalized.split("_"))
    return normalized in SECRET_KEY_NAMES or bool(parts & SECRET_KEY_PARTS)


def redact_value(value: Any) -> Any:
    if isinstance(value, dict):
        return {
            str(key): "[REDACTED]" if is_secret_key(key) else redact_value(item)
            for key, item in value.items()
        }
    if isinstance(value, list):
        return [redact_value(item) for item in value]
    if isinstance(value, str):
        return SECRET_RE.sub("[REDACTED]", value)
    return value
