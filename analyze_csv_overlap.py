import argparse
import csv
import math
from itertools import combinations
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent


def load_dataset(path, item_column, weight_column, boolean_weight=False):
    occupations = {}
    titles = {}
    with path.open(newline="", encoding="utf-8") as csv_file:
        for row in csv.DictReader(csv_file):
            code = row["occupation_code"]
            titles[code] = row["occupation_title"]
            weight = row[weight_column]
            if boolean_weight:
                weight = 1.0 if weight.lower() == "true" else 0.0
            occupations.setdefault(code, {})[row[item_column]] = float(weight)
    return occupations, titles


def jaccard_similarity(left, right):
    union = set(left) | set(right)
    return len(set(left) & set(right)) / len(union) if union else 0.0


def weighted_cosine_similarity(left, right):
    dimensions = set(left) | set(right)
    left_norm = math.sqrt(sum(left.get(name, 0.0) ** 2 for name in dimensions))
    right_norm = math.sqrt(sum(right.get(name, 0.0) ** 2 for name in dimensions))
    if not left_norm or not right_norm:
        return 0.0
    dot_product = sum(left.get(name, 0.0) * right.get(name, 0.0) for name in dimensions)
    return dot_product / (left_norm * right_norm)


def render_report(occupations, titles, dataset_name):
    lines = [
        f"# O*NET {dataset_name} Overlap Analysis",
        "",
        f"Pairwise comparison of the four target occupations using `tidy_{dataset_name.lower()}.csv`.",
        "",
        "## Methodology",
        "",
        "- **Jaccard similarity**: shared item names divided by the total unique item names in the pair.",
        "- **Weighted cosine similarity**: cosine similarity of item-weight vectors; absent items receive weight `0`.",
        "- Values are rounded to one decimal place.",
        "",
        "## Pairwise Results",
        "",
        "| Occupation A | Occupation B | Jaccard | Weighted cosine | Shared items |",
        "|---|---|---:|---:|---:|",
    ]
    for left_code, right_code in combinations(sorted(occupations), 2):
        left = occupations[left_code]
        right = occupations[right_code]
        shared = sorted(set(left) & set(right))
        lines.append(
            f"| {left_code} ({titles[left_code]}) | {right_code} ({titles[right_code]}) | "
            f"{jaccard_similarity(left, right) * 100:.1f}% | "
            f"{weighted_cosine_similarity(left, right) * 100:.1f}% | "
            f"{', '.join(shared) if shared else 'None'} |"
        )
    return "\n".join(lines) + "\n"


def main():
    parser = argparse.ArgumentParser(description="Analyze pairwise overlap in a tidy O*NET CSV.")
    parser.add_argument("input", type=Path, help="Tidy CSV path")
    parser.add_argument("item_column", help="Column containing item names")
    parser.add_argument("weight_column", help="Column containing item weights")
    parser.add_argument("dataset_name", help="Dataset name used in the report title")
    parser.add_argument("output", type=Path, help="Markdown report path")
    parser.add_argument(
        "--boolean-weight",
        action="store_true",
        help="Treat true/false weights as 1/0",
    )
    args = parser.parse_args()

    occupations, titles = load_dataset(
        args.input,
        args.item_column,
        args.weight_column,
        boolean_weight=args.boolean_weight,
    )
    if len(occupations) < 2:
        raise ValueError("At least two occupations are required for pairwise analysis")

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        render_report(occupations, titles, args.dataset_name), encoding="utf-8"
    )
    print(f"Saved {args.output}")


if __name__ == "__main__":
    main()
