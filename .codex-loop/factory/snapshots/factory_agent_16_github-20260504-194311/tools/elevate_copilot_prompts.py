from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from textwrap import dedent


FACTORY_VERSION = "copilot-factory-0.2.0"
RUNTIMES = ["codex", "claude", "github-copilot", "langchain"]
DIRECTOR_AGENT = "factory_agent_01_director"
DIRECTOR_MISSION = "Owns the whole run, keeps gates honest and prevents scope drift."
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
CLOUD_AGENT = "factory_agent_11_cloud"
CLOUD_MISSION = "Audits migration, target platform and modernization increments."
CLOUD_AUDIT_VERSION = "cloud-migration-target-modernization-audit-1.0"
CLOUD_AUDIT_ARTIFACT = "shared/cloud_migration_audit.json"
CLOUD_TARGET_COPILOT = "journey_to_cloud"
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
]

FAMILY_RULES = {
    "core": {
        "mission": "Protect the operating model, normalize truth and keep every specialist aligned to the same SDLC evidence.",
        "risk": "Fragmented guidance, undocumented assumptions, duplicated registries and tool use without evidence.",
        "primary_gate": "The copilot must turn ambiguity into a small, auditable operating contract before anyone writes code.",
    },
    "development": {
        "mission": "Produce stack-specific implementation plans, patches and verification loops without breaking ownership boundaries.",
        "risk": "Fast code that ignores architecture, test contracts, CI health or source-of-truth constraints.",
        "primary_gate": "No patch plan is valid until affected files, tests, rollback path and acceptance evidence are named.",
    },
    "quality": {
        "mission": "Find defects before users do by converting requirements, code, risks and telemetry into executable checks.",
        "risk": "Happy-path testing, unprioritized findings, weak reproduction steps and noisy reports.",
        "primary_gate": "Every finding needs severity, evidence, reproduction path and a concrete verification command.",
    },
    "devops": {
        "mission": "Make builds, releases and runtime diagnostics reproducible, observable and reversible.",
        "risk": "Treating CI failures as text problems instead of environment, dependency, secret, cache or workflow problems.",
        "primary_gate": "No release recommendation without logs, command history, rollback and owner impact.",
    },
    "cloud": {
        "mission": "Move legacy systems to safer cloud increments with explicit target architecture and risk burn-down.",
        "risk": "Big-bang migration, hidden coupling, unpriced platform assumptions and missing operational ownership.",
        "primary_gate": "Every migration step must preserve a working system and name data, network, security and observability impacts.",
    },
    "orchestration": {
        "mission": "Route work to the cheapest competent specialist, keep state, and prevent tool or prompt sprawl.",
        "risk": "Everyone doing everything, context flooding, runaway token cost and untraceable handoffs.",
        "primary_gate": "Every handoff must include intent, selected copilot, excluded copilots, evidence pack and stop condition.",
    },
    "marketplace": {
        "mission": "Package copilots as reusable products with manifests, versioning, compatibility and trust signals.",
        "risk": "Shipping impressive prompts that cannot be installed, audited, updated or compared safely.",
        "primary_gate": "No package is complete without manifest, changelog, compatibility matrix, examples and validation report.",
    },
}

STACK_RULES = {
    "java": [
        "Inspect build files before proposing framework changes: pom.xml, build.gradle, settings.gradle and CI workflows.",
        "Respect package boundaries, dependency direction, transaction scope and existing test style.",
        "Prefer small refactors with characterization tests before broad modernization.",
    ],
    "spring": [
        "Check controllers, service boundaries, configuration properties, security filters and transactional annotations.",
        "Name the API contract impact before changing DTOs, validation or persistence models.",
    ],
    "maven": [
        "Use Maven lifecycle evidence and dependency tree impact before changing plugins or versions.",
    ],
    "gradle": [
        "Use Gradle task graph and wrapper compatibility before changing plugins or versions.",
    ],
    "angular": [
        "Audit component inputs, outputs, signals, reactive forms, accessibility and change detection before editing.",
        "Keep UI changes consistent with existing design system and test the rendered behavior, not only TypeScript.",
    ],
    "typescript": [
        "Preserve strict typing, avoid hidden any, and validate generated contracts at module boundaries.",
    ],
    "node": [
        "Trace route, service, persistence and observability boundaries before changing handlers.",
        "Name idempotency, timeout and retry behavior for backend operations.",
    ],
    "python": [
        "Use Python for deterministic catalog work, parsing, scoring, data shaping and validation before LLM calls.",
        "Prefer typed data contracts, pathlib, json schema style validation and reproducible command-line tools.",
    ],
    "github_actions": [
        "Read workflow YAML, failing logs and matrix configuration before proposing fixes.",
    ],
    "cloud": [
        "Separate application, data, identity, network, deployment and observability decisions.",
    ],
    "legacy": [
        "Document current behavior before modernization; never erase unknown business rules.",
    ],
    "all": [
        "Start with source evidence, not memory. Keep every recommendation traceable to files, logs or catalog entries.",
    ],
}

RUNTIME_RULES = {
    "codex": {
        "name": "Codex",
        "focus": "Tool-capable local execution: inspect repository state, edit scoped files, run validators and report exact evidence.",
        "avoid": "Do not answer as pure advice when files can be inspected or validators can be run.",
    },
    "claude": {
        "name": "Claude",
        "focus": "Long-context synthesis: compress evidence, compare trade-offs, produce review-ready artifacts and ask for executor handoff when code tools are absent.",
        "avoid": "Do not invent file state. Label assumptions when live repository access is unavailable.",
    },
    "github-copilot": {
        "name": "GitHub Copilot Agents",
        "focus": "Repository-native PR/issue/check workflow using GitHub evidence, MCP connectors and minimal patch scopes.",
        "avoid": "Do not bypass CI, unresolved review feedback or branch policy.",
    },
}


def is_architecture_decision_copilot(copilot: dict) -> bool:
    return copilot.get("id") == ARCHITECTURE_TARGET_COPILOT


def architecture_runtime_contract() -> dict:
    return {
        "artifact": ARCHITECTURE_AUDIT_ARTIFACT,
        "version": ARCHITECTURE_AUDIT_VERSION,
        "ownerAgent": ARCHITECTURE_AGENT,
        "mission": ARCHITECTURE_MISSION,
        "requiredEvidence": ARCHITECTURE_REQUIRED_EVIDENCE,
        "qualityGates": ARCHITECTURE_QUALITY_GATES,
        "runtimeEquivalence": ARCHITECTURE_RUNTIME_EQUIVALENCE,
    }


def architecture_audit_artifact() -> dict:
    return {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "id": "architecture_decision_audit_v1",
        "version": ARCHITECTURE_AUDIT_VERSION,
        "ownerAgent": ARCHITECTURE_AGENT,
        "copilotId": ARCHITECTURE_TARGET_COPILOT,
        "mission": ARCHITECTURE_MISSION,
        "runtimeEquivalence": ARCHITECTURE_RUNTIME_EQUIVALENCE,
        "requiredEvidence": [
            {
                "id": "principles",
                "minimumRefs": 1,
                "description": "Architecture principles or guardrails used to evaluate the decision.",
            },
            {
                "id": "adr",
                "minimumRefs": 1,
                "description": "ADR, decision log or equivalent record with context and consequences.",
            },
            {
                "id": "technical_decision_quality",
                "minimumRefs": 1,
                "description": "Trade-off analysis covering maintainability, reliability and release readiness.",
            },
            {
                "id": "validation",
                "minimumRefs": 1,
                "description": "Deterministic command, route evidence or review checklist proving the audit path.",
            },
        ],
        "qualityGates": [
            {
                "id": "principle_alignment",
                "passSignal": "Decision cites the relevant principle and states alignment or exception.",
                "failSignal": "Decision claims architecture quality without a named principle.",
            },
            {
                "id": "adr_completeness",
                "passSignal": "Context, decision, consequences and status are recorded.",
                "failSignal": "ADR evidence is missing, stale or only describes the preferred option.",
            },
            {
                "id": "decision_quality",
                "passSignal": "Trade-offs, alternatives and risk impact are explicit.",
                "failSignal": "Decision hides operational or integration consequences.",
            },
            {
                "id": "traceability_and_cost",
                "passSignal": "All runtimes point to the same audit artifact and avoid repeated broad prompt expansion.",
                "failSignal": "Architecture evidence drifts between runtime adapters.",
            },
        ],
        "requiredOutputFields": [
            "copilot_id",
            "decision",
            "evidence",
            "actions",
            "validation",
            "risks",
        ],
        "routingSignals": ARCHITECTURE_ROUTING_SIGNALS,
        "validationCommands": ARCHITECTURE_VALIDATION_COMMANDS,
    }


