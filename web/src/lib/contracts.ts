import { CONTRACT_ADDRESS } from "./config";
import type { Address } from "./genlayer";
import { parseJson, readContract, writeAndWait } from "./genlayer";

export type EvidenceRow = {
  evidence_id: string;
  schema_id: string;
  source_url: string;
  data_hash: string;
  status: string;
  preview?: string;
  appeals?: number;
};

export type Stats = {
  total: number;
  pending_audit: number;
  valid: number;
  invalid: number;
};

export async function listIds(): Promise<string[]> {
  const raw = await readContract<string>(CONTRACT_ADDRESS, "list_ids", []);
  return parseJson<string[]>(raw, []);
}

export async function getEvidence(id: string): Promise<EvidenceRow | null> {
  const raw = await readContract<string>(CONTRACT_ADDRESS, "get_evidence", [id]);
  const parsed = parseJson<EvidenceRow & { error?: string }>(raw, {} as EvidenceRow);
  if ("error" in parsed && parsed.error) return null;
  return parsed.evidence_id ? parsed : null;
}

export async function getStats(): Promise<Stats | null> {
  const raw = await readContract<string>(CONTRACT_ADDRESS, "get_stats", []);
  return parseJson<Stats | null>(raw, null);
}

export async function registerSchema(
  account: Address,
  provider: unknown,
  schemaId: string,
  jsonSchema: string,
): Promise<string> {
  return writeAndWait(account, provider, CONTRACT_ADDRESS, "register_schema", [
    schemaId,
    jsonSchema,
  ]);
}

export async function attachEvidence(
  account: Address,
  provider: unknown,
  evidenceId: string,
  schemaId: string,
  sourceUrl: string,
  metadataJson: string,
): Promise<string> {
  return writeAndWait(account, provider, CONTRACT_ADDRESS, "attach_evidence", [
    evidenceId,
    schemaId,
    sourceUrl,
    metadataJson,
  ]);
}

export async function auditEvidence(
  account: Address,
  provider: unknown,
  evidenceId: string,
): Promise<string> {
  return writeAndWait(account, provider, CONTRACT_ADDRESS, "audit", [evidenceId]);
}

export async function appealEvidence(
  account: Address,
  provider: unknown,
  evidenceId: string,
): Promise<string> {
  return writeAndWait(account, provider, CONTRACT_ADDRESS, "appeal", [evidenceId]);
}
