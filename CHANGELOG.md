# Changelog


## [0.3.0] — 2026-09-18 · Studio Dev (61997)

- Contract: GenVM v0.3 API (`gl.contract.Contract`, `gl.nondet.web.render`, `gl.eq_principle.strict_eq`) and runner `py-genlayer:5jycge4q…`; deployed to `0x29f558390ac213D5697a4cf46e707111c0741122` with source verified on chain.
- Console: `genlayer-js@2.0.0-rc.1` `studioDevnet` chain with fee deposits, wallet stays on 61997, **Get test GEN** faucet, tx links to the Studio Dev explorer.
- Tests: stub covers the v0.3 API.

## 0.2.0 — 2026-08-30

- Real GenLayer consensus: `attach_evidence` freezes `get_webpage` digest under `eq_principle_strict_eq`
- `audit` re-fetches live URL + schema-checks metadata; locked after first audit
- `appeal` (max 3) for `invalid` records
- Stricter 0x address validation; FIFO audit trim; unknown JSON types rejected

## 0.1.0 — 2026-08-30

- Initial MetaEvidence IC (deterministic schema check)
