# M0 design and milestones

## Decisions

M0 is an executable transition kernel for exactly three static tasks: `low`, `mid`, `high`, with fixed distinct priorities 1, 2, 3. Task IDs at the experimental ABI are 0, 1, 2. Each task can have one outstanding activation, represented by a Boolean. This is deliberately a finite first configuration, not an arbitrary-size scheduler.

`State` has independent `active` membership and `current` task. The invariant `Valid s` means `current = select active`; malformed combinations are representable, so preservation is not guaranteed by the type alone. `taskState` derives Suspended when inactive, Running when active and current, and Ready otherwise. The eligible set includes both Ready and Running tasks. `select` chooses high, then mid, then low, or idle. No duplicate ready queue is maintained in M0.

Transitions are atomic, sequential and at task service boundaries. Activation sets only the target's membership and reschedules; a duplicate or invalid ID preserves the entire input state. Termination removes the current task and reschedules. Idle termination returns a project-defined call-level error; this is not a complete OSEK context matrix. Query results are values, not pointer writes. `None` represents idle/invalid query output, with an error distinguishing the latter.

`Control.returned` carries the logical service response. After activation preempts a caller, actual delivery to that caller must wait until it resumes; M0 has no saved machine continuation. `Control.dispatch` on successful termination says that the caller continuation must be discarded. It is not a normal successful return. The C host demo checks this distinction with nonlocal transfer; machine stacks/registers are a later refinement obligation.

Frame conditions concern activation membership. Derived Running/Ready state can legitimately change for the old and new runner. `unrelated_task_state` proves equality when membership agrees and neither old nor new current task is the observed task. This prevents an incorrectly strong claim that activation cannot change any other task's scheduling state.

## Proof boundary

`select_member` and `select_highest` check the actual selection algorithm over all Boolean memberships and all three task choices by kernel-checked finite case reduction. The scheduler proofs are separate from representational facts such as the size of an Option. `activate_preserves`, `terminate_preserves`, and induction on finite command lists establish reachable validity from the initial empty state. Error/frame theorems apply even where a valid-input assumption is unnecessary; each exact statement is in `Proofs.lean`.

Assumptions are explicitly catalogued in `trace/requirements.json`: static three-task configuration, atomic single-caller transitions, valid inputs for preservation, canonical scalar ABI states, and the trusted tool/runtime boundary. `propext` is Lean's standard propositional extensionality axiom, used by simplification. No new domain-specific axiom is introduced. The audit lists dependencies per theorem; proof checking is performed by Lean's kernel, not by `native_decide`.

The abstract logic's safety properties are checked. No liveness or progress fairness claim is made: repeated high-priority activation can starve lower tasks. “Full preemptive” at M0 means immediate priority reselection at modeled service transitions; there are no asynchronous interrupt events or instruction-level context switches. Generated C behavior is experimentally compared, not formally refined from Lean. Compiler, runtime, FFI, libc, host OS, C control transfer, future assembly and hardware are outside the proved kernel model.

## Milestones

| Stage | Deliverable | Exit gate |
|---|---|---|
| M0 | Three-task logic, proofs, host/actual generated C, trace/evidence | Clean exact-SHA local verification; recorded missing remote gates |
| M0-publication | Repository, Actions and Pages | Remote SHA equals local; actual Actions and Pages URLs verified |
| M1 | Arbitrary static distinct-priority task configuration | Generic selection/preservation proofs and configuration validation |
| M2 | First emulated target and minimal HAL | Boot, UART trace, real task context switch and termination transfer |
| M3 | Runtime constraints | Allocation/deallocation and stack bounds, reentrancy design, refinement obligations |
| M4 | Incremental OSEK/ATK2 feature expansion | Explicit feature requirements/proofs/tests; no class claim until complete |

## Proposed first target / minimal HAL

Propose QEMU AArch64 `virt`, `cortex-a53`, one core, with a versioned machine model pinned at M2. The [official QEMU description](https://www.qemu.org/docs/master/system/arm/virt.html) documents this CPU and platform. Rationale: straightforward UART/interrupt/timer instrumentation and a 64-bit host-to-target path before addressing smaller MCU runtime restrictions. This is a project proposal, not an AUTOSAR or ATK2 requirement, and no QEMU execution has occurred yet.

Start HAL with reset entry/linker script, explicit stack/BSS initialization, PL011 polled output, fail-stop panic, `start_first_task`, `switch_context`, and non-returning `discard_and_dispatch`. Add interrupt mask/restore and architectural timer/GIC only after the context invariant is tested. Preserve registers/stacks and translate `Control` outcomes explicitly. Lean runtime availability, allocation and freestanding port effort must be assessed before promising bare metal; C generation does not settle them. CPU selection remains open to the owner.

## Deferred scope

Equal-priority FIFO; ChainTask; multiple activations; Extended Tasks/events; resources/priority ceiling; alarms/counters/schedule tables; startup/autostart/shutdown and hooks; ISR categories; multicore; memory/time protection; all standard error precedence and call-level rules. Safety conformance, liveness, WCET and interruption safety require different evidence and remain separate.
