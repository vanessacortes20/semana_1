from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import pandas as pd
from src.eda import run_eda

RAW = Path("data/raw/ocupacion_y_desempleo.csv")
REPORT = Path("reports/eda_summary.md")
FIGS = Path("reports/figures")

def main():
    df = pd.read_csv(RAW)
    run_eda(df, REPORT, FIGS)
    print(f"OK: reporte EDA -> {REPORT}")

if __name__ == "__main__":
    main()
