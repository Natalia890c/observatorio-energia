# Reporte de calidad de las fuentes en capa plata

## Alcance y método de conteo

Este reporte consolida la revisión de los Parquet disponibles en `data/bronze/` y
`data/silver/`. Las fuentes se cuentan como cinco grupos: XM, IDEAM, NOAA, EPM y
EnerAndes. XM reúne sus series horarias, diarias y el catálogo; IDEAM reúne
precipitación y temperatura.

Se documentan **al menos 16 reglas por fuente (81 en total)**. Una regla es un control
distinto sobre estructura, validez, conversión, consistencia o conservación de
los registros. En las tablas, las columnas Antes y Después cuentan filas o
valores que incumplen el control, salvo cuando la unidad indica explícitamente
un conteo de registros transformados, eliminados o retenidos. Cero después
significa que no quedan incumplimientos en Silver; los casos no corregibles se
contabilizan por separado en cuarentena. Los valores faltantes que se conservan
intencionalmente se identifican como tales, no como errores resueltos.

## Resumen

| Fuente | Reglas documentadas | Bronze | Silver | Cuarentena |
|---|---:|---:|---:|---:|
| XM | 16 | 356.889 | 8.461.372 | 2 |
| IDEAM | 16 | 47.153 | 47.153 | 0 |
| NOAA | 16 | 921 | 921 | 0 |
| EPM | 16 | 3.623 | 3.612 | 1 |
| EnerAndes | 17 | 4.184 | 4.007 | 45 |

Las cantidades de Silver corresponden al snapshot inspeccionado. En generación
XM, las 2.473.215 celdas vacías se preservan como valores nulos; no se imputan
como cero ni se consideran cuarentena. Los datos de EnerAndes y EPM incluyen
archivos de cuarentena separados.

## Fuente: XM

**Problemas identificados:** columnas horarias anchas que deben convertirse a
filas, celdas de generación vacías, duplicados exactos y un código de recurso
con dos nombres distintos. Las celdas vacías de generación se consideran
desconocidas, no generación igual a cero.

| # | Problema / control | Regla aplicada | Antes | Después |
|---:|---|---|---:|---:|
| 1 | Precio: tabla horaria ancha | Desplegar 24 horas por fecha | 1.004 filas | 24.096 filas |
| 2 | Demanda: tabla horaria ancha | Desplegar 24 horas por fecha | 1.004 filas | 24.096 filas |
| 3 | Generación: tabla horaria ancha | Desplegar 24 horas por recurso y fecha | 350.361 filas | Parquet existente: 8.408.664; limpiador actual: 5.935.449 |
| 4 | Columnas `Hour01`–`Hour24` faltantes | Requerir las 24 horas en cada serie | 0 columnas faltantes | 0 |
| 5 | Fechas horarias inválidas | Convertir fecha y rechazar fechas inválidas | 0 | 0 |
| 6 | Valores horarios de precio no numéricos | Convertir a número | 0 | 0 |
| 7 | Valores horarios de demanda no numéricos | Convertir a número | 0 | 0 |
| 8 | Valores horarios de generación no numéricos (excluye blancos) | Convertir valores presentes a número | 0 | 0 |
| 9 | Horas vacías de generación | El limpiador actual excluye la observación vacía, sin convertirla en cero | 2.473.215 vacíos | 2.473.215 filas excluidas al reprocesar; Parquet existente conserva 2.473.215 nulos |
| 10 | Valores horarios negativos | Rechazar valores negativos | 0 | 0 |
| 11 | Etiquetas de hora fuera de 1–24 | Numerar las horas del 1 al 24 | 0 | 0 |
| 12 | Fecha/identificador duplicados en series diarias | Mantener clave fecha e identificador única | 0 | 0 |
| 13 | Fechas o valores diarios inválidos en embalses y aportes | Tipar fecha y valor numérico | 0 | 0 |
| 14 | Valores diarios negativos en embalses y aportes | Validar valor no negativo | 0 | 0 |
| 15 | Duplicados exactos en catálogo | Conservar una sola copia | 2 filas excedentes | 0 |
| 16 | Código `PRG1` con dos nombres | No escoger por inferencia; enviar ambas filas a cuarentena | 2 filas conflictivas | 0 en Silver; 2 en cuarentena |

**Métricas por tablas:** embalses, 1.004 → 1.004 filas; aportes, 1.004 →
1.004; catálogo, 2.512 → 2.508. El catálogo final guardado tiene códigos
únicos.

## Fuente: IDEAM

