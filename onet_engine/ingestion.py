import argparse
import json
import os
from pathlib import Path

import requests
from dotenv import load_dotenv

API_URL = "https://api-v2.onetcenter.org/online/occupations/{code}/{path}"
RAW_DATA_DIR = Path("data/raw")
REPORTS = {
	"overview": "",
	"tasks": "details/tasks",
	"skills": "details/skills",
	"technology_skills": "details/technology_skills",
	"knowledge": "details/knowledge",
}


def download_occupation(code, api_key, output_dir=RAW_DATA_DIR):
	output_dir.mkdir(parents=True, exist_ok=True)
	downloaded_files = []

	for report_name, report_path in REPORTS.items():
		url = API_URL.format(code=code, path=report_path)
		response = requests.get(
			url,
			headers={"X-API-Key": api_key, "Accept": "application/json"},
			timeout=30,
		)
		response.raise_for_status()
		payload = response.json()
		output_path = output_dir / f"{code}_{report_name}.json"
		output_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
		downloaded_files.append(output_path)
		print(f"Saved {output_path}")

	return downloaded_files


def main():
	parser = argparse.ArgumentParser(description="Download raw O*NET occupation reports.")
	parser.add_argument("code", help="O*NET-SOC code, for example 15-2031.00")
	args = parser.parse_args()

	load_dotenv(Path(__file__).resolve().parent.parent / ".env")
	api_key = os.getenv("ONET_API_KEY")
	if not api_key:
		parser.error("ONET_API_KEY not found in .env file")

	try:
		download_occupation(args.code, api_key)
	except (requests.RequestException, ValueError) as error:
		parser.error(f"download failed: {error}")


if __name__ == "__main__":
	main()
