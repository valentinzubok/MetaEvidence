# MetaEvidence — Studio Dev (chain 61997) deploy record

| | |
|---|---|
| **Network** | GenLayer Studio Dev / Studio Next — chain `61997`, GenVM `v0.3.0-rc7` |
| **RPC** | `https://studio-dev.genlayer.com/api` |
| **Contract** | [`0x29f558390ac213D5697a4cf46e707111c0741122`](https://explorer-studio-dev.genlayer.com/address/0x29f558390ac213D5697a4cf46e707111c0741122) |
| **Owner** | `0x6f6077eC587f2964d30aCE8D803Edc27988046e3` |
| **Source** | [`contracts/MetaEvidence.py`](contracts/MetaEvidence.py) — runner `py-genlayer:5jycge4q8k23462jtb0b9fyey1s9qz928sz2nbrd9mg4sxqg2qng` |
| **Source sha256** | `a6c69a843a80a69f88daf678c809d04e7bab9f3ecb6f5e845966a59b7909e715` |
| **App** | https://metaevidence-console.vercel.app (source: [`web/`](web/)) |

## Verify the source yourself

```bash
curl -s -X POST https://studio-dev.genlayer.com/api -H 'content-type: application/json' \
  -d '{"jsonrpc":"2.0","id":1,"method":"gen_getContractCode","params":["0x29f558390ac213D5697a4cf46e707111c0741122"]}' \
  | python3 -c "import sys,json,base64,hashlib; print(hashlib.sha256(base64.b64decode(json.load(sys.stdin)['result'])).hexdigest())"
shasum -a 256 contracts/MetaEvidence.py
# both print a6c69a843a80a69f88daf678c809d04e7bab9f3ecb6f5e845966a59b7909e715
```

## On-chain lifecycle (all `ACCEPTED`, execution `SUCCESS`)

| # | Step | Result | Tx |
|---|------|--------|----|
| 0 | deploy (`owner_address` = `0x6f60…46e3`) | contract created | `0x54c3bd4ab87ab8a4ae223f77874213cc7aeff14e5ce4c94eb3bad8c4447216cb` |
| 1 | `register_schema("model-v1", {required: model, version})` | schema stored | `0x5a9ab7d70680e462669c5ccd1c48dbac2bacc9aee62d556cddf226dce0e16a3d` |
| 2 | `attach_evidence("ev-1", …, hello.html, {model, version})` | page frozen, sha256 `c0535e4b…` | `0x5449702c70915c2abb9d17a8a4f73ad68132d8e4bdaec3f3de594be7a3bc1efd` |
| 3 | `audit("ev-1")` | **valid** (hash match + schema ok) | `0xf53e26d8a8fdf3c48faa71f03a7c7df724f6d62c7bfe72351d592a9d9aa2a749` |
| 4 | `attach_evidence("ev-2", …, {model})` — `version` missing | page frozen | `0xf89a21f50fc9d8793b4b8b6bada9bef3dd8ff42792b264ef8cf04f4b4faccc8d` |
| 5 | `audit("ev-2")` | **invalid** (schema check fails) | `0xbfe00885cac374977b5120707b50ef19f11ff038fe13a80280af1fd1286bd6ed` |
| 6 | `appeal("ev-2")` | re-audited, still **invalid**, `appeals: 1` | `0xb7757b86c0933e284509a13e61644e3f788b02f597fb9e8f88a12f6bfbb35ac4` |

Resulting state (`get_stats`): `{"schemas":1,"evidence_total":2,"pending_audit":0,"valid":1,"invalid":1,"audits":3,"max_appeals":3}`

## Reproducible app path

1. Open https://metaevidence-console.vercel.app. With no wallet connected, the table loads `list_ids` / `get_evidence`
   from the contract above: `ev-1 valid`, `ev-2 invalid`, with the frozen sha256.
2. **Connect MetaMask**. The app adds or switches to chain 61997 (`GenLayer Studio Dev`). Click **Get test GEN** if the fee balance is 0.
3. **Attach evidence** with a new `evidence_id` (for example `ev-app-1`). Validators fetch `source_url` and agree on its SHA-256 under `eq_principle.strict_eq`.
4. Click **audit** on the new row. Validators re-fetch the page, compare the hash, schema-check the metadata, and set the status to `valid` or `invalid`.
5. For an `invalid` row, click **appeal** (max 3). Each action shows the tx hash linked to the explorer, and the table refreshes from chain.

The earlier Studionet (61999) deployment `0xF39330…E54C` ran v0.2 and is superseded.