**Problemas identificados:** tipar fechas y variables meteorológicas, comprobar
identificación de estaciones, rangos geográficos, coherencia térmica y unicidad
diaria. La revisión no encontró filas que debieran eliminarse o ponerse en
cuarentena.

| # | Problema / control | Regla aplicada | Antes | Después |
|---:|---|---|---:|---:|
| 1 | Observaciones de precipitación | Conservar registros válidos | 29.804 filas | 29.804 filas |
| 2 | Observaciones de temperatura | Conservar registros válidos | 17.349 filas | 17.349 filas |
| 3 | Fechas de precipitación inválidas | Convertir a fecha | 0 | 0 |
| 4 | Fechas de temperatura inválidas | Convertir a fecha | 0 | 0 |
| 5 | Códigos de estación vacíos | Requerir código | 0 | 0 |
| 6 | Nombres de estación vacíos | Requerir nombre | 0 | 0 |
| 7 | Municipios vacíos | Conservar municipio asociado a la estación | 0 | 0 |
| 8 | Latitudes no numéricas | Convertir a número | 0 | 0 tras conversión de auditoría |
| 9 | Latitudes fuera de −90 a 90 | Validar rango geográfico | 0 | 0 |
| 10 | Longitudes no numéricas | Convertir a número | 0 | 0 tras conversión de auditoría |
| 11 | Longitudes fuera de −180 a 180 | Validar rango geográfico | 0 | 0 |
| 12 | Precipitación no numérica o negativa | Convertir a número y exigir valor ≥ 0 | 0 | 0 |
| 13 | Temperaturas no numéricas | Convertir media, mínima y máxima a número | 0 | 0 |
| 14 | Temperaturas fuera de −10 °C a 60 °C | Validar rango físico definido para el proyecto | 0 | 0 |
| 15 | Temperatura mínima mayor que máxima | Exigir mínima ≤ máxima | 0 | 0 |
| 16 | Media fuera del intervalo mínima–máxima, `n_obs` no positivo/no entero o clave estación-fecha repetida | Validar coherencia, conteo entero positivo y clave única | 0 | 0 |

No se enviaron registros IDEAM a cuarentena. Los valores observados se
conservaron; no se recortaron máximos por umbrales estadísticos.

## Fuente: NOAA (ONI)

**Problemas identificados:** convertir las temporadas trimestrales móviles a
mes central, validar valores y evitar que una temporada se asigne a un mes
incorrecto. Se usa `ANOM` como anomalía ONI y se conserva la fase derivada de
los umbrales del proyecto.

| # | Problema / control | Regla aplicada | Antes | Después |
|---:|---|---|---:|---:|
| 1 | Registros ONI | Conservar observaciones válidas | 921 filas | 921 filas |
| 2 | Etiquetas `SEAS` desconocidas | Aceptar solo las 12 temporadas móviles | 0 | 0 |
| 3 | Años no numéricos | Convertir `YR` a entero | 0 | 0 |
| 4 | Años fuera del intervalo esperado | Validar 1950–2100 | 0 | 0 |
| 5 | Valores `TOTAL` no numéricos | Convertir a número | 0 | 0 |
| 6 | Valores `ANOM` no numéricos | Convertir a número | 0 | 0 |
| 7 | Claves año-temporada duplicadas | Exigir unicidad de `YR` + `SEAS` | 0 | 0 |
| 8 | Temporadas sin mes central asignable | Mapear DJF→enero, …, NDJ→diciembre | 0 | 0 |
| 9 | Fechas mensuales inválidas | Construir fecha al primer día del mes central | 0 | 0 |
| 10 | Meses fuera de 1–12 | Validar mes calendario | 0 | 0 |
| 11 | Fechas mensuales duplicadas | Exigir una observación por mes | 0 | 0 |
| 12 | Fases fuera del catálogo | Permitir El Niño, La Niña o Neutral | 0 | 0 |
| 13 | Fases El Niño mal clasificadas | Aplicar ANOM ≥ 0,5 | 0 | 0 |
| 14 | Fases La Niña mal clasificadas | Aplicar ANOM ≤ −0,5 | 0 | 0 |
| 15 | Fases neutrales mal clasificadas | Aplicar −0,5 < ANOM < 0,5 | 0 | 0 |
| 16 | Campos de fecha, índice o linaje vacíos | Requerir valores completos en Silver | 0 | 0 |

La distribución Silver comprobada es: Neutral 448, La Niña 238 y El Niño 235.
El rango mensual va de enero de 1950 a septiembre de 2026. No hay filas en
cuarentena.

