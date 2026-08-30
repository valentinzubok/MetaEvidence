# MetaEvidence API (v0.2)

## Write methods

| Method | Inputs | Notes |
|--------|--------|-------|
| `register_schema(schema_id, json_schema)` | strings | JSON object with `required` + typed `properties` |
| `attach_evidence(evidence_id, schema_id, source_url, metadata_json)` | strings | Freezes live `get_webpage` SHA-256 under `eq_principle_strict_eq` |
| `audit(evidence_id)` | id | Re-fetch + schema check; **only** while `pending_audit` |
| `appeal(evidence_id)` | id | Re-check `invalid` only; ≤3 |
| `set_fee(receiver, amount)` | 0x, digit string | Bookkeeping hint (no native payout) |
| `transfer_ownership(new_owner)` | 0x | Owner only |

## View methods

| Method | Returns |
|--------|---------|
| `get_schema` / `get_evidence` / `get_audit_result` | JSON records |
| `list_ids` / `list_by_status` | arrays |
| `get_events` / `get_owner` / `get_fee` / `get_stats` | JSON |

## Lifecycle

`register_schema` → `attach_evidence` (pending) → `audit` → `valid` \| `invalid` → `appeal` (max 3)

## Limits

| Constant | Value |
|----------|-------|
| `MAX_APPEALS` | 3 |
| `MAX_SCHEMA_LEN` / `MAX_META_LEN` | 4096 |
| `MAX_ID_LEN` | 64 |
| `source_url` | https only |

## Example (Studio)

```text
register_schema("model-v1", '{"required":["model","version"],"properties":{"model":{"type":"string"},"version":{"type":"string"}}}')
attach_evidence("ev-1", "model-v1", "https://test-server.genlayer.com/static/genvm/hello.html", '{"model":"gpt-demo","version":"1.0"}')
audit("ev-1")
# if invalid:
appeal("ev-1")
```

## Errors

- `source_url fetch failed or empty — cannot attach`
- `only pending_audit evidence can be audited — use appeal`
- `only invalid evidence can be appealed`
- `appeal limit exceeded (max 3)`
- `unknown schema_id — register first`
