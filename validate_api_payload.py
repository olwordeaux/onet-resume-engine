import argparse
import json
import os
import re
import sys
from pathlib import Path

import requests
from dotenv import load_dotenv

API_URL = "https://api-v2.onetcenter.org/online/occupations/{code}/"
OCCUPATION_CODE_PATTERN = re.compile(r"^\d\d-\d\d\d\d\.\d\d$")
REQUIRED_FIELDS = {
    "code",
    "title",
    "tags",
    "description",
    "summary_contents",
    "details_contents",
    "custom_contents",
}


def describe(value, path="response"):
    if isinstance(value, dict):
        print(f"{path}: object ({len(value)} keys)")
        for key, child in value.items():
            describe(child, f"{path}.{key}")
    elif isinstance(value, list):
        print(f"{path}: array ({len(value)} items)")
        if value:
            describe(value[0], f"{path}[0]")
    else:
        print(f"{path}: {type(value).__name__}")


def parse_args():
    parser = argparse.ArgumentParser(description="Inspect one O*NET occupation payload.")
    parser.add_argument(
        "--code",
        default="15-1252.00",
        help="O*NET-SOC code to inspect (default: 15-1252.00)",
    )
    parser.add_argument(
        "--save",
        type=Path,
        help="Optional path for saving the raw JSON response",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    if not OCCUPATION_CODE_PATTERN.fullmatch(args.code):
        print(f"Invalid O*NET-SOC code: {args.code}", file=sys.stderr)
        return 1

    load_dotenv(Path(__file__).with_name(".env"))
    api_key = os.getenv("ONET_API_KEY")
    if not api_key:
        print("ONET_API_KEY not found in .env file.", file=sys.stderr)
        return 1

    url = API_URL.format(code=args.code)
    response = requests.get(
        url,
        headers={"X-API-Key": api_key, "Accept": "application/json"},
        timeout=20,
    )
    print(f"HTTP {response.status_code} {response.headers.get('content-type', '')}")
    response.raise_for_status()

    payload = response.json()
    if not isinstance(payload, dict):
        print(f"Expected a JSON object, got {type(payload).__name__}", file=sys.stderr)
        return 1

    missing_fields = REQUIRED_FIELDS - payload.keys()
    if missing_fields:
        print(f"Missing required fields: {sorted(missing_fields)}", file=sys.stderr)
        return 1

    print(f"Top-level keys: {sorted(payload)}")
    describe(payload)
    print("Payload validation successful.")

    if args.save:
        args.save.parent.mkdir(parents=True, exist_ok=True)
        args.save.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
        print(f"Raw response saved to {args.save}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
