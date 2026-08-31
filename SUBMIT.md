# Portal — MetaEvidence v0.2 (Intelligent Contracts)

**Type:** Builder → Intelligent Contracts

## Studionet smoke (DONE — v0.2)

| Item | Value |
|------|--------|
| Address | `0xF39330E2233E612CCcbAb1B148C94b136dEAE54C` |
| Explorer | https://explorer-studio.genlayer.com/address/0xF39330E2233E612CCcbAb1B148C94b136dEAE54C |
| Deploy | `0x058e2863f9d600958a5730d0ebb842226742ff25710997df478f6281567c88c9` |
| register_schema | `0xcaf61a3b681bdf5da3a5fd3f6638fac9a0503ac3aa23cca5689b3feeab4e679d` |
| attach_evidence | `0x2297ba643d1df8f12e5857e2c07ca4c14293b3e57261b07f7f6298fb4cf1cd8d` |
| audit | `0x4562f5e816a083b3dfd6672eb7ca8d360df260da11eb9679e7245f7b6576f202` |
| Verified | `get_evidence("ev-1")` → `status: valid`; page SHA-256 `c0535e4be2b79ffd93291305436bf889314e4a3faec05ecffcbb7df31ad9e51a` |

Source commit: `985e264` — https://github.com/valentinzubok/MetaEvidence/blob/main/contracts/MetaEvidence.py

## Title

```text
MetaEvidence v0.2 — live URL freeze + schema audit under eq_principle_strict_eq
```

## Notes (paste into Portal)

```text
MetaEvidence v0.2 registers JSON schemas and freezes live HTTPS pages via get_webpage under eq_principle_strict_eq on attach_evidence, then audits by re-fetching the same digest and validating metadata against the schema. Invalid records can appeal (max 3) with the same strict_eq path.

Lifecycle: register_schema → attach_evidence (freeze URL + metadata) → audit → valid|invalid → appeal.

Studionet smoke (all FINALIZED SUCCESS):
- Contract: 0xF39330E2233E612CCcbAb1B148C94b136dEAE54C
- Deploy: 0x058e2863f9d600958a5730d0ebb842226742ff25710997df478f6281567c88c9
- register_schema("model-v1", …): 0xcaf61a3b681bdf5da3a5fd3f6638fac9a0503ac3aa23cca5689b3feeab4e679d
- attach_evidence("ev-1", "model-v1", hello.html URL, metadata): 0x2297ba643d1df8f12e5857e2c07ca4c14293b3e57261b07f7f6298fb4cf1cd8d
- audit("ev-1") → valid: 0x4562f5e816a083b3dfd6672eb7ca8d360df260da11eb9679e7245f7b6576f202

GitHub: https://github.com/valentinzubok/MetaEvidence (commit 985e264)
Demo: https://valentinzubok.github.io/MetaEvidence/
Explorer: https://explorer-studio.genlayer.com/address/0xF39330E2233E612CCcbAb1B148C94b136dEAE54C
```

## Evidence links

1. https://github.com/valentinzubok/MetaEvidence
2. https://github.com/valentinzubok/MetaEvidence/blob/main/contracts/MetaEvidence.py
3. https://valentinzubok.github.io/MetaEvidence/
4. https://explorer-studio.genlayer.com/address/0xF39330E2233E612CCcbAb1B148C94b136dEAE54C
5. https://explorer-studio.genlayer.com/tx/0x058e2863f9d600958a5730d0ebb842226742ff25710997df478f6281567c88c9
6. https://explorer-studio.genlayer.com/tx/0xcaf61a3b681bdf5da3a5fd3f6638fac9a0503ac3aa23cca5689b3feeab4e679d
7. https://explorer-studio.genlayer.com/tx/0x2297ba643d1df8f12e5857e2c07ca4c14293b3e57261b07f7f6298fb4cf1cd8d
8. https://explorer-studio.genlayer.com/tx/0x4562f5e816a083b3dfd6672eb7ca8d360df260da11eb9679e7245f7b6576f202