def architecture_runtime_section(copilot: dict) -> str:
    if not is_architecture_decision_copilot(copilot):
        return ""
    return clean_template(f"""\

    ## Architecture Decision Audit

    - Artifact: `{ARCHITECTURE_AUDIT_ARTIFACT}`
    - Mission: {ARCHITECTURE_MISSION}
    - Required evidence: {", ".join(ARCHITECTURE_REQUIRED_EVIDENCE)}
    - Quality gates: {", ".join(ARCHITECTURE_QUALITY_GATES)}
    """)


def is_design_boundary_copilot(copilot: dict) -> bool:
    return copilot.get("id") in DESIGN_TARGET_COPILOTS and "design" in copilot.get("sdlc_phases", [])


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


def design_injection_contract(copilot_id: str) -> dict:
    return {
        "artifact": design_audit_source(copilot_id),
        "ownerAgent": DESIGN_AGENT,
        "mission": DESIGN_MISSION,
        "requiredEvidence": DESIGN_REQUIRED_EVIDENCE,
        "qualityGates": DESIGN_QUALITY_GATES,
        "requiredOutputFields": DESIGN_REQUIRED_OUTPUT_FIELDS,
        "requiredHandoffFields": DESIGN_REQUIRED_HANDOFF_FIELDS,
        "runtimeEquivalence": design_runtime_equivalence(copilot_id),
    }


def design_audit_artifact(copilot_id: str) -> dict:
    return {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "id": "design_boundary_audit_v1",
        "version": DESIGN_AUDIT_VERSION,
        "ownerAgent": DESIGN_AGENT,
        "copilotId": copilot_id,
        "mission": DESIGN_MISSION,
        "runtimeEquivalence": design_runtime_equivalence(copilot_id),
        "requiredEvidence": [
            {
                "id": "domain_boundaries",
                "minimumRefs": 1,
                "description": "Named bounded context, module, UI/API surface or data ownership boundary under review.",
            },
            {
                "id": "contracts",
                "minimumRefs": 1,
                "description": "Schema, interface, route, event, DTO or acceptance contract that callers and implementers share.",
            },
            {
                "id": "handoff_clarity",
                "minimumRefs": 1,
                "description": "Owner, next action, excluded scope, dependency and stop condition for the next runtime or copilot.",
            },
            {
                "id": "validation",
                "minimumRefs": 1,
                "description": "Deterministic command, schema check, route payload or review checklist proving the handoff path.",
            },
        ],
        "qualityGates": [
            {
                "id": "boundary_ownership",
                "passSignal": "Every changed domain surface names owner, caller, callee and allowed dependency direction.",
                "failSignal": "The plan changes a module, API or data boundary without naming ownership and dependency direction.",
            },
            {
                "id": "contract_completeness",
                "passSignal": "Inputs, outputs, errors, versioning and compatibility expectations are present or a gap is recorded.",
                "failSignal": "The contract only describes happy-path behavior or leaves callers to infer payload shape.",
            },
            {
                "id": "handoff_readiness",
                "passSignal": "Next owner, evidence pack, excluded scope, validation command and stop condition are explicit.",
                "failSignal": "The next runtime or copilot receives a vague task with no acceptance evidence or owner.",
            },
            {
                "id": "traceability_and_cost",
                "passSignal": "Python-first checks, source references and runtime adapter trace remain equivalent across all four runtimes.",
                "failSignal": "One runtime changes gate names, expands prompt cost materially, or drops the shared design audit reference.",
            },
        ],
        "requiredOutputFields": DESIGN_REQUIRED_OUTPUT_FIELDS,
        "requiredHandoffFields": DESIGN_REQUIRED_HANDOFF_FIELDS,
        "routingSignals": DESIGN_ROUTING_SIGNALS,
        "validationCommands": DESIGN_VALIDATION_COMMANDS,
    }


def design_runtime_section(copilot: dict) -> str:
    if not is_design_boundary_copilot(copilot):
        return ""
    return clean_template(f"""\

    ## Design Boundary Audit

    - Artifact: `{DESIGN_AUDIT_ARTIFACT}`
    - Mission: {DESIGN_MISSION}
    - Required evidence: {", ".join(DESIGN_REQUIRED_EVIDENCE)}
    - Quality gates: {", ".join(DESIGN_QUALITY_GATES)}
    - Required handoff field: `handoff`
    - Required handoff subfields: {", ".join(DESIGN_REQUIRED_HANDOFF_FIELDS)}
    """)


def is_build_implementation_copilot(copilot: dict) -> bool:
    return copilot.get("id") in BUILD_TARGET_COPILOTS and "build" in copilot.get("sdlc_phases", [])


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


def build_injection_contract(copilot_id: str) -> dict:
    return {
        "artifact": build_audit_source(copilot_id),
        "ownerAgent": BUILD_AGENT,
        "mission": BUILD_MISSION,
        "requiredEvidence": BUILD_REQUIRED_EVIDENCE,
        "qualityGates": BUILD_QUALITY_GATES,
        "requiredOutputFields": BUILD_REQUIRED_OUTPUT_FIELDS,
        "requiredImplementationFields": BUILD_REQUIRED_IMPLEMENTATION_FIELDS,
        "runtimeEquivalence": build_runtime_equivalence(copilot_id),
    }


def build_stack_rule_matrix(copilot: dict) -> list[dict]:
    matrix = []
    for stack in copilot.get("stacks", []):
        matrix.append({
            "stack": stack,
            "rules": STACK_RULES.get(stack, [f"Apply repository evidence before changing {stack} artifacts."]),
        })
    return matrix


def build_audit_artifact(copilot: dict) -> dict:
    return {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "id": "implementation_plan_audit_v1",
        "version": BUILD_AUDIT_VERSION,
        "ownerAgent": BUILD_AGENT,
        "copilotId": copilot["id"],
        "mission": BUILD_MISSION,
        "runtimeEquivalence": build_runtime_equivalence(copilot["id"]),
        "stackRuleMatrix": build_stack_rule_matrix(copilot),
        "requiredEvidence": [
            {
                "id": "implementation_plan",
                "minimumRefs": 1,
                "description": "Scoped plan steps tied to files, modules or generated artifacts before code changes proceed.",
            },
            {
                "id": "stack_rules",
                "minimumRefs": 1,
                "description": "Stack-specific rules from this copilot package that were checked against the plan.",
            },
            {
                "id": "affected_files",
                "minimumRefs": 1,
                "description": "Concrete files, globs, modules or generated paths in scope, with unrelated scope excluded.",
            },
            {
                "id": "validation",
                "minimumRefs": 1,
                "description": "Deterministic command, test, lint, typecheck or schema check that proves build readiness.",
            },
        ],
        "qualityGates": [
            {
                "id": "scoped_implementation_plan",
                "passSignal": "Plan names changed files, ownership, sequencing and explicit out-of-scope boundaries.",
                "failSignal": "Plan says to implement broadly without affected files, owner or stop condition.",
            },
            {
                "id": "stack_rule_alignment",
                "passSignal": "Plan references relevant stack rules and explains any unsupported or deferred rule.",
                "failSignal": "Plan ignores stack-specific framework, build-tool, UI or runtime constraints.",
            },
            {
                "id": "test_and_rollback_readiness",
                "passSignal": "Validation commands and rollback notes are present before handoff to an editing runtime.",
                "failSignal": "Patch work starts without tests, typecheck/build signal or rollback path.",
            },
            {
                "id": "traceability_and_cost",
                "passSignal": "Python-first checks, source refs and one shared contract drive all four runtime adapters.",
                "failSignal": "One runtime invents a separate build plan or expands prompt cost without artifact evidence.",
            },
        ],
        "requiredOutputFields": BUILD_REQUIRED_OUTPUT_FIELDS,
        "requiredImplementationFields": BUILD_REQUIRED_IMPLEMENTATION_FIELDS,
        "routingSignals": BUILD_ROUTING_SIGNALS,
        "validationCommands": BUILD_VALIDATION_COMMANDS,
    }


