# Modelo dimensional – Observatorio de Energía

## 1. Objetivo

La capa Gold organiza la información energética en un modelo dimensional para facilitar consultas analíticas sobre ventas, mercado eléctrico y generación.

## 2. Arquitectura

El modelo utiliza un esquema dimensional tipo estrella, compuesto por tres tablas de hechos y seis dimensiones.

### Tablas de hechos

| Tabla | Grano | Medidas principales |
|---|---|---|
| fact_ventas_mensual | Mes, municipio, segmento y tipo de compra | energia_kwh, valor_cop, clientes |
| fact_mercado_horario | Fecha y hora | precio_bolsa, demanda_mwh |
| fact_generacion_recurso | Fecha, hora y recurso | generacion |

### Dimensiones

| Dimensión | Grano | Llave principal |
|---|---|---|
| dim_mes | Un mes | mes_id |
| dim_municipio | Un municipio | municipio_id |
| dim_segmento | Un segmento | segmento_id |
| dim_fecha | Un día | fecha_id |
| dim_recurso | Un recurso de generación | codigo_recurso |
| dim_fuente_energia | Una fuente energética | fuente_energia |

## 3. Diagrama del modelo

```mermaid
erDiagram
    DIM_MES ||--o{ FACT_VENTAS_MENSUAL : mes_id
    DIM_MUNICIPIO ||--o{ FACT_VENTAS_MENSUAL : municipio_id
    DIM_SEGMENTO ||--o{ FACT_VENTAS_MENSUAL : segmento_id
    DIM_RECURSO ||--o{ FACT_GENERACION_RECURSO : codigo_recurso
    DIM_FECHA ||--o{ FACT_MERCADO_HORARIO : fecha
    DIM_FECHA ||--o{ FACT_GENERACION_RECURSO : fecha
    DIM_FUENTE_ENERGIA ||--o{ DIM_RECURSO : fuente_energia
```

Nota: las relaciones de fecha y fuente energética representan relaciones lógicas propuestas. Los modelos actuales no implementan todas estas llaves foráneas explícitamente.

## 4. Descripción de las tablas de hechos

### fact_ventas_mensual

Registra las ventas de energía agrupadas por periodo mensual, municipio, segmento y tipo de compra. Permite analizar energía comercializada, valor económico y cantidad de clientes.

### fact_mercado_horario

Integra el precio de bolsa y la demanda real del sistema eléctrico mediante fecha y hora. Su información procede de XM.

### fact_generacion_recurso

Registra la generación eléctrica por recurso, fecha y hora. Se relaciona con el catálogo de recursos de XM mediante codigo_recurso.

## 5. Dimensiones descriptivas

- dim_mes: permite analizar las ventas por año, mes y trimestre.
- dim_municipio: identifica los municipios mediante código DIVIPOLA.
- dim_segmento: clasifica los segmentos de clientes.
- dim_fecha: contiene atributos temporales y la fase ENSO.
- dim_recurso: contiene el catálogo descriptivo de recursos de generación.
- dim_fuente_energia: identifica las fuentes energéticas registradas en XM.

## 6. Fuentes de información

- EnerAndes: ventas mensuales de energía.
- XM: precio de bolsa, demanda, generación y catálogo de recursos.
- NOAA: anomalía ONI y fase ENSO.

## 7. Validación

La ejecución de dbt build construyó nueve modelos y ejecutó 29 pruebas de calidad. Resultado registrado: 39 ejecuciones aprobadas, cero errores y cero advertencias.

## 8. Estado de implementación de las relaciones

| Relación | Tipo | Estado |
|---|---|---|
| fact_ventas_mensual.mes_id → dim_mes.mes_id | Clave foránea | Implementada y probada |
| fact_ventas_mensual.municipio_id → dim_municipio.municipio_id | Clave foránea | Implementada y probada |
| fact_ventas_mensual.segmento_id → dim_segmento.segmento_id | Clave foránea | Implementada y probada |
| fact_generacion_recurso.codigo_recurso → dim_recurso.codigo_recurso | Clave foránea | Implementada y probada |
| fact_mercado_horario.fecha → dim_fecha.fecha | Relación lógica | Pendiente de implementar |
| fact_generacion_recurso.fecha → dim_fecha.fecha | Relación lógica | Pendiente de implementar |
| dim_recurso.fuente_energia → dim_fuente_energia.fuente_energia | Relación lógica | Pendiente de implementar |

Las relaciones lógicas permiten identificar las asociaciones dimensionales previstas, pero no deben interpretarse como restricciones de integridad referencial implementadas en dbt.
