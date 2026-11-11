# Bitácora individual de trabajo

## 1. Información general
- **Proyecto**: Observatorio Energía y Clima.
- **Actividad**: Desarrollo y validación de la capa plata para EnerAndes y las demás fuentes.
- **Integrante**: Oscar Márquez Arrieta.
- **Rol principal**: Data Quality Analyst / BI Analyst.
- **Periodo registrado**: 10 de noviembre de 2026.
- **Evidencia**: comandos ejecutados en el entorno local y archivos generados en `data/silver/`.

## 2. Objetivo

Completar la limpieza de las ventas de EnerAndes para los años 2023 a 2026 y preparar las demás fuentes del proyecto en la capa plata. El trabajo incluyó revisar los datos de bronce, definir reglas de transformación, conservar los registros que requieren revisión y comprobar los resultados con pruebas y consultas de validación.

## 3. Actividades desarrolladas

### 3.1. Limpieza y consolidación de EnerAndes
Se amplió la limpieza para detectar los encabezados de las cuatro hojas del Excel, descartar títulos, notas y totales, normalizar fechas y municipios, unificar categorías y convertir los valores de energía de MWh a kWh.

Los registros con energía vacía o negativa y otros datos no corregibles se conservaron en cuarentena con su motivo, número de fila y contenido original. Los duplicados equivalentes se consolidaron; los valores de facturación vacíos se conservaron sin inferir un valor.

**Resultados verificados:**
- 4.184 filas de bronce procesadas.
- 4.007 ventas en `data/silver/enerandes_ventas.parquet`.
- 45 filas en `data/silver/enerandes_cuarentena.parquet`.
- La tabla limpia pasó la validación de Pandera.
- Se actualizaron `docs/reporte_calidad.md` y las instrucciones de ejecución en `README.md`.
- Las 17 pruebas de pytest pasaron; `dbt build` completó 18 de 18 modelos y pruebas.

### 3.2. Conversión de las series horarias de XM
Se preparó `src/silver/xm.py` con la función `pasar_a_horario`, que transforma las columnas `Hour01` a `Hour24` en registros por hora, convierte los valores a formato numérico y conserva como nulos las celdas vacías.

Se generaron las siguientes tablas:
- `xm_precio_bolsa.parquet`: 24.096 filas.
- `xm_demanda.parquet`: 24.096 filas.
- `xm_generacion.parquet`: 8.408.664 filas; se conservaron 2.473.215 valores faltantes como nulos, no como ceros.

La generación se procesó por bloques. En Windows, el archivo temporal quedó bloqueado al intentar renombrarlo mientras DuckDB lo leía; se validó el temporal, se cerró la conexión y luego se movió al nombre definitivo.

### 3.3. Limpieza de otras tablas de XM
Se normalizaron las fechas y valores de embalses y aportes, conservando las columnas de linaje:
- `xm_embalses.parquet`: 1.004 filas.
- `xm_aportes_energia.parquet`: 1.004 filas.

En ambos archivos los valores se mantuvieron en la unidad original de XM.

Para el catálogo de recursos se eliminaron duplicados exactos. Las dos filas con código `PRG1` y nombres distintos se separaron para revisión:
- `xm_listado_recursos.parquet`: 2.508 recursos con códigos únicos.
- `xm_listado_recursos_cuarentena.parquet`: 2 filas.

### 3.4. Limpieza de IDEAM
Se tiparon las fechas y las medidas numéricas, manteniendo el código y nombre de estación, el municipio y el linaje:
- `ideam_precipitacion_diaria.parquet`: 29.804 filas.
- `ideam_temperatura_diaria.parquet`: 17.349 filas.

La revisión previa no encontró fechas inválidas, mediciones vacías o no numéricas, valores negativos ni duplicados por estación y fecha.

### 3.5. Limpieza de NOAA
Se transformó el ONI de temporadas trimestrales móviles a una fila mensual, asignando cada temporada a su mes central en el año indicado por NOAA (por ejemplo, `DJF` a enero). Se utilizó `ANOM` como valor del ONI y se asignó la fase con los umbrales solicitados: El Niño para valores mayores o iguales a 0,5; La Niña para valores menores o iguales a -0,5; Neutral en los demás casos.

Resultado: `noaa_oni.parquet`, con 921 filas mensuales desde enero de 1950 hasta septiembre de 2026. Se verificó que las fechas fueran únicas y que las fases correspondieran a los umbrales.

### 3.6. Limpieza de la fuente propia EPM
Se normalizaron los años, meses y valores tarifarios. Se consolidaron 10 duplicados exactos y se conservaron los valores negativos asociados a `Restricciones: Rm`, sin asumir que fueran errores. La fila sin dimensiones, periodo y valores tarifarios interpretables se envió a cuarentena.

- `epm_tarifas_historicas.parquet`: 3.612 filas.
- `epm_tarifas_historicas_cuarentena.parquet`: 1 fila.

## 4. Decisiones técnicas y aprendizajes
- Los espacios en generación se trataron como datos faltantes, no como ceros, porque el origen no permite afirmar que representen generación igual a cero.
- Los trimestres del ONI se asignaron al mes central y se usó `ANOM`, no `TOTAL`, para representar la anomalía del índice.
- En el catálogo XM y en EPM se conservaron para revisión las filas conflictivas o incompletas en lugar de escoger valores por inferencia.
- Se mantuvieron los valores negativos de EPM en `Restricciones: Rm`, ya que forman parte de los datos publicados de ese componente.
- El procesamiento por bloques permitió generar el Parquet horario de generación sin cargar la expansión completa en memoria.

## 5. Verificaciones realizadas

Se verificaron los conteos de filas de los diez archivos principales de plata, el rango de horas de las tablas horarias, la unicidad de códigos en el catálogo, las fases del ONI y los conteos de las dos cuarentenas verificadas. Los resultados coincidieron con los conteos esperados.

También se ejecutaron las pruebas automatizadas de EnerAndes y la construcción de dbt durante la actividad de limpieza de esa fuente. Las transformaciones de las demás fuentes se ejecutaron mediante comandos manuales en PowerShell y se verificaron sobre los Parquet resultantes.

## 6. Alcance y trabajo pendiente

Los Parquet de plata quedaron generados y verificados en el entorno local. Sin embargo, salvo la función de conversión horaria en `src/silver/xm.py` y el proceso de EnerAndes, las transformaciones de las demás fuentes se ejecutaron manualmente; aún no están integradas en un único comando reproducible del pipeline.

Como siguiente mejora, se puede organizar cada limpieza de fuente en módulos de `src/silver/`, agregar pruebas específicas y documentar o automatizar la generación de las tablas de plata. Los archivos de bronce se conservaron sin modificar.

## 7. Conclusión

El trabajo dejó preparadas y validadas las principales fuentes de la capa plata: ventas de EnerAndes, series horarias y diarias de XM, catálogo de recursos, observaciones de IDEAM, ONI mensual de NOAA y tarifas históricas de EPM. Se conservaron explícitamente los valores faltantes y se separaron los registros conflictivos identificados para revisión, evitando corregir datos por suposición.
