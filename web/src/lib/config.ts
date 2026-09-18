/** Live MetaEvidence deploy on GenLayer Studio Dev (chain 61997). Override via env. */
export const CONTRACT_ADDRESS = (process.env.NEXT_PUBLIC_METAEVIDENCE_ADDRESS ||
  "0x29f558390ac213D5697a4cf46e707111c0741122") as `0x${string}`;

/** Studio Dev / Studio Next — chain ID 61997. */
export const CHAIN_ID = 61997;
export const RPC_URL =
  process.env.NEXT_PUBLIC_GENLAYER_RPC || "https://studio-dev.genlayer.com/api";
export const EXPLORER_BASE =
  process.env.NEXT_PUBLIC_GENLAYER_EXPLORER || "https://explorer-studio-dev.genlayer.com";
export const EXPLORER = `${EXPLORER_BASE}/address/${CONTRACT_ADDRESS}`;
export const txUrl = (hash: string) => `${EXPLORER_BASE}/tx/${hash}`;

export const GITHUB =
  "https://github.com/valentinzubok/MetaEvidence";

export const DEMO_URL = "https://test-server.genlayer.com/static/genvm/hello.html";

export const DEFAULT_SCHEMA = "model-v1";

export const SCHEMA_JSON =
  '{"required":["model","version"],"properties":{"model":{"type":"string"},"version":{"type":"string"}}}';

export const DEFAULT_METADATA = '{"model":"gpt-demo","version":"1.0"}';
