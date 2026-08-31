export const CONTRACT_ADDRESS = (process.env.NEXT_PUBLIC_METAEVIDENCE_ADDRESS ??
  "0xF39330E2233E612CCcbAb1B148C94b136dEAE54C") as `0x${string}`;

export const EXPLORER =
  "https://explorer-studio.genlayer.com/address/0xF39330E2233E612CCcbAb1B148C94b136dEAE54C";

export const DEMO_URL = "https://test-server.genlayer.com/static/genvm/hello.html";

export const DEFAULT_SCHEMA = "model-v1";

export const SCHEMA_JSON =
  '{"required":["model","version"],"properties":{"model":{"type":"string"},"version":{"type":"string"}}}';

export const DEFAULT_METADATA = '{"model":"gpt-demo","version":"1.0"}';
