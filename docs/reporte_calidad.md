# Reporte de calidad: ventas de EnerAndes (2023-2026)

- Filas en bronce: 4,184
- Filas en plata: 4,007
- Filas en cuarentena: 45

| Hoja | Problema | Regla aplicada | Antes | Después |
|---:|---|---|---:|---:|
| 2023 | Títulos y notas antes del encabezado | Ignorarlos como filas de datos | 0 | 0 |
| 2023 | Fila de encabezado | Utilizarla para identificar las columnas; no cargarla como dato | 1 | 0 |
| 2023 | Filas de totales | Excluirlas del conjunto de ventas | 1 | 0 |
| 2023 | Filas completamente vacías | Excluirlas del conjunto de ventas | 0 | 0 |
| 2023 | Segmentos vacíos | Asignar 'No informado' | 15 | 0 |
| 2023 | Valores facturados vacíos | Conservar vacío; no inferir el dato | 7 | 7 |
| 2023 | Ventas duplicadas | Conservar una sola copia | 32 | 0 |
| 2023 | Claves duplicadas con valores distintos | Enviar la colisión a cuarentena | 0 | 0 |
| 2024 | Títulos y notas antes del encabezado | Ignorarlos como filas de datos | 0 | 0 |
| 2024 | Fila de encabezado | Utilizarla para identificar las columnas; no cargarla como dato | 1 | 0 |
| 2024 | Filas de totales | Excluirlas del conjunto de ventas | 1 | 0 |
| 2024 | Filas completamente vacías | Excluirlas del conjunto de ventas | 0 | 0 |
| 2024 | Segmentos vacíos | Asignar 'No informado' | 3 | 0 |
| 2024 | Valores facturados vacíos | Conservar vacío; no inferir el dato | 11 | 11 |
| 2024 | Ventas duplicadas | Conservar una sola copia | 31 | 0 |
| 2024 | Claves duplicadas con valores distintos | Enviar la colisión a cuarentena | 0 | 0 |
| 2025 | Títulos y notas antes del encabezado | Ignorarlos como filas de datos | 3 | 0 |
| 2025 | Fila de encabezado | Utilizarla para identificar las columnas; no cargarla como dato | 1 | 0 |
| 2025 | Filas de totales | Excluirlas del conjunto de ventas | 1 | 0 |
| 2025 | Filas completamente vacías | Excluirlas del conjunto de ventas | 0 | 0 |
| 2025 | Segmentos vacíos | Asignar 'No informado' | 6 | 0 |
| 2025 | Valores facturados vacíos | Conservar vacío; no inferir el dato | 4 | 4 |
| 2025 | Ventas duplicadas | Conservar una sola copia | 31 | 0 |
| 2025 | Claves duplicadas con valores distintos | Enviar la colisión a cuarentena | 0 | 0 |
| 2026 | Títulos y notas antes del encabezado | Ignorarlos como filas de datos | 3 | 0 |
| 2026 | Fila de encabezado | Utilizarla para identificar las columnas; no cargarla como dato | 1 | 0 |
| 2026 | Filas de totales | Excluirlas del conjunto de ventas | 1 | 0 |
| 2026 | Filas completamente vacías | Excluirlas del conjunto de ventas | 0 | 0 |
| 2026 | Segmentos vacíos | Asignar 'No informado' | 5 | 0 |
| 2026 | Valores facturados vacíos | Conservar vacío; no inferir el dato | 7 | 7 |
| 2026 | Ventas duplicadas | Conservar una sola copia | 24 | 0 |
| 2026 | Claves duplicadas con valores distintos | Enviar la colisión a cuarentena | 0 | 0 |

# Calidad de datos: fuentes XM

| Fuente | Problema o regla | Antes | Después |
|---|---|---:|---:|
| Precio de bolsa | Transformar 24 columnas horarias a registros | 1.004 | 24.096 |
| Demanda | Transformar 24 columnas horarias a registros | 1.004 | 24.096 |
| Generación | Transformar 24 columnas horarias a registros | 350.345 | 5.935.362 |
| Generación | Observaciones horarias vacías excluidas, sin convertirlas en cero | 2.472.918 | 0 |
| Embalses | Validar fechas y valores numéricos | 1.004 | 1.004 |
| Aportes de energía | Validar fechas y valores numéricos | 1.004 | 1.004 |
| Catálogo de recursos | Eliminar duplicados exactos | 2.494 | 2.492 |

Las fuentes horarias se transformaron a formato largo, conservando fecha, identificador, código, hora y valor. Los valores horarios vacíos de generación no se imputaron. Los valores no numéricos y las fechas inválidas generan errores de validación. En el catálogo se eliminaron dos duplicados exactos.

# Calidad de datos: fuentes IDEAM

| Fuente | Regla aplicada | Antes | Después |
|---|---|---:|---:|
| Precipitación | Conversión de coordenadas, precipitación y observaciones a valores numéricos | 2.784 | 2.784 |
| Precipitación | Duplicados por estación y fecha | 0 | 0 |
| Precipitación | Valores negativos | 0 | 0 |
| Temperatura | Conversión de coordenadas y temperaturas a valores numéricos | 17.349 | 17.349 |
| Temperatura | Duplicados por estación y fecha | 0 | 0 |
| Temperatura | Temperatura mínima superior a máxima | 0 | 0 |
| Temperatura | Temperatura media fuera del intervalo mínimo-máximo | 0 | 0 |

Las dos fuentes conservaron sus registros y columnas de linaje. Las temperaturas extremas observadas y la precipitación máxima se conservaron, sin descartarlas por criterios arbitrarios. La cobertura temporal de precipitación va de junio a julio de 2026 y la de temperatura de enero de 2025 a julio de 2026.

# Calidad de datos: NOAA ONI

| Regla aplicada | Antes | Después |
|---|---:|---:|
| Registros originales | 920 | 920 |
| Valores inválidos en año, anomalía y temperatura total | 0 | 0 |
| Temporadas no reconocidas | 0 | 0 |
| Duplicados por año y temporada | 0 | 0 |
| Clasificación Neutral | — | 448 |
| Clasificación La Niña | — | 238 |
| Clasificación El Niño | — | 234 |

Se convirtió cada trimestre móvil a su mes central. La fase ENSO se asignó usando la anomalía ONI: El Niño cuando ANOM >= 0,5; La Niña cuando ANOM <= -0,5; Neutral en los demás casos. Se conservaron los 920 registros y el linaje de origen.

# Calidad de datos: tarifas históricas EPM

| Problema o regla | Antes | Después |
|---|---:|---:|
| Registros Bronze | 3.623 | — |
| Duplicados exactos | 10 | 0 |
| Registro con campos tarifarios, año y mes incompletos | 1 | 0 en Silver |
| Registros conservados en Silver | — | 3.612 |
| Registros en cuarentena | — | 1 |

Se convirtieron los campos tarifarios y temporales a tipos numéricos. Los diez duplicados exactos fueron eliminados y el registro incompleto se envió a cuarentena. Los valores negativos asociados al concepto «Restricciones: Rm» se conservaron, porque corresponden a componentes tarifarios presentes en la fuente y no se cuenta con evidencia para clasificarlos como errores.

El archivo de cuarentena conserva el registro original y su motivo de exclusión.
