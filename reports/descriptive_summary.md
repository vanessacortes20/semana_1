# Análisis descriptivo (Python)

## Tamaño del dataset

- Filas: 300
- Columnas: 5

## Tipos de datos

```text
fecha_(mes_año)           object
metodología               object
cobertura_geográfica      object
tasa_de_ocupación_(%)    float64
tasa_de_desempleo_(%)    float64
```

## Resumen numérico

```text
                       count     mean     std      min      25%      50%      75%     max   median     iqr
tasa_de_ocupación_(%)  300.0  58.1202  2.8550  42.4971  56.8410  58.3178  59.9602  64.008  58.3178  3.1193
tasa_de_desempleo_(%)  300.0  11.6125  2.4488   7.0249   9.7353  11.1928  12.9061  21.972  11.1928  3.1708
```

## Outliers por regla IQR (conteo)

```text
tasa_de_ocupación_(%)    9
tasa_de_desempleo_(%)    5
```

## Resumen categórico

### Cardinalidad (número de categorías)

```text
fecha_(mes_año)         300
metodología               1
cobertura_geográfica      1
```


### Top categorías (frecuencias)


**fecha_(mes_año)**

```text
fecha_(mes_año)
2001-01-01    1
2001-02-01    1
2001-03-01    1
2001-04-01    1
2001-05-01    1
2001-06-01    1
2001-07-01    1
2001-08-01    1
2001-09-01    1
2001-10-01    1
```


**metodología**

```text
metodología
metodología geih empalme dane 2022    300
```


**cobertura_geográfica**

```text
cobertura_geográfica
total nacional    300
```
