# Output Topology Frontier Report

Generated: 2026-05-05T19:37:33.728Z
Workspace: c:\Users\abaratas\Desktop\CARPETA PROYECTOS\TEST CODEX\NuevoProyecto
Autonomous ready: yes
Score: 901/1000 (A)

## Topology

- Output root: products
- Registry: .codex-loop/factory/project-registry.json
- Registry exists: false
- Registry parseable: true
- Registry product count: 0

## productFolders

- None.

## registryPaths

- None.

## duplicateSlugs

- None.

## unsafeRegistryPaths

- None.

## rootLevelProjectFiles

- None.

## Gaps

- unsafe-output-root: controlled
  Mitigation: Use a dedicated root such as products/ for portfolio products.
- missing-project-registry: controlled
  Mitigation: .codex-loop/factory/project-registry.json is the source of truth for product slug, path, status and verification.
- slug-or-path-collision: controlled
  Mitigation: Every product needs a unique kebab-case slug and a path under the configured output root.
- root-product-pollution: controlled
  Mitigation: Keep product-specific apps under products/<slug>/; root is for orchestration/shared docs only.

## Raw JSON

```json
{
  "generatedAt": "2026-05-05T19:37:33.728Z",
  "workspace": "c:\\Users\\abaratas\\Desktop\\CARPETA PROYECTOS\\TEST CODEX\\NuevoProyecto",
  "autonomousReady": true,
  "summary": {
    "totalScore": 901,
    "maxScore": 1000,
    "grade": "A",
    "criticalFailures": 0,
    "majorFailures": 1,
    "warnings": 18
  },
  "outputGaps": [
    {
      "id": "unsafe-output-root",
      "status": "controlled",
      "mitigation": "Use a dedicated root such as products/ for portfolio products."
    },
    {
      "id": "missing-project-registry",
      "status": "controlled",
      "mitigation": ".codex-loop/factory/project-registry.json is the source of truth for product slug, path, status and verification."
    },
    {
      "id": "slug-or-path-collision",
      "status": "controlled",
      "mitigation": "Every product needs a unique kebab-case slug and a path under the configured output root."
    },
    {
      "id": "root-product-pollution",
      "status": "controlled",
      "mitigation": "Keep product-specific apps under products/<slug>/; root is for orchestration/shared docs only."
    }
  ],
  "topology": {
    "score": 10,
    "maxScore": 10,
    "outputRoot": "products",
    "outputRootSafe": true,
    "registryPath": ".codex-loop/factory/project-registry.json",
    "registryExists": false,
    "registryParseable": true,
    "registryProductCount": 0,
    "registryPaths": [],
    "productFolders": [],
    "duplicateSlugs": [],
    "unsafeRegistryPaths": [],
    "rootLevelProjectFiles": [],
    "warnings": []
  }
}
```