def build_runtime_section(copilot: dict) -> str:
    if not is_build_implementation_copilot(copilot):
        return ""
    return clean_template(f"""\

    ## Build Implementation Audit

    - Artifact: `{BUILD_AUDIT_ARTIFACT}`
    - Mission: {BUILD_MISSION}
    - Required evidence: {", ".join(BUILD_REQUIRED_EVIDENCE)}
    - Quality gates: {", ".join(BUILD_QUALITY_GATES)}
    - Required implementation field: `implementation`
    - Required implementation subfields: {", ".join(BUILD_REQUIRED_IMPLEMENTATION_FIELDS)}
    """)


def is_cloud_migration_copilot(copilot: dict) -> bool:
    return copilot.get("id") == CLOUD_TARGET_COPILOT and "cloud" in copilot.get("sdlc_phases", [])


def cloud_audit_source() -> str:
    return f"dist/copilots/{CLOUD_TARGET_COPILOT}/shared/cloud_migration_audit.json"


def cloud_runtime_equivalence() -> dict:
    return {
        "sourceOfTruth": cloud_audit_source(),
        "runtimes": RUNTIMES,
        "traceSource": "generated/runtime-injection-map.json#/copilots/journey_to_cloud/cloudMigrationAudit",
        "maxUnexplainedDrift": 0,
    }


def cloud_runtime_contract() -> dict:
    return {
        "artifact": CLOUD_AUDIT_ARTIFACT,
        "version": CLOUD_AUDIT_VERSION,
        "ownerAgent": CLOUD_AGENT,
        "mission": CLOUD_MISSION,
        "requiredEvidence": CLOUD_REQUIRED_EVIDENCE,
        "qualityGates": CLOUD_QUALITY_GATES,
        "requiredOutputFields": CLOUD_REQUIRED_OUTPUT_FIELDS,
        "requiredCloudMigrationFields": CLOUD_REQUIRED_MIGRATION_FIELDS,
        "runtimeEquivalence": cloud_runtime_equivalence(),
    }


def cloud_injection_contract() -> dict:
    return {
        "artifact": cloud_audit_source(),
        "ownerAgent": CLOUD_AGENT,
        "mission": CLOUD_MISSION,
        "requiredEvidence": CLOUD_REQUIRED_EVIDENCE,
        "qualityGates": CLOUD_QUALITY_GATES,
        "requiredOutputFields": CLOUD_REQUIRED_OUTPUT_FIELDS,
        "requiredCloudMigrationFields": CLOUD_REQUIRED_MIGRATION_FIELDS,
        "runtimeEquivalence": cloud_runtime_equivalence(),
    }


def cloud_audit_artifact() -> dict:
    return {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "id": "cloud_migration_audit_v1",
        "version": CLOUD_AUDIT_VERSION,
        "ownerAgent": CLOUD_AGENT,
        "copilotId": CLOUD_TARGET_COPILOT,
        "mission": CLOUD_MISSION,
        "runtimeEquivalence": cloud_runtime_equivalence(),
        "requiredEvidence": [
            {
                "id": "migration_inventory",
                "minimumRefs": 1,
                "description": "Current-state systems, integrations, data flows, owners and coupling that shape the migration path.",
            },
            {
                "id": "target_platform",
                "minimumRefs": 1,
                "description": "Target runtime, data, identity, network, observability and operating-model constraints.",
            },
            {
                "id": "modernization_increments",
                "minimumRefs": 3,
                "description": "Reversible modernization steps that preserve service continuity and avoid unbounded rewrites.",
            },
            {
                "id": "validation",
                "minimumRefs": 1,
                "description": "Deterministic command, schema check or review gate that proves the cloud plan is traceable.",
            },
        ],
        "qualityGates": [
            {
                "id": "incremental_migration_plan",
                "passSignal": "Each migration increment names current-state evidence, target capability, validation and rollback.",
                "failSignal": "The plan jumps from legacy state to target platform without bounded intermediate states.",
            },
            {
                "id": "platform_fit_and_constraints",
                "passSignal": "Target platform choice records runtime, data, identity, network, observability and operating constraints.",
                "failSignal": "Cloud provider or platform claims appear without constraints, caveats or local evidence.",
            },
            {
                "id": "modernization_traceability",
                "passSignal": "Modernization actions trace to source evidence, owner, affected surface and acceptance signal.",
                "failSignal": "Modernization is described as generic improvement without changed surfaces or owners.",
            },
            {
                "id": "cost_time_guard",
                "passSignal": "Python-first checks verify artifacts and LLM escalation is limited to platform trade-off judgement.",
                "failSignal": "Prompt growth or repeated LLM analysis replaces deterministic artifact checks.",
            },
        ],
        "requiredOutputFields": CLOUD_REQUIRED_OUTPUT_FIELDS,
        "requiredCloudMigrationFields": CLOUD_REQUIRED_MIGRATION_FIELDS,
        "migrationIncrementTemplate": {
            "requiredFields": [
                "increment_id",
                "source_evidence",
                "target_capability",
                "modernization_action",
                "validation_command",
                "rollback_path",
            ],
            "emptyStatePolicy": "If evidence is unavailable, mark the increment blocked and record the missing source rather than inventing platform facts.",
            "privacyPolicy": "Use placeholders for credentials, billing data, customer data and connector demonstrations.",
        },
        "targetPlatformDecisionInputs": [
            "runtime",
            "data",
            "identity",
            "network",
            "observability",
            "operating_model",
            "rollback",
        ],
        "validationCommands": CLOUD_VALIDATION_COMMANDS,
        "costControl": {
            "deterministicPythonFirst": True,
            "llmEscalation": "allowed_after_platform_tradeoff_only",
            "maxPromptGrowthRatio": 0.1,
        },
    }


def cloud_runtime_section(copilot: dict) -> str:
    if not is_cloud_migration_copilot(copilot):
        return ""
    return clean_template(f"""\

    ## Cloud Migration Audit

    - Artifact: `{CLOUD_AUDIT_ARTIFACT}`
    - Mission: {CLOUD_MISSION}
    - Required evidence: {", ".join(CLOUD_REQUIRED_EVIDENCE)}
    - Quality gates: {", ".join(CLOUD_QUALITY_GATES)}
    - Required cloud migration field: `cloud_migration`
    - Required cloud migration subfields: {", ".join(CLOUD_REQUIRED_MIGRATION_FIELDS)}
    """)


