import csv
import math
from itertools import combinations
from pathlib import Path

INPUT_PATH = Path(__file__).parent / "data/processed/tidy_capabilities.csv"
KINDS = ("skills", "knowledge")


def load_capabilities(path):
    occupations = {}
    with path.open(newline="", encoding="utf-8") as csv_file:
        for row in csv.DictReader(csv_file):
            occupation = row["occupation_code"]
            kind = row["kind"]
            occupations.setdefault(occupation, {item: {} for item in KINDS})
            occupations[occupation][kind][row["name"]] = float(row["importance"])
    return occupations


def jaccard_similarity(left, right):
    left_names = set(left)
    right_names = set(right)
    union = left_names | right_names
    return len(left_names & right_names) / len(union) if union else 0.0


def weighted_cosine_similarity(left, right):
    dimensions = set(left) | set(right)
    left_norm = math.sqrt(sum(left.get(name, 0.0) ** 2 for name in dimensions))
    right_norm = math.sqrt(sum(right.get(name, 0.0) ** 2 for name in dimensions))
    if not left_norm or not right_norm:
        return 0.0
    dot_product = sum(left.get(name, 0.0) * right.get(name, 0.0) for name in dimensions)
    return dot_product / (left_norm * right_norm)


def percent(value):
    return f"{value * 100:.1f}%"


def pair_rows(occupations, kind):
    rows = []
    for left_code, right_code in combinations(sorted(occupations), 2):
        left = occupations[left_code][kind]
        right = occupations[right_code][kind]
        rows.append(
            {
                "left": left_code,
                "right": right_code,
                "jaccard": jaccard_similarity(left, right),
                "cosine": weighted_cosine_similarity(left, right),
                "shared": sorted(set(left) & set(right)),
            }
        )
    return rows


def render_report(occupations):
    lines = [
        "# O*NET Skill Overlap Analysis",
        "",
        "Pairwise comparison of the four target occupations using the tidy capability dataset.",
        "",
        "## Methodology",
        "",
        "- **Jaccard similarity**: shared capability names divided by the total unique capability names in the pair.",
        "- **Weighted cosine similarity**: cosine similarity of importance-weight vectors keyed by capability name; absent capabilities receive weight `0`.",
        "- Skills and knowledge are analyzed separately. Values are rounded to one decimal place.",
        "",
    ]

    for kind in KINDS:
        label = kind.capitalize()
        lines.extend(
            [
                f"## {label} Overlap",
                "",
                "| Occupation A | Occupation B | Jaccard | Weighted cosine | Shared capabilities |",
                "|---|---|---:|---:|---:|",
            ]
        )
        for row in pair_rows(occupations, kind):
            shared = ", ".join(row["shared"]) if row["shared"] else "None"
            lines.append(
                f"| {row['left']} | {row['right']} | {percent(row['jaccard'])} | "
                f"{percent(row['cosine'])} | {shared} |"
            )
        lines.extend(["", "### Occupation Codes", ""])
        for code in sorted(occupations):
            lines.append(f"- `{code}`")
        lines.append("")

    return "\n".join(lines)


def main():
    occupations = load_capabilities(INPUT_PATH)
    if len(occupations) < 2:
        raise ValueError("At least two occupations are required for pairwise analysis")
    missing_kinds = {
        code: set(KINDS) - set(occupations[code]) for code in occupations if set(KINDS) - set(occupations[code])
    }
    if missing_kinds:
        raise ValueError(f"Missing capability groups: {missing_kinds}")

    print(render_report(occupations))


if __name__ == "__main__":
    main()
