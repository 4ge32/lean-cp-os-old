# Generated C and runtime boundary

`LeanCpOs/Bridge.lean` exports `lean_cp_step` with three `UInt32` values and a `UInt64` result. `c/bridge.h` fixes the experimental bit layout. Task states/results are not pointer-based AUTOSAR API types. `initialize_LeanCpOs_Bridge` and the Lean runtime initializer run once before calls; C owns and releases the initializer result. Scalar arguments/results have no cross-boundary reference ownership, but the implementation uses Lean objects internally.

The build regenerates `Model.c` and `Bridge.c` using `lake env lean -c`, compiles them with the pinned Lean `leanc` at `-O2 -fstack-usage`, compiles host-only C with GCC, and links the actual generated objects with `leanc` and the packaged runtime. Logs record each command; `report.json` hashes source, generated C, object files, binaries, `.olean` files, headers and tool/runtime binaries.

`runtime.json` counts generated allocation/increment/decrement call sites and retains compiler per-function stack usage. These are code-shape observations, not dynamic call counts or complete path costs. Current generated C contains `lean_alloc_ctor`, `lean_inc` and `lean_dec`. Decrementing an object can trigger cascading reference-count releases in the runtime. No bound for this chain has been proved; no zero-allocation, WCET or total stack bound is claimed. Finite task membership does not by itself establish bounds for the compiler/runtime paths.

The pure transition functions do not share mutable kernel state. This does not establish C/Lean runtime initialization thread safety, allocator interrupt safety, reentrancy or application synchronization. The `control_flow.c` test explicitly uses globals and is not reentrant. IRQ and concurrent entry are outside M0. No hand-written assembly exists yet.

Both Lean host execution and compiled C share the Lean compiler/runtime; their agreement is not independent compiler verification. Python's set-based oracle adds an independent behavioral comparison for tested inputs. Encoding correctness, arbitrary UInt32 boundary behavior, compiler preservation, C undefined-behavior freedom, runtime correctness, host OS and hardware remain trusted/tested boundaries.

## Bootstrap-host adaptation

The initial execution environment reports virtual PIDs that do not correspond to numeric `/proc/<pid>/exe` entries. Unmodified Lean 4.19.0 therefore failed to locate its executable. `tools/proc_self_compat.c` supplies an **optional host-only** readlink adapter: only the current process's numeric executable lookup is redirected to `/proc/self/exe`. It does not alter Lean definitions, theorem reduction, the kernel or C generation. The exact adapter binary hash is captured when used. Normal Linux/CI does not enable it. Local success with this adapter is separate from unmodified GitHub runner execution, which is not yet observed.

```sh
gcc -shared -fPIC -O2 tools/proc_self_compat.c -ldl -o /tmp/lean-cp-proc.so
export LD_PRELOAD=/tmp/lean-cp-proc.so
```

The bundled Clang does not find all host libc headers in this environment, so host C is compiled with GCC; generated C compilation and final linking use the pinned Lean tools. No tool binary or runtime proof checker is patched.
