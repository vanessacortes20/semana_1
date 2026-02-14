from __future__ import annotations
import pandas as pd
import re


# =========================
# Funciones puras (df -> df)
# =========================

def standardize_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Estandariza nombres de columnas:
    - strip
    - lower
    - espacios -> _
    """
    out = df.copy()
    out.columns = (
        out.columns.astype(str)
        .str.strip()
        .str.lower()
        .str.replace(" ", "_", regex=False)
    )
    return out


def drop_exact_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    """Elimina filas duplicadas exactas."""
    return df.drop_duplicates().copy()


def trim_strings(df: pd.DataFrame) -> pd.DataFrame:
    """Recorta espacios en columnas tipo texto."""
    out = df.copy()
    cols = out.select_dtypes(include=["object", "string"]).columns
    for c in cols:
        out[c] = out[c].astype("string").str.strip()
    return out


def normalize_missing_tokens(df: pd.DataFrame) -> pd.DataFrame:
    """
    Normaliza tokens comunes de faltantes a NA (solo en texto).
    """
    out = df.copy()
    tokens = {"", "na", "n/a", "null", "none", "nan", "sin dato", "s/d"}
    cols = out.select_dtypes(include=["object", "string"]).columns
    for c in cols:
        s = out[c].astype("string").str.strip()
        out[c] = s.str.lower().replace(list(tokens), pd.NA)
    return out


def parse_percent_columns(df: pd.DataFrame, cols: list[str]) -> pd.DataFrame:
    """
    Convierte columnas de porcentaje (ej: '12,3%' o '12.3 %') a float.
    Regla:
      - quita % y espacios
      - coma decimal -> punto
      - coerción segura
    """
    out = df.copy()
    for c in cols:
        if c in out.columns:
            s = out[c].astype("string").str.strip()
            s = s.str.replace("%", "", regex=False)
            s = s.str.replace(",", ".", regex=False)
            s = s.str.replace(" ", "", regex=False)
            out[c] = pd.to_numeric(s, errors="coerce")
    return out


def parse_month_year(df: pd.DataFrame, col: str) -> pd.DataFrame:
    """
    Convierte columna tipo 'Mes año' a datetime.
    Soporta formatos comunes:
      - 'Enero 2024'
      - 'ene 2024'
      - '2024-01'
      - '01/2024'
    Si no puede parsear, deja NaT.
    """
    out = df.copy()
    if col not in out.columns:
        return out

    s = out[col].astype("string").str.strip()

    # Intento 1: parseo directo (para '2024-01', '01/2024', etc.)
    dt = pd.to_datetime(s, errors="coerce", dayfirst=True)

    # Intento 2: si falló, tratar mes en español (Enero 2024, ene 2024)
    # mapeo básico de meses
    meses = {
        "enero": "01", "ene": "01",
        "febrero": "02", "feb": "02",
        "marzo": "03", "mar": "03",
        "abril": "04", "abr": "04",
        "mayo": "05", "may": "05",
        "junio": "06", "jun": "06",
        "julio": "07", "jul": "07",
        "agosto": "08", "ago": "08",
        "septiembre": "09", "sep": "09", "setiembre": "09", "set": "09",
        "octubre": "10", "oct": "10",
        "noviembre": "11", "nov": "11",
        "diciembre": "12", "dic": "12",
    }

    def _spanish_month_to_ym(x: str) -> str | None:
        if x is None:
            return None
        x = str(x).strip().lower()
        # Buscar algo tipo "mes año"
        parts = re.split(r"\s+", x)
        if len(parts) < 2:
            return None
        mes = parts[0]
        year = parts[-1]
        if mes in meses and year.isdigit() and len(year) == 4:
            return f"{year}-{meses[mes]}-01"
        return None

    mask_failed = dt.isna()
    if mask_failed.any():
        candidate = s[mask_failed].map(_spanish_month_to_ym)
        dt2 = pd.to_datetime(candidate, errors="coerce")
        dt.loc[mask_failed] = dt2

    out[col] = dt
    return out


def impute_missing(df: pd.DataFrame) -> pd.DataFrame:
    """
    Imputación simple y defendible:
    - numéricas: mediana
    - categóricas: 'desconocido'
    """
    out = df.copy()

    num_cols = out.select_dtypes(include=["number"]).columns
    for c in num_cols:
        out[c] = out[c].fillna(out[c].median())

    cat_cols = out.select_dtypes(include=["object", "string", "category"]).columns
    for c in cat_cols:
        out[c] = out[c].fillna("desconocido")

    return out


def enforce_domain_rules(df: pd.DataFrame) -> pd.DataFrame:
    """
    Reglas de negocio / validez.
    Para tasas (%) lo razonable es [0, 100].
    Se dejan fuera de rango como NA para que la imputación las trate.
    """
    out = df.copy()
    for c in ["tasa_de_ocupación_(%)", "tasa_de_desempleo_(%)",
              "tasa_de_ocupacion_(%)", "tasa_de_desempleo_(%)"]:
        if c in out.columns:
            out.loc[(out[c] < 0) | (out[c] > 100), c] = pd.NA
    return out


def clean_pipeline(df: pd.DataFrame) -> pd.DataFrame:
    """
    Pipeline puro: entra df, sale df limpio.
    Ajustado a tu dataset de ocupación/desempleo.
    """
    out = df.copy()
    out = standardize_columns(out)
    out = drop_exact_duplicates(out)
    out = trim_strings(out)
    out = normalize_missing_tokens(out)

    # columnas esperadas tras estandarizar (ajusta si tu estándar deja tildes distinto)
    out = parse_month_year(out, "fecha_(mes_año)")
    out = parse_percent_columns(out, ["tasa_de_ocupación_(%)", "tasa_de_desempleo_(%)"])
    out = enforce_domain_rules(out)

    out = impute_missing(out)
    return out
