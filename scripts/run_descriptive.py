from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import pandas as pd
from src.descriptive import generate_descriptive_report

CLEAN_CSV = ROOT / "data" / "processed" / "ocupacion_y_desempleo_clean.csv"
OUT_MD = ROOT / "reports" / "descriptive_summary.md"

def main():
    df = pd.read_csv(CLEAN_CSV)
    generate_descriptive_report(df, OUT_MD, top_n=10)
    print(f"OK: reporte descriptivo -> {OUT_MD}")

if __name__ == "__main__":
    main()
