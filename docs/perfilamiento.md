# Perfilamiento de datos de bronce

> Perfil generado el 25 de octubre de 2026 sobre los archivos Parquet disponibles localmente en `data/bronze/`. Los resultados describen ese snapshot y pueden cambiar al volver a extraer los datos.

## Criterios

- Filas y columnas corresponden al Parquet, incluidas las tres columnas de linaje (`_fuente`, `_origen`, `_extraido_en`).
- Tipos son los tipos inferidos por pandas al leer Parquet.
- Nulos son valores nulos de Parquet (no cadenas vacías ni marcadores textuales). El porcentaje es `nulos / filas × 100`.
- Filas duplicadas cuenta las repeticiones excedentes (`duplicated(keep="first")`) comparando solo columnas de datos; se excluye el linaje para que metadatos de extracción no oculten duplicados.
- Los rangos son inclusivos. Para EnerAndes se interpretaron los formatos mensuales presentes en `col_0`; encabezados y filas `TOTAL` se ignoran solo al calcular el rango y permanecen en el archivo. En NOAA y EPM se dispone solo del año. El catálogo XM muestra la fecha de captura, no un periodo histórico.

## Resumen por archivo

| Archivo | Filas | Columnas | Filas duplicadas* | Rango de fechas |
|---|---:|---:|---:|---|
| `enerandes_ventas_2023.parquet` | 1.114 | 10 | 32 | 2023-01-01 a 2023-12-01 (periodos detectados en col_0; encabezados/totales ignorados solo para el rango) |
| `enerandes_ventas_2024.parquet` | 1.114 | 11 | 32 | 2024-01-01 a 2024-12-01 (periodos detectados en col_0; encabezados/totales ignorados solo para el rango) |
| `enerandes_ventas_2025.parquet` | 1.117 | 10 | 32 | 2025-01-01 a 2025-12-01 (periodos detectados en col_0; encabezados/totales ignorados solo para el rango) |
| `enerandes_ventas_2026.parquet` | 839 | 10 | 24 | 2026-01-01 a 2026-09-01 (periodos detectados en col_0; encabezados/totales ignorados solo para el rango) |
| `epm_tarifas_historicas.parquet` | 3.623 | 15 | 10 | 2016 a 2021 (solo año) |
| `ideam_precipitacion_diaria.parquet` | 29.804 | 11 | 0 | 2025-01-01 a 2026-07-24 |
| `ideam_temperatura_diaria.parquet` | 17.349 | 13 | 0 | 2025-01-01 a 2026-07-24 |
| `noaa_oni.parquet` | 920 | 7 | 0 | 1950 a 2026 (solo año) |
| `xm_aportes_energia.parquet` | 1.004 | 6 | 0 | 2024-01-01 a 2026-09-30 |
| `xm_demanda.parquet` | 1.004 | 30 | 0 | 2024-01-01 a 2026-09-30 |
| `xm_embalses.parquet` | 1.004 | 6 | 0 | 2024-01-01 a 2026-09-30 |
| `xm_generacion.parquet` | 350.361 | 30 | 0 | 2024-01-01 a 2026-09-30 |
| `xm_listado_recursos.parquet` | 2.493 | 14 | 2 | 2026-10-25 a 2026-10-25 (fecha de captura del catálogo) |
| `xm_precio_bolsa.parquet` | 1.004 | 30 | 0 | 2024-01-01 a 2026-09-30 |

\* Repeticiones excedentes de filas de datos; se excluye linaje.

## Perfil por columna

### `enerandes_ventas_2023.parquet`

- **Filas:** 1.114 | **Columnas:** 10 | **Filas duplicadas:** 32 | **Rango:** 2023-01-01 a 2023-12-01 (periodos detectados en col_0; encabezados/totales ignorados solo para el rango)

| Columna | Tipo | Nulos | Nulos (%) |
|---|---|---:|---:|
| `col_0` | `str` | 0 | 0.00% |
| `col_1` | `str` | 1 | 0.09% |
| `col_2` | `str` | 16 | 1.44% |
| `col_3` | `str` | 1 | 0.09% |
| `col_4` | `str` | 10 | 0.90% |
| `col_5` | `str` | 8 | 0.72% |
| `col_6` | `str` | 1 | 0.09% |
| `_fuente` | `str` | 0 | 0.00% |
| `_origen` | `str` | 0 | 0.00% |
| `_extraido_en` | `str` | 0 | 0.00% |

