# Source and rights record

No specification PDF, extracted full text or ATK2 code is distributed here. Metadata and the project's own requirement statements are in `trace/`. All checks below were made on 2026-10-12.

| Source | Fixed version / anchor | Role and verification |
|---|---|---|
| OSEK/VDX Operating System | 2.2.3, 2005-02-17; §§4.2.2, 4.5, 4.6.1, 13.2.3.1/.2/.5/.6 | Primary M0 behavior source. Official-release PDF read via academic mirror; bytes hashed. Section references used because this document does not assign AUTOSAR-style IDs to these services. |
| ATK2 external specification, ATK2-0010 | 1.2.2, 2017-03-24; §§2.5, 3.9.4/.5/.8/.9 | Reference interpretation/design. Official PDF read and hashed. Verified COS IDs remain ATK2 document identifiers. |
| AUTOSAR CP OS | R24-11; §7.1.2, p36, SWS_Os_00001 | Proposed modern delta baseline. Official indexed section checked. Complete PDF and hash still unavailable due server timeout/502. Full compliance mapping has not been done. |

Source URLs and exact hashes are in [sources.json](../trace/sources.json). The OSEK historical publisher endpoint is `http://portal.osek-vdx.org/files/pdf/specs/os223.pdf`; the retrieved publisher-authored document is hosted at [IRISA](https://www.irisa.fr/alf/downloads/puaut/TPNXT/images/os223.pdf). Its cover identifies it as the official release; mirror bytes are not asserted identical to a separately obtained publisher copy.

The [ATK2 project page](https://www.toppers.jp/atk2.html) states its external specification is based on **AUTOSAR Release 4.0 Revision 3**. That historical basis is not R24-11. ATK2's added clarifications and implementation choices are reference-design decisions, not automatically normative AUTOSAR requirements. This project independently chooses the three-task model, derived task states, scalar ABI and host nonlocal dispatcher.

Recommend R24-11 as the first modern comparison snapshot: it provides a fixed CP OS release with an identifiable OSEK compatibility requirement, while avoiding a moving “latest” target. This is a reproducibility choice, not a claim it is current or superior to R25-11. Final adoption is contingent on obtaining the complete document, reviewing applicable deltas and hashing it. The only modern SWS ID currently recorded is the verified `SWS_Os_00001`; the broad compatibility obligation is explicitly **unimplemented** by M0.

## Rights decisions

- OSEK 2.2.3 cover reserves reproduction subject to written permission. Neither original text nor an extracted/translated copy is committed.
- ATK2-0010 p.i provides its own document conditions, requiring copyright/conditions/disclaimer preservation and modification marking. It explicitly does not license AUTOSAR IP. No copy is redistributed.
- [TOPPERS license](https://www.toppers.jp/license.html) and [AUTOSAR usage notice](https://www.toppers.jp/autosar.html) were checked. An implementation's exact headers must be reviewed before reuse; this project does not copy ATK2 implementation code.
- [AUTOSAR official CP guidance](https://www.autosar.org/standards/classic-platform) refers commercial exploitation to partnership. The exact R24-11 OS disclaimer is not yet fully retrieved, so its detailed reuse conditions are unresolved; no spec material is bundled. This record is an engineering provenance policy, not a legal opinion or a commercial-use clearance.
- **Project source license is undecided.** No MIT/Apache/GPL permission is implicitly selected by a public repository request. Only original project files and generated evidence are intended for publication.
- Lean is an external tool dependency obtained from the official pinned release. The full tool distribution is not vendored. Binary evidence includes runtime components; see the distribution's [LICENSE](https://github.com/leanprover/lean4/blob/v4.19.0/LICENSE) and third-party notices before redistribution. Runtime license notices must accompany packaged binary evidence.

## Reference implementation inspected

ATK2-SC1 **1.4.2** (official 2017-03-24 archive) is pinned separately from document version 1.2.2. Archive and `kernel/task_manage.c` hashes are recorded. The activation limit and termination dispatch paths plus the actual file license header were inspected. Its successful termination uses a distinct discard-and-dispatch path, with normal return reserved for errors; M0 uses this as design context without copying implementation text. ATK2 resource/interrupt checks are intentionally deferred here.
