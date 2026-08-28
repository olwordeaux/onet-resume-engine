import csv
import math
from itertools import combinations
from pathlib import Path

from analyze_csv_overlap import jaccard_similarity, weighted_cosine_similarity

PROJECT_ROOT = Path(__file__).parent
DATA_DIR = PROJECT_ROOT / "data/processed"
OUTPUT_PATH = PROJECT_ROOT / "reports/onet_career_transition_pathways.md"
JACCARD_THRESHOLD = 0.25
COSINE_THRESHOLD = 0.75


def load_vectors(path, item_column, weight_column, kind=None, boolean_weight=False):
    vectors = {}
    titles = {}
    with path.open(newline="", encoding="utf-8") as csv_file:
        for row in csv.DictReader(csv_file):
            code = row["occupation_code"]
            titles[code] = row["occupation_title"]
            weight = row[weight_column]
            if boolean_weight:
                weight = 1.0 if weight.lower() == "true" else 0.0
            if kind is None or row.get("kind") == kind:
                vectors.setdefault(code, {})[row[item_column]] = float(weight)
    return vectors, titles


def build_recommendations():
    skills, titles = load_vectors(
        DATA_DIR / "tidy_capabilities.csv",
        "name",
        "importance",
        kind="skills",
    )
    software, software_titles = load_vectors(
        DATA_DIR / "tidy_software.csv",
        "software",
        "hot_technology",
        boolean_weight=True,
    )
    titles.update(software_titles)

    knowledge, _ = load_vectors(
        DATA_DIR / "tidy_capabilities.csv",
        "name",
        "importance",
        kind="knowledge",
    )

    rows = []
    for left_code, right_code in combinations(sorted(skills), 2):
        skill_cosine = weighted_cosine_similarity(skills[left_code], skills[right_code])
        knowledge_jaccard = jaccard_similarity(knowledge[left_code], knowledge[right_code])
        software_jaccard = jaccard_similarity(software[left_code], software[right_code])
        qualifies = (
            software_jaccard >= JACCARD_THRESHOLD
            and knowledge_jaccard >= JACCARD_THRESHOLD
            and skill_cosine >= COSINE_THRESHOLD
        )
        rows.append(
            {
                "left": left_code,
                "right": right_code,
                "software_jaccard": software_jaccard,
                "knowledge_jaccard": knowledge_jaccard,
                "skill_cosine": skill_cosine,
                "qualifies": qualifies,
            }
        )
    return rows, titles


def render_report(rows, titles):
    qualified = [row for row in rows if row["qualifies"]]
    lines = [
        "# O*NET Career Transition Pathways",
        "",
        "Pairwise recommendations filtered from the three tidy O*NET CSV datasets.",
        "",
        "## Filter Rules",
        "",
        "A pathway qualifies only when **all three** conditions pass:",
        "",
        f"- Software Jaccard similarity: at least {JACCARD_THRESHOLD:.0%}.",
        f"- Knowledge Jaccard similarity: at least {JACCARD_THRESHOLD:.0%}.",
        f"- Skills weighted cosine similarity: at least {COSINE_THRESHOLD:.0%}.",
        "",
        "## Recommended Pathways",
        "",
    ]
    if qualified:
        lines.extend(
            [
                "| From occupation | To occupation | Software Jaccard | Knowledge Jaccard | Skills cosine |",
                "|---|---|---:|---:|---:|",
            ]
        )
        for row in qualified:
            lines.append(
                f"| {row['left']} ({titles[row['left']]}) | {row['right']} ({titles[row['right']]}) | "
                f"{row['software_jaccard']:.1%} | {row['knowledge_jaccard']:.1%} | "
                f"{row['skill_cosine']:.1%} |"
            )
    else:
        lines.append("No occupation pairs meet all three thresholds.")

    lines.extend(
        [
            "",
            "## All Pairwise Results",
            "",
            "| Occupation A | Occupation B | Software Jaccard | Knowledge Jaccard | Skills cosine | Result |",
            "|---|---|---:|---:|---:|---|",
        ]
    )
    for row in rows:
        result = "Recommended" if row["qualifies"] else "Below threshold"
        lines.append(
            f"| {row['left']} | {row['right']} | {row['software_jaccard']:.1%} | "
            f"{row['knowledge_jaccard']:.1%} | {row['skill_cosine']:.1%} | {result} |"
        )
    return "\n".join(lines) + "\n"


def main():
    rows, titles = build_recommendations()
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(render_report(rows, titles), encoding="utf-8")
    print(f"Saved {OUTPUT_PATH}")
    print(f"Recommended pathways: {sum(row['qualifies'] for row in rows)}")


if __name__ == "__main__":
    main()