### `enerandes_ventas_2024.parquet`

- **Filas:** 1.114 | **Columnas:** 11 | **Filas duplicadas:** 32 | **Rango:** 2024-01-01 a 2024-12-01 (periodos detectados en col_0; encabezados/totales ignorados solo para el rango)

| Columna | Tipo | Nulos | Nulos (%) |
|---|---|---:|---:|
| `col_0` | `str` | 0 | 0.00% |
| `col_1` | `str` | 1 | 0.09% |
| `col_2` | `str` | 4 | 0.36% |
| `col_3` | `str` | 1 | 0.09% |
| `col_4` | `str` | 8 | 0.72% |
| `col_5` | `str` | 1 | 0.09% |
| `col_6` | `str` | 12 | 1.08% |
| `col_7` | `str` | 1 | 0.09% |
| `_fuente` | `str` | 0 | 0.00% |
| `_origen` | `str` | 0 | 0.00% |
| `_extraido_en` | `str` | 0 | 0.00% |

### `enerandes_ventas_2025.parquet`

- **Filas:** 1.117 | **Columnas:** 10 | **Filas duplicadas:** 32 | **Rango:** 2025-01-01 a 2025-12-01 (periodos detectados en col_0; encabezados/totales ignorados solo para el rango)

| Columna | Tipo | Nulos | Nulos (%) |
|---|---|---:|---:|
| `col_0` | `str` | 1 | 0.09% |
| `col_1` | `str` | 4 | 0.36% |
| `col_2` | `str` | 10 | 0.90% |
| `col_3` | `str` | 4 | 0.36% |
| `col_4` | `str` | 10 | 0.90% |
| `col_5` | `str` | 8 | 0.72% |
| `col_6` | `str` | 4 | 0.36% |
| `_fuente` | `str` | 0 | 0.00% |
| `_origen` | `str` | 0 | 0.00% |
| `_extraido_en` | `str` | 0 | 0.00% |

### `enerandes_ventas_2026.parquet`

- **Filas:** 839 | **Columnas:** 10 | **Filas duplicadas:** 24 | **Rango:** 2026-01-01 a 2026-09-01 (periodos detectados en col_0; encabezados/totales ignorados solo para el rango)

| Columna | Tipo | Nulos | Nulos (%) |
|---|---|---:|---:|
| `col_0` | `str` | 1 | 0.12% |
| `col_1` | `str` | 4 | 0.48% |
| `col_2` | `str` | 9 | 1.07% |
| `col_3` | `str` | 4 | 0.48% |
| `col_4` | `str` | 9 | 1.07% |
| `col_5` | `str` | 11 | 1.31% |
| `col_6` | `str` | 4 | 0.48% |
| `_fuente` | `str` | 0 | 0.00% |
| `_origen` | `str` | 0 | 0.00% |
| `_extraido_en` | `str` | 0 | 0.00% |

### `epm_tarifas_historicas.parquet`

- **Filas:** 3.623 | **Columnas:** 15 | **Filas duplicadas:** 10 | **Rango:** 2016 a 2021 (solo año)

| Columna | Tipo | Nulos | Nulos (%) |
|---|---|---:|---:|
| `tipodeinformacion` | `str` | 0 | 0.00% |
| `tipodetarifa` | `str` | 0 | 0.00% |
| `tipodedato` | `str` | 0 | 0.00% |
| `rangodeconsumo` | `str` | 0 | 0.00% |
| `nivel` | `str` | 0 | 0.00% |
| `propiedadepm` | `str` | 1 | 0.03% |
| `compartido` | `str` | 1 | 0.03% |
| `propiedaddelcliente` | `str` | 1 | 0.03% |
| `punta` | `str` | 1 | 0.03% |
| `fueradepunta` | `str` | 1 | 0.03% |
| `year` | `str` | 1 | 0.03% |
| `mes` | `str` | 1 | 0.03% |
| `_fuente` | `str` | 0 | 0.00% |
| `_origen` | `str` | 0 | 0.00% |
| `_extraido_en` | `str` | 0 | 0.00% |

### `ideam_precipitacion_diaria.parquet`

- **Filas:** 29.804 | **Columnas:** 11 | **Filas duplicadas:** 0 | **Rango:** 2025-01-01 a 2026-07-24