def elevate(root: Path | None = None) -> None:
    root = root or Path(__file__).resolve().parents[1]
    data_dir = root / "data"
    dist_dir = root / "dist" / "copilots"
    generated_dir = root / "generated"
    copilots = load_json(data_dir / "copilots.json")

    injection_map: dict[str, dict] = {
        "version": FACTORY_VERSION,
        "generatedAt": now(),
        "runtimes": RUNTIMES,
        "copilots": {},
    }
    prompt_stats: list[dict] = []

    for copilot in copilots:
        contract = build_contract(copilot)
        cid = copilot["id"]
        base = dist_dir / cid
        shared = load_json(base / "shared" / "spec.json")
        shared.update(contract)
        shared["version"] = FACTORY_VERSION
        if is_architecture_decision_copilot(copilot):
            shared["architectureDecisionAudit"] = architecture_runtime_contract()
        if is_design_boundary_copilot(copilot):
            shared["designBoundaryAudit"] = design_runtime_contract(cid)
        if is_build_implementation_copilot(copilot):
            shared["buildImplementationAudit"] = build_runtime_contract(cid)
        if is_cloud_migration_copilot(copilot):
            shared["cloudMigrationAudit"] = cloud_runtime_contract()
        write_json(base / "shared" / "spec.json", shared)
        write_text(base / "shared" / "output_schema.json", json.dumps(contract["outputSchema"], indent=2) + "\n")
        write_text(base / "shared" / "runtime_contract.md", render_runtime_contract(copilot, contract))
        if is_architecture_decision_copilot(copilot):
            write_json(base / ARCHITECTURE_AUDIT_ARTIFACT, architecture_audit_artifact())
        if is_design_boundary_copilot(copilot):
            write_json(base / DESIGN_AUDIT_ARTIFACT, design_audit_artifact(cid))
        if is_build_implementation_copilot(copilot):
            write_json(base / BUILD_AUDIT_ARTIFACT, build_audit_artifact(copilot))
        if is_cloud_migration_copilot(copilot):
            write_json(base / CLOUD_AUDIT_ARTIFACT, cloud_audit_artifact())
        write_text(base / "README.md", render_copilot_readme(copilot, contract))

        codex = render_markdown_agent(copilot, contract, "codex")
        claude = render_markdown_agent(copilot, contract, "claude")
        github = render_markdown_agent(copilot, contract, "github-copilot")
        lang_profile = {**shared, "contract": contract}
        lang_agent = render_langchain_agent(copilot, contract)

        write_text(base / "codex" / "AGENT.md", codex)
        write_text(base / "claude" / "AGENT.md", claude)
        write_text(base / "github-copilot" / "copilot-agent.md", github)
        write_json(base / "langchain" / "agent_profile.json", lang_profile)
        write_text(base / "langchain" / "agent.py", lang_agent)

        injection_map["copilots"][cid] = {
            "name": copilot["name"],
            "family": copilot["family"],
            "sourceOfTruth": f"dist/copilots/{cid}/shared/spec.json",
            "systemPrompt": f"dist/copilots/{cid}/shared/spec.json#/systemPrompt",
            "developerPrompt": f"dist/copilots/{cid}/shared/spec.json#/developerPrompt",
            "outputSchema": f"dist/copilots/{cid}/shared/output_schema.json",
            "runtimeFiles": {
                "codex": f"dist/copilots/{cid}/codex/AGENT.md",
                "claude": f"dist/copilots/{cid}/claude/AGENT.md",
                "github-copilot": f"dist/copilots/{cid}/github-copilot/copilot-agent.md",
                "langchain": f"dist/copilots/{cid}/langchain/agent.py",
            },
            "pythonBrain": {
                "router": "tools/semantic_router.py",
                "factory": "tools/generate_copilot_factory.py",
                "qualityAudit": "tools/validate_prompt_quality.py",
            },
        }
        if is_design_boundary_copilot(copilot):
            injection_map["copilots"][cid]["designBoundaryAudit"] = design_injection_contract(cid)
        if is_build_implementation_copilot(copilot):
            injection_map["copilots"][cid]["buildImplementationAudit"] = build_injection_contract(cid)
        if is_cloud_migration_copilot(copilot):
            injection_map["copilots"][cid]["cloudMigrationAudit"] = cloud_injection_contract()
        prompt_stats.append({
            "id": cid,
            "codexChars": len(codex),
            "claudeChars": len(claude),
            "githubChars": len(github),
            "langchainChars": len(lang_agent),
            "systemPromptChars": len(contract["systemPrompt"]),
            "developerPromptChars": len(contract["developerPrompt"]),
        })

    write_json(generated_dir / "runtime-injection-map.json", injection_map)
    write_text(generated_dir / "runtime-injection-map.md", render_injection_map_md(injection_map))
    write_text(generated_dir / "python-brain-report.md", render_python_brain_report(copilots))
    write_json(generated_dir / "prompt-size-baseline.json", {
        "version": FACTORY_VERSION,
        "generatedAt": now(),
        "stats": prompt_stats,
    })
    write_text(root / "README.md", render_root_readme())
    write_text(root / "OPERATING_SYSTEM.md", render_operating_system())
    write_json(root / "factory.config.json", {
        "version": FACTORY_VERSION,
        "brain": "python_deterministic_orchestrator",
        "llm_role": "sparse_cerebellum_for_code_reasoning_architecture_tradeoffs_and_final_copy",
        "copilots": len(copilots),
        "runtimes": RUNTIMES,
        "factoryAgents": len(load_json(data_dir / "agent_roster.json")),
        "qualityGate": {
            "structure": "python tools/validate_copilot_factory.py",
            "promptDepth": "python tools/validate_prompt_quality.py",
            "runtimeEquivalence": "python tools/validate_runtime_equivalence.py",
            "fullRun": "python tools/run_factory.py",
        },
        "controlRoom": control_room_contract(),
        "runtimeInjection": "generated/runtime-injection-map.json",
        "codexLoop": {
            "tasksFile": "tasks.json",
            "freePromptFile": "factory-prompt.md",
            "workspaceSettings": ".vscode/settings.json",
        },
    })


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


def build_contract(copilot: dict) -> dict:
    family = FAMILY_RULES[copilot["family"]]
    stack_lines = stack_rules(copilot)
    playbook = phase_playbook(copilot)
    outputs = output_schema(copilot)
    system = render_system_prompt(copilot, family, stack_lines)
    developer = render_developer_prompt(copilot, family, stack_lines)
    return {
        "version": FACTORY_VERSION,
        "systemPrompt": system,
        "developerPrompt": developer,
        "runtimeInjection": {
            "identity": copilot["name"],
            "copilotId": copilot["id"],
            "family": copilot["family"],
            "connectors": copilot["connectors"],
            "envKeys": copilot["env_keys"],
            "sourceOfTruth": "../shared/spec.json",
            "routingMode": "python_first_llm_sparse",
            "stateRule": "Every output must cite the local catalog, repository evidence, or the explicit user request.",
        },
        "sdlcPlaybook": playbook,
        "outputSchema": outputs,
        "qualityRubric": quality_rubric(copilot, family),
        "pythonBrain": {
            "cheapDeterministicWork": [
                "catalog validation",
                "semantic routing",
                "MCP connector declaration checks",
                "SDLC phase matrix checks",
                "artifact completeness checks",
                "prompt depth and schema validation",
            ],
            "llmEscalationAllowedFor": [
                "non-trivial code edits",
                "architecture trade-off judgement",
                "ambiguous legacy behavior synthesis",
                "final human-facing report polish after evidence exists",
            ],
            "llmEscalationForbiddenFor": [
                "counting files",
                "routing by explicit stack tags",
                "checking missing generated artifacts",
                "validating schema keys",
                "secret scanning",
            ],
        },
        "committee": committee_contract(copilot),
    }


def render_system_prompt(copilot: dict, family: dict, stack_lines: list[str]) -> str:
    return clean_template(f"""\
    You are {copilot['name']}, a production-grade SDLC copilot.

    Mission:
    {family['mission']}

    Scope:
    - Primary function: {copilot['function']}
    - Runtime family: {copilot['family']}
    - Stacks: {', '.join(copilot['stacks'])}
    - SDLC phases: {', '.join(copilot['sdlc_phases'])}
    - Declared connectors: {', '.join(copilot['connectors'])}
    - Declared environment variable names: {', '.join(copilot['env_keys'])}

    Non-negotiable behavior:
    1. Start from evidence. If a repository, issue, PR, build log, SonarQube issue or catalog is available, inspect that before giving guidance.
    2. Python is the deterministic brain. Use Python tools for routing, catalog checks, schema checks, prompt checks, matrix generation and repetitive audits. Use an LLM only for judgement-heavy synthesis.
    3. Do not store secrets, invent connector access, fake CI results or pretend to have inspected files that were not inspected.
    4. Keep work scoped to the selected copilot mission. If another copilot owns the problem, hand off with an evidence pack instead of expanding silently.
    5. Every recommendation must include a next action, owner, evidence source and validation method.
    6. Prefer product-grade outputs over chatty advice: scorecards, ADR reviews, test matrices, patch plans, routing decisions, remediation backlogs or runbooks.

    Stack rules:
    {as_bullets(stack_lines)}

    Main risk to prevent:
    {family['risk']}

    Primary quality gate:
    {family['primary_gate']}
    """)


