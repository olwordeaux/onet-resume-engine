import os

import pandas as pd


CORE_CODES = ["11-1011.00", "11-1021.00", "15-1211.00", "15-1232.00"]


def generate_progress_bar(score: float) -> str:
    filled_blocks = max(0, min(10, int(round(score / 10))))
    empty_blocks = 10 - filled_blocks
    return f"`{'█' * filled_blocks + '░' * empty_blocks}` {score:.1f}%"


def aggregate_sub_category(capabilities: pd.DataFrame) -> pd.DataFrame:
    grouped = capabilities.groupby("name", as_index=False)["importance"].mean()
    return grouped.sort_values(by="importance", ascending=False).head(10)


def format_markdown_list(capabilities: pd.DataFrame) -> str:
    lines = [
        f"- **{row['name']}**: {generate_progress_bar(row['importance'])}"
        for _, row in capabilities.iterrows()
    ]
    return "\n".join(lines) or "- No data available"


def main() -> None:
    print("=" * 60)
    print("GENERATING COMPOSITE: IT CONSULTANT & FRACTIONAL CIO")
    print("=" * 60)

    capabilities_df = pd.read_csv("data/processed/tidy_capabilities.csv")
    software_df = pd.read_csv("data/processed/tidy_software.csv")

    missing_codes = sorted(set(CORE_CODES) - set(capabilities_df["occupation_code"]))
    if missing_codes:
        raise ValueError(f"Missing core occupation data: {', '.join(missing_codes)}")

    cap_filtered = capabilities_df[
        capabilities_df["occupation_code"].isin(CORE_CODES)
    ].copy()
    soft_filtered = software_df[
        software_df["occupation_code"].isin(CORE_CODES)
    ].copy()

    capability_ids = cap_filtered["capability_id"].astype("string")
    essential_df = aggregate_sub_category(
        cap_filtered[capability_ids.str.startswith("2.A", na=False)]
    )
    transferable_df = aggregate_sub_category(
        cap_filtered[capability_ids.str.startswith("2.B", na=False)]
    )
    knowledge_df = aggregate_sub_category(
        cap_filtered[capability_ids.str.startswith("2.C", na=False)]
    )

    soft_filtered["hot_technology"] = soft_filtered["hot_technology"].astype(bool)
    composite_soft = (
        soft_filtered.groupby("software", as_index=False)["hot_technology"]
        .any()
        .sort_values(by=["hot_technology", "software"], ascending=[False, True])
    )
    software_lines = [
        f"- **{row['software']}**{' (Hot)' if row['hot_technology'] else ''}"
        for _, row in composite_soft.head(15).iterrows()
    ]
    software_str = "\n".join(software_lines) or "- No data available"

    markdown_output = f"""# O*NET Composite Occupational Profile: Independent IT Consultant & Fractional CIO

_Note: This is a mathematically generated composite profile blending data from Chief Executives (11-1011.00), General/Operations Managers (11-1021.00), Computer Systems Analysts (15-1211.00), and Computer User Support Specialists (15-1232.00). It is a modeling heuristic, not evidence about any individual's lived experience._

## Alternate / Target Job Titles
- Independent IT Consultant
- Fractional CIO / CTO
- B2B Technology Strategist
- IT Services Business Owner
- Principal Systems Analyst

## Technology & Software Stack
{software_str}

## Skills (Transferable & Advisory)
{format_markdown_list(transferable_df)}

## Essential Skills
{format_markdown_list(essential_df)}

## Knowledge Domains
{format_markdown_list(knowledge_df)}
"""

    os.makedirs("reports", exist_ok=True)
    output_file = "reports/Composite_Independent_IT_Consultant.md"
    with open(output_file, "w", encoding="utf-8") as report_file:
        report_file.write(markdown_output)

    print(f"Success! 4-code composite profile saved to: {output_file}")


if __name__ == "__main__":
    main()