| Columna | Tipo | Nulos | Nulos (%) |
|---|---|---:|---:|
| `codigoestacion` | `str` | 0 | 0.00% |
| `nombreestacion` | `str` | 0 | 0.00% |
| `municipio` | `str` | 0 | 0.00% |
| `latitud` | `str` | 0 | 0.00% |
| `longitud` | `str` | 0 | 0.00% |
| `fecha` | `str` | 0 | 0.00% |
| `precipitacion_mm` | `str` | 0 | 0.00% |
| `n_obs` | `str` | 0 | 0.00% |
| `_fuente` | `str` | 0 | 0.00% |
| `_origen` | `str` | 0 | 0.00% |
| `_extraido_en` | `str` | 0 | 0.00% |

### `ideam_temperatura_diaria.parquet`

- **Filas:** 17.349 | **Columnas:** 13 | **Filas duplicadas:** 0 | **Rango:** 2025-01-01 a 2026-07-24

| Columna | Tipo | Nulos | Nulos (%) |
|---|---|---:|---:|
| `codigoestacion` | `str` | 0 | 0.00% |
| `nombreestacion` | `str` | 0 | 0.00% |
| `municipio` | `str` | 0 | 0.00% |
| `latitud` | `str` | 0 | 0.00% |
| `longitud` | `str` | 0 | 0.00% |
| `fecha` | `str` | 0 | 0.00% |
| `temperatura_media_c` | `str` | 0 | 0.00% |
| `temperatura_minima_c` | `str` | 0 | 0.00% |
| `temperatura_maxima_c` | `str` | 0 | 0.00% |
| `n_obs` | `str` | 0 | 0.00% |
| `_fuente` | `str` | 0 | 0.00% |
| `_origen` | `str` | 0 | 0.00% |
| `_extraido_en` | `str` | 0 | 0.00% |

### `noaa_oni.parquet`

- **Filas:** 920 | **Columnas:** 7 | **Filas duplicadas:** 0 | **Rango:** 1950 a 2026 (solo año)

| Columna | Tipo | Nulos | Nulos (%) |
|---|---|---:|---:|
| `SEAS` | `str` | 0 | 0.00% |
| `YR` | `str` | 0 | 0.00% |
| `TOTAL` | `str` | 0 | 0.00% |
| `ANOM` | `str` | 0 | 0.00% |
| `_fuente` | `str` | 0 | 0.00% |
| `_origen` | `str` | 0 | 0.00% |
| `_extraido_en` | `str` | 0 | 0.00% |

### `xm_aportes_energia.parquet`

- **Filas:** 1.004 | **Columnas:** 6 | **Filas duplicadas:** 0 | **Rango:** 2024-01-01 a 2026-09-30

| Columna | Tipo | Nulos | Nulos (%) |
|---|---|---:|---:|
| `Date` | `str` | 0 | 0.00% |
| `Id` | `str` | 0 | 0.00% |
| `Value` | `str` | 0 | 0.00% |
| `_fuente` | `str` | 0 | 0.00% |
| `_origen` | `str` | 0 | 0.00% |
| `_extraido_en` | `str` | 0 | 0.00% |

### `xm_demanda.parquet`

- **Filas:** 1.004 | **Columnas:** 30 | **Filas duplicadas:** 0 | **Rango:** 2024-01-01 a 2026-09-30

| Columna | Tipo | Nulos | Nulos (%) |
|---|---|---:|---:|
| `Date` | `str` | 0 | 0.00% |
| `Id` | `str` | 0 | 0.00% |
| `code` | `str` | 0 | 0.00% |
| `Hour01` | `str` | 0 | 0.00% |
| `Hour02` | `str` | 0 | 0.00% |
| `Hour03` | `str` | 0 | 0.00% |
| `Hour04` | `str` | 0 | 0.00% |
| `Hour05` | `str` | 0 | 0.00% |
| `Hour06` | `str` | 0 | 0.00% |
| `Hour07` | `str` | 0 | 0.00% |
| `Hour08` | `str` | 0 | 0.00% |
| `Hour09` | `str` | 0 | 0.00% |
| `Hour10` | `str` | 0 | 0.00% |
| `Hour11` | `str` | 0 | 0.00% |
| `Hour12` | `str` | 0 | 0.00% |
| `Hour13` | `str` | 0 | 0.00% |
| `Hour14` | `str` | 0 | 0.00% |
| `Hour15` | `str` | 0 | 0.00% |
| `Hour16` | `str` | 0 | 0.00% |
| `Hour17` | `str` | 0 | 0.00% |
| `Hour18` | `str` | 0 | 0.00% |
| `Hour19` | `str` | 0 | 0.00% |
| `Hour20` | `str` | 0 | 0.00% |
| `Hour21` | `str` | 0 | 0.00% |
| `Hour22` | `str` | 0 | 0.00% |
| `Hour23` | `str` | 0 | 0.00% |
| `Hour24` | `str` | 0 | 0.00% |
| `_fuente` | `str` | 0 | 0.00% |
| `_origen` | `str` | 0 | 0.00% |
| `_extraido_en` | `str` | 0 | 0.00% |

