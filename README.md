<img width="931" height="105" alt="image" src="https://github.com/user-attachments/assets/af823622-6ac3-4ce8-a96e-b4b219ceb741" />

---

# Actividad – EDA, Limpieza Modular y Análisis Descriptivo

## Descripción general

Esta actividad consiste en construir un pipeline en Python para analizar indicadores de ocupación y desempleo en Colombia. El flujo incluye análisis exploratorio de datos (EDA), limpieza modular mediante funciones puras, generación de un dataset limpio y análisis descriptivo, con reportes automáticos en formato Markdown.

---

## Objetivos

- Evaluar la calidad del dataset original.
- Identificar problemas de formato y tipado.
- Aplicar limpieza modular usando funciones puras.
- Generar un dataset limpio.
- Realizar análisis descriptivo sobre los datos depurados.

---

## Descripción del dataset

El dataset contiene indicadores laborales de ocupación y desempleo a nivel nacional y por áreas metropolitanas en Colombia.

**Archivo original:**

1_Ocupacion_y_desempleo_total_nacional_7_o_13_areas_metropolitanas.csv

**Fuente:** Banco de la República de Colombia.

Variables principales:

- Fecha (Mes año)  
- Metodología  
- Cobertura geográfica  
- Tasa de ocupación (%)  
- Tasa de desempleo (%)  

## Estructura del repositorio

```text
.
├── data/
│   ├── raw/              # Dataset original
│   └── processed/        # Dataset limpio (CSV)
│
├── reports/
│   ├── eda_summary.md          # Resultados del EDA
│   ├── descriptive_summary.md  # Análisis descriptivo
│   └── figures/                # Gráficos generados automáticamente
│
├── src/
│   ├── cleaning.py       # Funciones puras de limpieza
│   ├── eda.py            # Lógica del EDA
│   └── descriptive.py    # Lógica del análisis descriptivo
│
├── scripts/
│   ├── run_eda.py         # Ejecuta EDA sobre dataset original
│   ├── run_cleaning.py    # Genera dataset limpio
│   └── run_descriptive.py # Ejecuta análisis descriptivo
│
├── requirements.txt
├── .gitignore
└── README.md

```

---

## Metodología

### EDA
Se analizan tipos de datos, valores faltantes, duplicados y cardinalidad para justificar la limpieza.

### Limpieza

Implementada en `src/cleaning.py` mediante funciones puras (`DataFrame → DataFrame`), incluyendo:

- Estandarización de columnas.
- Conversión de porcentajes a numérico.
- Parseo de fechas.
- Validación básica de dominio.

### Análisis descriptivo

Se realiza sobre el dataset limpio e incluye estadísticas básicas (media, mediana, desviación, IQR y outliers).

## Ejecución

Desde la raíz del repositorio:

```bash
pip install -r requirements.txt
python scripts/run_eda.py
python scripts/run_cleaning.py
python scripts/run_descriptive.py

```

## Flujo

Dataset original → EDA → Limpieza → Dataset limpio → Análisis descriptivo

## Resultados

- Dataset limpio: `data/processed/ocupacion_y_desempleo_clean.csv`
- Reportes:
  - `reports/eda_summary.md`
  - `reports/descriptive_summary.md`

## Tecnologías

- Python
- Pandas
- NumPy
- Matplotlib

## Conclusión

La actividad implementa un flujo básico de preparación de datos que parte del diagnóstico del dataset original, aplica limpieza modular y finaliza con análisis descriptivo sobre los datos depurados.





