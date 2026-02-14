from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import pandas as pd
from src.cleaning import clean_pipeline

RAW = ROOT / "data" / "raw" / "ocupacion_y_desempleo.csv"
OUT_PARQUET = ROOT / "data" / "processed" / "ocupacion_y_desempleo_clean.parquet"
OUT_CSV = ROOT / "data" / "processed" / "ocupacion_y_desempleo_clean.csv"

def main():
    df = pd.read_csv(RAW)
    df_clean = clean_pipeline(df)

    OUT_PARQUET.parent.mkdir(parents=True, exist_ok=True)

    df_clean.to_parquet(OUT_PARQUET, index=False)
    df_clean.to_csv(OUT_CSV, index=False)

    print(f"Raw: {df.shape} -> Clean: {df_clean.shape}")
    print(f"Saved parquet: {OUT_PARQUET}")
    print(f"Saved csv: {OUT_CSV}")

if __name__ == "__main__":
    main()
