import json
from pathlib import Path

import pytest

from conftest import load_contract

ROOT = Path(__file__).resolve().parents[1]
mod = load_contract(ROOT, "MetaEvidence.py")

SCHEMA = json.dumps(
    {
        "type": "object",
        "required": ["model", "version"],
        "properties": {"model": {"type": "string"}, "version": {"type": "string"}},
    }
)


def test_parse_schema_ok():
    parsed = mod._parse_schema(SCHEMA)
    assert parsed["required"] == ["model", "version"]


def test_parse_schema_invalid_json():
    with pytest.raises(Exception, match="valid JSON"):
        mod._parse_schema("{bad")


def test_build_audit_report_valid():
    schema = json.loads(SCHEMA)
    meta = {"model": "gpt-demo", "version": "1.0"}
    digest = mod._hash_text(json.dumps(meta, sort_keys=True, separators=(",", ":")))
    report = json.loads(mod._build_audit_report(schema, meta, digest))
    assert report["valid"] is True


def test_build_audit_report_missing_field():
    schema = json.loads(SCHEMA)
    meta = {"model": "gpt-demo"}
    digest = mod._hash_text(json.dumps(meta, sort_keys=True, separators=(",", ":")))
    report = json.loads(mod._build_audit_report(schema, meta, digest))
    assert report["valid"] is False
    assert "version" in report["missing_fields"]
