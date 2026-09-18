"use client";

import { useCallback, useEffect, useState } from "react";
import {
  DEFAULT_METADATA,
  DEFAULT_SCHEMA,
  DEMO_URL,
  CHAIN_ID,
  EXPLORER,
  GITHUB,
  SCHEMA_JSON,
  txUrl,
} from "@/lib/config";
import { fundWithTestGen, getNativeBalance } from "@/lib/genlayer";
import {
  appealEvidence,
  attachEvidence,
  auditEvidence,
  getEvidence,
  getStats,
  listIds,
  registerSchema,
  type EvidenceRow,
} from "@/lib/contracts";
import { useWallet } from "./WalletProvider";

export function MetaEvidenceApp() {
  const { address, provider, ready, error, connect } = useWallet();
  const [ids, setIds] = useState<string[]>([]);
  const [rows, setRows] = useState<EvidenceRow[]>([]);
  const [stats, setStats] = useState<string>("");
  const [loading, setLoading] = useState(true);
  const [busy, setBusy] = useState("");
  const [tx, setTx] = useState("");
  const [msg, setMsg] = useState("");
  const [gen, setGen] = useState("");

  const [evidenceId, setEvidenceId] = useState("ev-app-1");
  const [sourceUrl, setSourceUrl] = useState(DEMO_URL);
  const [metadata, setMetadata] = useState(DEFAULT_METADATA);

  const refresh = useCallback(async () => {
    setLoading(true);
    setMsg("");
    try {
      const list = await listIds();
      setIds(list);
      const loaded = await Promise.all(list.map((id) => getEvidence(id)));
      setRows(loaded.filter(Boolean) as EvidenceRow[]);
      const s = await getStats();
      setStats(s ? JSON.stringify(s) : "");
      if (address) setGen(await getNativeBalance(address));
    } catch (e) {
      setMsg(`Error: ${e instanceof Error ? e.message : "read failed"}`);
    } finally {
      setLoading(false);
    }
  }, [address]);

  useEffect(() => {
    void refresh();
  }, [refresh]);

  const run = async (label: string, fn: () => Promise<string | void>) => {
    if (!address || !provider) {
      setMsg("Connect MetaMask for write transactions");
      return;
    }
    setBusy(label);
    setMsg("");
    setTx("");
    try {
      const hash = await fn();
      if (hash) setTx(hash);
      setMsg(`${label} submitted (ACCEPTED) — data refreshed`);
      await refresh();
    } catch (e) {
      setMsg(`Error: ${e instanceof Error ? e.message : String(e)}`);
    } finally {
      setBusy("");
    }
  };

  return (
    <main className="wrap">
      <header>
        <h1>MetaEvidence Console</h1>
        <p className="muted">
          Schema passport on GenLayer Studio Dev (chain {CHAIN_ID}) — register schemas, freeze
          live URLs, audit metadata, appeal invalid records. Every value below is read from the
          contract; reads work without a wallet.
        </p>
        <div className="row">
          {address ? (
            <span className="pill ok">
              {address.slice(0, 6)}…{address.slice(-4)}
            </span>
          ) : (
            <button type="button" onClick={() => void connect()}>
              Connect MetaMask
            </button>
          )}
          {address && (
            <button
              type="button"
              className="ghost"
              disabled={!!busy}
              onClick={() =>
                void run("faucet", () => fundWithTestGen(address as `0x${string}`))
              }
            >
              Get test GEN{gen ? ` (${gen})` : ""}
            </button>
          )}
          <button type="button" className="ghost" onClick={() => void refresh()} disabled={loading}>
            {loading ? "Loading…" : "Refresh"}
          </button>
        </div>
        {error && <p className="msg">{error}</p>}
        {msg && <p className={msg.startsWith("Error") ? "msg" : "okmsg"}>{msg}</p>}
        {busy && <p className="muted">Waiting for GenLayer consensus: {busy}…</p>}
        {tx && (
          <p className="tx">
            tx:{" "}
            <a href={txUrl(tx)} target="_blank" rel="noreferrer">
              {tx}
            </a>
          </p>
        )}
        {stats && <p className="muted">on-chain stats: {stats}</p>}
      </header>

      <section className="grid">
        <div className="card">
          <h2>Register schema</h2>
          <p className="muted">Wallet required. Fails if model-v1 already exists.</p>
          <button
            type="button"
            disabled={!ready || !!busy}
            onClick={() =>
              void run("register_schema", () =>
                registerSchema(address!, provider, DEFAULT_SCHEMA, SCHEMA_JSON),
              )
            }
          >
            register_schema(&quot;{DEFAULT_SCHEMA}&quot;)
          </button>
        </div>

        <div className="card">
          <h2>Attach evidence</h2>
          <label>evidence_id</label>
          <input value={evidenceId} onChange={(e) => setEvidenceId(e.target.value)} />
          <label>source_url</label>
          <input value={sourceUrl} onChange={(e) => setSourceUrl(e.target.value)} />
          <label>metadata_json</label>
          <textarea rows={3} value={metadata} onChange={(e) => setMetadata(e.target.value)} />
          <button
            type="button"
            disabled={!ready || !!busy}
            onClick={() =>
              void run("attach_evidence", () =>
                attachEvidence(
                  address!,
                  provider,
                  evidenceId,
                  DEFAULT_SCHEMA,
                  sourceUrl,
                  metadata,
                ),
              )
            }
          >
            attach_evidence
          </button>
        </div>
      </section>

      <section className="card">
        <h2>On-chain evidence ({loading ? "…" : ids.length})</h2>
        {loading && <p className="muted">Loading from Studio Dev…</p>}
        {!loading && ids.length === 0 && (
          <p className="muted">No records yet — smoke deploy has ev-1 on chain; try Refresh.</p>
        )}
        <table>
          <thead>
            <tr>
              <th>id</th>
              <th>status</th>
              <th>hash</th>
              <th>actions</th>
            </tr>
          </thead>
          <tbody>
            {rows.map((r) => (
              <tr key={r.evidence_id}>
                <td>{r.evidence_id}</td>
                <td className={r.status === "valid" ? "ok" : r.status === "invalid" ? "bad" : ""}>
                  {r.status}
                </td>
                <td className="mono">{(r.data_hash || "").slice(0, 12)}…</td>
                <td className="row">
                  {r.status === "pending_audit" && (
                    <button
                      type="button"
                      disabled={!ready || !!busy}
                      onClick={() =>
                        void run("audit", () => auditEvidence(address!, provider, r.evidence_id))
                      }
                    >
                      audit
                    </button>
                  )}
                  {r.status === "invalid" && (
                    <button
                      type="button"
                      disabled={!ready || !!busy}
                      onClick={() =>
                        void run("appeal", () =>
                          appealEvidence(address!, provider, r.evidence_id),
                        )
                      }
                    >
                      appeal
                    </button>
                  )}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </section>

      <footer className="footer">
        <a href={GITHUB} target="_blank" rel="noreferrer">
          GitHub
        </a>
        <a href={EXPLORER} target="_blank" rel="noreferrer">
          Studio Dev contract
        </a>
        <span className="muted">IC source: contracts/MetaEvidence.py · bindings: web/src/lib/contracts.ts</span>
      </footer>
    </main>
  );
}
