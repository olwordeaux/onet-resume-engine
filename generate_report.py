import os
import pandas as pd

raw_dir = "data/raw"
proc_dir = "data/processed"

print("="*60)
print("             O*NET DATA PIPELINE AUDIT REPORT            ")
print("="*60)

# 1. Raw Folder Audit
raw_files = [f for f in os.listdir(raw_dir) if f.endswith(".json")] if os.path.exists(raw_dir) else []
raw_size = sum(os.path.getsize(os.path.join(raw_dir, f)) for f in raw_files) / 1024
print(f"📁 Ingestion Stage [data/raw/]:")
print(f"   - Raw Payloads:         {len(raw_files)} / 20 files")
print(f"   - Total Storage Size:   {raw_size:.2f} KB")
status_raw = "🟢 COMPLETE" if len(raw_files) == 20 else "🔴 INCOMPLETE"
print(f"   - Ingestion Status:     {status_raw}")

# 2. Processed Folder Audit
proc_files = os.listdir(proc_dir) if os.path.exists(proc_dir) else []
json_proc = [f for f in proc_files if f.endswith(".json") and not f.endswith("_clean.json")]
csv_proc = [f for f in proc_files if f.endswith(".csv")]
proc_size = sum(os.path.getsize(os.path.join(proc_dir, f)) for f in proc_files) / 1024
print(f"\n📁 Preparation Stage [data/processed/]:")
print(f"   - Master JSONs:         {len(json_proc)} / 4 files")
print(f"   - Tabular CSVs:         {len(csv_proc)} / 3 files")
print(f"   - Total Storage Size:   {proc_size:.2f} KB")
status_prep = "🟢 COMPLETE" if (len(json_proc) == 4 and len(csv_proc) == 3) else "🔴 INCOMPLETE"
print(f"   - Preparation Status:   {status_prep}")

# 3. Tidy CSV Dataset Verification
if csv_proc:
    print(f"\n📊 Tabular Tidy Dataset Verification:")
    for csv in sorted(csv_proc):
        csv_path = os.path.join(proc_dir, csv)
        df = pd.read_csv(csv_path)
        print(f"   - {csv:<22} ➔ Rows: {len(df):<3} | Columns: {len(df.columns)}")
print("="*60)
