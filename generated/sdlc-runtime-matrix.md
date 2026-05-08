# SDLC x Copilot x Runtime Matrix

Mission: Maintains the SDLC x Copilot x Runtime matrix.

Policy version: sdlc-copilot-runtime-matrix-1.0

Summary:

- Copilots: 18
- Phases: 11 (discovery, build, test, release, architecture, design, as_is, operate, devops, security, cloud)
- Runtimes: codex, claude, github-copilot, langchain
- Matrix cells: 204 / 204
- Trace ledger entries: 51 / 51
- Trace ledger digest: `58f56c6ff3b6cec65f1a00bc8c75630e9caa02e76cee19ec4b3a8a62902decbf`
- Missing runtime files: 0
- Max unexplained drift: 0
- Prompt bodies stored: False
- Cell equivalence pass: True (204 / 204)

Source artifacts:

- Catalog: `data/copilots.json`
- Runtime map: `generated/runtime-injection-map.json`
- Factory validation: `generated/validation-report.json#/sdlcRuntimeMatrix`
- Prompt quality: `generated/prompt-quality-report.json#/sdlcRuntimeMatrixAudit`
- Runtime equivalence: `generated/runtime-equivalence-report.json#/sdlcRuntimeMatrixAudit`

## Phase Coverage

| Phase | Copilots | Runtime cells |
|---|---:|---:|
| discovery | 4 | 16 |
| build | 8 | 32 |
| test | 10 | 40 |
| release | 8 | 32 |
| architecture | 3 | 12 |
| design | 5 | 20 |
| as_is | 1 | 4 |
| operate | 7 | 28 |
| devops | 3 | 12 |
| security | 1 | 4 |
| cloud | 1 | 4 |

## Runtime Coverage

| Runtime | Cells |
|---|---:|
| codex | 51 |
| claude | 51 |
| github-copilot | 51 |
| langchain | 51 |

## Trace Ledger

| Phase | Copilot | Runtime refs | Pairwise cases | Spec digest |
|---|---|---:|---:|---|
| discovery | devex | 4 | 6 | `39af69d22fac` |
| build | devex | 4 | 6 | `39af69d22fac` |
| test | devex | 4 | 6 | `39af69d22fac` |
| release | devex | 4 | 6 | `39af69d22fac` |
| architecture | aida_architecture | 4 | 6 | `d137afeb61a5` |
| design | aida_architecture | 4 | 6 | `d137afeb61a5` |
| release | aida_architecture | 4 | 6 | `d137afeb61a5` |
| discovery | as_is_discovery | 4 | 6 | `b167724fceda` |
| as_is | as_is_discovery | 4 | 6 | `b167724fceda` |
| discovery | single_registry | 4 | 6 | `a6565bd7bd87` |
| operate | single_registry | 4 | 6 | `a6565bd7bd87` |
| build | firefly_v5 | 4 | 6 | `cc8381ec3e4a` |
| test | firefly_v5 | 4 | 6 | `cc8381ec3e4a` |
| devops | firefly_v5 | 4 | 6 | `cc8381ec3e4a` |
| build | firefly_v6 | 4 | 6 | `33577e223044` |
| test | firefly_v6 | 4 | 6 | `33577e223044` |
| devops | firefly_v6 | 4 | 6 | `33577e223044` |
| build | moonshine | 4 | 6 | `b780061888c3` |
| test | moonshine | 4 | 6 | `b780061888c3` |
| operate | moonshine | 4 | 6 | `b780061888c3` |
| design | java_generic | 4 | 6 | `1b4b44d0d152` |
| build | java_generic | 4 | 6 | `1b4b44d0d152` |
| test | java_generic | 4 | 6 | `1b4b44d0d152` |
| architecture | java_architect | 4 | 6 | `e6ed37559c38` |
| design | java_architect | 4 | 6 | `e6ed37559c38` |
| release | java_architect | 4 | 6 | `e6ed37559c38` |
| design | angular_18 | 4 | 6 | `8a25deab66b0` |
| build | angular_18 | 4 | 6 | `8a25deab66b0` |
| test | angular_18 | 4 | 6 | `8a25deab66b0` |
| design | nodejs | 4 | 6 | `f356c3fc5b09` |
| build | nodejs | 4 | 6 | `f356c3fc5b09` |
| test | nodejs | 4 | 6 | `f356c3fc5b09` |
| operate | nodejs | 4 | 6 | `f356c3fc5b09` |
| build | python | 4 | 6 | `fa2723a2117e` |
| test | python | 4 | 6 | `fa2723a2117e` |
| operate | python | 4 | 6 | `fa2723a2117e` |
| test | qa_general | 4 | 6 | `5efe790701b8` |
| release | qa_general | 4 | 6 | `5efe790701b8` |
| test | sonarqube_remediation | 4 | 6 | `c0e2b9a929ea` |
| security | sonarqube_remediation | 4 | 6 | `c0e2b9a929ea` |
| release | sonarqube_remediation | 4 | 6 | `c0e2b9a929ea` |
| devops | cicd | 4 | 6 | `e990279893ca` |
| release | cicd | 4 | 6 | `e990279893ca` |
| operate | cicd | 4 | 6 | `e990279893ca` |
| architecture | journey_to_cloud | 4 | 6 | `293951f9f793` |
| cloud | journey_to_cloud | 4 | 6 | `293951f9f793` |
| release | journey_to_cloud | 4 | 6 | `293951f9f793` |
| discovery | copilots_manager | 4 | 6 | `f33ce4004325` |
| operate | copilots_manager | 4 | 6 | `f33ce4004325` |
| release | firefly_marketplace | 4 | 6 | `228e6dba2d6e` |
| operate | firefly_marketplace | 4 | 6 | `228e6dba2d6e` |

