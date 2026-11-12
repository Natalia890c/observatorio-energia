# Bitácora individual de trabajo

## 1. Información general
- **Proyecto**: Observatorio Energía y Clima.
- **Actividad**: Desarrollo y validación de la capa plata para EnerAndes y las demás fuentes.
- **Integrante**: Oscar Márquez Arrieta.
- **Rol principal**: Data Quality Analyst / BI Analyst.
- **Periodo registrado**: 10 y 11 de noviembre de 2026.
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
- En la primera etapa, las 17 pruebas de pytest pasaron; `dbt build` completó 18 de 18 modelos y pruebas.

### 3.2. Conversión de las series horarias de XM
Se preparó `src/silver/xm.py` con la función `pasar_a_horario`, que transforma las columnas `Hour01` a `Hour24` en registros por hora y convierte los valores a formato numérico. El limpiador actual excluye las celdas vacías, sin convertirlas en cero.

En los Parquet generados anteriormente quedaron estas cantidades:
- `xm_precio_bolsa.parquet`: 24.096 filas.
- `xm_demanda.parquet`: 24.096 filas.
- `xm_generacion.parquet`: 8.408.664 filas; se conservaron 2.473.215 valores faltantes como nulos, no como ceros.

La generación se procesó por bloques. En Windows, el archivo temporal quedó bloqueado al intentar renombrarlo mientras DuckDB lo leía; se validó el temporal, se cerró la conexión y luego se movió al nombre definitivo. El proceso automático actual produce 5.935.449 filas porque deja por fuera las 2.473.215 horas vacías.

### 3.3. Limpieza de otras tablas de XM
Se normalizaron las fechas y valores de embalses y aportes, conservando las columnas de linaje:
- `xm_embalses.parquet`: 1.004 filas.
- `xm_aportes_energia.parquet`: 1.004 filas.

En ambos archivos los valores se mantuvieron en la unidad original de XM.

En el catálogo guardado se eliminaron duplicados exactos. Las dos filas con código `PRG1` y nombres distintos se separaron manualmente para revisión:
- `xm_listado_recursos.parquet`: 2.508 recursos con códigos únicos.
- `xm_listado_recursos_cuarentena.parquet`: 2 filas.

El proceso automático separa esos códigos en conflicto antes de limpiar el catálogo y guarda las dos filas en cuarentena.

### 3.4. Limpieza de IDEAM
Se tiparon las fechas y las medidas numéricas, manteniendo el código y nombre de estación, el municipio y el linaje:
- `ideam_precipitacion_diaria.parquet`: 29.804 filas.
- `ideam_temperatura_diaria.parquet`: 17.349 filas.

La revisión previa no encontró fechas inválidas, mediciones vacías o no numéricas, valores negativos ni duplicados por estación y fecha. El proceso automático convierte latitud y longitud a números antes de guardar Plata.

### 3.5. Limpieza de NOAA
Se transformó el ONI de temporadas trimestrales móviles a una fila mensual, asignando cada temporada a su mes central en el año indicado por NOAA (por ejemplo, `DJF` a enero). Se utilizó `ANOM` como valor del ONI y se asignó la fase con los umbrales solicitados: El Niño para valores mayores o iguales a 0,5; La Niña para valores menores o iguales a -0,5; Neutral en los demás casos.

Resultado: `noaa_oni.parquet`, con 921 filas mensuales desde enero de 1950 hasta septiembre de 2026. Se verificó que las fechas fueran únicas y que las fases correspondieran a los umbrales. El proceso automático guarda el ONI con nombres de columnas estandarizados para los modelos Gold.

### 3.6. Limpieza de la fuente propia EPM
Se normalizaron los años, meses y valores tarifarios. Se consolidaron 10 duplicados exactos y se conservaron los valores negativos asociados a `Restricciones: Rm`, sin asumir que fueran errores. La fila sin dimensiones, periodo y valores tarifarios interpretables se envió a cuarentena.

- `epm_tarifas_historicas.parquet`: 3.612 filas.
- `epm_tarifas_historicas_cuarentena.parquet`: 1 fila.

### 3.7. Reglas de calidad y pruebas para las fuentes
Se agregaron esquemas de Pandera para las tablas de XM, IDEAM, NOAA y EPM en
`src/quality/esquemas.py`. Los limpiadores revisan, por ejemplo, que las fechas
y los números se puedan leer, que no falten campos obligatorios, que las horas
estén entre 1 y 24 y que las temperaturas sean coherentes. Las ventas de
EnerAndes también se validan antes de guardarse.

