# Portal — MetaEvidence (Intelligent Contracts) · Studionet smoke DONE

## Smoke (FINALIZED — 20 validators)

| Item | Value |
|------|--------|
| Address | `0x51313B5783B10bA164C83754EBA40831239B9698` |
| Owner | `0x6f6077eC587f2964d30aCE8D803Edc27988046e3` |
| Explorer | https://explorer-studio.genlayer.com/address/0x51313B5783B10bA164C83754EBA40831239B9698 |
| Deploy | `0xaa5af4883b7ff67e1b8a40224f7dfa18e926f734f302cfd88f58f3b4465af7be` |
| register_schema | `0xf33bcbeb9408eb6a22ab24b8adfd53e94e7b52be973f7f9edf9beeae8554354b` |
| attach_evidence | `0xe0d464b95696fcce5ad61710427bda4388e586f907bd43aed92a96105f1c1618` |
| audit | `0xa74ce369e130993ce16ce580287ee6c67edc65168a72ae36243a07731036088a` |
| data_hash (ev-1) | `ea193544dd98f34124518ae5972152fb66f83f6f634db6157bb2ebaa1b7051ee` |

Verified: `get_evidence("ev-1")` → `status=valid`, `hash_match=true`, `missing_fields=[]`. Zero ERROR/UNDETERMINED.

> Note: if Portal rejects a tx link, re-copy `register_schema` hash from Explorer (must be 66 chars with `0x`).

## Contribution Type

**Builder → Intelligent Contracts**

## Title

```text
MetaEvidence — JSON schema audit passport (register → attach → audit) on GenLayer
```

## Notes / Description (paste into Portal)

```text
MetaEvidence registers JSON schemas for external resources (AI models, APIs, datasets), attaches metadata + SHA-256 data_hash, and audits compliance under eq_principle_strict_eq (required fields, types, hash match).

Lifecycle covered on Studionet (Normal / Full Consensus, 20 validators): register_schema → attach_evidence → audit → status=valid (hash_match=true). All txs FINALIZED. Zero ERROR/UNDETERMINED.

Use case: public “passport” for model cards / API version claims — independent of publisher code.

GitHub: https://github.com/valentinzubok/MetaEvidence
Studionet: 0x51313B5783B10bA164C83754EBA40831239B9698
Deploy: 0xaa5af4883b7ff67e1b8a40224f7dfa18e926f734f302cfd88f58f3b4465af7be
register_schema: 0xf33bcbeb9408eb6a22ab24b8adfd53e94e7b52be973f7f9edf9beeae8554354b
attach_evidence: 0xe0d464b95696fcce5ad61710427bda4388e586f907bd43aed92a96105f1c1618
audit: 0xa74ce369e130993ce16ce580287ee6c67edc65168a72ae36243a07731036088a
data_hash: ea193544dd98f34124518ae5972152fb66f83f6f634db6157bb2ebaa1b7051ee
Explorer: https://explorer-studio.genlayer.com/address/0x51313B5783B10bA164C83754EBA40831239B9698
```

## Evidence links (Portal)

1. https://github.com/valentinzubok/MetaEvidence
2. https://github.com/valentinzubok/MetaEvidence/blob/main/contracts/MetaEvidence.py
3. https://explorer-studio.genlayer.com/address/0x51313B5783B10bA164C83754EBA40831239B9698
4. https://explorer-studio.genlayer.com/tx/0xaa5af4883b7ff67e1b8a40224f7dfa18e926f734f302cfd88f58f3b4465af7be
5. https://explorer-studio.genlayer.com/tx/0xe0d464b95696fcce5ad61710427bda4388e586f907bd43aed92a96105f1c1618
6. https://explorer-studio.genlayer.com/tx/0xa74ce369e130993ce16ce580287ee6c67edc65168a72ae36243a07731036088a
