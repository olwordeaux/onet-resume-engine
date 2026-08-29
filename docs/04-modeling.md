# 4. Modeling

## Occupation Comparisons

The analysis scripts compare occupations pairwise using two measures:

- Jaccard similarity measures shared item names divided by the total unique item names.
- Weighted cosine similarity compares importance-score vectors, assigning zero to an item absent from one occupation.

Skills, knowledge, software, and tasks are analyzed from the tidy CSV datasets.

## Career Transition Rules

Transition pathways are identified when occupation pairs meet these thresholds:

- Software Jaccard similarity is at least 25%.
- Knowledge Jaccard similarity is at least 25%.
- Skills weighted cosine similarity is at least 75%.

These rules are implemented in the core analysis pipeline.

## Composite Profile

`build_it_consultant_profile.py` combines four occupations: Chief Executives, General and Operations Managers, Computer Systems Analysts, and Computer User Support Specialists. It averages importance scores by capability name and combines software tools, retaining a hot-technology flag when any source occupation marks the tool as hot.
