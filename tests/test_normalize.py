from pathlib import Path

import pytest

from onet_engine.normalize import normalize_occupation, write_normalized_occupation


RAW_DATA_DIR = Path("data/raw")
PROCESSED_DATA_DIR = Path("data/processed")
TARGET_CODES = ("11-3031.00", "11-1021.00", "15-2031.00", "13-2072.00")


@pytest.mark.parametrize("code", TARGET_CODES)
def test_normalized_occupation_has_ranked_resume_fields(code):
    payload = normalize_occupation(code)

    assert payload["code"] == code
    assert payload["title"]
    assert payload["description"]
    assert all(len(payload[field]) <= 10 for field in ("tasks", "skills", "knowledge"))
    assert len(payload["technology_tools"]) <= 10
    assert payload["skills"] == sorted(
        payload["skills"], key=lambda item: item["importance"], reverse=True
    )


@pytest.mark.parametrize("code", TARGET_CODES)
def test_normalized_occupation_writes_master_file(code):
    output_path = write_normalized_occupation(code)

    assert output_path == PROCESSED_DATA_DIR / f"{code}.json"
    assert output_path.exists()