def render_developer_prompt(copilot: dict, family: dict, stack_lines: list[str]) -> str:
    outputs = "\n".join(f"- {item}: must be concrete, evidence-backed and machine-checkable when possible." for item in copilot["outputs"])
    phases = "\n".join(f"- {phase}: {phase_instruction(phase)}" for phase in copilot["sdlc_phases"])
    return clean_template(f"""\
    Developer operating instructions for {copilot['name']}:

    Execution order:
    1. Intake: restate the requested outcome in one precise sentence.
    2. Route: confirm why this copilot is selected and name any secondary copilots that should be consulted.
    3. Evidence: collect the smallest useful set of files, logs, catalog entries or connector outputs.
    4. Deterministic pass: use Python or structured checks for anything countable or schema-like.
    5. Judgement pass: use the LLM only to interpret trade-offs, synthesize risks or design non-trivial patches.
    6. Output: return the expected artifact in the declared schema, then a short human summary.
    7. Verification: include exact commands, checks or acceptance criteria.
    8. Handoff: if blocked, provide the evidence pack and stop condition.

    Expected outputs:
    {outputs}

    Phase instructions:
    {phases}

    Connector discipline:
    - Connector declarations are not credentials. They are capability contracts.
    - Required connectors for this copilot: {', '.join(copilot['connectors'])}
    - Environment variable names only: {', '.join(copilot['env_keys'])}
    - If a connector is unavailable, produce an offline audit using local files and mark connector evidence as pending.

    Cost discipline:
    - Python handles discovery, scoring, diff summaries, schema checks and regression matrices.
    - Codex or Claude handles only the narrow judgement slice that Python cannot decide.
    - Never send an entire repository to an LLM when a file list, symbol graph or targeted excerpt is enough.

    Failure discipline:
    - If evidence contradicts the user request, state the contradiction plainly.
    - If a task is too broad, split it into phase-gated batches.
    - If a proposed change touches security, release, credentials or production connectors, require explicit human approval.
    """)


def render_markdown_agent(copilot: dict, contract: dict, runtime: str) -> str:
    rule = RUNTIME_RULES[runtime]
    output_schema = markdown_output_schema(copilot, contract)
    runtime_specific = runtime_specific_protocol(runtime, copilot)
    architecture_section = architecture_runtime_section(copilot)
    design_section = design_runtime_section(copilot)
    build_section = build_runtime_section(copilot)
    cloud_section = cloud_runtime_section(copilot)
    sdlc_rows = "\n".join(
        f"| {item['phase']} | {item['goal']} | {item['pythonCheck']} | {item['exitEvidence']} |"
        for item in contract["sdlcPlaybook"]
    )
    rubric_rows = "\n".join(
        f"| {item['criterion']} | {item['passSignal']} | {item['failSignal']} |"
        for item in contract["qualityRubric"]
    )
    return clean_template(f"""\
    # {copilot['name']} - {rule['name']} Agent V2

    ## Runtime Injection

    - Copilot ID: `{copilot['id']}`
    - Runtime: `{runtime}`
    - Source of truth: `../shared/spec.json`
    - Output schema: `../shared/output_schema.json`
    - Connectors: {', '.join(copilot['connectors'])}
    - Env var names: {', '.join(copilot['env_keys'])}
    - Python router: `../../../tools/semantic_router.py`
    - Prompt quality gate: `../../../tools/validate_prompt_quality.py`

    ## System Prompt

    {contract['systemPrompt']}

    ## Developer Prompt

    {contract['developerPrompt']}
    {architecture_section}
    {design_section}
    {build_section}
    {cloud_section}

    ## Execution Protocol

    1. Classify the request by SDLC phase, stack, repository area, risk and expected artifact.
    2. Load `../shared/spec.json` and verify the selected copilot still matches the request.
    3. Run or mentally apply the Python-first route: catalog lookup, semantic score, connector requirement check, artifact completeness check.
    4. Collect evidence before generating advice. Evidence can be file paths, line references, CI logs, Sonar issues, issue/PR context, architecture docs or explicit user constraints.
    5. Produce one of the declared outputs, not an open-ended essay.
    6. Include validation commands or acceptance checks. If no command exists, define a deterministic review checklist.
    7. Record limitations and handoff needs in a compact form.

    ## Python Brain Contract

    Python owns all cheap repeatable work. This agent may request or run deterministic scripts for:

    - Routing and copilot selection.
    - Prompt depth validation.
    - Runtime artifact completeness.
    - SDLC matrix generation.
    - Connector and environment variable declaration checks.
    - Test matrix expansion, including pairwise and negative cases where relevant.
    - Secret pattern scanning.

    The LLM layer is used only for interpretation, code changes, architectural trade-off reasoning and final human-readable synthesis. If a deterministic Python check can answer the question, use that path first.

    ## SDLC Playbook

    | Phase | Goal | Python Check | Exit Evidence |
    |---|---|---|---|
    {sdlc_rows}

    ## Evidence Gates

    - Gate 1: The selected copilot must match stack, phase or output tags.
    - Gate 2: Every material claim must cite file, log, catalog, connector output or explicit user instruction.
    - Gate 3: Every proposed change must name affected files or modules.
    - Gate 4: Every plan must name a validation method.
    - Gate 5: Every blocker must include the smallest missing input needed to proceed.

    ## Outputs

    The preferred machine-readable shape is:

    ```json
    {output_schema}
    ```

    Human-facing responses should follow this order:

    1. Decision or finding.
    2. Evidence.
    3. Action plan or patch plan.
    4. Validation.
    5. Handoff, only if needed.

    ## Quality Rubric

    | Criterion | Pass Signal | Fail Signal |
    |---|---|---|
    {rubric_rows}

    ## Runtime Specific Protocol

    {runtime_specific}

    Runtime focus: {rule['focus']}

    Runtime avoid: {rule['avoid']}

    ## Escalation

    Escalate to another copilot when:

    - The request enters a phase outside `{copilot['name']}` ownership.
    - A connector is required but unavailable and the missing evidence changes the decision.
    - A production, credential, security, release or irreversible action is requested.
    - The confidence score is low after catalog routing.

    Escalation packet:

    ```json
    {{
      "fromCopilot": "{copilot['id']}",
      "reason": "why this copilot cannot finish alone",
      "evidence": ["paths, logs, ids, issue links or catalog refs"],
      "recommendedCopilots": ["target ids"],
      "stopCondition": "what must be true before continuing"
    }}
    ```

    ## Committee Handoff

    This copilot participates in the factory committee. It must leave enough structure for QA, Architecture, DevOps and Release auditors to verify the result without re-reading the whole conversation.
    """)


def markdown_output_schema(copilot: dict, contract: dict) -> str:
    if not is_cloud_migration_copilot(copilot):
        return json.dumps(contract["outputSchema"], indent=2)
    return json.dumps(
        {
            "$ref": "../shared/output_schema.json",
            "required": CLOUD_REQUIRED_OUTPUT_FIELDS,
            "cloud_migration_required": CLOUD_REQUIRED_MIGRATION_FIELDS,
            "migration_increment_required": [
                "increment_id",
                "source_evidence",
                "target_capability",
                "modernization_action",
                "validation_command",
                "rollback_path",
            ],
        },
        indent=2,
    )


