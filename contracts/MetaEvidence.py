# { "Depends": "py-genlayer:15qfivjvy80800rh998pcxmd2m8va1wq2qzqhz850n8ggcr4i9q0" }

from genlayer import *
import hashlib
import json
import re

# MetaEvidence v0.2 — schema passport with live URL fetch under strict_eq.
# Copyright (c) 2026 Valentyn Zubok. MIT License.
#
# Lifecycle: register_schema → attach_evidence → audit → valid|invalid → appeal (max 3).
# Consensus: eq_principle_strict_eq over get_webpage digest + deterministic schema check.
# Fee fields are bookkeeping hints for indexers (no native payout on Studionet).

MAX_ID_LEN = 64
MAX_SCHEMA_LEN = 4096
MAX_META_LEN = 4096
MAX_AUDITS = 500
MAX_APPEALS = 3
PREVIEW_CHARS = 280
HASH_ALGO = "sha256"

STATUS_PENDING = "pending_audit"
STATUS_VALID = "valid"
STATUS_INVALID = "invalid"

ADDR_RE = re.compile(r"^0x[a-fA-F0-9]{40}$")
HTTPS_URL_RE = re.compile(r"^https://[^\s<>\"']+$", re.IGNORECASE)


def _normalize_id(value: str, label: str = "id") -> str:
    eid = str(value).strip()
    if not eid:
        raise Exception(f"{label} is required")
    if len(eid) > MAX_ID_LEN:
        raise Exception(f"{label} exceeds 64 chars")
    for ch in eid:
        ok = ("a" <= ch.lower() <= "z") or ("0" <= ch <= "9") or ch in "-_/"
        if not ok:
            raise Exception(f"{label}: only a-z, 0-9, -, _, /")
    return eid


def _require_address(label: str, value: str) -> str:
    addr = str(value).strip()
    if not ADDR_RE.match(addr):
        raise Exception(f"{label} must be a 0x address")
    return addr


def _hash_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _normalize(text: str) -> str:
    return " ".join(str(text).split())


def _require_https(url: str) -> str:
    u = str(url).strip()
    if not HTTPS_URL_RE.match(u):
        raise Exception("source_url must be https:// with no whitespace")
    if len(u) > 2048:
        raise Exception("source_url exceeds 2048 chars")
    return u


def _parse_schema(json_schema: str) -> dict:
    raw = str(json_schema).strip()
    if len(raw) > MAX_SCHEMA_LEN:
        raise Exception("json_schema exceeds 4096 chars")
    try:
        parsed = json.loads(raw)
    except Exception:
        raise Exception("json_schema must be valid JSON")
    if not isinstance(parsed, dict):
        raise Exception("json_schema must be a JSON object")
    required = parsed.get("required", [])
    if not isinstance(required, list):
        raise Exception("schema.required must be an array")
    props = parsed.get("properties", {})
    if props is not None and not isinstance(props, dict):
        raise Exception("schema.properties must be an object")
    return parsed


def _parse_metadata(metadata_json: str) -> dict:
    raw = str(metadata_json).strip()
    if len(raw) > MAX_META_LEN:
        raise Exception("metadata_json exceeds 4096 chars")
    try:
        parsed = json.loads(raw)
    except Exception:
        raise Exception("metadata_json must be valid JSON")
    if not isinstance(parsed, dict):
        raise Exception("metadata_json must be a JSON object")
    return parsed


def _json_type_ok(value, expected_type: str) -> bool:
    if expected_type == "string":
        return isinstance(value, str)
    if expected_type == "integer":
        return isinstance(value, int) and not isinstance(value, bool)
    if expected_type == "number":
        return isinstance(value, (int, float)) and not isinstance(value, bool)
    if expected_type == "boolean":
        return isinstance(value, bool)
    if expected_type == "array":
        return isinstance(value, list)
    if expected_type == "object":
        return isinstance(value, dict)
    return False


def _capture_source(url: str) -> str:
    entry = {
        "url": url,
        "content_hash": "",
        "hash_algo": HASH_ALGO,
        "preview": "",
        "byte_len": 0,
        "status": "error",
    }
    try:
        raw = gl.get_webpage(url, mode="text")
        if raw is None or str(raw).strip() == "":
            raw = gl.get_webpage(url, mode="html")
        normalized = _normalize(raw if raw is not None else "")
        if normalized == "":
            entry["status"] = "empty"
        else:
            entry["content_hash"] = _hash_text(normalized)
            entry["preview"] = normalized[:PREVIEW_CHARS]
            entry["byte_len"] = len(normalized)
            entry["status"] = "ok"
    except Exception as exc:
        entry["preview"] = str(exc)[:120]
        entry["status"] = "error"
    return json.dumps(entry, sort_keys=True, separators=(",", ":"))