## Fuente: EPM (tarifas históricas)

**Problemas identificados:** diez repeticiones exactas y una fila con cinco
medidas tarifarias, año y mes vacíos. Los valores negativos de `Restricciones:
Rm` se conservan porque son componentes publicados por la fuente y no existe
evidencia para tratarlos como errores.

| # | Problema / control | Regla aplicada | Antes | Después |
|---:|---|---|---:|---:|
| 1 | Filas de tarifas | Conservar registros interpretables | 3.623 | 3.612 Silver + 1 cuarentena |
| 2 | Filas duplicadas exactas | Conservar una copia | 10 excedentes | 0 |
| 3 | Año vacío o no numérico | Convertir año a entero; poner fila inválida en cuarentena | 1 | 0 Silver; 1 cuarentena |
| 4 | Año fuera de 1900–2100 | Validar rango | 0 | 0 |
| 5 | Mes no reconocido | Mapear nombres españoles a mes 1–12 | 1 | 0 Silver; 1 cuarentena |
| 6 | `propiedadepm` vacío/no interpretable | Convertir a número; cuarentena si falta | 1 | 0 Silver |
| 7 | `compartido` vacío/no interpretable | Convertir a número; cuarentena si falta | 1 | 0 Silver |
| 8 | `propiedaddelcliente` vacío/no interpretable | Convertir a número; cuarentena si falta | 1 | 0 Silver |
| 9 | `punta` vacío/no interpretable | Convertir a número; cuarentena si falta | 1 | 0 Silver |
| 10 | `fueradepunta` vacío/no interpretable | Convertir a número; cuarentena si falta | 1 | 0 Silver |
| 11 | Valores no numéricos no vacíos en medidas | Rechazar conversión inválida | 0 | 0 |
| 12 | Categorías vacías (tipo de información, tarifa, dato, rango y nivel) | Requerir las cinco dimensiones | 0 | 0 |
| 13 | Valores tarifarios negativos | Conservar; no imputar ni forzar a cero | 15 celdas negativas | 15 celdas negativas |
| 14 | Linaje incompleto | Conservar fuente, URL y fecha de extracción | 0 | 0 |
| 15 | Registro incompleto no utilizable | Separar con motivo en cuarentena | 1 fila inválida | 1 fila documentada |
| 16 | Mes fuera de 1–12 después del mapeo | Validar rango de mes | 0 | 0 |

## Fuente: EnerAndes

**Problemas identificados:** encabezados heterogéneos, títulos y notas previos,
totales, formatos de fecha distintos, unidades mixtas en 2024, variantes de
municipios y categorías, duplicados, energía faltante o negativa. La fecha
`01/03/2026` se interpreta como día/mes/año: marzo de 2026.

| # | Problema / control | Regla aplicada | Antes | Después |
|---:|---|---|---:|---:|
| 1 | Encabezados no uniformes en cuatro hojas | Detectar encabezado y mapear nombres estándar | 4 encabezados | 0 encabezados cargados como ventas |
| 2 | Títulos y notas en 2025–2026 | Ignorar filas anteriores al encabezado | 6 filas | 0 filas en Silver |
| 3 | Filas TOTAL | Excluir sumas globales del conjunto de ventas | 4 | 0 |
| 4 | Fechas con formatos heterogéneos | Convertir fechas reconocidas a `AAAA-MM` | 0 errores de conversión | 0 |
| 5 | Fechas de 2026 interpretadas día/mes/año | Leer `01/MM/AAAA` como el día 1 del mes MM | 834 periodos | 834 periodos parseables; marzo = `2026-03` |
| 6 | Formatos de fecha mixtos en 2024 | Reconocer `AAAA-MM`, `mes-aa` y `MM/AAAA` | 1.112 filas de datos | 1.112 periodos interpretables |
| 7 | Unidad MWh en 2024 | Multiplicar energía MWh por 1.000 y expresar en kWh | 347 filas MWh | 0 unidades MWh pendientes en ventas Silver |
| 8 | Energía vacía o no numérica | Enviar a cuarentena, no inventar medida | 27 filas | 0 en Silver; 27 en cuarentena |
| 9 | Energía negativa | Enviar a cuarentena | 18 filas | 0 en Silver; 18 en cuarentena |
| 10 | Valores de facturación vacíos | Conservar nulo; no inferir precio | 29 celdas | 28 celdas nulas en Silver |
| 11 | Municipios escritos de varias formas | Normalizar alias y asignar DIVIPOLA | 31 variantes observadas | 15 nombres oficiales |
| 12 | Variantes de segmento | Estandarizar a Residencial, Comercial e Industrial; vacíos como No informado | 6 formas válidas | 3 categorías válidas (+ No informado cuando aplica) |
| 13 | Variantes de modalidad de compra | Estandarizar a Bolsa o Contrato | 4 formas | 2 categorías |
| 14 | Filas duplicadas equivalentes | Conservar una sola venta por clave de negocio | 118 repeticiones excedentes | 0 |
| 15 | Clientes vacíos, negativos o no enteros | Requerir conteo entero no negativo; cuarentena si falla | 0 filas detectadas | 0 |
| 16 | Claves de venta duplicadas con medidas diferentes | Cuarentena para revisión, no escoger una medida | 0 conflictos | 0 |
| 17 | Linaje de origen | Conservar hoja de Excel y marca de extracción en bronce | 0 campos faltantes | 0 |

