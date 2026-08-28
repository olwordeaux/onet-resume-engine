# 5. Evaluation

## Integrity Evaluation

`tests/test_resume_integrity.py` verifies that every occupation mapped to the master resume has:

- One normalized JSON profile in `data/processed/`.
- Five required raw O*NET payloads in `data/raw/`.

## Dataset Audit

`generate_report.py` checks raw payload counts, normalized profile counts, tidy CSV presence, and tidy CSV row and column counts. The current audit result is 9 occupations, 45 raw payloads, 9 normalized profiles, and 3 tidy CSVs.

## Automated Tests

The repository test suite validates normalization, data files, vector generation, report headings, and resume integrity.

```bash
python -m pytest tests
```

The latest run passed all 60 tests.

## Modeling Constraint

The composite profile uses arithmetic averages across selected occupations. This is a transparent modeling heuristic, not direct evidence that one person performed every represented task or possesses every represented capability.
