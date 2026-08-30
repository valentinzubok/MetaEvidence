import json
from pathlib import Path

import pytest

from conftest import load_contract

ROOT = Path(__file__).resolve().parents[1]
mod = load_contract(ROOT, "MetaEvidence.py")
OWNER = "0x1111111111111111111111111111111111111111"

SCHEMA = json.dumps(
    {
        "type": "object",
        "required": ["model", "version"],
        "properties": {"model": {"type": "string"}, "version": {"type": "string"}},
    }
)


def _hub():
    return mod.MetaEvidence(OWNER)


def test_register_attach_audit_valid():
    c = _hub()
    c.register_schema("model-v1", SCHEMA)
    meta = {"model": "gpt-demo", "version": "1.0"}
    meta_json = json.dumps(meta)
    digest = mod._hash_text(json.dumps(meta, sort_keys=True, separators=(",", ":")))
    c.attach_evidence("ev-1", "model-v1", digest, meta_json)
    entry = json.loads(c.get_evidence("ev-1"))
    assert entry["status"] == "pending_audit"
    c.audit("ev-1")
    entry = json.loads(c.get_evidence("ev-1"))
    assert entry["status"] == "valid"
    audit = json.loads(c.get_audit_result(entry["last_audit_id"]))
    assert audit["status"] == "valid"


def test_audit_invalid_on_hash_mismatch():
    c = _hub()
    c.register_schema("model-v1", SCHEMA)
    meta = {"model": "gpt-demo", "version": "1.0"}
    c.attach_evidence("ev-bad", "model-v1", "deadbeef" * 8, json.dumps(meta))
    c.audit("ev-bad")
    entry = json.loads(c.get_evidence("ev-bad"))
    assert entry["status"] == "invalid"


def test_duplicate_schema():
    c = _hub()
    c.register_schema("model-v1", SCHEMA)
    with pytest.raises(Exception, match="duplicate schema_id"):
        c.register_schema("model-v1", SCHEMA)


def test_attach_unknown_schema():
    c = _hub()
    with pytest.raises(Exception, match="unknown schema_id"):
        c.attach_evidence("ev-x", "missing", "a" * 64, "{}")
