# Portal — MetaEvidence (Projects)

**Type:** Builder → **Projects** (not Intelligent Contracts — submit IC separately)

## Requirements

- Live app with MetaMask + genlayer-js calling Studionet
- IC source in `contracts/MetaEvidence.py` (same repo)
- Deploy `web/` to Vercel (root directory: `web`)

## Local dev

```bash
cd web && npm install && npm run dev
# http://localhost:3001
```

## Vercel deploy

```bash
cd web
vercel --prod
# Set root to web if deploying from monorepo in Vercel UI
```

Env: `NEXT_PUBLIC_METAEVIDENCE_ADDRESS=0xF39330E2233E612CCcbAb1B148C94b136dEAE54C`

## Title

```text
MetaEvidence — schema passport console (Next.js + Studionet IC)
```

## Notes (paste)

```text
MetaEvidence is a GenLayer Project: a Next.js console where the main workflow is on-chain evidence passports.

Use case: register JSON schemas, attach live HTTPS evidence (get_webpage + strict_eq freeze), audit metadata against schema, appeal invalid records — all via genlayer-js + MetaMask on Studionet.

Intelligent Contract (in-repo): contracts/MetaEvidence.py
Studionet: 0xF39330E2233E612CCcbAb1B148C94b136dEAE54C
App: web/ (Next.js) — https://metaevidence-console.vercel.app
GitHub: https://github.com/valentinzubok/MetaEvidence

Smoke txs (IC, already submitted separately):
Deploy 0x058e2863f9d600958a5730d0ebb842226742ff25710997df478f6281567c88c9
attach 0x2297ba643d1df8f12e5857e2c07ca4c14293b3e57261b07f7f6298fb4cf1cd8d
audit 0x4562f5e816a083b3dfd6672eb7ca8d360df260da11eb9679e7245f7b6576f202
```

## Evidence

1. https://github.com/valentinzubok/MetaEvidence
2. https://metaevidence-console.vercel.app
3. https://github.com/valentinzubok/MetaEvidence/blob/main/contracts/MetaEvidence.py
4. https://explorer-studio.genlayer.com/address/0xF39330E2233E612CCcbAb1B148C94b136dEAE54C