def runtime_specific_protocol(runtime: str, copilot: dict) -> str:
    if runtime == "codex":
        return as_bullets(
            [
                "Inspect local files with fast search before editing.",
                "Use scoped patches and preserve unrelated user changes.",
                "Run `python tools/validate_copilot_factory.py`, `python tools/validate_prompt_quality.py` and `python tools/validate_runtime_equivalence.py` after prompt or factory changes.",
                "When implementing stack changes, run the nearest existing test or explain why it cannot run.",
                "Final responses should be concise and include exact files changed.",
            ]
        ) + "\n"
    if runtime == "claude":
        return as_bullets(
            [
                "Use long context to compare evidence packs and produce structured review artifacts.",
                "If tool access is missing, do not pretend to inspect files; request an evidence bundle or mark assumptions.",
                "Prefer tables for trade-offs, risks and decisions.",
                "Produce executor-ready handoffs for Codex or GitHub Copilot when code edits are needed.",
            ]
        ) + "\n"
    return as_bullets(
        [
            "Start from GitHub issue, PR, review thread, branch, workflow or check evidence.",
            "Respect repository branch policy and review status.",
            "Use MCP connector declarations only as capability contracts until credentials are configured.",
            "Keep PR comments actionable: file, line, risk, fix, test.",
            "If SonarQube is declared, correlate issue keys with code paths and remediation priority.",
        ]
    ) + "\n"


def render_langchain_agent(copilot: dict, contract: dict) -> str:
    class_name = "".join(part.title() for part in copilot["id"].split("_")) + "Agent"
    profile = {
        "id": copilot["id"],
        "name": copilot["name"],
        "family": copilot["family"],
        "function": copilot["function"],
        "connectors": copilot["connectors"],
        "env_keys": copilot["env_keys"],
        "stacks": copilot["stacks"],
        "sdlc_phases": copilot["sdlc_phases"],
        "outputs": copilot["outputs"],
        "version": FACTORY_VERSION,
    }
    profile_json = json.dumps(profile, sort_keys=True)
    output_schema_json = repr(contract["outputSchema"])
    sdlc_playbook_json = json.dumps(contract["sdlcPlaybook"], sort_keys=True)
    quality_rubric_json = json.dumps(contract["qualityRubric"], sort_keys=True)
    architecture_decision_json = (
        json.dumps(architecture_runtime_contract(), sort_keys=True)
        if is_architecture_decision_copilot(copilot)
        else "None"
    )
    design_boundary_json = (
        json.dumps(design_runtime_contract(copilot["id"]), sort_keys=True)
        if is_design_boundary_copilot(copilot)
        else "None"
    )
    build_implementation_json = (
        json.dumps(build_runtime_contract(copilot["id"]), sort_keys=True)
        if is_build_implementation_copilot(copilot)
        else "None"
    )
    return clean_template(f'''\
    """LangChain-compatible Python brain for {copilot['name']}.

    This file intentionally has no hard dependency on langchain. The class can be
    wrapped as a Tool, Runnable or AgentExecutor adapter later. Python owns routing,
    audit, schema checks and prompt rendering; LLM calls should receive only the
    `render_prompt()` result plus a small evidence bundle.
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


    PROFILE = {profile_json}
    SYSTEM_PROMPT = {json.dumps(contract['systemPrompt'])}
    DEVELOPER_PROMPT = {json.dumps(contract['developerPrompt'])}
    OUTPUT_SCHEMA = {output_schema_json}
    SDLC_PLAYBOOK = {sdlc_playbook_json}
    QUALITY_RUBRIC = {quality_rubric_json}
    ARCHITECTURE_DECISION_AUDIT = {architecture_decision_json}
    DESIGN_BOUNDARY_AUDIT = {design_boundary_json}
    BUILD_IMPLEMENTATION_AUDIT = {build_implementation_json}


    @dataclass
    class AuditResult:
        pass_: bool
        score: int
        issues: list[str]
        evidence_needed: list[str]

        def to_dict(self) -> dict[str, Any]:
            return {{
                "pass": self.pass_,
                "score": self.score,
                "issues": self.issues,
                "evidence_needed": self.evidence_needed,
            }}


    class {class_name}:
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
            architecture_words = {{"architecture", "arquitectura", "principles", "principios", "adr", "decision", "quality", "calidad", "technical", "tecnica", "tecnico"}}
            design_words = {{"design", "diseno", "domain", "dominio", "boundary", "boundaries", "limites", "contract", "contracts", "contratos", "handoff", "traspaso"}}
            build_words = {{"build", "implementation", "implementacion", "plan", "patch", "stack", "rules", "reglas", "affected", "files", "archivos", "rollback", "validation", "tests"}}
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
            plan = {{
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
                "audit": audit,
            }}
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
            user_payload = {{
                "request": safe_request,
                "profile": self.profile,
                "plan": plan,
                "output_schema": OUTPUT_SCHEMA,
                "sdlc_playbook": SDLC_PLAYBOOK,
                "evidence": safe_evidence,
            }}
            return [
                {{"role": "system", "content": SYSTEM_PROMPT}},
                {{"role": "developer", "content": DEVELOPER_PROMPT}},
                {{"role": "user", "content": json.dumps(user_payload, indent=2)}},
            ]


    def build_agent() -> {class_name}:
        return {class_name}()


    if __name__ == "__main__":
        import sys
        agent = build_agent()
        request = " ".join(sys.argv[1:]) or "route and audit this request"
        print(json.dumps(agent.plan(request, {{"source_refs": [], "validation": []}}), indent=2))
    ''')


def phase_playbook(copilot: dict) -> list[dict]:
    phases = copilot["sdlc_phases"] or ["discovery"]
    return [
        {
            "phase": phase,
            "goal": phase_instruction(phase),
            "pythonCheck": python_check_for_phase(phase),
            "exitEvidence": exit_evidence_for_phase(phase, copilot),
        }
        for phase in phases
    ]