## Consolidado de errores y cuarentena

| Fuente | Motivo | Registros |
|---|---|---:|
| EnerAndes | Energía vacía o no numérica | 27 |
| EnerAndes | Energía negativa | 18 |
| XM | Código `PRG1` duplicado con nombres discordantes | 2 |
| EPM | Medidas tarifarias, año y mes vacíos/no interpretables | 1 |
| IDEAM | Sin registros enviados a cuarentena | 0 |
| NOAA | Sin registros enviados a cuarentena | 0 |
| **Total** |  | **48** |

### Registros EnerAndes en cuarentena

`fila_excel` es el número de fila anotado por el limpiador para ubicar el registro
en la hoja bronce. Los datos originales completos se mantienen en
`data/silver/enerandes_cuarentena.parquet`.

| Año | Fila | Periodo | Municipio | Energía kWh | Motivo |
|---:|---:|---|---|---:|---|
| 2023 | 24 | 2023-08 | Bello | — | Energía vacía o no numérica |
| 2023 | 130 | 2023-06 | Turbo | -594733 | Energía negativa |
| 2023 | 200 | 2023-01 | Turbo | -387623 | Energía negativa |
| 2023 | 326 | 2023-03 | Apartadó | — | Energía vacía o no numérica |
| 2023 | 361 | 2023-02 | Turbo | — | Energía vacía o no numérica |
| 2023 | 370 | 2023-03 | Caucasia | — | Energía vacía o no numérica |
| 2023 | 425 | 2023-09 | Bello | -1865901 | Energía negativa |
| 2023 | 445 | 2023-04 | Caucasia | -487400 | Energía negativa |
| 2023 | 515 | 2023-09 | Marinilla | — | Energía vacía o no numérica |
| 2023 | 754 | 2023-10 | Sabaneta | — | Energía vacía o no numérica |
| 2023 | 1032 | 2023-09 | Sabaneta | -825187 | Energía negativa |
| 2023 | 1040 | 2023-08 | Santa Fe de Antioquia | — | Energía vacía o no numérica |
| 2023 | 1042 | 2023-10 | Girardota | — | Energía vacía o no numérica |
| 2023 | 1052 | 2023-01 | Caucasia | -423148 | Energía negativa |
| 2023 | 1056 | 2023-02 | Sabaneta | -171773 | Energía negativa |
| 2023 | 1074 | 2023-12 | Apartadó | — | Energía vacía o no numérica |
| 2024 | 20 | 2024-05 | Santa Fe de Antioquia | -59769 | Energía negativa |
| 2024 | 132 | 2024-01 | Caucasia | — | Energía vacía o no numérica |
| 2024 | 184 | 2024-03 | La Estrella | — | Energía vacía o no numérica |
| 2024 | 440 | 2024-06 | Girardota | -226225 | Energía negativa |
| 2024 | 591 | 2024-04 | La Estrella | -512379 | Energía negativa |
| 2024 | 638 | 2024-02 | Caucasia | — | Energía vacía o no numérica |
| 2024 | 737 | 2024-07 | Bello | — | Energía vacía o no numérica |
| 2024 | 757 | 2024-07 | Bello | — | Energía vacía o no numérica |
| 2024 | 767 | 2024-09 | Medellín | — | Energía vacía o no numérica |
| 2024 | 980 | 2024-12 | Itagüí | — | Energía vacía o no numérica |
| 2025 | 134 | 2025-04 | Santa Fe de Antioquia | — | Energía vacía o no numérica |
| 2025 | 168 | 2025-01 | Rionegro | — | Energía vacía o no numérica |
| 2025 | 401 | 2025-10 | Caldas | -306401 | Energía negativa |
| 2025 | 416 | 2025-10 | Rionegro | — | Energía vacía o no numérica |
| 2025 | 455 | 2025-02 | Sabaneta | -233892 | Energía negativa |
| 2025 | 488 | 2025-03 | Copacabana | — | Energía vacía o no numérica |
| 2025 | 561 | 2025-03 | Copacabana | — | Energía vacía o no numérica |
| 2025 | 795 | 2025-01 | Marinilla | -426032 | Energía negativa |
| 2025 | 1033 | 2025-08 | Santa Fe de Antioquia | -29502 | Energía negativa |
| 2025 | 1077 | 2025-12 | Copacabana | — | Energía vacía o no numérica |
| 2026 | 6 | 2026-05 | Bello | — | Energía vacía o no numérica |
| 2026 | 323 | 2026-09 | Caldas | — | Energía vacía o no numérica |
| 2026 | 400 | 2026-09 | Copacabana | — | Energía vacía o no numérica |
| 2026 | 595 | 2026-05 | Turbo | -449452 | Energía negativa |
| 2026 | 610 | 2026-01 | Bello | — | Energía vacía o no numérica |
| 2026 | 630 | 2026-02 | Envigado | -935622 | Energía negativa |
| 2026 | 727 | 2026-01 | Envigado | -1237867 | Energía negativa |
| 2026 | 801 | 2026-03 | Marinilla | — | Energía vacía o no numérica |
| 2026 | 820 | 2026-02 | Caldas | -76806 | Energía negativa |