### `xm_embalses.parquet`

- **Filas:** 1.004 | **Columnas:** 6 | **Filas duplicadas:** 0 | **Rango:** 2024-01-01 a 2026-09-30

| Columna | Tipo | Nulos | Nulos (%) |
|---|---|---:|---:|
| `Date` | `str` | 0 | 0.00% |
| `Id` | `str` | 0 | 0.00% |
| `Value` | `str` | 0 | 0.00% |
| `_fuente` | `str` | 0 | 0.00% |
| `_origen` | `str` | 0 | 0.00% |
| `_extraido_en` | `str` | 0 | 0.00% |

### `xm_generacion.parquet`

- **Filas:** 350.361 | **Columnas:** 30 | **Filas duplicadas:** 0 | **Rango:** 2024-01-01 a 2026-09-30

| Columna | Tipo | Nulos | Nulos (%) |
|---|---|---:|---:|
| `Date` | `str` | 0 | 0.00% |
| `Id` | `str` | 0 | 0.00% |
| `code` | `str` | 0 | 0.00% |
| `Hour01` | `str` | 0 | 0.00% |
| `Hour02` | `str` | 0 | 0.00% |
| `Hour03` | `str` | 0 | 0.00% |
| `Hour04` | `str` | 0 | 0.00% |
| `Hour05` | `str` | 0 | 0.00% |
| `Hour06` | `str` | 0 | 0.00% |
| `Hour07` | `str` | 0 | 0.00% |
| `Hour08` | `str` | 0 | 0.00% |
| `Hour09` | `str` | 0 | 0.00% |
| `Hour10` | `str` | 0 | 0.00% |
| `Hour11` | `str` | 0 | 0.00% |
| `Hour12` | `str` | 0 | 0.00% |
| `Hour13` | `str` | 0 | 0.00% |
| `Hour14` | `str` | 0 | 0.00% |
| `Hour15` | `str` | 0 | 0.00% |
| `Hour16` | `str` | 0 | 0.00% |
| `Hour17` | `str` | 0 | 0.00% |
| `Hour18` | `str` | 0 | 0.00% |
| `Hour19` | `str` | 0 | 0.00% |
| `Hour20` | `str` | 0 | 0.00% |
| `Hour21` | `str` | 0 | 0.00% |
| `Hour22` | `str` | 0 | 0.00% |
| `Hour23` | `str` | 0 | 0.00% |
| `Hour24` | `str` | 0 | 0.00% |
| `_fuente` | `str` | 0 | 0.00% |
| `_origen` | `str` | 0 | 0.00% |
| `_extraido_en` | `str` | 0 | 0.00% |

### `xm_listado_recursos.parquet`

- **Filas:** 2.493 | **Columnas:** 14 | **Filas duplicadas:** 2 | **Rango:** 2026-10-25 a 2026-10-25 (fecha de captura del catálogo)

| Columna | Tipo | Nulos | Nulos (%) |
|---|---|---:|---:|
| `Date` | `str` | 0 | 0.00% |
| `Id` | `str` | 0 | 0.00% |
| `Code` | `str` | 0 | 0.00% |
| `Name` | `str` | 0 | 0.00% |
| `Type` | `str` | 0 | 0.00% |
| `Disp` | `str` | 0 | 0.00% |
| `RecType` | `str` | 0 | 0.00% |
| `CompanyCode` | `str` | 0 | 0.00% |
| `EnerSource` | `str` | 0 | 0.00% |
| `OperStartdate` | `str` | 0 | 0.00% |
| `State` | `str` | 0 | 0.00% |
| `_fuente` | `str` | 0 | 0.00% |
| `_origen` | `str` | 0 | 0.00% |
| `_extraido_en` | `str` | 0 | 0.00% |

