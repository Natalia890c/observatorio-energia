# Reporte de calidad de las fuentes en capa plata

Este reporte consolida los controles de calidad aplicados a las cinco fuentes.
Las columnas Antes y Después describen los registros o valores que incumplen
cada control, excepto cuando la regla especifica explícitamente una conversión
o conservación. Los registros no corregibles se mantienen en cuarentena cuando
corresponde.

## Fuente: XM

XM reúne las series horarias, las series diarias y el catálogo de recursos.
Las celdas vacías de generación se excluyen sin imputarlas como cero.

| # | Problema / control | Regla aplicada | Antes | Después |
|---:|---|---|---:|---:|
| 1 | Precio en formato horario ancho | Desplegar las 24 horas por fecha | 1.004 filas | 24.096 filas |
| 2 | Demanda en formato horario ancho | Desplegar las 24 horas por fecha | 1.004 filas | 24.096 filas |
| 3 | Generación en formato horario ancho | Desplegar horas con valor por recurso y fecha | 350.361 filas | 5.935.449 filas |
| 4 | Columnas horarias faltantes | Requerir Hour01–Hour24 | 0 faltantes | 0 |
| 5 | Fechas horarias inválidas | Convertir fecha y rechazar las inválidas | 0 | 0 |
| 6 | Precios horarios no numéricos | Convertir valores presentes a número | 0 | 0 |
| 7 | Demanda horaria no numérica | Convertir valores presentes a número | 0 | 0 |
| 8 | Generación horaria no numérica | Convertir valores presentes a número | 0 | 0 |
| 9 | Horas vacías de generación | Excluirlas sin convertirlas a cero | 2.473.215 | 2.473.215 excluidas |
| 10 | Valores horarios negativos | Rechazar valores negativos | 0 | 0 |
| 11 | Hora fuera del rango 1–24 | Asignar la hora desde la columna de origen | 0 | 0 |
| 12 | Duplicados en series diarias | Mantener única la clave fecha e identificador | 0 | 0 |
| 13 | Fechas o valores diarios inválidos | Convertir fecha y valor numérico | 0 | 0 |
| 14 | Valores diarios negativos | Validar valores no negativos | 0 | 0 |
| 15 | Duplicados exactos del catálogo | Conservar una sola copia | 2 excedentes | 0 |
| 16 | Código PRG1 con nombres discordantes | Enviar ambas filas a cuarentena | 2 filas | 0 en Silver; 2 en cuarentena |

## Fuente: IDEAM

IDEAM agrupa las observaciones diarias de precipitación y temperatura. Se
validan los campos comunes de estación, coordenadas, fecha y número de
observaciones, además de las reglas específicas para cada variable.

| # | Problema / control | Regla aplicada | Antes | Después |
|---:|---|---|---:|---:|
| 1 | Observaciones de precipitación | Conservar registros válidos | 29.804 filas | 29.804 filas |
| 2 | Observaciones de temperatura | Conservar registros válidos | 17.349 filas | 17.349 filas |
| 3 | Fechas de precipitación inválidas | Convertir a fecha | 0 | 0 |
| 4 | Fechas de temperatura inválidas | Convertir a fecha | 0 | 0 |
| 5 | Códigos de estación vacíos | Requerir código de estación | 0 | 0 |
| 6 | Nombres de estación vacíos | Requerir nombre de estación | 0 | 0 |
| 7 | Municipios vacíos | Requerir municipio asociado a la estación | 0 | 0 |
| 8 | Latitudes no numéricas | Convertir a número | 0 | 0 |
| 9 | Latitudes fuera de −90 a 90 | Validar rango geográfico | 0 | 0 |
| 10 | Longitudes no numéricas | Convertir a número | 0 | 0 |
| 11 | Longitudes fuera de −180 a 180 | Validar rango geográfico | 0 | 0 |
| 12 | Precipitación no numérica o negativa | Convertir a número y exigir valor ≥ 0 | 0 | 0 |
| 13 | Temperaturas no numéricas | Convertir media, mínima y máxima a número | 0 | 0 |
| 14 | Temperaturas fuera de −10 °C a 60 °C | Validar el rango definido para el proyecto | 0 | 0 |
| 15 | Temperatura mínima mayor que máxima | Exigir mínima ≤ máxima | 0 | 0 |
| 16 | Media fuera de rango, n_obs inválido o clave repetida | Validar coherencia, conteo entero positivo y clave estación-fecha única | 0 | 0 |

