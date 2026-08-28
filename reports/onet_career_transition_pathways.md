# O*NET Career Transition Pathways

Pairwise recommendations filtered from the three tidy O*NET CSV datasets.

## Filter Rules

A pathway qualifies only when **all three** conditions pass:

- Software Jaccard similarity: at least 25%.
- Knowledge Jaccard similarity: at least 25%.
- Skills weighted cosine similarity: at least 75%.

## Recommended Pathways

| From occupation | To occupation | Software Jaccard | Knowledge Jaccard | Skills cosine |
|---|---|---:|---:|---:|
| 11-1021.00 (General and Operations Managers) | 11-3031.00 (Financial Managers) | 25.0% | 66.7% | 81.8% |

## All Pairwise Results

| Occupation A | Occupation B | Software Jaccard | Knowledge Jaccard | Skills cosine | Result |
|---|---|---:|---:|---:|---|
| 11-1021.00 | 11-3031.00 | 25.0% | 66.7% | 81.8% | Recommended |
| 11-1021.00 | 13-2072.00 | 11.1% | 53.8% | 70.4% | Below threshold |
| 11-1021.00 | 15-2031.00 | 17.6% | 53.8% | 59.4% | Below threshold |
| 11-3031.00 | 13-2072.00 | 11.1% | 81.8% | 75.3% | Below threshold |
| 11-3031.00 | 15-2031.00 | 0.0% | 42.9% | 70.5% | Below threshold |
| 13-2072.00 | 15-2031.00 | 0.0% | 53.8% | 90.6% | Below threshold |
