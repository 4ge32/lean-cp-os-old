# Lean CP OS

A small executable and proved **three-task transition kernel**, studying OSEK OS / AUTOSAR Classic Platform OS with TOPPERS ATK2 as a reference. This is the start of a kernel project, not a production OS or a conformance claim.

**M0:** one core; exactly three statically configured Basic Tasks, priorities 1 < 2 < 3; at most one activation each; immediate priority selection at modeled scheduling points. Suspended/Ready/Running, activation, termination and two queries are implemented in Lean 4.19.0. Actual generated C is linked to host C and exercised through a scalar C ABI.

## Run

Linux x86_64, Python 3, GCC, Git, curl and tar with zstd are needed. There are no external Lean package dependencies.

```sh
bash scripts/bootstrap_lean.sh /tmp/lean-cp-toolchain
export PATH=/tmp/lean-cp-toolchain/lean-4.19.0-linux/bin:$PATH
python3 scripts/verify.py --out evidence/local
```

The verifier requires a clean committed tree. For development only, `--allow-dirty` records `exact_commit: false`; such results must not be attributed to the commit. The report is `evidence/local/index.html`; `report.json`, `trace.json`, `axioms.json`, `runtime.json`, logs, generated C, binaries and SHA256SUMS accompany it.

## What is checked

- Lean checks 28 theorem declarations: initial validity, scheduler selection/membership/maximality, state consistency, transition/finite-sequence preservation, errors and frame conditions, and termination dispatch semantics.
- `Audit.lean` prints every theorem's axiom dependencies. The gate accepts only Lean's standard propositional extensionality (`propext`); additional axioms, admitted goals and native-evaluation proof bypass are rejected.
- 2,763 vectors are checked by Lean execution and linked generated C against an independent Python set-based oracle: 240 finite cases, 23 boundary cases and 625 sequences of four operations.
- A host C dispatcher demonstrates that successful termination skips the task's continuation; an idle error returns. It uses `setjmp/longjmp`, not a target context-switch implementation.
- Trace links and gaps are checked separately. A structurally complete map is not complete verification.

## Navigate

- [Design, proof boundary and milestones](docs/DESIGN.md)
- [Sources, versions and rights](docs/SOURCES.md)
- [Runtime / C ABI audit](docs/RUNTIME.md)
- [CI, per-commit evidence and publication](docs/CI.md)
- [Machine-readable requirements](trace/requirements.json), [sources](trace/sources.json), [test catalogue](trace/tests.json)

`python3 scripts/impact.py <base-sha>` reports conservative affected requirements, theorems and tests. All gates still run for every enumerated commit.

## Current limitations

No equal-priority FIFO, ChainTask, multiple activation queues, Extended Tasks, events, resources, alarms, interrupts, multicore, protection, hooks or complete call-level checking. No BCC1, SC1, AUTOSAR, ISO 26262 or production safety claim. No liveness/starvation, WCET, stack/memory bound, IRQ/reentrancy or machine-code refinement proof. The current C ABI is an experimental test protocol, not the AUTOSAR pointer/status ABI.

Public repository creation, remote push, GitHub Actions execution and Pages publication have **not** been completed in the bootstrap environment. The authenticated account was `4ge32`; repository lookup was 404 (which can also indicate missing access), the connector cannot create repositories, and browser creation was denied. Local work and publication configuration are retained for continuation. Do not infer that a remote URL exists from the project name.

A source-code license has deliberately **not been selected**. Public visibility and licensing are separate decisions. No third-party specification text or reference implementation code is included.
