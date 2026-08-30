import json
from pathlib import Path

import pytest

from conftest import load_contract

ROOT = Path(__file__).resolve().parents[1]
mod = load_contract(ROOT, "MetaEvidence.py")


def test_parse_schema_ok():
    schema = '{"required":["a"],"properties":{"a":{"type":"string"}}}'
    assert mod._parse_schema(schema)["required"] == ["a"]


def test_parse_schema_invalid_json():
    with pytest.raises(Exception, match="valid JSON"):
        mod._parse_schema("{bad")


def test_json_type_rejects_unknown():
    assert mod._json_type_ok("x", "string") is True
    assert mod._json_type_ok([], "mystery") is False


def test_require_https():
    with pytest.raises(Exception, match="https"):
        mod._require_https("http://example.com")


def test_capture_source_ok():
    raw = json.loads(mod._capture_source("https://example.com/a"))
    assert raw["status"] == "ok"
    assert len(raw["content_hash"]) == 64