No se enviaron registros IDEAM a cuarentena.

## Fuente: NOAA (ONI)

El índice ONI se transforma desde temporadas trimestrales móviles a
observaciones mensuales usando el mes central. La fase ENSO se deriva de ANOM.

| # | Problema / control | Regla aplicada | Antes | Después |
|---:|---|---|---:|---:|
| 1 | Registros ONI | Conservar observaciones válidas | 921 filas | 921 filas |
| 2 | Etiquetas SEAS desconocidas | Aceptar solo las 12 temporadas reconocidas | 0 | 0 |
| 3 | Años no numéricos | Convertir YR a entero | 0 | 0 |
| 4 | Años fuera del intervalo esperado | Validar 1950–2100 | 0 | 0 |
| 5 | Valores TOTAL no numéricos | Convertir a número | 0 | 0 |
| 6 | Valores ANOM no numéricos | Convertir a número | 0 | 0 |
| 7 | Claves año-temporada duplicadas | Exigir unicidad de YR + SEAS | 0 | 0 |
| 8 | Temporadas sin mes central asignable | Mapear cada temporada a su mes central | 0 | 0 |
| 9 | Fechas mensuales inválidas | Construir fecha al primer día del mes | 0 | 0 |
| 10 | Meses fuera de 1–12 | Validar mes calendario | 0 | 0 |
| 11 | Fechas mensuales duplicadas | Exigir una observación por mes | 0 | 0 |
| 12 | Fases fuera del catálogo | Permitir El Niño, La Niña o Neutral | 0 | 0 |
| 13 | Fases El Niño mal clasificadas | Aplicar ANOM ≥ 0,5 | 0 | 0 |
| 14 | Fases La Niña mal clasificadas | Aplicar ANOM ≤ −0,5 | 0 | 0 |
| 15 | Fases neutrales mal clasificadas | Aplicar −0,5 < ANOM < 0,5 | 0 | 0 |
| 16 | Campos de fecha, índice o linaje vacíos | Requerir valores completos en Silver | 0 | 0 |

Distribución Silver comprobada: 448 observaciones neutrales, 238 de La Niña y
235 de El Niño. No hay filas en cuarentena.

## Fuente: EPM (tarifas históricas)

Se normalizan los nombres de mes, años y valores tarifarios. Los valores
negativos de Restricciones se conservan porque forman parte de los datos
publicados y no hay evidencia para tratarlos como errores.

