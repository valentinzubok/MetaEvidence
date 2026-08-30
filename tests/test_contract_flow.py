import json
from pathlib import Path

import pytest

from conftest import load_contract

ROOT = Path(__file__).resolve().parents[1]
mod = load_contract(ROOT, "MetaEvidence.py")
OWNER = "0x1111111111111111111111111111111111111111"
OTHER = "0x2222222222222222222222222222222222222222"
URL = "https://test-server.genlayer.com/static/genvm/hello.html"

SCHEMA = json.dumps(
    {
        "type": "object",
        "required": ["model", "version"],
        "properties": {"model": {"type": "string"}, "version": {"type": "string"}},
    }
)


def _hub():
    return mod.MetaEvidence(OWNER)


def test_attach_audit_valid():
    c = _hub()
    c.register_schema("model-v1", SCHEMA)
    c.attach_evidence("ev-1", "model-v1", URL, '{"model":"gpt-demo","version":"1.0"}')
    entry = json.loads(c.get_evidence("ev-1"))
    assert entry["status"] == "pending_audit"
    assert len(entry["data_hash"]) == 64
    c.audit("ev-1")
    entry = json.loads(c.get_evidence("ev-1"))
    assert entry["status"] == "valid"
    audit = json.loads(c.get_audit_result(entry["last_audit_id"]))
    assert audit["status"] == "valid"
    assert audit["report"]["hash_match"] is True


def test_audit_only_pending():
    c = _hub()
    c.register_schema("model-v1", SCHEMA)
    c.attach_evidence("ev-2", "model-v1", URL, '{"model":"x","version":"1"}')
    c.audit("ev-2")
    with pytest.raises(Exception, match="pending_audit"):
        c.audit("ev-2")


def test_appeal_after_invalid(monkeypatch):
    import genlayer

    c = _hub()
    c.register_schema("model-v1", SCHEMA)
    c.attach_evidence("ev-3", "model-v1", URL, '{"model":"x","version":"1"}')
    # Drift live content → invalid on audit
    monkeypatch.setattr(genlayer, "get_webpage", lambda url, mode="text": "CHANGED PAGE")
    c.audit("ev-3")
    entry = json.loads(c.get_evidence("ev-3"))
    assert entry["status"] == "invalid"
    # Restore original content for successful appeal
    monkeypatch.setattr(genlayer, "get_webpage", lambda url, mode="text": "Hello world!")
    c.appeal("ev-3")
    entry = json.loads(c.get_evidence("ev-3"))
    assert entry["status"] == "valid"
    assert entry["appeals"] == 1


def test_duplicate_schema():
    c = _hub()
    c.register_schema("model-v1", SCHEMA)
    with pytest.raises(Exception, match="duplicate schema_id"):
        c.register_schema("model-v1", SCHEMA)


def test_attach_unknown_schema():
    c = _hub()
    with pytest.raises(Exception, match="unknown schema_id"):
        c.attach_evidence("ev-x", "missing", URL, "{}")


def test_schema_type_mismatch_invalidates():
    c = _hub()
    c.register_schema("model-v1", SCHEMA)
    c.attach_evidence("ev-bad-type", "model-v1", URL, '{"model":"x","version":1}')
    # Keep same page so hash matches; schema type fails (version should be string)
    c.audit("ev-bad-type")
    entry = json.loads(c.get_evidence("ev-bad-type"))
    assert entry["status"] == "invalid"


def test_views_and_admin():
    import genlayer

    c = _hub()
    genlayer.message.sender_address = OWNER
    assert c.get_owner() == OWNER
    c.register_schema("model-v1", SCHEMA)
    c.attach_evidence("ev-v", "model-v1", URL, '{"model":"a","version":"b"}')
    pending = json.loads(c.list_by_status("pending_audit"))
    assert "ev-v" in pending
    stats = json.loads(c.get_stats())
    assert stats["max_appeals"] == 3
    c.set_fee(OWNER, "10")
    assert json.loads(c.get_fee())["amount"] == "10"
    c.transfer_ownership(OTHER)
    assert c.get_owner() == OTHER
    genlayer.message.sender_address = OWNER