## Cells

| Phase | Copilot | Runtime | Adapter file | Spec digest | Schema digest |
|---|---|---|---|---|---|
| discovery | devex | codex | `dist/copilots/devex/codex/AGENT.md` | `39af69d22fac` | `e52cbeeeb3d8` |
| discovery | devex | claude | `dist/copilots/devex/claude/AGENT.md` | `39af69d22fac` | `e52cbeeeb3d8` |
| discovery | devex | github-copilot | `dist/copilots/devex/github-copilot/copilot-agent.md` | `39af69d22fac` | `e52cbeeeb3d8` |
| discovery | devex | langchain | `dist/copilots/devex/langchain/agent.py` | `39af69d22fac` | `e52cbeeeb3d8` |
| build | devex | codex | `dist/copilots/devex/codex/AGENT.md` | `39af69d22fac` | `e52cbeeeb3d8` |
| build | devex | claude | `dist/copilots/devex/claude/AGENT.md` | `39af69d22fac` | `e52cbeeeb3d8` |
| build | devex | github-copilot | `dist/copilots/devex/github-copilot/copilot-agent.md` | `39af69d22fac` | `e52cbeeeb3d8` |
| build | devex | langchain | `dist/copilots/devex/langchain/agent.py` | `39af69d22fac` | `e52cbeeeb3d8` |
| test | devex | codex | `dist/copilots/devex/codex/AGENT.md` | `39af69d22fac` | `e52cbeeeb3d8` |
| test | devex | claude | `dist/copilots/devex/claude/AGENT.md` | `39af69d22fac` | `e52cbeeeb3d8` |
| test | devex | github-copilot | `dist/copilots/devex/github-copilot/copilot-agent.md` | `39af69d22fac` | `e52cbeeeb3d8` |
| test | devex | langchain | `dist/copilots/devex/langchain/agent.py` | `39af69d22fac` | `e52cbeeeb3d8` |
| release | devex | codex | `dist/copilots/devex/codex/AGENT.md` | `39af69d22fac` | `e52cbeeeb3d8` |
| release | devex | claude | `dist/copilots/devex/claude/AGENT.md` | `39af69d22fac` | `e52cbeeeb3d8` |
| release | devex | github-copilot | `dist/copilots/devex/github-copilot/copilot-agent.md` | `39af69d22fac` | `e52cbeeeb3d8` |
| release | devex | langchain | `dist/copilots/devex/langchain/agent.py` | `39af69d22fac` | `e52cbeeeb3d8` |
| architecture | aida_architecture | codex | `dist/copilots/aida_architecture/codex/AGENT.md` | `d137afeb61a5` | `52ecc737d5fa` |
| architecture | aida_architecture | claude | `dist/copilots/aida_architecture/claude/AGENT.md` | `d137afeb61a5` | `52ecc737d5fa` |
| architecture | aida_architecture | github-copilot | `dist/copilots/aida_architecture/github-copilot/copilot-agent.md` | `d137afeb61a5` | `52ecc737d5fa` |
| architecture | aida_architecture | langchain | `dist/copilots/aida_architecture/langchain/agent.py` | `d137afeb61a5` | `52ecc737d5fa` |
| design | aida_architecture | codex | `dist/copilots/aida_architecture/codex/AGENT.md` | `d137afeb61a5` | `52ecc737d5fa` |
| design | aida_architecture | claude | `dist/copilots/aida_architecture/claude/AGENT.md` | `d137afeb61a5` | `52ecc737d5fa` |
| design | aida_architecture | github-copilot | `dist/copilots/aida_architecture/github-copilot/copilot-agent.md` | `d137afeb61a5` | `52ecc737d5fa` |
| design | aida_architecture | langchain | `dist/copilots/aida_architecture/langchain/agent.py` | `d137afeb61a5` | `52ecc737d5fa` |
| release | aida_architecture | codex | `dist/copilots/aida_architecture/codex/AGENT.md` | `d137afeb61a5` | `52ecc737d5fa` |
| release | aida_architecture | claude | `dist/copilots/aida_architecture/claude/AGENT.md` | `d137afeb61a5` | `52ecc737d5fa` |
| release | aida_architecture | github-copilot | `dist/copilots/aida_architecture/github-copilot/copilot-agent.md` | `d137afeb61a5` | `52ecc737d5fa` |
| release | aida_architecture | langchain | `dist/copilots/aida_architecture/langchain/agent.py` | `d137afeb61a5` | `52ecc737d5fa` |
| discovery | as_is_discovery | codex | `dist/copilots/as_is_discovery/codex/AGENT.md` | `b167724fceda` | `8f27cbb5dcb5` |
| discovery | as_is_discovery | claude | `dist/copilots/as_is_discovery/claude/AGENT.md` | `b167724fceda` | `8f27cbb5dcb5` |
| discovery | as_is_discovery | github-copilot | `dist/copilots/as_is_discovery/github-copilot/copilot-agent.md` | `b167724fceda` | `8f27cbb5dcb5` |
| discovery | as_is_discovery | langchain | `dist/copilots/as_is_discovery/langchain/agent.py` | `b167724fceda` | `8f27cbb5dcb5` |
| as_is | as_is_discovery | codex | `dist/copilots/as_is_discovery/codex/AGENT.md` | `b167724fceda` | `8f27cbb5dcb5` |
| as_is | as_is_discovery | claude | `dist/copilots/as_is_discovery/claude/AGENT.md` | `b167724fceda` | `8f27cbb5dcb5` |
| as_is | as_is_discovery | github-copilot | `dist/copilots/as_is_discovery/github-copilot/copilot-agent.md` | `b167724fceda` | `8f27cbb5dcb5` |
| as_is | as_is_discovery | langchain | `dist/copilots/as_is_discovery/langchain/agent.py` | `b167724fceda` | `8f27cbb5dcb5` |
| discovery | single_registry | codex | `dist/copilots/single_registry/codex/AGENT.md` | `a6565bd7bd87` | `25dbd5a88d4f` |
| discovery | single_registry | claude | `dist/copilots/single_registry/claude/AGENT.md` | `a6565bd7bd87` | `25dbd5a88d4f` |
| discovery | single_registry | github-copilot | `dist/copilots/single_registry/github-copilot/copilot-agent.md` | `a6565bd7bd87` | `25dbd5a88d4f` |
| discovery | single_registry | langchain | `dist/copilots/single_registry/langchain/agent.py` | `a6565bd7bd87` | `25dbd5a88d4f` |
| operate | single_registry | codex | `dist/copilots/single_registry/codex/AGENT.md` | `a6565bd7bd87` | `25dbd5a88d4f` |
| operate | single_registry | claude | `dist/copilots/single_registry/claude/AGENT.md` | `a6565bd7bd87` | `25dbd5a88d4f` |
| operate | single_registry | github-copilot | `dist/copilots/single_registry/github-copilot/copilot-agent.md` | `a6565bd7bd87` | `25dbd5a88d4f` |
| operate | single_registry | langchain | `dist/copilots/single_registry/langchain/agent.py` | `a6565bd7bd87` | `25dbd5a88d4f` |
| build | firefly_v5 | codex | `dist/copilots/firefly_v5/codex/AGENT.md` | `cc8381ec3e4a` | `16a05a521301` |
| build | firefly_v5 | claude | `dist/copilots/firefly_v5/claude/AGENT.md` | `cc8381ec3e4a` | `16a05a521301` |
| build | firefly_v5 | github-copilot | `dist/copilots/firefly_v5/github-copilot/copilot-agent.md` | `cc8381ec3e4a` | `16a05a521301` |
| build | firefly_v5 | langchain | `dist/copilots/firefly_v5/langchain/agent.py` | `cc8381ec3e4a` | `16a05a521301` |
| test | firefly_v5 | codex | `dist/copilots/firefly_v5/codex/AGENT.md` | `cc8381ec3e4a` | `16a05a521301` |
| test | firefly_v5 | claude | `dist/copilots/firefly_v5/claude/AGENT.md` | `cc8381ec3e4a` | `16a05a521301` |
| test | firefly_v5 | github-copilot | `dist/copilots/firefly_v5/github-copilot/copilot-agent.md` | `cc8381ec3e4a` | `16a05a521301` |
| test | firefly_v5 | langchain | `dist/copilots/firefly_v5/langchain/agent.py` | `cc8381ec3e4a` | `16a05a521301` |
| devops | firefly_v5 | codex | `dist/copilots/firefly_v5/codex/AGENT.md` | `cc8381ec3e4a` | `16a05a521301` |
| devops | firefly_v5 | claude | `dist/copilots/firefly_v5/claude/AGENT.md` | `cc8381ec3e4a` | `16a05a521301` |
| devops | firefly_v5 | github-copilot | `dist/copilots/firefly_v5/github-copilot/copilot-agent.md` | `cc8381ec3e4a` | `16a05a521301` |
| devops | firefly_v5 | langchain | `dist/copilots/firefly_v5/langchain/agent.py` | `cc8381ec3e4a` | `16a05a521301` |
| build | firefly_v6 | codex | `dist/copilots/firefly_v6/codex/AGENT.md` | `33577e223044` | `c303d7bffd70` |
| build | firefly_v6 | claude | `dist/copilots/firefly_v6/claude/AGENT.md` | `33577e223044` | `c303d7bffd70` |
| build | firefly_v6 | github-copilot | `dist/copilots/firefly_v6/github-copilot/copilot-agent.md` | `33577e223044` | `c303d7bffd70` |
| build | firefly_v6 | langchain | `dist/copilots/firefly_v6/langchain/agent.py` | `33577e223044` | `c303d7bffd70` |
| test | firefly_v6 | codex | `dist/copilots/firefly_v6/codex/AGENT.md` | `33577e223044` | `c303d7bffd70` |
| test | firefly_v6 | claude | `dist/copilots/firefly_v6/claude/AGENT.md` | `33577e223044` | `c303d7bffd70` |
| test | firefly_v6 | github-copilot | `dist/copilots/firefly_v6/github-copilot/copilot-agent.md` | `33577e223044` | `c303d7bffd70` |
| test | firefly_v6 | langchain | `dist/copilots/firefly_v6/langchain/agent.py` | `33577e223044` | `c303d7bffd70` |
| devops | firefly_v6 | codex | `dist/copilots/firefly_v6/codex/AGENT.md` | `33577e223044` | `c303d7bffd70` |
| devops | firefly_v6 | claude | `dist/copilots/firefly_v6/claude/AGENT.md` | `33577e223044` | `c303d7bffd70` |
| devops | firefly_v6 | github-copilot | `dist/copilots/firefly_v6/github-copilot/copilot-agent.md` | `33577e223044` | `c303d7bffd70` |
| devops | firefly_v6 | langchain | `dist/copilots/firefly_v6/langchain/agent.py` | `33577e223044` | `c303d7bffd70` |
| build | moonshine | codex | `dist/copilots/moonshine/codex/AGENT.md` | `b780061888c3` | `17d05917382e` |
| build | moonshine | claude | `dist/copilots/moonshine/claude/AGENT.md` | `b780061888c3` | `17d05917382e` |
| build | moonshine | github-copilot | `dist/copilots/moonshine/github-copilot/copilot-agent.md` | `b780061888c3` | `17d05917382e` |
| build | moonshine | langchain | `dist/copilots/moonshine/langchain/agent.py` | `b780061888c3` | `17d05917382e` |
| test | moonshine | codex | `dist/copilots/moonshine/codex/AGENT.md` | `b780061888c3` | `17d05917382e` |
| test | moonshine | claude | `dist/copilots/moonshine/claude/AGENT.md` | `b780061888c3` | `17d05917382e` |
| test | moonshine | github-copilot | `dist/copilots/moonshine/github-copilot/copilot-agent.md` | `b780061888c3` | `17d05917382e` |
| test | moonshine | langchain | `dist/copilots/moonshine/langchain/agent.py` | `b780061888c3` | `17d05917382e` |
| operate | moonshine | codex | `dist/copilots/moonshine/codex/AGENT.md` | `b780061888c3` | `17d05917382e` |
| operate | moonshine | claude | `dist/copilots/moonshine/claude/AGENT.md` | `b780061888c3` | `17d05917382e` |
| operate | moonshine | github-copilot | `dist/copilots/moonshine/github-copilot/copilot-agent.md` | `b780061888c3` | `17d05917382e` |
| operate | moonshine | langchain | `dist/copilots/moonshine/langchain/agent.py` | `b780061888c3` | `17d05917382e` |
| design | java_generic | codex | `dist/copilots/java_generic/codex/AGENT.md` | `1b4b44d0d152` | `7e261539e412` |
| design | java_generic | claude | `dist/copilots/java_generic/claude/AGENT.md` | `1b4b44d0d152` | `7e261539e412` |
| design | java_generic | github-copilot | `dist/copilots/java_generic/github-copilot/copilot-agent.md` | `1b4b44d0d152` | `7e261539e412` |
| design | java_generic | langchain | `dist/copilots/java_generic/langchain/agent.py` | `1b4b44d0d152` | `7e261539e412` |
| build | java_generic | codex | `dist/copilots/java_generic/codex/AGENT.md` | `1b4b44d0d152` | `7e261539e412` |
| build | java_generic | claude | `dist/copilots/java_generic/claude/AGENT.md` | `1b4b44d0d152` | `7e261539e412` |
| build | java_generic | github-copilot | `dist/copilots/java_generic/github-copilot/copilot-agent.md` | `1b4b44d0d152` | `7e261539e412` |
| build | java_generic | langchain | `dist/copilots/java_generic/langchain/agent.py` | `1b4b44d0d152` | `7e261539e412` |
| test | java_generic | codex | `dist/copilots/java_generic/codex/AGENT.md` | `1b4b44d0d152` | `7e261539e412` |
| test | java_generic | claude | `dist/copilots/java_generic/claude/AGENT.md` | `1b4b44d0d152` | `7e261539e412` |
| test | java_generic | github-copilot | `dist/copilots/java_generic/github-copilot/copilot-agent.md` | `1b4b44d0d152` | `7e261539e412` |
| test | java_generic | langchain | `dist/copilots/java_generic/langchain/agent.py` | `1b4b44d0d152` | `7e261539e412` |
| architecture | java_architect | codex | `dist/copilots/java_architect/codex/AGENT.md` | `e6ed37559c38` | `c80b7df19b8e` |
| architecture | java_architect | claude | `dist/copilots/java_architect/claude/AGENT.md` | `e6ed37559c38` | `c80b7df19b8e` |
| architecture | java_architect | github-copilot | `dist/copilots/java_architect/github-copilot/copilot-agent.md` | `e6ed37559c38` | `c80b7df19b8e` |
| architecture | java_architect | langchain | `dist/copilots/java_architect/langchain/agent.py` | `e6ed37559c38` | `c80b7df19b8e` |
| design | java_architect | codex | `dist/copilots/java_architect/codex/AGENT.md` | `e6ed37559c38` | `c80b7df19b8e` |
| design | java_architect | claude | `dist/copilots/java_architect/claude/AGENT.md` | `e6ed37559c38` | `c80b7df19b8e` |
| design | java_architect | github-copilot | `dist/copilots/java_architect/github-copilot/copilot-agent.md` | `e6ed37559c38` | `c80b7df19b8e` |
| design | java_architect | langchain | `dist/copilots/java_architect/langchain/agent.py` | `e6ed37559c38` | `c80b7df19b8e` |
| release | java_architect | codex | `dist/copilots/java_architect/codex/AGENT.md` | `e6ed37559c38` | `c80b7df19b8e` |
| release | java_architect | claude | `dist/copilots/java_architect/claude/AGENT.md` | `e6ed37559c38` | `c80b7df19b8e` |
| release | java_architect | github-copilot | `dist/copilots/java_architect/github-copilot/copilot-agent.md` | `e6ed37559c38` | `c80b7df19b8e` |
| release | java_architect | langchain | `dist/copilots/java_architect/langchain/agent.py` | `e6ed37559c38` | `c80b7df19b8e` |
| design | angular_18 | codex | `dist/copilots/angular_18/codex/AGENT.md` | `8a25deab66b0` | `2d32798a22fe` |
| design | angular_18 | claude | `dist/copilots/angular_18/claude/AGENT.md` | `8a25deab66b0` | `2d32798a22fe` |
| design | angular_18 | github-copilot | `dist/copilots/angular_18/github-copilot/copilot-agent.md` | `8a25deab66b0` | `2d32798a22fe` |
| design | angular_18 | langchain | `dist/copilots/angular_18/langchain/agent.py` | `8a25deab66b0` | `2d32798a22fe` |
| build | angular_18 | codex | `dist/copilots/angular_18/codex/AGENT.md` | `8a25deab66b0` | `2d32798a22fe` |
| build | angular_18 | claude | `dist/copilots/angular_18/claude/AGENT.md` | `8a25deab66b0` | `2d32798a22fe` |
| build | angular_18 | github-copilot | `dist/copilots/angular_18/github-copilot/copilot-agent.md` | `8a25deab66b0` | `2d32798a22fe` |
| build | angular_18 | langchain | `dist/copilots/angular_18/langchain/agent.py` | `8a25deab66b0` | `2d32798a22fe` |
| test | angular_18 | codex | `dist/copilots/angular_18/codex/AGENT.md` | `8a25deab66b0` | `2d32798a22fe` |
| test | angular_18 | claude | `dist/copilots/angular_18/claude/AGENT.md` | `8a25deab66b0` | `2d32798a22fe` |
| test | angular_18 | github-copilot | `dist/copilots/angular_18/github-copilot/copilot-agent.md` | `8a25deab66b0` | `2d32798a22fe` |
| test | angular_18 | langchain | `dist/copilots/angular_18/langchain/agent.py` | `8a25deab66b0` | `2d32798a22fe` |
| design | nodejs | codex | `dist/copilots/nodejs/codex/AGENT.md` | `f356c3fc5b09` | `548540dc30ac` |
| design | nodejs | claude | `dist/copilots/nodejs/claude/AGENT.md` | `f356c3fc5b09` | `548540dc30ac` |
| design | nodejs | github-copilot | `dist/copilots/nodejs/github-copilot/copilot-agent.md` | `f356c3fc5b09` | `548540dc30ac` |
| design | nodejs | langchain | `dist/copilots/nodejs/langchain/agent.py` | `f356c3fc5b09` | `548540dc30ac` |
| build | nodejs | codex | `dist/copilots/nodejs/codex/AGENT.md` | `f356c3fc5b09` | `548540dc30ac` |
| build | nodejs | claude | `dist/copilots/nodejs/claude/AGENT.md` | `f356c3fc5b09` | `548540dc30ac` |
| build | nodejs | github-copilot | `dist/copilots/nodejs/github-copilot/copilot-agent.md` | `f356c3fc5b09` | `548540dc30ac` |
| build | nodejs | langchain | `dist/copilots/nodejs/langchain/agent.py` | `f356c3fc5b09` | `548540dc30ac` |
| test | nodejs | codex | `dist/copilots/nodejs/codex/AGENT.md` | `f356c3fc5b09` | `548540dc30ac` |
| test | nodejs | claude | `dist/copilots/nodejs/claude/AGENT.md` | `f356c3fc5b09` | `548540dc30ac` |
| test | nodejs | github-copilot | `dist/copilots/nodejs/github-copilot/copilot-agent.md` | `f356c3fc5b09` | `548540dc30ac` |
| test | nodejs | langchain | `dist/copilots/nodejs/langchain/agent.py` | `f356c3fc5b09` | `548540dc30ac` |
| operate | nodejs | codex | `dist/copilots/nodejs/codex/AGENT.md` | `f356c3fc5b09` | `548540dc30ac` |
| operate | nodejs | claude | `dist/copilots/nodejs/claude/AGENT.md` | `f356c3fc5b09` | `548540dc30ac` |
| operate | nodejs | github-copilot | `dist/copilots/nodejs/github-copilot/copilot-agent.md` | `f356c3fc5b09` | `548540dc30ac` |
| operate | nodejs | langchain | `dist/copilots/nodejs/langchain/agent.py` | `f356c3fc5b09` | `548540dc30ac` |
| build | python | codex | `dist/copilots/python/codex/AGENT.md` | `fa2723a2117e` | `a9491ddda849` |
| build | python | claude | `dist/copilots/python/claude/AGENT.md` | `fa2723a2117e` | `a9491ddda849` |
| build | python | github-copilot | `dist/copilots/python/github-copilot/copilot-agent.md` | `fa2723a2117e` | `a9491ddda849` |
| build | python | langchain | `dist/copilots/python/langchain/agent.py` | `fa2723a2117e` | `a9491ddda849` |
| test | python | codex | `dist/copilots/python/codex/AGENT.md` | `fa2723a2117e` | `a9491ddda849` |
| test | python | claude | `dist/copilots/python/claude/AGENT.md` | `fa2723a2117e` | `a9491ddda849` |
| test | python | github-copilot | `dist/copilots/python/github-copilot/copilot-agent.md` | `fa2723a2117e` | `a9491ddda849` |
| test | python | langchain | `dist/copilots/python/langchain/agent.py` | `fa2723a2117e` | `a9491ddda849` |
| operate | python | codex | `dist/copilots/python/codex/AGENT.md` | `fa2723a2117e` | `a9491ddda849` |
| operate | python | claude | `dist/copilots/python/claude/AGENT.md` | `fa2723a2117e` | `a9491ddda849` |
| operate | python | github-copilot | `dist/copilots/python/github-copilot/copilot-agent.md` | `fa2723a2117e` | `a9491ddda849` |
| operate | python | langchain | `dist/copilots/python/langchain/agent.py` | `fa2723a2117e` | `a9491ddda849` |
| test | qa_general | codex | `dist/copilots/qa_general/codex/AGENT.md` | `5efe790701b8` | `81e1fb2c7b7e` |
| test | qa_general | claude | `dist/copilots/qa_general/claude/AGENT.md` | `5efe790701b8` | `81e1fb2c7b7e` |
| test | qa_general | github-copilot | `dist/copilots/qa_general/github-copilot/copilot-agent.md` | `5efe790701b8` | `81e1fb2c7b7e` |
| test | qa_general | langchain | `dist/copilots/qa_general/langchain/agent.py` | `5efe790701b8` | `81e1fb2c7b7e` |
| release | qa_general | codex | `dist/copilots/qa_general/codex/AGENT.md` | `5efe790701b8` | `81e1fb2c7b7e` |
| release | qa_general | claude | `dist/copilots/qa_general/claude/AGENT.md` | `5efe790701b8` | `81e1fb2c7b7e` |
| release | qa_general | github-copilot | `dist/copilots/qa_general/github-copilot/copilot-agent.md` | `5efe790701b8` | `81e1fb2c7b7e` |
| release | qa_general | langchain | `dist/copilots/qa_general/langchain/agent.py` | `5efe790701b8` | `81e1fb2c7b7e` |
| test | sonarqube_remediation | codex | `dist/copilots/sonarqube_remediation/codex/AGENT.md` | `c0e2b9a929ea` | `eaf409e8209c` |
| test | sonarqube_remediation | claude | `dist/copilots/sonarqube_remediation/claude/AGENT.md` | `c0e2b9a929ea` | `eaf409e8209c` |
| test | sonarqube_remediation | github-copilot | `dist/copilots/sonarqube_remediation/github-copilot/copilot-agent.md` | `c0e2b9a929ea` | `eaf409e8209c` |
| test | sonarqube_remediation | langchain | `dist/copilots/sonarqube_remediation/langchain/agent.py` | `c0e2b9a929ea` | `eaf409e8209c` |
| security | sonarqube_remediation | codex | `dist/copilots/sonarqube_remediation/codex/AGENT.md` | `c0e2b9a929ea` | `eaf409e8209c` |
| security | sonarqube_remediation | claude | `dist/copilots/sonarqube_remediation/claude/AGENT.md` | `c0e2b9a929ea` | `eaf409e8209c` |
| security | sonarqube_remediation | github-copilot | `dist/copilots/sonarqube_remediation/github-copilot/copilot-agent.md` | `c0e2b9a929ea` | `eaf409e8209c` |
| security | sonarqube_remediation | langchain | `dist/copilots/sonarqube_remediation/langchain/agent.py` | `c0e2b9a929ea` | `eaf409e8209c` |
| release | sonarqube_remediation | codex | `dist/copilots/sonarqube_remediation/codex/AGENT.md` | `c0e2b9a929ea` | `eaf409e8209c` |
| release | sonarqube_remediation | claude | `dist/copilots/sonarqube_remediation/claude/AGENT.md` | `c0e2b9a929ea` | `eaf409e8209c` |
| release | sonarqube_remediation | github-copilot | `dist/copilots/sonarqube_remediation/github-copilot/copilot-agent.md` | `c0e2b9a929ea` | `eaf409e8209c` |
| release | sonarqube_remediation | langchain | `dist/copilots/sonarqube_remediation/langchain/agent.py` | `c0e2b9a929ea` | `eaf409e8209c` |
| devops | cicd | codex | `dist/copilots/cicd/codex/AGENT.md` | `e990279893ca` | `a4bb45da2c07` |
| devops | cicd | claude | `dist/copilots/cicd/claude/AGENT.md` | `e990279893ca` | `a4bb45da2c07` |
| devops | cicd | github-copilot | `dist/copilots/cicd/github-copilot/copilot-agent.md` | `e990279893ca` | `a4bb45da2c07` |
| devops | cicd | langchain | `dist/copilots/cicd/langchain/agent.py` | `e990279893ca` | `a4bb45da2c07` |
| release | cicd | codex | `dist/copilots/cicd/codex/AGENT.md` | `e990279893ca` | `a4bb45da2c07` |
| release | cicd | claude | `dist/copilots/cicd/claude/AGENT.md` | `e990279893ca` | `a4bb45da2c07` |
| release | cicd | github-copilot | `dist/copilots/cicd/github-copilot/copilot-agent.md` | `e990279893ca` | `a4bb45da2c07` |
| release | cicd | langchain | `dist/copilots/cicd/langchain/agent.py` | `e990279893ca` | `a4bb45da2c07` |
| operate | cicd | codex | `dist/copilots/cicd/codex/AGENT.md` | `e990279893ca` | `a4bb45da2c07` |
| operate | cicd | claude | `dist/copilots/cicd/claude/AGENT.md` | `e990279893ca` | `a4bb45da2c07` |
| operate | cicd | github-copilot | `dist/copilots/cicd/github-copilot/copilot-agent.md` | `e990279893ca` | `a4bb45da2c07` |
| operate | cicd | langchain | `dist/copilots/cicd/langchain/agent.py` | `e990279893ca` | `a4bb45da2c07` |
| architecture | journey_to_cloud | codex | `dist/copilots/journey_to_cloud/codex/AGENT.md` | `293951f9f793` | `09d5e8f650ec` |
| architecture | journey_to_cloud | claude | `dist/copilots/journey_to_cloud/claude/AGENT.md` | `293951f9f793` | `09d5e8f650ec` |
| architecture | journey_to_cloud | github-copilot | `dist/copilots/journey_to_cloud/github-copilot/copilot-agent.md` | `293951f9f793` | `09d5e8f650ec` |
| architecture | journey_to_cloud | langchain | `dist/copilots/journey_to_cloud/langchain/agent.py` | `293951f9f793` | `09d5e8f650ec` |
| cloud | journey_to_cloud | codex | `dist/copilots/journey_to_cloud/codex/AGENT.md` | `293951f9f793` | `09d5e8f650ec` |
| cloud | journey_to_cloud | claude | `dist/copilots/journey_to_cloud/claude/AGENT.md` | `293951f9f793` | `09d5e8f650ec` |
| cloud | journey_to_cloud | github-copilot | `dist/copilots/journey_to_cloud/github-copilot/copilot-agent.md` | `293951f9f793` | `09d5e8f650ec` |
| cloud | journey_to_cloud | langchain | `dist/copilots/journey_to_cloud/langchain/agent.py` | `293951f9f793` | `09d5e8f650ec` |
| release | journey_to_cloud | codex | `dist/copilots/journey_to_cloud/codex/AGENT.md` | `293951f9f793` | `09d5e8f650ec` |
| release | journey_to_cloud | claude | `dist/copilots/journey_to_cloud/claude/AGENT.md` | `293951f9f793` | `09d5e8f650ec` |
| release | journey_to_cloud | github-copilot | `dist/copilots/journey_to_cloud/github-copilot/copilot-agent.md` | `293951f9f793` | `09d5e8f650ec` |
| release | journey_to_cloud | langchain | `dist/copilots/journey_to_cloud/langchain/agent.py` | `293951f9f793` | `09d5e8f650ec` |
| discovery | copilots_manager | codex | `dist/copilots/copilots_manager/codex/AGENT.md` | `f33ce4004325` | `ac6c6976c359` |
| discovery | copilots_manager | claude | `dist/copilots/copilots_manager/claude/AGENT.md` | `f33ce4004325` | `ac6c6976c359` |
| discovery | copilots_manager | github-copilot | `dist/copilots/copilots_manager/github-copilot/copilot-agent.md` | `f33ce4004325` | `ac6c6976c359` |
| discovery | copilots_manager | langchain | `dist/copilots/copilots_manager/langchain/agent.py` | `f33ce4004325` | `ac6c6976c359` |
| operate | copilots_manager | codex | `dist/copilots/copilots_manager/codex/AGENT.md` | `f33ce4004325` | `ac6c6976c359` |
| operate | copilots_manager | claude | `dist/copilots/copilots_manager/claude/AGENT.md` | `f33ce4004325` | `ac6c6976c359` |
| operate | copilots_manager | github-copilot | `dist/copilots/copilots_manager/github-copilot/copilot-agent.md` | `f33ce4004325` | `ac6c6976c359` |
| operate | copilots_manager | langchain | `dist/copilots/copilots_manager/langchain/agent.py` | `f33ce4004325` | `ac6c6976c359` |
| release | firefly_marketplace | codex | `dist/copilots/firefly_marketplace/codex/AGENT.md` | `228e6dba2d6e` | `c2cde5b99a75` |
| release | firefly_marketplace | claude | `dist/copilots/firefly_marketplace/claude/AGENT.md` | `228e6dba2d6e` | `c2cde5b99a75` |
| release | firefly_marketplace | github-copilot | `dist/copilots/firefly_marketplace/github-copilot/copilot-agent.md` | `228e6dba2d6e` | `c2cde5b99a75` |
| release | firefly_marketplace | langchain | `dist/copilots/firefly_marketplace/langchain/agent.py` | `228e6dba2d6e` | `c2cde5b99a75` |
| operate | firefly_marketplace | codex | `dist/copilots/firefly_marketplace/codex/AGENT.md` | `228e6dba2d6e` | `c2cde5b99a75` |
| operate | firefly_marketplace | claude | `dist/copilots/firefly_marketplace/claude/AGENT.md` | `228e6dba2d6e` | `c2cde5b99a75` |
| operate | firefly_marketplace | github-copilot | `dist/copilots/firefly_marketplace/github-copilot/copilot-agent.md` | `228e6dba2d6e` | `c2cde5b99a75` |
| operate | firefly_marketplace | langchain | `dist/copilots/firefly_marketplace/langchain/agent.py` | `228e6dba2d6e` | `c2cde5b99a75` |