def output_schema(copilot: dict) -> dict:
    required = ["copilot_id", "decision", "evidence", "actions", "validation", "risks"]
    evidence_schema = {
        "type": "array",
        "items": {
            "type": "object",
            "required": ["kind", "ref", "summary"],
            "properties": {
                "kind": {"type": "string"},
                "ref": {"type": "string"},
                "summary": {"type": "string"},
            },
        },
    }
    handoff_schema = {"type": "object"}
    implementation_schema = {"type": "object"}
    cloud_migration_schema = {"type": "object"}
    if is_design_boundary_copilot(copilot):
        required.append("handoff")
        evidence_schema = {
            **evidence_schema,
            "minItems": len(DESIGN_REQUIRED_EVIDENCE),
            "allOf": [
                {
                    "contains": {
                        "type": "object",
                        "required": ["kind"],
                        "properties": {"kind": {"const": evidence_kind}},
                    }
                }
                for evidence_kind in DESIGN_REQUIRED_EVIDENCE
            ],
            "items": {
                **evidence_schema["items"],
                "properties": {
                    **evidence_schema["items"]["properties"],
                    "kind": {"enum": DESIGN_REQUIRED_EVIDENCE},
                },
                "additionalProperties": False,
            },
        }
        handoff_schema = {
            "type": "object",
            "required": DESIGN_REQUIRED_HANDOFF_FIELDS,
            "additionalProperties": False,
            "properties": {
                "next_owner": {"type": "string", "minLength": 1},
                "next_runtime": {"enum": RUNTIMES},
                "next_action": {"type": "string", "minLength": 1},
                "excluded_scope": {
                    "type": "array",
                    "minItems": 1,
                    "items": {"type": "string", "minLength": 1},
                },
                "dependency_direction": {"type": "string", "minLength": 1},
                "evidence_pack": {
                    "type": "array",
                    "minItems": 1,
                    "items": {"type": "string", "minLength": 1},
                },
                "validation_command": {"type": "string", "minLength": 1},
                "stop_condition": {"type": "string", "minLength": 1},
            },
        }
    if is_build_implementation_copilot(copilot):
        required.append("implementation")
        build_contains = [
            {
                "contains": {
                    "type": "object",
                    "required": ["kind"],
                    "properties": {"kind": {"const": evidence_kind}},
                }
            }
            for evidence_kind in BUILD_REQUIRED_EVIDENCE
        ]
        current_kinds = (
            evidence_schema.get("items", {})
            .get("properties", {})
            .get("kind", {})
            .get("enum", [])
        )
        evidence_kinds = list(dict.fromkeys([*current_kinds, *BUILD_REQUIRED_EVIDENCE]))
        evidence_schema = {
            **evidence_schema,
            "minItems": max(
                evidence_schema.get("minItems", 0),
                len(evidence_kinds),
            ),
            "allOf": [*evidence_schema.get("allOf", []), *build_contains],
            "items": {
                **evidence_schema["items"],
                "properties": {
                    **evidence_schema["items"]["properties"],
                    "kind": {"enum": evidence_kinds},
                },
                "additionalProperties": False,
            },
        }
        implementation_schema = {
            "type": "object",
            "required": BUILD_REQUIRED_IMPLEMENTATION_FIELDS,
            "additionalProperties": False,
            "properties": {
                "target_stack": {"type": "string", "minLength": 1},
                "affected_files": {
                    "type": "array",
                    "minItems": 1,
                    "items": {"type": "string", "minLength": 1},
                },
                "plan_steps": {
                    "type": "array",
                    "minItems": 1,
                    "items": {"type": "string", "minLength": 1},
                },
                "stack_rules_checked": {
                    "type": "array",
                    "minItems": 1,
                    "items": {"type": "string", "minLength": 1},
                },
                "validation_commands": {
                    "type": "array",
                    "minItems": 1,
                    "items": {"type": "string", "minLength": 1},
                },
                "rollback_plan": {"type": "string", "minLength": 1},
                "out_of_scope": {
                    "type": "array",
                    "minItems": 1,
                    "items": {"type": "string", "minLength": 1},
                },
                "evidence_pack": {
                    "type": "array",
                    "minItems": 1,
                    "items": {"type": "string", "minLength": 1},
                },
            },
        }
    if is_cloud_migration_copilot(copilot):
        required.append("cloud_migration")
        cloud_contains = [
            {
                "contains": {
                    "type": "object",
                    "required": ["kind"],
                    "properties": {"kind": {"const": evidence_kind}},
                }
            }
            for evidence_kind in CLOUD_REQUIRED_EVIDENCE
        ]
        current_kinds = (
            evidence_schema.get("items", {})
            .get("properties", {})
            .get("kind", {})
            .get("enum", [])
        )
        evidence_kinds = list(dict.fromkeys([*current_kinds, *CLOUD_REQUIRED_EVIDENCE]))
        evidence_schema = {
            **evidence_schema,
            "minItems": max(
                evidence_schema.get("minItems", 0),
                len(evidence_kinds),
            ),
            "allOf": [*evidence_schema.get("allOf", []), *cloud_contains],
            "items": {
                **evidence_schema["items"],
                "properties": {
                    **evidence_schema["items"]["properties"],
                    "kind": {"enum": evidence_kinds},
                },
                "additionalProperties": False,
            },
        }
        migration_increment_schema = {
            "type": "object",
            "required": [
                "increment_id",
                "source_evidence",
                "target_capability",
                "modernization_action",
                "validation_command",
                "rollback_path",
            ],
            "additionalProperties": False,
        }
        cloud_migration_schema = {
            "type": "object",
            "required": CLOUD_REQUIRED_MIGRATION_FIELDS,
            "additionalProperties": False,
            "properties": {
                "current_state_refs": {"type": "array"},
                "target_platform": {"type": "object"},
                "migration_increments": {
                    "type": "array",
                    "minItems": 3,
                    "items": migration_increment_schema,
                },
                "modernization_actions": {"type": "array"},
                "data_network_security_impacts": {"type": "array"},
                "rollback_and_parallel_run": {"type": "string"},
                "validation_commands": {"type": "array"},
                "evidence_pack": {"type": "array"},
                "out_of_scope": {"type": "array"},
            },
        }
    action_item_schema = {
        "type": "object",
        "required": ["owner", "action", "scope"],
        "properties": {
            "owner": {"type": "string"},
            "action": {"type": "string"},
            "scope": {"type": "string"},
        },
    }
    if is_cloud_migration_copilot(copilot):
        action_item_schema["additionalProperties"] = False

    output_schema = {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "title": f"{copilot['name']} Output Contract",
        "type": "object",
        "required": required,
        "properties": {
            "copilot_id": {"const": copilot["id"]},
            "decision": {"type": "string"},
            "confidence": {"type": "integer", "minimum": 0, "maximum": 100},
            "phase": {"enum": copilot["sdlc_phases"]},
            "expected_outputs": {"type": "array", "items": {"enum": copilot["outputs"]}},
            "evidence": evidence_schema,
            "actions": {
                "type": "array",
                "items": action_item_schema,
            },
            "validation": {"type": "array", "items": {"type": "string"}},
            "risks": {"type": "array", "items": {"type": "string"}},
            "handoff": handoff_schema,
            "implementation": implementation_schema,
            "cloud_migration": cloud_migration_schema,
        },
    }
    if is_cloud_migration_copilot(copilot):
        output_schema["additionalProperties"] = False
    return output_schema


def quality_rubric(copilot: dict, family: dict) -> list[dict]:
    return [
        {
            "criterion": "Evidence first",
            "passSignal": "Claims cite files, logs, catalog entries, connector outputs or explicit user constraints.",
            "failSignal": "Advice appears before evidence or invents repository state.",
        },
        {
            "criterion": "Python first",
            "passSignal": "Deterministic checks are delegated to scripts or structured validation.",
            "failSignal": "LLM is asked to count, route, validate keys or scan secrets.",
        },
        {
            "criterion": "Output contract",
            "passSignal": f"Produces one of: {', '.join(copilot['outputs'])}.",
            "failSignal": "Returns generic consultancy text with no artifact.",
        },
        {
            "criterion": "Scope control",
            "passSignal": "Names affected phases, files, connectors and owners.",
            "failSignal": "Expands beyond copilot mission without handoff.",
        },
        {
            "criterion": "Primary gate",
            "passSignal": family["primary_gate"],
            "failSignal": "Moves forward without the primary quality gate.",
        },
    ]


def committee_contract(copilot: dict) -> dict:
    return {
        "entryCriteria": [
            "request classified",
            "copilot route justified",
            "evidence pack started",
        ],
        "exitCriteria": [
            "declared output emitted",
            "validation named",
            "risks and handoff recorded",
        ],
        "peerAuditors": peer_auditors(copilot),
    }


def peer_auditors(copilot: dict) -> list[str]:
    peers = ["qa_general", "devex"]
    if "architecture" in copilot["sdlc_phases"] or copilot["family"] in {"cloud", "core"}:
        peers.append("aida_architecture")
    if "devops" in copilot["sdlc_phases"] or copilot["family"] == "devops":
        peers.append("cicd")
    if "security" in copilot["sdlc_phases"]:
        peers.append("sonarqube_remediation")
    return sorted(set(peer for peer in peers if peer != copilot["id"]))


def stack_rules(copilot: dict) -> list[str]:
    rules: list[str] = []
    for stack in copilot["stacks"]:
        rules.extend(STACK_RULES.get(stack, [f"Apply repository evidence before changing {stack} artifacts."]))
    return list(dict.fromkeys(rules))


def phase_instruction(phase: str) -> str:
    return {
        "discovery": "Find source systems, owners, constraints, risks and existing documents.",
        "as_is": "Document current behavior, interfaces, data flows and business rules before changing anything.",
        "architecture": "Evaluate decisions, boundaries, trade-offs, ADRs, risks and target principles.",
        "design": "Define contracts, modules, UX/API boundaries, data shape and acceptance criteria.",
        "build": "Create scoped implementation plans or patches with affected files and rollback notes.",
        "test": "Turn requirements and code risks into unit, integration, negative and regression tests.",
        "security": "Check secrets, auth, data exposure, dependency risk and least-privilege connector use.",
        "devops": "Inspect pipelines, logs, caches, environments, build reproducibility and release safety.",
        "cloud": "Plan migration increments, platform target, data movement, networking and operations.",
        "release": "Prepare versioning, changelog, risk signoff, deployment and rollback evidence.",
        "operate": "Define monitoring, incidents, runbooks, ownership and continuous improvement loops.",
    }.get(phase, "Produce evidence-backed work for this SDLC phase.")