def _schema_check(schema: dict, metadata: dict) -> dict:
    required = schema.get("required", [])
    props = schema.get("properties", {}) or {}
    missing = []
    type_mismatch = []
    for field in required:
        if field not in metadata:
            missing.append(field)
            continue
        expected = props.get(field, {})
        expected_type = expected.get("type")
        if expected_type and not _json_type_ok(metadata[field], expected_type):
            type_mismatch.append({"field": field, "expected": expected_type})
    return {
        "missing_fields": missing,
        "type_mismatch": type_mismatch,
        "schema_ok": len(missing) == 0 and len(type_mismatch) == 0,
    }


def _build_audit_report(schema: dict, metadata: dict, declared_hash: str, source_url: str) -> str:
    live = json.loads(_capture_source(source_url))
    live_hash = live.get("content_hash", "")
    hash_match = live.get("status") == "ok" and live_hash == str(declared_hash).strip()
    schema_part = _schema_check(schema, metadata)
    valid = bool(hash_match and schema_part["schema_ok"])
    return json.dumps(
        {
            "valid": valid,
            "hash_match": hash_match,
            "live_status": live.get("status"),
            "live_hash": live_hash,
            "declared_hash": declared_hash,
            "missing_fields": schema_part["missing_fields"],
            "type_mismatch": schema_part["type_mismatch"],
            "preview": live.get("preview", "")[:PREVIEW_CHARS],
        },
        sort_keys=True,
        separators=(",", ":"),
    )


