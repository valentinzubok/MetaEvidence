# Portal — MetaEvidence v0.2 (Intelligent Contracts)

**Type:** Builder → Intelligent Contracts  

Redeploy Studionet with `contracts/MetaEvidence.py` v0.2, then paste txs below.

## Title

```text
MetaEvidence v0.2 — live URL freeze + schema audit under eq_principle_strict_eq
```

## Notes (paste)

```text
MetaEvidence v0.2 freezes HTTPS pages via get_webpage under eq_principle_strict_eq on attach, then audits by re-fetching the live digest and checking JSON-schema required fields/types. Invalid records can appeal (max 3) with the same strict_eq path.

Lifecycle: register_schema → attach_evidence → audit → valid|invalid → appeal.

GitHub: https://github.com/valentinzubok/MetaEvidence
(Replace with new Studionet address + deploy/attach/audit txs after v0.2 smoke.)
```

## Studio smoke checklist

1. Deploy with owner `0x6f6077…`
2. `register_schema("model-v1", …)`
3. `attach_evidence("ev-1", "model-v1", "https://test-server.genlayer.com/static/genvm/hello.html", '{"model":"gpt-demo","version":"1.0"}')`
4. `audit("ev-1")` → `get_evidence` status `valid`
5. Optional: force drift / appeal path
