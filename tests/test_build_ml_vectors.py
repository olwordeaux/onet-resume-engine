import csv
from pathlib import Path

from onet_engine.build_ml_vectors import build_vectors


def test_build_vectors_writes_three_tidy_csvs(tmp_path):
    output_paths = build_vectors(Path("data/processed"), tmp_path)

    assert set(output_paths) == {"tasks", "software", "capabilities"}
    assert all(path.exists() for path in output_paths.values())

    for path in output_paths.values():
        with path.open(newline="", encoding="utf-8") as csv_file:
            rows = list(csv.DictReader(csv_file))
        assert rows
        assert all(value != "" for row in rows for value in row.values())


def test_build_vectors_has_expected_row_counts(tmp_path):
    output_paths = build_vectors(Path("data/processed"), tmp_path)

    with output_paths["tasks"].open(newline="", encoding="utf-8") as csv_file:
        assert len(list(csv.DictReader(csv_file))) == 40
    with output_paths["software"].open(newline="", encoding="utf-8") as csv_file:
        assert len(list(csv.DictReader(csv_file))) == 40
    with output_paths["capabilities"].open(newline="", encoding="utf-8") as csv_file:
        assert len(list(csv.DictReader(csv_file))) == 80