| # | Problema / control | Regla aplicada | Antes | Después |
|---:|---|---|---:|---:|
| 1 | Filas de tarifas | Conservar registros interpretables | 3.623 | 3.612 Silver + 1 cuarentena |
| 2 | Filas duplicadas exactas | Conservar una copia | 10 excedentes | 0 |
| 3 | Año vacío o no numérico | Convertir a entero y poner fila inválida en cuarentena | 1 | 0 Silver; 1 cuarentena |
| 4 | Año fuera de 1900–2100 | Validar rango | 0 | 0 |
| 5 | Mes no reconocido | Mapear nombres españoles a meses 1–12 | 1 | 0 Silver; 1 cuarentena |
| 6 | propiedadepm vacío o no interpretable | Convertir a número; cuarentena si falta | 1 | 0 Silver |
| 7 | compartido vacío o no interpretable | Convertir a número; cuarentena si falta | 1 | 0 Silver |
| 8 | propiedaddelcliente vacío o no interpretable | Convertir a número; cuarentena si falta | 1 | 0 Silver |
| 9 | punta vacía o no interpretable | Convertir a número; cuarentena si falta | 1 | 0 Silver |
| 10 | fueradepunta vacía o no interpretable | Convertir a número; cuarentena si falta | 1 | 0 Silver |
| 11 | Medidas no numéricas no vacías | Rechazar conversión inválida | 0 | 0 |
| 12 | Categorías vacías | Requerir información, tarifa, dato, rango y nivel | 0 | 0 |
| 13 | Valores tarifarios negativos | Conservar; no imputar ni forzar a cero | 15 celdas | 15 celdas conservadas |
| 14 | Linaje incompleto | Conservar fuente, URL y fecha de extracción | 0 | 0 |
| 15 | Registro incompleto no utilizable | Separar con motivo en cuarentena | 1 fila | 1 fila documentada |
| 16 | Mes fuera de 1–12 después del mapeo | Validar rango de mes | 0 | 0 |

## Fuente: EnerAndes

El limpiador normaliza cuatro hojas de ventas (2023–2026). Los valores de
facturación vacíos se conservan sin inferencia; las ventas no corregibles se
envían a cuarentena.

| # | Problema / control | Regla aplicada | Antes | Después |
|---:|---|---|---:|---:|
| 1 | Encabezados no uniformes | Detectar encabezado y mapear nombres estándar | 4 hojas | 0 encabezados cargados como ventas |
| 2 | Títulos y notas antes del encabezado | Ignorarlos como filas de datos | 6 filas | 0 en Silver |
| 3 | Filas TOTAL | Excluir sumas del conjunto de ventas | 4 filas | 0 |
| 4 | Fechas con formatos heterogéneos | Convertir formatos reconocidos a AAAA-MM | 0 errores | 0 |
| 5 | Fechas de 2026 en formato día/mes/año | Interpretar 01/MM/AAAA como el día 1 del mes MM | 834 periodos | 834 parseables |
| 6 | Formatos de fecha mixtos en 2024 | Reconocer AAAA-MM, mes-aa y MM/AAAA | 1.112 filas | 1.112 interpretables |
| 7 | Unidad MWh | Convertir energía de MWh a kWh multiplicando por 1.000 | 347 filas | 0 MWh pendientes |
| 8 | Energía vacía o no numérica | Enviar a cuarentena, no inventar medida | 27 filas | 0 Silver; 27 cuarentena |
| 9 | Energía negativa | Enviar a cuarentena | 18 filas | 0 Silver; 18 cuarentena |
| 10 | Valores de facturación vacíos | Conservar nulo; no inferir precio | 29 celdas | 28 celdas nulas en Silver |
| 11 | Variantes de nombres de municipios | Normalizar alias y asignar DIVIPOLA | 31 variantes | 15 nombres oficiales |
| 12 | Variantes de segmento | Estandarizar categorías y asignar No informado a vacíos | 6 formas válidas | 3 categorías válidas + No informado |
| 13 | Variantes de modalidad de compra | Estandarizar a Bolsa o Contrato | 4 formas | 2 categorías |
| 14 | Ventas duplicadas equivalentes | Conservar una venta por clave de negocio | 118 excedentes | 0 |
| 15 | Clientes vacíos, negativos o no enteros | Requerir conteo entero no negativo | 0 filas detectadas | 0 |
| 16 | Claves repetidas con medidas diferentes | Enviar colisiones a cuarentena | 0 conflictos | 0 |
| 17 | Linaje de origen | Conservar hoja de Excel y marca de extracción en bronce | 0 campos faltantes | 0 |

El conjunto contiene 4.184 filas en bronce, 4.007 en Silver y 45 en
cuarentena. El detalle por año se mantiene en
`docs/reporte_calidad_enerandes.md`, generado por el limpiador de esta fuente.
