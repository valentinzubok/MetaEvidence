# Intelligent Contract — MetaEvidence (source of truth)

GenLayer IC for schema passports with live URL freeze under `eq_principle_strict_eq`.

| Item | Value |
|------|--------|
| File | [`MetaEvidence.py`](./MetaEvidence.py) |
| Studio Dev (61997) | [`0x29f558390ac213D5697a4cf46e707111c0741122`](https://explorer-studio-dev.genlayer.com/address/0x29f558390ac213D5697a4cf46e707111c0741122) |
| Legacy Studionet (61999) | `0xF39330E2233E612CCcbAb1B148C94b136dEAE54C` (v0.2, superseded) |
| App bindings | [`web/src/lib/contracts.ts`](../web/src/lib/contracts.ts) |

## Method alignment (app ↔ contract)

| App call (`web/src/lib/contracts.ts`) | Contract method | Kind |
|---------------------------------------|-----------------|------|
| `listIds()` | `list_ids()` | view |
| `getEvidence(id)` | `get_evidence(evidence_id)` | view |
| `getStats()` | `get_stats()` | view |
| `registerSchema(...)` | `register_schema(schema_id, json_schema)` | write |
| `attachEvidence(...)` | `attach_evidence(evidence_id, schema_id, source_url, metadata_json)` | write — `gl.get_webpage` + SHA-256 under `eq_principle_strict_eq` |
| `auditEvidence(...)` | `audit(evidence_id)` | write — re-fetch + schema check |
| `appealEvidence(...)` | `appeal(evidence_id)` | write — max 3 appeals on invalid records |

## Core consensus path

1. `attach_evidence` → `_capture_source(url)` via `gl.get_webpage` → normalize → SHA-256 digest frozen under `eq_principle_strict_eq`
2. `audit` / `appeal` → re-fetch same URL → compare digest + validate metadata against registered JSON schema

## Deploy (Studio)

Constructor: `owner_address` (0x). Paste [`MetaEvidence.py`](./MetaEvidence.py) into [GenLayer Studio](https://studio.genlayer.com/contracts).
