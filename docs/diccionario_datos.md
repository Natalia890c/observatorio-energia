# Diccionario de datos – Capa Gold

Este documento describe las columnas de los modelos dimensionales y de hechos implementados en dbt.

## 1. fact_ventas_mensual

| Columna | Tipo | Descripción | Origen |
|---|---|---|---|
| mes_id | INTEGER | Identificador del mes AAAAMM | EnerAndes |
| municipio_id | VARCHAR | Código DIVIPOLA | EnerAndes |
| segmento_id | INTEGER | Identificador del segmento | dim_segmento |
| tipo_compra | VARCHAR | Modalidad de compra: Bolsa o Contrato | EnerAndes |
| energia_kwh | DOUBLE | Energía comercializada en kWh | EnerAndes |
| valor_cop | DOUBLE | Valor económico en pesos colombianos | EnerAndes |
| clientes | BIGINT | Cantidad de clientes | EnerAndes |

## 2. fact_mercado_horario

| Columna | Tipo | Descripción | Origen |
|---|---|---|---|
| fecha | DATE | Fecha de observación | XM |
| hora | TINYINT | Hora de observación | XM |
| precio_bolsa | DOUBLE | Precio de bolsa de energía | XM |
| demanda_mwh | DOUBLE | Demanda real del sistema | XM |

## 3. fact_generacion_recurso

| Columna | Tipo | Descripción | Origen |
|---|---|---|---|
| fecha | DATE | Fecha de generación | XM |
| hora | TINYINT | Hora de generación | XM |
| codigo_recurso | VARCHAR | Código identificador del recurso | XM |
| nombre_recurso | VARCHAR | Nombre del recurso | Catálogo XM |
| tipo_recurso | VARCHAR | Clasificación del recurso | Catálogo XM |
| fuente_energia | VARCHAR | Fuente energética | Catálogo XM |
| generacion | DOUBLE | Valor de generación registrado | XM |

## 4. dim_mes

| Columna | Tipo | Descripción | Origen |
|---|---|---|---|
| mes_id | INTEGER | Llave del mes en formato AAAAMM | EnerAndes |
| periodo | VARCHAR | Periodo AAAA-MM | EnerAndes |
| anio | INTEGER | Año del periodo | Derivado |
| mes | INTEGER | Número del mes | Derivado |
| trimestre | INTEGER | Trimestre calendario | Derivado |

## 5. dim_municipio

| Columna | Tipo | Descripción | Origen |
|---|---|---|---|
| municipio_id | VARCHAR | Código DIVIPOLA del municipio | EnerAndes |
| municipio | VARCHAR | Nombre del municipio | EnerAndes |

## 6. dim_segmento

| Columna | Tipo | Descripción | Origen |
|---|---|---|---|
| segmento_id | BIGINT | Identificador numérico del segmento | Derivado |
| segmento | VARCHAR | Nombre del segmento de clientes | EnerAndes |

## 7. dim_fecha

| Columna | Tipo | Descripción | Origen |
|---|---|---|---|
| fecha_id | INTEGER | Llave de fecha AAAAMMDD | EnerAndes, XM y NOAA |
| fecha | DATE | Fecha calendario | EnerAndes, XM y NOAA |
| anio | INTEGER | Año | Derivado |
| mes | INTEGER | Mes numérico | Derivado |
| nombre_mes | VARCHAR | Nombre del mes | Derivado |
| trimestre | INTEGER | Trimestre calendario | Derivado |
| dia | INTEGER | Día del mes | Derivado |
| dia_semana | INTEGER | Día de la semana | Derivado |
| fase_enso | VARCHAR | Clasificación ENSO | NOAA |
| anomalia_oni | DOUBLE | Anomalía del índice ONI | NOAA |

## 8. dim_recurso

| Columna | Tipo | Descripción | Origen |
|---|---|---|---|
| codigo_recurso | VARCHAR | Identificador del recurso | XM |
| nombre_recurso | VARCHAR | Nombre del recurso | XM |
| tipo_recurso | VARCHAR | Tipo de recurso | XM |
| tipo_despacho | VARCHAR | Modalidad de despacho | XM |
| tipo_recurso_operativo | VARCHAR | Clasificación operativa | XM |
| codigo_empresa | VARCHAR | Código de empresa | XM |
| fuente_energia | VARCHAR | Fuente de energía | XM |
| estado | VARCHAR | Estado operativo | XM |

## 9. dim_fuente_energia

| Columna | Tipo | Descripción | Origen |
|---|---|---|---|
| fuente_energia | VARCHAR | Nombre de la fuente energética | Catálogo XM |

## 10. Consideraciones

Los tipos de datos se expresan según los valores y transformaciones de los modelos SQL. Las columnas derivadas se calculan durante la construcción de la capa Gold. Los campos descriptivos de recursos pueden ser nulos cuando un código histórico no aparece en el catálogo actual.
