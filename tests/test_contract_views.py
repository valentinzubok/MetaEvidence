import json
from pathlib import Path

import pytest

from conftest import load_contract

ROOT = Path(__file__).resolve().parents[1]
mod = load_contract(ROOT, "MetaEvidence.py")
OWNER = "0x1111111111111111111111111111111111111111"
OTHER = "0x2222222222222222222222222222222222222222"

SCHEMA = json.dumps(
    {
        "type": "object",
        "required": ["model", "version"],
        "properties": {"model": {"type": "string"}, "version": {"type": "string"}},
    }
)


def _hub():
    return mod.MetaEvidence(OWNER)


def test_views_and_admin():
    import genlayer

    c = _hub()
    assert c.get_owner() == OWNER
    assert json.loads(c.get_schema("missing"))["error"] == "unknown schema_id"
    assert json.loads(c.get_audit_result("audit-9"))["error"] == "unknown audit_id"

    c.register_schema("model-v1", SCHEMA)
    meta = {"model": "x", "version": "1"}
    digest = mod._hash_text(json.dumps(meta, sort_keys=True, separators=(",", ":")))
    c.attach_evidence("ev-2", "model-v1", digest, json.dumps(meta))
    pending = json.loads(c.list_by_status("pending_audit"))
    assert "ev-2" in pending
    stats = json.loads(c.get_stats())
    assert stats["schemas"] == 1
    assert stats["evidence_total"] == 1

    c.set_fee(OWNER, "10")
    assert json.loads(c.get_fee())["amount"] == "10"
    c.transfer_ownership(OTHER)
    assert c.get_owner() == OTHER
    genlayer.message.sender_address = OTHER


def test_set_fee_validation():
    import genlayer

    c = _hub()
    genlayer.message.sender_address = OWNER
    with pytest.raises(Exception, match="receiver must be"):
        c.set_fee("bad", "1")
    genlayer.message.sender_address = OTHER
    with pytest.raises(Exception, match="only owner"):
        c.set_fee(OTHER, "1")
