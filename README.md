# MetaEvidence

<p align="center">
  <img src="assets/cover.png" alt="MetaEvidence — Schema audit. Public passport." width="100%" />
</p>

<p align="center">
  <strong>Schema audit. Public passport.</strong>
</p>

<p align="center">
  <a href="https://metaevidence-console.vercel.app"><img src="https://img.shields.io/badge/Live-Console-6366f1?style=flat-square" alt="Live console" /></a>
  <a href="https://github.com/valentinzubok/MetaEvidence/actions/workflows/ci.yml"><img src="https://github.com/valentinzubok/MetaEvidence/actions/workflows/ci.yml/badge.svg" alt="CI" /></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="License: MIT" /></a>
</p>

---

## What it is

**MetaEvidence** is a GenLayer product for **evidence passports**: register JSON schemas, freeze live HTTPS pages on-chain, audit metadata against schema, and appeal invalid records.

| Layer | What |
|-------|------|
| **Intelligent Contract** | [`contracts/MetaEvidence.py`](contracts/MetaEvidence.py) — `get_webpage` + `eq_principle_strict_eq` freeze, schema audit |
| **Console (Project)** | [`web/`](web/) — Next.js dApp on GenLayer Studio Dev (chain 61997) via **genlayer-js** + MetaMask |

**Live console:** https://metaevidence-console.vercel.app  
**Studio Dev (61997):** [`0x29f558390ac213D5697a4cf46e707111c0741122`](https://explorer-studio-dev.genlayer.com/address/0x29f558390ac213D5697a4cf46e707111c0741122) · on-chain code sha256 = `contracts/MetaEvidence.py` · [deploy record](STUDIO_DEV_DEPLOY.md)

Reads (`list_ids`, `get_evidence`) work **without wallet** — click **Refresh**. Writes need MetaMask on Studio Dev (the app switches the wallet to chain 61997; use **Get test GEN** for fees).

> Static flow preview (localStorage mock, not on-chain): [GitHub Pages demo](https://valentinzubok.github.io/MetaEvidence/) — for UI sketch only.

---

## Features

- **Schema registry** — `register_schema`
- **Live URL freeze** — `attach_evidence` under consensus digest
- **Audit / appeal** — `audit`, `appeal` (max 3)
- **Method map** — [`contracts/README.md`](contracts/README.md) ↔ [`web/src/lib/contracts.ts`](web/src/lib/contracts.ts)

---

## Quick start (console)

```bash
git clone https://github.com/valentinzubok/MetaEvidence.git
cd MetaEvidence/web
npm install
npm run dev   # http://localhost:3001
```

1. Open console → **Refresh** (see on-chain `ev-1` from smoke)
2. **Connect MetaMask** for attach / audit / appeal

Contract tests:

```bash
cd ..
pip install -r requirements-dev.txt
coverage run -m pytest -q && coverage report -m
```

---

## Portal

- **Intelligent Contracts** — see [`SUBMIT.md`](SUBMIT.md)
- **Projects** — see [`PROJECT_SUBMIT.md`](PROJECT_SUBMIT.md)

Screenshot for stewards: [`docs/console-screenshot.png`](docs/console-screenshot.png)

## API

See [`docs/API.md`](docs/API.md).

## License

MIT © 2026 Valentyn Zubok.