Se amplió `docs/reporte_calidad.md` para explicar, con palabras sencillas, los
problemas encontrados, las reglas aplicadas, los conteos antes y después y las
filas enviadas a cuarentena. El reporte contiene 16 reglas para XM, IDEAM,
NOAA y EPM, y 17 para EnerAndes. Se añadió una prueba automática que comprueba
que cada fuente tenga por lo menos 15 reglas.

**Comprobación:** al finalizar estos cambios, `python -m pytest -v` ejecutó 26
pruebas y todas pasaron.

Al inicio se encontraron diferencias entre los Parquet guardados y los
limpiadores actuales. Se resolvieron al crear y ejecutar `src/transformar.py`,
que regeneró todas las tablas de Plata; el estado final está descrito en el
reporte de calidad.

### 3.8. Relaciones entre hechos y dimensiones
Se completaron en dbt las relaciones que faltaban: la fecha de mercado y la
fecha de generación deben existir en la dimensión de fechas; y la fuente de
energía de cada recurso debe existir en su dimensión. También se conectó el
hecho de generación con la dimensión de recursos. Los recursos sin fuente
conocida se etiquetan como "No informado" para no perder sus registros.

Al probar el modelo, se vio que algunas horas de generación estaban vacías.
El hecho de Gold ahora deja esas filas fuera; así no se cuentan como generación
cero. `dbt build --project-dir dbt --profiles-dir dbt` terminó correctamente:
pasaron las 43 ejecuciones (10 modelos y 33 pruebas), incluidas las tres
relaciones añadidas.

Después se completó la revisión de las llaves. Se añadieron pruebas para
comprobar que la fecha del calendario no se repita y que las claves compuestas
de ventas, mercado horario y generación sean únicas. Las dimensiones también
comprueban sus llaves con `unique` y `not_null`, y las relaciones con `relationships`.
La nueva ejecución de `dbt build --project-dir dbt --profiles-dir dbt` pasó las
47 ejecuciones: 10 modelos y 37 pruebas, sin errores ni advertencias.

### 3.9. Proceso automático de transformación
Se creó `src/transformar.py` para leer las 14 tablas Bronze requeridas, limpiar
EnerAndes, XM, IDEAM, NOAA y EPM, y guardar las salidas Silver. Los registros
conflictivos o incompletos de EnerAndes, el catálogo XM y EPM se guardan en sus
archivos de cuarentena. Al terminar, el proceso ejecuta dbt para construir Gold
y revisar las pruebas. Se puede usar `--sin-dbt` para actualizar solo Plata.

**Resultados de la ejecución local:** 14 archivos Silver escritos; generación
XM: 5.935.449 filas; catálogo XM: 2.508 filas y 2 en cuarentena; EnerAndes:
4.007 filas y 45 en cuarentena; EPM: 3.612 filas y 1 en cuarentena. `dbt build`
pasó 47 de 47 ejecuciones. La prueba completa del proyecto pasó 27 de 27.

## 4. Decisiones técnicas y aprendizajes
- Los espacios en generación se trataron como datos faltantes, no como ceros, porque el origen no permite afirmar que representen generación igual a cero.
- Los trimestres del ONI se asignaron al mes central y se usó `ANOM`, no `TOTAL`, para representar la anomalía del índice.
- En el catálogo XM y en EPM se conservaron para revisión las filas conflictivas o incompletas en lugar de escoger valores por inferencia.
- Se mantuvieron los valores negativos de EPM en `Restricciones: Rm`, ya que forman parte de los datos publicados de ese componente.
- El procesamiento por bloques permitió generar el Parquet horario de generación sin cargar la expansión completa en memoria.

## 5. Verificaciones realizadas

Se verificaron los conteos de filas de los archivos principales de plata, el rango de horas de las tablas horarias, la unicidad de códigos del catálogo guardado, las fases del ONI y los conteos de las cuarentenas disponibles.

También se ejecutaron las pruebas automatizadas de las limpiezas, esquemas,
documentación y proceso de transformación. La ejecución final de
`python -m pytest -v` pasó **27 de 27 pruebas**. La construcción más reciente
de dbt completó 10 modelos y 37 pruebas (47 ejecuciones aprobadas).

## 6. Alcance y trabajo pendiente

El proceso `python -m src.transformar` automatiza la generación de Plata y la
construcción de Gold. Como mejora futura se puede integrar también la
extracción; por ahora, primero se debe ejecutar `python -m src.pipeline` para
crear o actualizar Bronze. Los archivos de bronce se conservaron sin modificar.

## 7. Conclusión

El trabajo dejó un proceso que lee Bronze, limpia las cinco fuentes, guarda las
tablas Silver y sus cuarentenas y construye Gold con dbt. Se conservaron para
revisión los casos que no se pueden corregir con seguridad y se añadieron
pruebas automáticas para verificar las reglas y relaciones del modelo.
