import argparse
import csv
import json
from pathlib import Path

PROCESSED_DATA_DIR = Path("data/processed")


def load_occupations(processed_dir=PROCESSED_DATA_DIR):
	return [
		json.loads(path.read_text(encoding="utf-8"))
		for path in sorted(processed_dir.glob("*.json"))
	]


def write_csv(path, fieldnames, rows):
	with path.open("w", newline="", encoding="utf-8") as csv_file:
		writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
		writer.writeheader()
		writer.writerows(rows)


def build_vectors(processed_dir=PROCESSED_DATA_DIR, output_dir=None):
	output_dir = output_dir or processed_dir
	occupations = load_occupations(processed_dir)
	task_rows = []
	software_rows = []
	capability_rows = []

	for occupation in occupations:
		occupation_fields = {
			"occupation_code": occupation["code"],
			"occupation_title": occupation["title"],
		}

		task_rows.extend(
			{
				**occupation_fields,
				"task_id": task["id"],
				"task_title": task["title"],
				"importance": task.get("importance", 0),
				"category": task.get("category", "Unknown"),
			}
			for task in occupation.get("tasks", [])
		)

		software_rows.extend(
			{
				**occupation_fields,
				"software": tool["title"],
				"hot_technology": tool.get("hot_technology", False),
			}
			for tool in occupation.get("technology_tools", [])
		)

		for kind in ("skills", "knowledge"):
			capability_rows.extend(
				{
					**occupation_fields,
					"kind": kind,
					"capability_id": capability["id"],
					"name": capability["name"],
					"description": capability["description"],
					"importance": capability.get("importance", 0),
				}
				for capability in occupation.get(kind, [])
			)

	output_paths = {
		"tasks": output_dir / "tidy_tasks.csv",
		"software": output_dir / "tidy_software.csv",
		"capabilities": output_dir / "tidy_capabilities.csv",
	}
	write_csv(
		output_paths["tasks"],
		("occupation_code", "occupation_title", "task_id", "task_title", "importance", "category"),
		task_rows,
	)
	write_csv(
		output_paths["software"],
		("occupation_code", "occupation_title", "software", "hot_technology"),
		software_rows,
	)
	write_csv(
		output_paths["capabilities"],
		(
			"occupation_code",
			"occupation_title",
			"kind",
			"capability_id",
			"name",
			"description",
			"importance",
		),
		capability_rows,
	)
	return output_paths


def main():
	parser = argparse.ArgumentParser(description="Build tidy CSV vectors from processed O*NET JSON.")
	parser.add_argument(
		"--processed-dir",
		type=Path,
		default=PROCESSED_DATA_DIR,
		help="Directory containing normalized occupation JSON files",
	)
	args = parser.parse_args()

	for path in build_vectors(args.processed_dir).values():
		print(f"Saved {path}")


if __name__ == "__main__":
	main()
