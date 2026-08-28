import os
import pytest

# Final resume mapping: Parsons is mapped strictly to your single selected 41-3091.00 code!
RESUME_MAPPING = {
    "Sprouts Farmers Market (Grocery Clerk)": ["53-7065.00"],
    "Wells Fargo (Senior Operations Analyst)": ["15-2031.00"],
    "O.N.E. Consulting (Principal IT Consultant & Fractional CIO)": ["11-1011.00", "11-1021.00", "15-1211.00", "15-1232.00"],
    "Global State Mortgage (Branch Manager)": ["11-1021.00"],
    "Family Lending (Senior Loan Officer)": ["13-2072.00"],
    "Specialty Lending (Branch Manager)": ["11-1021.00"],
    "First Choice Mortgage (Senior Loan Officer)": ["13-2072.00"],
    "Parson's Technology (Inside Sales Representative)": ["41-3091.00"]
}

REQUIRED_SUFFIXES = ["overview", "tasks", "technology_skills", "skills", "knowledge"]

def test_resume_data_integrity():
    """
    Integrity Audit:
    Verifies that every single position listed on Andrew's Master Resume
    has its associated O*NET raw and processed files fully ingested on disk.
    """
    raw_dir = "data/raw"
    processed_dir = "data/processed"
    missing_data = []

    for position, codes in RESUME_MAPPING.items():
        for code in codes:
            processed_path = os.path.join(processed_dir, f"{code}.json")
            if not os.path.exists(processed_path):
                missing_data.append((position, code, f"Processed file missing: {processed_path}"))
                continue

            for suffix in REQUIRED_SUFFIXES:
                raw_path = os.path.join(raw_dir, f"{code}_{suffix}.json")
                if not os.path.exists(raw_path):
                    missing_data.append((position, code, f"Raw payload missing: {raw_path}"))

    if missing_data:
        print("\n❌ INTEGRITY BREACH: Missing O*NET data detected:")
        for pos, code, reason in missing_data:
            print(f"   - Position: '{pos}' ➔ Code: {code} | {reason}")
        pytest.fail("Resume integrity check failed. Please ingest missing codes.")

    print("\n🟢 INTEGRITY PASSED: All resume positions have 100% of their O*NET data ready!")
