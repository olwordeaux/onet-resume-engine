# O*NET Skill Overlap Analysis

Pairwise comparison of the four target occupations using the tidy capability dataset.

## Methodology

- **Jaccard similarity**: shared capability names divided by the total unique capability names in the pair.
- **Weighted cosine similarity**: cosine similarity of importance-weight vectors keyed by capability name; absent capabilities receive weight `0`.
- Skills and knowledge are analyzed separately. Values are rounded to one decimal place.

## Skills Overlap

| Occupation A | Occupation B | Jaccard | Weighted cosine | Shared capabilities |
|---|---|---:|---:|---:|
| 11-1021.00 | 11-3031.00 | 66.7% | 81.8% | Active Listening, Complex Problem Solving, Coordination, Critical Thinking, Management of Personnel Resources, Monitoring, Reading Comprehension, Speaking |
| 11-1021.00 | 13-2072.00 | 53.8% | 70.4% | Active Learning, Active Listening, Complex Problem Solving, Critical Thinking, Reading Comprehension, Social Perceptiveness, Speaking |
| 11-1021.00 | 15-2031.00 | 42.9% | 59.4% | Active Learning, Active Listening, Complex Problem Solving, Critical Thinking, Reading Comprehension, Speaking |
| 11-3031.00 | 13-2072.00 | 53.8% | 75.3% | Active Listening, Complex Problem Solving, Critical Thinking, Judgment and Decision Making, Reading Comprehension, Speaking, Writing |
| 11-3031.00 | 15-2031.00 | 53.8% | 70.5% | Active Listening, Complex Problem Solving, Critical Thinking, Judgment and Decision Making, Reading Comprehension, Speaking, Writing |
| 13-2072.00 | 15-2031.00 | 81.8% | 90.6% | Active Learning, Active Listening, Complex Problem Solving, Critical Thinking, Judgment and Decision Making, Mathematics, Reading Comprehension, Speaking, Writing |

### Occupation Codes

- `11-1021.00`
- `11-3031.00`
- `13-2072.00`
- `15-2031.00`
## Knowledge Overlap

| Occupation A | Occupation B | Jaccard | Weighted cosine | Shared capabilities |
|---|---|---:|---:|---:|
| 11-1021.00 | 11-3031.00 | 66.7% | 83.6% | Administration and Management, Administrative, Customer and Personal Service, Economics and Accounting, English Language, Mathematics, Personnel and Human Resources, Sales and Marketing |
| 11-1021.00 | 13-2072.00 | 53.8% | 76.1% | Administration and Management, Administrative, Customer and Personal Service, Economics and Accounting, English Language, Mathematics, Sales and Marketing |
| 11-1021.00 | 15-2031.00 | 53.8% | 67.9% | Administration and Management, Customer and Personal Service, Economics and Accounting, Engineering and Technology, English Language, Mathematics, Production and Processing |
| 11-3031.00 | 13-2072.00 | 81.8% | 91.9% | Administration and Management, Administrative, Customer and Personal Service, Economics and Accounting, Education and Training, English Language, Law and Government, Mathematics, Sales and Marketing |
| 11-3031.00 | 15-2031.00 | 42.9% | 53.1% | Administration and Management, Customer and Personal Service, Economics and Accounting, Education and Training, English Language, Mathematics |
| 13-2072.00 | 15-2031.00 | 53.8% | 64.5% | Administration and Management, Computers and Electronics, Customer and Personal Service, Economics and Accounting, Education and Training, English Language, Mathematics |

### Occupation Codes

- `11-1021.00`
- `11-3031.00`
- `13-2072.00`
- `15-2031.00`
