import argparse
import json
from pathlib import Path

RAW_DATA_DIR = Path("data/raw")
PROCESSED_DATA_DIR = Path("data/processed")
TOP_N = 10
REPORT_NAMES = ("overview", "tasks", "skills", "technology_skills", "knowledge")


def load_report(code, report_name, raw_dir=RAW_DATA_DIR):
	path = raw_dir / f"{code}_{report_name}.json"
	return json.loads(path.read_text(encoding="utf-8"))


def ranked_items(items, fields):
	normalized = [{field: item[field] for field in fields if field in item} for item in items]
	return sorted(normalized, key=lambda item: item.get("importance", 0), reverse=True)[:TOP_N]


def normalize_occupation(code, raw_dir=RAW_DATA_DIR):
	reports = {name: load_report(code, name, raw_dir) for name in REPORT_NAMES}
	overview = reports["overview"]

	technology = {}
	for category in reports["technology_skills"].get("category", []):
		for example in category.get("example", []) + category.get("example_more", []):
			title = example.get("title")
			if title:
				technology[title] = {
					"title": title,
					"hot_technology": example.get("hot_technology", False),
				}

	return {
		"code": overview["code"],
		"title": overview["title"],
		"description": overview["description"],
		"tasks": ranked_items(
			reports["tasks"].get("task", []), ("id", "title", "importance", "category")
		),
		"skills": ranked_items(
			reports["skills"].get("element", []), ("id", "name", "description", "importance")
		),
		"knowledge": ranked_items(
			reports["knowledge"].get("element", []),
			("id", "name", "description", "importance"),
		),
		"technology_tools": sorted(
			technology.values(), key=lambda item: (not item["hot_technology"], item["title"].lower())
		)[:TOP_N],
	}


def write_normalized_occupation(code, raw_dir=RAW_DATA_DIR, processed_dir=PROCESSED_DATA_DIR):
	normalized = normalize_occupation(code, raw_dir)
	processed_dir.mkdir(parents=True, exist_ok=True)
	output_path = processed_dir / f"{code}.json"
	output_path.write_text(json.dumps(normalized, indent=2) + "\n", encoding="utf-8")
	return output_path


def main():
	parser = argparse.ArgumentParser(description="Normalize raw O*NET occupation reports.")
	parser.add_argument("code", help="O*NET-SOC code, for example 15-2031.00")
	args = parser.parse_args()
	output_path = write_normalized_occupation(args.code)
	print(f"Saved {output_path}")


if __name__ == "__main__":
	main()