def python_check_for_phase(phase: str) -> str:
    return {
        "discovery": "file inventory, connector declarations, source map generation",
        "as_is": "schema extraction, endpoint inventory, dependency graph",
        "architecture": "ADR presence, dependency direction, module boundary matrix",
        "design": "contract schema check, acceptance criteria completeness",
        "build": "affected-file diff summary, lint/test command discovery",
        "test": "test matrix expansion, pairwise/negative case generation",
        "security": "secret pattern scan, dependency policy check, connector least-privilege check",
        "devops": "workflow YAML parse, failed job log summarization",
        "cloud": "migration inventory, platform capability matrix",
        "release": "manifest, changelog and version compatibility check",
        "operate": "runbook and alert coverage check",
    }.get(phase, "catalog and schema validation")


def exit_evidence_for_phase(phase: str, copilot: dict) -> str:
    return f"{phase} artifact plus one validation signal for {copilot['name']}"


def render_runtime_contract(copilot: dict, contract: dict) -> str:
    architecture_section = architecture_runtime_section(copilot)
    design_section = design_runtime_section(copilot)
    build_section = build_runtime_section(copilot)
    cloud_section = cloud_runtime_section(copilot)
    return clean_template(f"""\
    # Runtime Contract - {copilot['name']}

    This file is the human-readable contract shared by Codex, Claude, GitHub Copilot Agents and LangChain.

    ## Identity

    - ID: `{copilot['id']}`
    - Family: `{copilot['family']}`
    - Function: {copilot['function']}

    ## System Prompt

    {contract['systemPrompt']}

    ## Developer Prompt

    {contract['developerPrompt']}

    ## Output Schema

    See `output_schema.json`.
    {architecture_section}
    {design_section}
    {build_section}
    {cloud_section}
    """)


def render_copilot_readme(copilot: dict, contract: dict) -> str:
    architecture_section = architecture_runtime_section(copilot)
    design_section = design_runtime_section(copilot)
    build_section = build_runtime_section(copilot)
    cloud_section = cloud_runtime_section(copilot)
    return clean_template(f"""\
    # {copilot['name']}

    Product-grade copilot package generated by `{FACTORY_VERSION}`.

    ## Purpose

    {copilot['function']}

    ## Runtime Files

    - Codex: `codex/AGENT.md`
    - Claude: `claude/AGENT.md`
    - GitHub Copilot Agents: `github-copilot/copilot-agent.md`
    - LangChain/Python: `langchain/agent.py`
    - Shared spec: `shared/spec.json`
    - Output schema: `shared/output_schema.json`

    ## Python Brain

    Python owns routing, validation, audit matrices and prompt quality checks. The LLM runtime receives only the current request, the evidence pack and this copilot contract.

    ## Peer Auditors

    {as_bullets(contract['committee']['peerAuditors'])}
    {architecture_section}
    {design_section}
    {build_section}
    {cloud_section}
    """)


def render_root_readme() -> str:
    return clean_template(f"""\
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
    - `dist/copilots/journey_to_cloud/shared/cloud_migration_audit.json`: Cloud Auditor contract for migration, target platform and modernization increments.
    - `dist/copilots/<copilot>/codex/AGENT.md`: Codex injection.
    - `dist/copilots/<copilot>/claude/AGENT.md`: Claude injection.
    - `dist/copilots/<copilot>/github-copilot/copilot-agent.md`: GitHub Copilot profile.
    - `dist/copilots/<copilot>/langchain/agent.py`: Python/LangChain brain.
    - `generated/factory-audit.json`: factory-level pass/fail summary, including Build and Cloud Auditor evidence.
    - `generated/runtime-injection-map.json`: where each prompt and runtime contract lives.
    - `generated/prompt-quality-report.*`: prompt-depth QA gate.
    - `generated/runtime-equivalence-report.*`: cross-runtime drift gate.

    ## Control Room Director Contract

    `factory_agent_01_director` is the run owner. Its mission is encoded as a machine-readable control contract in `factory.config.json` under `controlRoom`, and as the first queue gate in `tasks.json`.

    The director cannot mark a run done unless these artifacts exist and agree:

    - State lock evidence: `.codex-loop/run.lock.json` exists, has the required fields (`id`, `pid`, `workspace`, `startedAt`, `heartbeatAt`, `mode`), matches this workspace and has a heartbeat that does not precede the start time.
    - Gate evidence: `generated/validation-report.json`, `generated/prompt-quality-report.json` and `generated/runtime-equivalence-report.json` are the truth sources for structure, prompt depth and runtime drift.
    - Scope evidence: task files must stay inside the declared task file list or documented factory roots; product code belongs under `products/<slug>/` with registry updates when a product is created.
    - Equivalence evidence: `dist/copilots/<copilot>/shared/spec.json` remains canonical, with Codex, Claude, GitHub Copilot and LangChain treated as runtime adapters over that spec.
    - Cost evidence: deterministic Python gates run before any sparse LLM judgement, so traceability comes from generated reports instead of repeated prompt expansion.
    """)


def render_operating_system() -> str:
    return clean_template(f"""\
    # Copilot Factory Operating System

    ## Mission

    Create equivalent, auditable copilots for Codex, Claude, GitHub Copilot Agents and LangChain while keeping token cost low. The Factory Director owns the whole run, keeps gates honest and prevents scope drift through verifiable state locks, report gates and runtime-equivalence evidence.

    ## Abstraction Layers

    1. Catalog Brain: Python owns copilot definitions, connectors, env names, outputs and SDLC phases.
    2. Semantic Brain: Python routes requests using stack tags, phase tags, connector requirements and output contracts.
    3. Prompt Brain: Python renders system/developer prompts from shared copilot specs, so runtime prompts do not drift.
    4. Runtime Adapters: Codex, Claude, GitHub Copilot and LangChain receive the same operating contract in runtime-native form.
    5. SDLC Committee: Discovery, Architecture, Design, Build, Test, Security, DevOps, Cloud, Release and Operate auditors can verify each artifact.
    6. LLM Cerebellum: Codex/Claude are used only for narrow judgement, code edits and final synthesis after Python prepared the evidence.

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


def render_injection_map_md(injection_map: dict) -> str:
    rows = []
    for cid, item in injection_map["copilots"].items():
        rows.append(
            f"| {cid} | {item['name']} | {item['runtimeFiles']['codex']} | {item['runtimeFiles']['langchain']} |"
        )
    return "# Runtime Injection Map\n\n| ID | Name | Codex | LangChain |\n|---|---|---|---|\n" + "\n".join(rows) + "\n"


def render_python_brain_report(copilots: list[dict]) -> str:
    rows = []
    for copilot in copilots:
        rows.append(
            f"| {copilot['id']} | {', '.join(copilot['sdlc_phases'])} | {', '.join(copilot['outputs'])} |"
        )
    return clean_template(f"""\
    # Python Brain Report

    Python is the orchestrator for this factory. It generates prompt contracts, routes work, validates prompt depth and emits schemas.

    ## Cheap Work Owned By Python

    - Catalog generation and normalization.
    - Semantic routing.
    - Prompt quality audit.
    - Runtime artifact completeness.
    - SDLC phase matrix.
    - Output schema generation.
    - Connector/env declaration validation.

    ## Copilot Contracts

    | ID | SDLC Phases | Outputs |
    |---|---|---|
    {chr(10).join(rows)}
    """)


def as_bullets(items: list[str]) -> str:
    return "\n".join(f"- {item}" for item in items)


def clean_template(text: str) -> str:
    lines = text.strip("\n").splitlines()
    cleaned = [line[4:] if line.startswith("    ") else line for line in lines]
    return "\n".join(cleaned).rstrip() + "\n"


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data) -> None:
    write_text(path, json.dumps(data, indent=2) + "\n")


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


if __name__ == "__main__":
    elevate()
