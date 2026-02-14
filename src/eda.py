from __future__ import annotations
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

def _save_missing_bar(missing_pct: pd.Series, out_dir: Path) -> Path:
    out_dir.mkdir(parents=True, exist_ok=True)
    fig_path = out_dir / "missing_pct.png"

    top = missing_pct.sort_values(ascending=False).head(25)
    plt.figure()
    top.plot(kind="bar")
    plt.title("Top columnas con % de nulos")
    plt.ylabel("% nulos")
    plt.tight_layout()
    plt.savefig(fig_path, dpi=160)
    plt.close()

    return fig_path

def run_eda(df: pd.DataFrame, report_path: Path, figures_dir: Path) -> None:
    report_path.parent.mkdir(parents=True, exist_ok=True)

    shape = df.shape
    dtypes = df.dtypes
    missing_pct = (df.isna().mean() * 100).round(2)
    duplicates = int(df.duplicated().sum())

    # cardinalidad de categóricas (ayuda a justificar normalización)
    cat_cols = df.select_dtypes(include=["object", "string", "category"]).columns
    cardinality = (
        df[cat_cols].nunique(dropna=True).sort_values(ascending=False)
        if len(cat_cols) else pd.Series(dtype="int64")
    )

    fig_missing = _save_missing_bar(missing_pct, figures_dir)

    lines = []
    lines.append("# Reporte EDA (Python)\n")
    lines.append("## Tamaño del dataset\n")
    lines.append(f"- Filas: {shape[0]}\n- Columnas: {shape[1]}\n")

    lines.append("## Tipos de datos\n")
    lines.append("```text\n" + dtypes.to_string() + "\n```\n")

    lines.append("## Valores faltantes (% por columna)\n")
    lines.append("```text\n" + missing_pct.sort_values(ascending=False).to_string() + "\n```\n")
    lines.append(f"- Gráfico: {fig_missing.as_posix()}\n")

    lines.append("## Duplicados exactos\n")
    lines.append(f"- Total duplicados: {duplicates}\n")

    if len(cardinality):
        lines.append("\n## Cardinalidad de columnas categóricas (número de categorías)\n")
        lines.append("```text\n" + cardinality.head(30).to_string() + "\n```\n")

    report_path.write_text("\n".join(lines), encoding="utf-8")
