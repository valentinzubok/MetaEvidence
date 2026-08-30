# MetaEvidence API

## Write methods

| Method | Inputs | Notes |
|--------|--------|-------|
| `register_schema(schema_id, json_schema)` | strings | JSON object with `required` + `properties` |
| `attach_evidence(evidence_id, schema_id, data_hash, metadata_json)` | strings | SHA-256 hex of canonical metadata JSON |
| `audit(evidence_id)` | id | `eq_principle_strict_eq` field + hash check |
| `set_fee(receiver, amount)` | 0x, digit string | Owner only |
| `transfer_ownership(new_owner)` | 0x | Owner only |

## View methods

| Method | Returns |
|--------|---------|
| `get_schema(schema_id)` | schema record |
| `get_evidence(evidence_id)` | evidence record |
| `get_audit_result(audit_id)` | `{status, report, …}` |
| `list_ids` | evidence ids |
| `list_by_status(status)` | `pending_audit` / `valid` / `invalid` |
| `get_events` / `get_owner` / `get_fee` / `get_stats` | JSON |

## Lifecycle

`SchemaRegistered` → `EvidenceAttached (pending_audit)` → `audit` → `valid` | `invalid`

## Events

`SchemaRegistered`, `EvidenceAttached`, `AuditPerformed`, `AuditResult`, `FeeUpdated`, `OwnershipTransferred`

## Limits

| Constant | Value |
|----------|-------|
| `MAX_SCHEMA_LEN` | 4096 |
| `MAX_META_LEN` | 4096 |
| `MAX_ID_LEN` | 64 |
| `MAX_AUDITS` | 500 (rolling trim) |

## Example (Studio)

```text
register_schema("model-v1", '{"required":["model","version"],"properties":{"model":{"type":"string"},"version":{"type":"string"}}}')
attach_evidence("ev-1", "model-v1", "<sha256-hex>", '{"model":"gpt-demo","version":"1.0"}')
audit("ev-1")
get_audit_result("audit-1")
```

## Errors

- `duplicate schema_id` / `duplicate evidence_id`
- `unknown schema_id — register first`
- `data_hash must be a 64-char sha256 hex digest`
- `metadata_json must be valid JSON`