### `xm_precio_bolsa.parquet`

- **Filas:** 1.004 | **Columnas:** 30 | **Filas duplicadas:** 0 | **Rango:** 2024-01-01 a 2026-09-30

| Columna | Tipo | Nulos | Nulos (%) |
|---|---|---:|---:|
| `Date` | `str` | 0 | 0.00% |
| `Id` | `str` | 0 | 0.00% |
| `code` | `str` | 0 | 0.00% |
| `Hour01` | `str` | 0 | 0.00% |
| `Hour02` | `str` | 0 | 0.00% |
| `Hour03` | `str` | 0 | 0.00% |
| `Hour04` | `str` | 0 | 0.00% |
| `Hour05` | `str` | 0 | 0.00% |
| `Hour06` | `str` | 0 | 0.00% |
| `Hour07` | `str` | 0 | 0.00% |
| `Hour08` | `str` | 0 | 0.00% |
| `Hour09` | `str` | 0 | 0.00% |
| `Hour10` | `str` | 0 | 0.00% |
| `Hour11` | `str` | 0 | 0.00% |
| `Hour12` | `str` | 0 | 0.00% |
| `Hour13` | `str` | 0 | 0.00% |
| `Hour14` | `str` | 0 | 0.00% |
| `Hour15` | `str` | 0 | 0.00% |
| `Hour16` | `str` | 0 | 0.00% |
| `Hour17` | `str` | 0 | 0.00% |
| `Hour18` | `str` | 0 | 0.00% |
| `Hour19` | `str` | 0 | 0.00% |
| `Hour20` | `str` | 0 | 0.00% |
| `Hour21` | `str` | 0 | 0.00% |
| `Hour22` | `str` | 0 | 0.00% |
| `Hour23` | `str` | 0 | 0.00% |
| `Hour24` | `str` | 0 | 0.00% |
| `_fuente` | `str` | 0 | 0.00% |
| `_origen` | `str` | 0 | 0.00% |
| `_extraido_en` | `str` | 0 | 0.00% |

## Hallazgos de calidad

1. **IDEAM no llega al fin del rango solicitado.** La precipitación (29.804 filas) y la temperatura (17.349 filas) terminan el **24-07-2026**; no tienen filas posteriores. Frente al 30-09-2026 quedan **68 días** sin cobertura en ambos archivos.
2. **Duplicados en EnerAndes.** Al comparar los campos de datos sin linaje, aparecen **32 filas repetidas** en cada archivo de 2023, 2024 y 2025, y **24** en 2026: **120 repeticiones excedentes de 4.184 filas (2,87%)** en total.
3. **Duplicados en tarifas EPM.** `epm_tarifas_historicas.parquet` tiene **10 repeticiones excedentes**; hay 20 filas involucradas en grupos duplicados de un total de 3.623 filas (**0,28%** excedente).
4. **Duplicados en catálogo XM.** `xm_listado_recursos.parquet` contiene **2 repeticiones excedentes** (4 filas pertenecen a grupos duplicados) de 2.493 filas (**0,08%** excedente).
5. **Registro tarifario incompleto.** En EPM, **1 de 3.623 filas (0,03%)** tiene nulos en los cinco campos de tarifa (`propiedadepm`, `compartido`, `propiedaddelcliente`, `punta`, `fueradepunta`), además de `year` y `mes` (**7 valores nulos en esa fila**). Corresponde a `Costo Unitario` / `Costo compra: Gm, i`.
6. **Formato heterogéneo en Excel EnerAndes.** `col_0` presenta **2, 2, 4 y 4** filas no interpretables como periodo mensual en 2023, 2024, 2025 y 2026 respectivamente; incluyen encabezados/títulos y filas `TOTAL`, que se conservaron intencionalmente en bronce. Además, las hojas tienen entre **10 y 11 columnas** y encabezados distintos.
7. **Tipos en la capa bronce.** En los 14 Parquet, los valores se leen con tipo `str`, incluidos campos numéricos y fechas. Es coherente con conservar los datos de origen sin tipar, pero la capa analítica deberá convertirlos y validar errores antes de cálculos.
8. **Nulos concentrados en EPM y EnerAndes.** Los 9 archivos NOAA, IDEAM y XM no presentan nulos en las columnas perfiladas; los nulos se concentran en las cuatro hojas de EnerAndes y la fila tarifaria EPM detallada arriba.
