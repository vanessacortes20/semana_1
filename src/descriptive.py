from __future__ import annotations
import pandas as pd
import numpy as np
from pathlib import Path

def _numeric_describe(df: pd.DataFrame) -> pd.DataFrame:
    num = df.select_dtypes(include=["number"])
    if num.shape[1] == 0:
        return pd.DataFrame()

    desc = num.describe().T  # count, mean, std, min, 25%, 50%, 75%, max
    desc["median"] = num.median(numeric_only=True)
    desc["iqr"] = desc["75%"] - desc["25%"]
    return desc

def _outliers_iqr_counts(df: pd.DataFrame) -> pd.Series:
    num = df.select_dtypes(include=["number"])
    if num.shape[1] == 0:
        return pd.Series(dtype="int64")

    q1 = num.quantile(0.25)
    q3 = num.quantile(0.75)
    iqr = q3 - q1
    lower = q1 - 1.5 * iqr
    upper = q3 + 1.5 * iqr

    mask = num.lt(lower) | num.gt(upper)
    return mask.sum().sort_values(ascending=False)

def _top_categories(df: pd.DataFrame, col: str, top_n: int = 10) -> pd.Series:
    s = df[col].astype("string")
    return s.value_counts(dropna=False).head(top_n)

def generate_descriptive_report(df: pd.DataFrame, report_path: Path, top_n: int = 10) -> None:
    report_path.parent.mkdir(parents=True, exist_ok=True)

    lines: list[str] = []
    lines.append("# Análisis descriptivo (Python)\n")

    lines.append("## Tamaño del dataset\n")
    lines.append(f"- Filas: {df.shape[0]}\n- Columnas: {df.shape[1]}\n")

    lines.append("## Tipos de datos\n")
    lines.append("```text\n" + df.dtypes.to_string() + "\n```\n")

    # Numéricas
    desc_num = _numeric_describe(df)
    lines.append("## Resumen numérico\n")
    if desc_num.empty:
        lines.append("- No se detectaron columnas numéricas (`number`).\n")
    else:
        cols = ["count", "mean", "std", "min", "25%", "50%", "75%", "max", "median", "iqr"]
        lines.append("```text\n" + desc_num[cols].round(4).to_string() + "\n```\n")

        out_counts = _outliers_iqr_counts(df)
        lines.append("## Outliers por regla IQR (conteo)\n")
        lines.append("```text\n" + out_counts.to_string() + "\n```\n")

    # Categóricas
    cat_cols = df.select_dtypes(include=["object", "string", "category"]).columns
    lines.append("## Resumen categórico\n")
    if len(cat_cols) == 0:
        lines.append("- No se detectaron columnas categóricas.\n")
    else:
        cardinality = df[cat_cols].nunique(dropna=True).sort_values(ascending=False)
        lines.append("### Cardinalidad (número de categorías)\n")
        lines.append("```text\n" + cardinality.to_string() + "\n```\n")

        lines.append("\n### Top categorías (frecuencias)\n")
        for c in cat_cols:
            lines.append(f"\n**{c}**\n")
            lines.append("```text\n" + _top_categories(df, c, top_n=top_n).to_string() + "\n```\n")

    report_path.write_text("\n".join(lines), encoding="utf-8")
