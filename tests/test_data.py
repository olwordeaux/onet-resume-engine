import json
from pathlib import Path

import pytest


RAW_DATA_DIR = Path("data/raw")
TARGET_CODES = {
    "11-3031.00",
    "11-1021.00",
    "15-2031.00",
    "13-2072.00",
}
REPORT_NAMES = {
    "overview",
    "tasks",
    "skills",
    "technology_skills",
    "knowledge",
}


@pytest.mark.parametrize("code", sorted(TARGET_CODES))
def test_occupation_reports_exist(code):
    paths = list(RAW_DATA_DIR.glob(f"{code}_*.json"))
    assert {path.stem.removeprefix(f"{code}_") for path in paths} == REPORT_NAMES


@pytest.mark.parametrize("path", sorted(RAW_DATA_DIR.glob("*.json")))
def test_occupation_report_is_json_object(path):
    payload = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(payload, dict)
    assert payload
