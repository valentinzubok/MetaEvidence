# MetaEvidence

<p align="center">
  <img src="assets/cover.png" alt="MetaEvidence — Schema audit. Public passport." width="100%" />
</p>

<p align="center">
  <strong>Schema audit. Public passport.</strong>
</p>

<p align="center">
  <a href="https://github.com/valentinzubok/MetaEvidence/actions/workflows/ci.yml"><img src="https://github.com/valentinzubok/MetaEvidence/actions/workflows/ci.yml/badge.svg" alt="CI" /></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="License: MIT" /></a>
  <a href="https://valentinzubok.github.io/MetaEvidence/"><img src="https://img.shields.io/badge/demo-GitHub%20Pages-2dd4bf" alt="Demo" /></a>
</p>

## Overview

**MetaEvidence** registers JSON schemas for external resources (AI models, APIs, datasets) and audits attached metadata under `eq_principle_strict_eq`.

```
register_schema → attach_evidence → audit → valid | invalid
```

| Event | When |
|-------|------|
| `SchemaRegistered` | new schema id |
| `EvidenceAttached` | metadata + data_hash linked |
| `AuditPerformed` / `AuditResult` | consensus field + hash check |

### Why GenLayer

AI providers publish models and APIs with claims (version, signature, license). MetaEvidence turns those claims into an on-chain **audit passport** — independent of the publisher’s code repo.

## Install

```bash
git clone https://github.com/valentinzubok/MetaEvidence.git
cd MetaEvidence
pip install -r requirements-dev.txt
coverage run -m pytest -q && coverage report -m
```

Studio: paste [`contracts/MetaEvidence.py`](contracts/MetaEvidence.py).

## API

See [`docs/API.md`](docs/API.md).

## Demo

```bash
cd demo && python3 -m http.server 5176
```

Live: https://valentinzubok.github.io/MetaEvidence/

## License

MIT © 2026 Valentyn Zubok.
