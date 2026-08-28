# 6. Deployment

## Outputs

The pipeline writes its outputs locally:

- Raw API responses: `data/raw/`
- Normalized occupation profiles: `data/processed/*.json`
- Tidy analysis data: `data/processed/tidy_*.csv`
- Markdown analysis reports: `reports/`

## Main Operations

```bash
python -m onet_engine.ingestion <O*NET-SOC-code>
python -m onet_engine.normalize <O*NET-SOC-code>
python -m onet_engine.build_ml_vectors
python generate_report.py
python generate_process_report.py
python -m pytest tests
```

## Reproducibility

The source scripts, tests, and Markdown reports are version-controlled. Raw and processed data are ignored by Git and must be regenerated with a valid `ONET_API_KEY` when setting up another environment.

## Presentation Artifact

`reports/onet_pipeline_process.md` is the concise end-to-end explanation of the completed pipeline. This document set provides the CRISP-DM detail behind each step.
