# O*NET Tasks Overlap Analysis

Pairwise comparison of the four target occupations using `tidy_tasks.csv`.

## Methodology

- **Jaccard similarity**: shared item names divided by the total unique item names in the pair.
- **Weighted cosine similarity**: cosine similarity of item-weight vectors; absent items receive weight `0`.
- Values are rounded to one decimal place.

## Pairwise Results

| Occupation A | Occupation B | Jaccard | Weighted cosine | Shared items |
|---|---|---:|---:|---:|
| 11-1021.00 (General and Operations Managers) | 11-3031.00 (Financial Managers) | 0.0% | 0.0% | None |
| 11-1021.00 (General and Operations Managers) | 13-2072.00 (Loan Officers) | 0.0% | 0.0% | None |
| 11-1021.00 (General and Operations Managers) | 15-2031.00 (Operations Research Analysts) | 0.0% | 0.0% | None |
| 11-3031.00 (Financial Managers) | 13-2072.00 (Loan Officers) | 0.0% | 0.0% | None |
| 11-3031.00 (Financial Managers) | 15-2031.00 (Operations Research Analysts) | 0.0% | 0.0% | None |
| 13-2072.00 (Loan Officers) | 15-2031.00 (Operations Research Analysts) | 0.0% | 0.0% | None |
