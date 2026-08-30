# { "Depends": "py-genlayer:15qfivjvy80800rh998pcxmd2m8va1wq2qzqhz850n8ggcr4i9q0" }

from genlayer import *
import hashlib
import json
import re

# MetaEvidence v0.1 — structured metadata audit passport for external resources.
# Copyright (c) 2026 Valentyn Zubok. MIT License.
#
# Lifecycle: register_schema → attach_evidence → pending_audit → valid | invalid
# Audit consensus via eq_principle_strict_eq on deterministic field-check report.

MAX_ID_LEN = 64
MAX_SCHEMA_LEN = 4096
MAX_META_LEN = 4096
MAX_AUDITS = 500

STATUS_PENDING = "pending_audit"
STATUS_VALID = "valid"
STATUS_INVALID = "invalid"

HTML_TAG_RE = re.compile(r"<[^>]+>")


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


def _hash_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _sanitize_json_blob(raw: str, max_len: int, label: str) -> str:
    cleaned = HTML_TAG_RE.sub(" ", str(raw))
    cleaned = " ".join(cleaned.split())
    if len(cleaned) > max_len:
        raise Exception(f"{label} exceeds {max_len} chars")
    return cleaned


def _parse_schema(json_schema: str) -> dict:
    blob = _sanitize_json_blob(json_schema, MAX_SCHEMA_LEN, "json_schema")
    try:
        parsed = json.loads(blob)
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
    blob = _sanitize_json_blob(metadata_json, MAX_META_LEN, "metadata_json")
    try:
        parsed = json.loads(blob)
    except Exception:
        raise Exception("metadata_json must be valid JSON")
    if not isinstance(parsed, dict):
        raise Exception("metadata_json must be a JSON object")
    return parsed


def _build_audit_report(schema: dict, metadata: dict, declared_hash: str) -> str:
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
        if expected_type and expected_type != type(metadata[field]).__name__:
            # map python types loosely
            py_map = {
                "string": "str",
                "integer": "int",
                "number": ("int", "float"),
                "boolean": "bool",
            }
            allowed = py_map.get(expected_type, expected_type)
            if isinstance(allowed, tuple):
                ok = type(metadata[field]).__name__ in allowed
            else:
                ok = type(metadata[field]).__name__ == allowed
            if not ok:
                type_mismatch.append({"field": field, "expected": expected_type})

    computed_hash = _hash_text(json.dumps(metadata, sort_keys=True, separators=(",", ":")))
    hash_match = computed_hash == str(declared_hash).strip()
    valid = len(missing) == 0 and len(type_mismatch) == 0 and hash_match
    return json.dumps(
        {
            "valid": valid,
            "missing_fields": missing,
            "type_mismatch": type_mismatch,
            "hash_match": hash_match,
            "computed_hash": computed_hash,
            "declared_hash": declared_hash,
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
        if not owner_address or not str(owner_address).startswith("0x"):
            raise Exception("owner_address must be a 0x address")
        self.owner = str(owner_address)
        self.fee_receiver = str(owner_address)
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

    @gl.public.write
    def transfer_ownership(self, new_owner: str) -> None:
        self._only_owner()
        if not new_owner or not str(new_owner).startswith("0x"):
            raise Exception("new_owner must be a 0x address")
        self.owner = str(new_owner)
        self._append_event("OwnershipTransferred", {"to": self.owner})

    @gl.public.write
    def set_fee(self, receiver: str, amount: str) -> None:
        self._only_owner()
        if not receiver or not str(receiver).startswith("0x"):
            raise Exception("receiver must be a 0x address")
        amt = str(amount).strip()
        if not amt.isdigit():
            raise Exception("amount must be digits only")
        self.fee_receiver = str(receiver)
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
        self, evidence_id: str, schema_id: str, data_hash: str, metadata_json: str
    ) -> None:
        eid = _normalize_id(evidence_id, "evidence_id")
        sid = _normalize_id(schema_id, "schema_id")
        schemas = self._load_schemas()
        if sid not in schemas:
            raise Exception("unknown schema_id — register first")

        digest = str(data_hash).strip().lower()
        if len(digest) != 64 or any(c not in "0123456789abcdef" for c in digest):
            raise Exception("data_hash must be a 64-char sha256 hex digest")

        metadata = _parse_metadata(metadata_json)
        evidence = self._load_evidence()
        if eid in evidence:
            raise Exception("duplicate evidence_id")

        issuer = str(gl.message.sender_address)
        evidence[eid] = {
            "evidence_id": eid,
            "schema_id": sid,
            "data_hash": digest,
            "metadata_json": json.dumps(metadata, sort_keys=True, separators=(",", ":")),
            "status": STATUS_PENDING,
            "last_audit_id": "",
            "issuer": issuer,
        }
        self._save_evidence(evidence)
        order = self._load_order()
        order.append(eid)
        self._save_order(order)
        self._append_event(
            "EvidenceAttached",
            {"evidence_id": eid, "schema_id": sid, "data_hash": digest, "issuer": issuer},
        )

    @gl.public.write
    def audit(self, evidence_id: str) -> None:
        eid = _normalize_id(evidence_id, "evidence_id")
        evidence = self._load_evidence()
        if eid not in evidence:
            raise Exception("unknown evidence_id")

        entry = evidence[eid]
        schema = json.loads(self._load_schemas()[entry["schema_id"]]["json_schema"])
        metadata = json.loads(entry["metadata_json"])

        def leader_fn() -> str:
            return _build_audit_report(schema, metadata, entry["data_hash"])

        report_json = gl.eq_principle_strict_eq(leader_fn)
        report = json.loads(report_json)
        valid = bool(report.get("valid"))
        status = STATUS_VALID if valid else STATUS_INVALID

        audit_id = self._next_audit_id()
        audits = self._load_audits()
        if len(audits) >= MAX_AUDITS:
            # drop oldest keys deterministically
            keys = sorted(audits.keys())[:50]
            for k in keys:
                del audits[k]
        audits[audit_id] = {
            "audit_id": audit_id,
            "evidence_id": eid,
            "status": status,
            "report": report,
            "caller": str(gl.message.sender_address),
        }
        self._save_audits(audits)

        entry["status"] = status
        entry["last_audit_id"] = audit_id
        evidence[eid] = entry
        self._save_evidence(evidence)

        self._append_event(
            "AuditPerformed",
            {"audit_id": audit_id, "evidence_id": eid, "status": status},
        )
        self._append_event(
            "AuditResult",
            {"audit_id": audit_id, "evidence_id": eid, "valid": valid},
        )

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
        ids = [eid for eid, e in evidence.items() if e.get("status") == wanted]
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
        schemas = self._load_schemas()
        return json.dumps(
            {
                "schemas": len(schemas),
                "evidence_total": len(evidence),
                "pending_audit": pending,
                "valid": valid,
                "invalid": invalid,
                "audits": len(self._load_audits()),
            },
            separators=(",", ":"),
        )
