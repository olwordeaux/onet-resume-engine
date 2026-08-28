import csv
from pathlib import Path

from onet_engine.build_ml_vectors import build_vectors, load_occupations


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
    occupations = load_occupations(Path("data/processed"))
    expected_task_count = sum(len(occupation["tasks"]) for occupation in occupations)
    expected_software_count = sum(
        len(occupation["technology_tools"]) for occupation in occupations
    )
    expected_capability_count = sum(
        len(occupation["skills"]) + len(occupation["knowledge"])
        for occupation in occupations
    )

    with output_paths["tasks"].open(newline="", encoding="utf-8") as csv_file:
        assert len(list(csv.DictReader(csv_file))) == expected_task_count
    with output_paths["software"].open(newline="", encoding="utf-8") as csv_file:
        assert len(list(csv.DictReader(csv_file))) == expected_software_count
    with output_paths["capabilities"].open(newline="", encoding="utf-8") as csv_file:
        assert len(list(csv.DictReader(csv_file))) == expected_capability_count
