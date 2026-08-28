# O*NET Resume Engine: Process Report

## Purpose

Convert O*NET occupation data into normalized profiles, analysis datasets, and resume-oriented reports.

## Process

| Step | What happens | Implementation |
| --- | --- | --- |
| 1. Select occupations | Identify O*NET-SOC codes relevant to the resume or analysis. | `find_entrepreneur_codes.py` and configuration in the calling command |
| 2. Ingest data | Download five O*NET API payloads for each code: overview, tasks, skills, technology skills, and knowledge. | `onet_engine/ingestion.py` |
| 3. Normalize data | Convert the separate API payloads into one JSON profile per occupation and keep the top 10 ranked items. | `onet_engine/normalize.py` |
| 4. Build tidy datasets | Flatten normalized profiles into task, software, and capability CSV files for analysis. | `onet_engine/build_ml_vectors.py` |
| 5. Analyze occupations | Compare skills, knowledge, software, and tasks; calculate similarity and transition pathways. | `analyze_skill_overlap.py`, `analyze_csv_overlap.py`, `recommend_transition_pathways.py` |
| 6. Generate profiles | Render occupation or composite profiles as Markdown. | `onet_engine/render_markdown.py`, `build_it_consultant_profile.py` |
| 7. Audit data integrity | Check that raw payloads, normalized profiles, and tidy CSVs are present and internally consistent. | `generate_report.py`, `tests/test_resume_integrity.py` |
| 8. Validate changes | Run automated tests before committing changes. | `python -m pytest tests` or `make test` |

## Current Dataset

- Occupations with normalized profiles: **9**
- Raw API payloads: **45**
- Occupation codes: `11-1011.00`, `11-1021.00`, `11-3031.00`, `13-2072.00`, `15-1211.00`, `15-1232.00`, `15-2031.00`, `41-3091.00`, `53-7065.00`

| Tidy dataset | Rows | Columns |
| --- | ---: | ---: |
| `tidy_capabilities.csv` | 180 | 7 |
| `tidy_software.csv` | 90 | 4 |
| `tidy_tasks.csv` | 90 | 6 |

## Modeling Constraint

Composite profiles use arithmetic averages across the selected occupations. This is a transparent modeling heuristic; it is not evidence that any individual has performed every task or possesses every capability represented in the composite.

## Reproduce

```bash
python -m onet_engine.ingestion <O*NET-SOC-code>
python -m onet_engine.normalize <O*NET-SOC-code>
python -m onet_engine.build_ml_vectors
python generate_report.py
python -m pytest tests
```