### Otros registros en cuarentena

| Fuente / archivo | Identificador | Registro(s) | Motivo y campos conservados |
|---|---|---|---|
| XM / `xm_listado_recursos_cuarentena.parquet` | Code `PRG1` | `PROELECTRICA`; `PROELECTRICA 1` | El mismo código tiene nombres distintos; se conservan ambas filas y su linaje, sin elegir una por inferencia. |
| EPM / `epm_tarifas_historicas_cuarentena.parquet` | `Monomia`, `Costo Unitario`, `Costo compra: Gm, i`, nivel `I` | 1 fila | Faltan los cinco valores tarifarios, el año y el mes; se conserva el registro original y el motivo. |

## Diferencias entre los Parquet guardados y los limpiadores actuales

Las cifras de Silver en el resumen describen los archivos que están guardados
en este checkout; no implican que todos hayan sido regenerados tras integrar
los esquemas Pandera. La ejecución de los limpiadores sobre los bronces locales
confirmó estas diferencias:

- **XM generación:** `pasar_a_horario` excluye las 2.473.215 observaciones
  vacías y devuelve 5.935.449 filas, pero el Parquet guardado contiene
  8.408.664 filas y conserva esas celdas como nulos. Por tanto, el archivo
  guardado aún no representa la salida del limpiador actual.
- **XM catálogo:** el Parquet guardado tiene 2.508 recursos y hay dos registros
  `PRG1` en su archivo de cuarentena. El limpiador actual elimina duplicados
  exactos, pero lanza un `ValueError` ante códigos con atributos discordantes;
  no genera esa cuarentena.
- **IDEAM:** el limpiador actual devuelve latitud y longitud como `float64`;
  esos dos campos están serializados como texto en los Parquet guardados. Sus
  valores son convertibles y están dentro de rango, pero conviene regenerar
  las salidas para que el tipo persistido coincida con el esquema.
- **NOAA:** valores, meses, fechas y fases guardados coinciden con los
  comprobados; los nombres de columnas del archivo actual (`oni`, `fase`) y su
  estructura son distintos de la salida del limpiador actual
  (`anomalia_oni`, `fase_enso`, `temporada` y `temperatura_oceanica_total`).
- **EPM:** cantidad de Silver y cuarentena coincide con el limpiador actual;
  el archivo guardado contiene campos derivados adicionales, por lo que su
  estructura tampoco es idéntica a la salida actual.

Estas diferencias deben resolverse regenerando los Parquet con los limpiadores
actuales antes de afirmar que todas las salidas persistidas están sincronizadas.

## Comprobación del mínimo de reglas

El test `test_reporte_calidad_tiene_minimo_de_reglas_por_fuente` cuenta las filas
numeradas de cada tabla de reglas en este documento y exige al menos 15 para
XM, IDEAM, NOAA, EPM y EnerAndes. Conteo documentado: **XM 16; IDEAM 16; NOAA
16; EPM 16; EnerAndes 17 (81 en total)**.
