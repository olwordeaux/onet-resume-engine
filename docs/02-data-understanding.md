# 2. Data Understanding

## Source

The source is the O*NET API. For each occupation code, the pipeline downloads five JSON payloads:

- Overview
- Tasks
- Skills
- Technology skills
- Knowledge

## Current Coverage

- Occupations: 9
- Raw payloads: 45
- Raw payloads per occupation: 5

The selected codes are stored as raw API files in `data/raw/`. The API key is read from `.env` as `ONET_API_KEY` and is not part of the repository data.

## Data Elements Used

- Tasks: task ID, title, importance, and category
- Skills and knowledge: element ID, name, description, and importance
- Technology: software title and hot-technology flag

## Data Quality Checks

The integrity test checks that every resume-mapped occupation has all five raw payloads and its normalized processed profile.
