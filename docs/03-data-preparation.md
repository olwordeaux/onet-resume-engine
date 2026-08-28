# 3. Data Preparation

## Ingestion

`onet_engine/ingestion.py` downloads the five O*NET reports for a supplied occupation code and saves them unchanged in `data/raw/`.

## Normalization

`onet_engine/normalize.py` combines the five reports into one JSON profile in `data/processed/`. It keeps the top 10 ranked tasks, skills, knowledge elements, and technology tools.

## Tidy Datasets

`onet_engine/build_ml_vectors.py` flattens the normalized profiles into:

- `tidy_tasks.csv`
- `tidy_software.csv`
- `tidy_capabilities.csv`

The current datasets contain 90 task rows, 90 software rows, and 180 capability rows across nine occupations.

## Reproduction Commands

```bash
python -m onet_engine.ingestion <O*NET-SOC-code>
python -m onet_engine.normalize <O*NET-SOC-code>
python -m onet_engine.build_ml_vectors
```