class MetaEvidence(gl.Contract):
    owner: str
    fee_receiver: str
    fee_per_audit: str
    schemas_json: str
    evidence_json: str
    audits_json: str
    order_json: str
    audit_seq: str
    events_json: str

    def __init__(self, owner_address: str):
        self.owner = _require_address("owner_address", owner_address)
        self.fee_receiver = self.owner
        self.fee_per_audit = "0"
        self.schemas_json = "{}"
        self.evidence_json = "{}"
        self.audits_json = "{}"
        self.order_json = "[]"
        self.audit_seq = "0"
        self.events_json = "[]"

    def _load_schemas(self):
        return json.loads(self.schemas_json)

    def _save_schemas(self, schemas):
        self.schemas_json = json.dumps(schemas, sort_keys=True, separators=(",", ":"))

    def _load_evidence(self):
        return json.loads(self.evidence_json)

    def _save_evidence(self, evidence):
        self.evidence_json = json.dumps(evidence, sort_keys=True, separators=(",", ":"))

    def _load_audits(self):
        return json.loads(self.audits_json)

    def _save_audits(self, audits):
        self.audits_json = json.dumps(audits, sort_keys=True, separators=(",", ":"))

    def _load_order(self):
        return json.loads(self.order_json)

    def _save_order(self, order):
        self.order_json = json.dumps(order, separators=(",", ":"))

    def _append_event(self, kind: str, payload: dict):
        events = json.loads(self.events_json)
        events.append({"kind": kind, **payload})
        if len(events) > 200:
            events = events[-200:]
        self.events_json = json.dumps(events, separators=(",", ":"))

    def _only_owner(self):
        if str(gl.message.sender_address) != self.owner:
            raise Exception("only owner")

    def _next_audit_id(self) -> str:
        n = int(self.audit_seq) + 1
        self.audit_seq = str(n)
        return f"audit-{n}"

    def _trim_audits(self, audits: dict) -> dict:
        if len(audits) < MAX_AUDITS:
            return audits

        # FIFO by numeric suffix of audit-N
        def _num(k):
            try:
                return int(str(k).split("-")[-1])
            except Exception:
                return 0

        keep_n = MAX_AUDITS - 50
        ordered = sorted(audits.keys(), key=_num)
        keep = ordered[-keep_n:]
        return {k: audits[k] for k in keep}

    def _run_audit(self, eid: str, entry: dict, via: str) -> dict:
        schemas = self._load_schemas()
        sid = entry["schema_id"]
        if sid not in schemas:
            raise Exception("unknown schema_id")
        schema = json.loads(schemas[sid]["json_schema"])
        metadata = json.loads(entry["metadata_json"])
        source_url = entry["source_url"]
        declared = entry["data_hash"]

        def leader_fn() -> str:
            return _build_audit_report(schema, metadata, declared, source_url)

        report_json = gl.eq_principle_strict_eq(leader_fn)
        report = json.loads(report_json)
        valid = bool(report.get("valid"))
        status = STATUS_VALID if valid else STATUS_INVALID

        audit_id = self._next_audit_id()
        audits = self._trim_audits(self._load_audits())
        audits[audit_id] = {
            "audit_id": audit_id,
            "evidence_id": eid,
            "status": status,
            "via": via,
            "report": report,
            "fee_receiver": self.fee_receiver,
            "fee_per_audit": self.fee_per_audit,
            "caller": str(gl.message.sender_address),
        }
        self._save_audits(audits)

        entry["status"] = status
        entry["last_audit_id"] = audit_id
        entry["checks"] = int(entry.get("checks", 0)) + 1
        self._append_event(
            "AuditResult",
            {
                "audit_id": audit_id,
                "evidence_id": eid,
                "valid": valid,
                "via": via,
                "status": status,
            },
        )
        return entry

    @gl.public.write
    def transfer_ownership(self, new_owner: str) -> None:
        self._only_owner()
        self.owner = _require_address("new_owner", new_owner)
        self._append_event("OwnershipTransferred", {"to": self.owner})

    @gl.public.write
    def set_fee(self, receiver: str, amount: str) -> None:
        """Bookkeeping fee hint per audit (no native payout on Studionet)."""
        self._only_owner()
        self.fee_receiver = _require_address("receiver", receiver)
        amt = str(amount).strip()
        if not amt.isdigit():
            raise Exception("amount must be digits only")
        self.fee_per_audit = amt
        self._append_event("FeeUpdated", {"receiver": self.fee_receiver, "amount": amt})

    @gl.public.write
    def register_schema(self, schema_id: str, json_schema: str) -> None:
        sid = _normalize_id(schema_id, "schema_id")
        schemas = self._load_schemas()
        if sid in schemas:
            raise Exception("duplicate schema_id")
        parsed = _parse_schema(json_schema)
        issuer = str(gl.message.sender_address)
        schemas[sid] = {
            "schema_id": sid,
            "json_schema": json.dumps(parsed, sort_keys=True, separators=(",", ":")),
            "issuer": issuer,
        }
        self._save_schemas(schemas)
        self._append_event("SchemaRegistered", {"schema_id": sid, "issuer": issuer})

    @gl.public.write
    def attach_evidence(
        self,
        evidence_id: str,
        schema_id: str,
        source_url: str,
        metadata_json: str,
    ) -> None:
        """Freeze live page digest under strict_eq, attach metadata + schema_id."""
        eid = _normalize_id(evidence_id, "evidence_id")
        sid = _normalize_id(schema_id, "schema_id")
        schemas = self._load_schemas()
        if sid not in schemas:
            raise Exception("unknown schema_id — register first")

        url = _require_https(source_url)
        metadata = _parse_metadata(metadata_json)
        evidence = self._load_evidence()
        if eid in evidence:
            raise Exception("duplicate evidence_id")

        def leader_fn() -> str:
            return _capture_source(url)

        snap_json = gl.eq_principle_strict_eq(leader_fn)
        snap = json.loads(snap_json)
        if snap.get("status") != "ok":
            raise Exception("source_url fetch failed or empty — cannot attach")

        digest = snap["content_hash"]
        issuer = str(gl.message.sender_address)
        evidence[eid] = {
            "evidence_id": eid,
            "schema_id": sid,
            "source_url": url,
            "data_hash": digest,
            "hash_algo": HASH_ALGO,
            "metadata_json": json.dumps(metadata, sort_keys=True, separators=(",", ":")),
            "status": STATUS_PENDING,
            "last_audit_id": "",
            "checks": 0,
            "appeals": 0,
            "issuer": issuer,
            "preview": snap.get("preview", "")[:PREVIEW_CHARS],
        }
        self._save_evidence(evidence)
        order = self._load_order()
        order.append(eid)
        self._save_order(order)
        self._append_event(
            "EvidenceAttached",
            {
                "evidence_id": eid,
                "schema_id": sid,
                "source_url": url,
                "data_hash": digest,
                "issuer": issuer,
            },
        )

    @gl.public.write
    def audit(self, evidence_id: str) -> None:
        """First audit only while pending_audit. Re-check invalid via appeal()."""
        eid = _normalize_id(evidence_id, "evidence_id")
        evidence = self._load_evidence()
        if eid not in evidence:
            raise Exception("unknown evidence_id")
        entry = evidence[eid]
        if entry.get("status") != STATUS_PENDING:
            raise Exception("only pending_audit evidence can be audited — use appeal")
        entry = self._run_audit(eid, entry, via="audit")
        evidence[eid] = entry
        self._save_evidence(evidence)

    @gl.public.write
    def appeal(self, evidence_id: str) -> None:
        """Re-fetch + schema-check an invalid record (max MAX_APPEALS)."""
        eid = _normalize_id(evidence_id, "evidence_id")
        evidence = self._load_evidence()
        if eid not in evidence:
            raise Exception("unknown evidence_id")
        entry = evidence[eid]
        if entry.get("status") != STATUS_INVALID:
            raise Exception("only invalid evidence can be appealed")
        if int(entry.get("appeals", 0)) >= MAX_APPEALS:
            raise Exception("appeal limit exceeded (max 3)")

        entry["appeals"] = int(entry.get("appeals", 0)) + 1
        evidence[eid] = entry
        self._save_evidence(evidence)
        self._append_event(
            "Appeal",
            {
                "id": eid,
                "appeals": entry["appeals"],
                "max_appeals": MAX_APPEALS,
                "caller": str(gl.message.sender_address),
            },
        )

        evidence = self._load_evidence()
        entry = evidence[eid]
        entry = self._run_audit(eid, entry, via="appeal")
        evidence[eid] = entry
        self._save_evidence(evidence)

    @gl.public.view
    def get_schema(self, schema_id: str) -> str:
        sid = _normalize_id(schema_id, "schema_id")
        schemas = self._load_schemas()
        if sid not in schemas:
            return json.dumps({"error": "unknown schema_id"})
        return json.dumps(schemas[sid], sort_keys=True)

    @gl.public.view
    def get_evidence(self, evidence_id: str) -> str:
        eid = _normalize_id(evidence_id, "evidence_id")
        evidence = self._load_evidence()
        if eid not in evidence:
            return json.dumps({"error": "unknown evidence_id"})
        return json.dumps(evidence[eid], sort_keys=True)

    @gl.public.view
    def get_audit_result(self, audit_id: str) -> str:
        aid = _normalize_id(audit_id, "audit_id")
        audits = self._load_audits()
        if aid not in audits:
            return json.dumps({"error": "unknown audit_id"})
        return json.dumps(audits[aid], sort_keys=True)

    @gl.public.view
    def list_ids(self) -> str:
        return self.order_json

    @gl.public.view
    def list_by_status(self, status: str) -> str:
        wanted = str(status).strip().lower()
        evidence = self._load_evidence()
        order = self._load_order()
        ids = [eid for eid in order if eid in evidence and evidence[eid].get("status") == wanted]
        return json.dumps(ids, separators=(",", ":"))

    @gl.public.view
    def get_events(self) -> str:
        return self.events_json

    @gl.public.view
    def get_owner(self) -> str:
        return self.owner

    @gl.public.view
    def get_fee(self) -> str:
        return json.dumps(
            {"receiver": self.fee_receiver, "amount": self.fee_per_audit},
            separators=(",", ":"),
        )

    @gl.public.view
    def get_stats(self) -> str:
        evidence = self._load_evidence()
        pending = valid = invalid = 0
        for e in evidence.values():
            st = e.get("status")
            if st == STATUS_PENDING:
                pending += 1
            elif st == STATUS_VALID:
                valid += 1
            elif st == STATUS_INVALID:
                invalid += 1
        return json.dumps(
            {
                "schemas": len(self._load_schemas()),
                "evidence_total": len(evidence),
                "pending_audit": pending,
                "valid": valid,
                "invalid": invalid,
                "audits": len(self._load_audits()),
                "max_appeals": MAX_APPEALS,
            },
            separators=(",", ":"),
        )
