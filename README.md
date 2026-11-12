# Observatorio Energía y Clima – Equipo

**Natalia Castro Ospino**
**Oscar Márquez Arrieta**

> Proyecto Integrado IV – Integración de Información · IU Digital de Antioquia · 2026-2

## 👥 Integrantes

| Nombre | Usuario GitHub | Rol |
|---|---|---|
| Natalia Castro | @Natalia890c | Líder técnico / Data Engineer |
| Oscar Márquez | @OscarLMAR | Data Quality Analyst |
| Natalia Castro | @Natalia890c | Analytics Engineer |
| Oscar Márquez | @OscarLMAR | BI Analyst / Storyteller |

## 🎯 Objetivo

Integrar datos del mercado eléctrico (XM), del clima (IDEAM y NOAA) y de ventas internas (EnerAndes) para analizar el riesgo energético de Colombia ante El Niño 2026.

## 📦 Fuentes de datos (capa bronce)

| Fuente | Tipo | Archivo en `data/bronze/` |
|---|---|---|
| XM – API Sinergox | API REST (POST, JSON) | `xm_precio_bolsa`, `xm_demanda`, `xm_embalses`, `xm_generacion`, `xm_aportes_energia`, `xm_listado_recursos` |
| IDEAM – datos.gov.co | API Socrata (SoQL) | `ideam_precipitacion_diaria`, `ideam_temperatura_diaria` |
| NOAA – índice ONI | Archivo de texto | `noaa_oni` |
| EnerAndes | Excel interno | `enerandes_ventas_2023`, `enerandes_ventas_2024`, `enerandes_ventas_2025` … `enerandes_ventas_2026` |
| EPM – tarifas de energía | API Socrata de datos.gov.co | `epm_tarifas_historicas` |

## ⚙️ Cómo ejecutar

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m src.pipeline          # descarga las fuentes a data/bronze/
python -m src.pipeline --forzar # vuelve a descargar las fuentes
python -m src.silver.enerandes  # limpia y une las ventas de EnerAndes 2023-2026
python -m src.consultar         # consultas SQL de BI con DuckDB
python -m pytest                # ejecuta las pruebas automáticas
```

El pipeline ejecuta los extractores de XM, IDEAM, NOAA, EnerAndes y las tarifas históricas de EPM. Los archivos existentes se omiten cuando corresponde, salvo que se solicite una nueva extracción con --forzar.
El Excel de EnerAndes requerido por el pipeline está incluido en `data/insumos/ventas_enerandes_2023_2026.xlsx`. Se necesita conexión a internet para descargar las fuentes externas.

Para volver a descargar todo: `python -m src.pipeline --forzar`. El rango de fechas se cambia en `src/config.py`.
La precipitación y la temperatura del IDEAM se consultan desde el 1 de enero de 2025. Ambas se filtran por Antioquia y se agregan por estación y día directamente en SoQL; la temperatura incluye promedio, mínimo y máximo diarios.
Para generar o actualizar únicamente estos dos archivos: `python -m src.extract.ideam --forzar`.

### Limpieza de EnerAndes (capa plata)

Después de extraer las cuatro hojas a `data/bronze/`, ejecute `python -m src.silver.enerandes`.
El proceso detecta los encabezados aunque haya títulos o notas previas, estandariza las
fechas mensuales de 2023-2026, convierte MWh a kWh y normaliza los municipios, segmentos
y modalidades. Consolida las ventas en `data/silver/enerandes_ventas.parquet`.
Las filas con datos requeridos ausentes, valores negativos, unidades o categorías no
reconocidas, o claves duplicadas con medidas en conflicto quedan en
`data/silver/enerandes_cuarentena.parquet`, con el motivo, número de fila y contenido
original para su revisión. Los duplicados equivalentes se consolidan; un valor de
facturación vacío se conserva como nulo porque no se puede inferir. El reporte de
conteos se escribe en `docs/reporte_calidad.md`.

El perfil de calidad de los archivos Parquet locales, con conteos de filas, tipos, nulos, duplicados, rangos temporales y hallazgos, está en [`docs/perfilamiento.md`](docs/perfilamiento.md).

### Fuente propia: tarifas históricas de EPM

Se incorpora el dataset [Histórico de Tarifas de Energía Eléctrica – EPM (2016-2021)](https://www.datos.gov.co/d/sfcd-b3ey), publicado por Empresas Públicas de Medellín en datos.gov.co. Contiene tarifas del mercado regulado según año, mes, nivel, tipo de tarifa y modalidad de consumo. Se usará como referencia histórica para contextualizar los costos de energía en Antioquia frente a los precios de XM y las ventas de EnerAndes. Su cobertura publicada llega hasta 2021, por lo que no representa tarifas vigentes para el periodo de análisis de 2024-2026. El extractor guarda las filas recibidas sin limpiarlas ni transformarlas.

## 🏗️ Arquitectura

```
Fuentes -> BRONCE (dato tal cual + linaje) -> PLATA (limpio) -> ORO (modelo estrella) -> Dashboard
```
## Estructura

```
observatorio-energia/
├── data/
│   ├── insumos/
│   ├── bronze/      # datos completos generados localmente; ignorados por Git
│   └── sample/      # primeras 200 filas de cada Parquet de bronce, en CSV
├── src/
│   ├── config.py
│   ├── pipeline.py
│   ├── utils.py
│   └── extract/
│       ├── xm.py
│       ├── ideam.py
│       ├── noaa.py
│       ├── enerandes.py
│       └── epm_tarifas.py
├── consultas/
├── requirements.txt
└── README.md
```

Las muestras CSV están versionadas en `data/sample/` para inspección y uso de ejemplo. Los Parquet completos se generan localmente en `data/bronze/`, carpeta excluida de Git; para reconstruirlos desde cero basta con instalar `requirements.txt` y ejecutar `python -m src.pipeline`.

Natalia Castro Ospino: [Link al video](https://drive.google.com/file/d/1t1kE_6Q2EJQ34p0MpEHuqUvkG6-gnkyC/view?usp=drivesdk)

## Capturas de evidencia
Se incluyen capturas de la ejecución del pipeline y del resultado de las pruebas automáticas.

## 🤖 Uso de IA

Se utilizó ChatGPT como herramienta de apoyo para analizar mensajes de error Y organizar tareas técnicas Las modificaciones se verificaron mediante comandos y ejecuciones en el entorno local.

## Consultas analíticas – Capa Gold

Las consultas SQL se encuentran en `consultas/oro/` y utilizan los modelos dimensionales construidos con dbt y DuckDB.

### 1. Precio de bolsa y demanda mensual

Archivo: `consultas/oro/01_precio_demanda_mensual.sql`

Calcula el precio promedio de bolsa, la demanda promedio y la cantidad de observaciones por mes.

**Resultados observados:**

| Mes | Precio promedio | Demanda promedio | Registros |
|---|---:|---:|---:|
| Enero 2024 | 558,72 | 9.202.503,60 | 744 |
| Febrero 2024 | 568,71 | 9.307.901,93 | 696 |
| Marzo 2024 | 622,77 | 9.500.107,29 | 744 |
| Abril 2024 | 748,66 | 9.372.401,31 | 720 |
| Mayo 2024 | 291,55 | 9.243.697,64 | 744 |

En los primeros cinco meses de 2024 se observa variabilidad en el precio promedio de bolsa, mientras que la demanda promedio presenta valores relativamente cercanos.

### 2. Generación eléctrica por fuente de energía

Archivo: `consultas/oro/02_generacion_por_fuente.sql`

Agrupa la generación por fuente energética y calcula la generación acumulada y el número de registros.

**Principales resultados:**

| Fuente | Generación acumulada |
|---|---:|
| AGUA | 170.122.100.000 aprox. |
| GAS | 25.837.730.000 aprox. |
| CARBON | 18.457.590.000 aprox. |
| RAD SOLAR | 13.000.320.000 aprox. |
| BAGAZO | 2.435.259.000 aprox. |

AGUA presenta la mayor generación acumulada en los datos consultados, seguida de GAS y CARBON. Los registros sin clasificación se conservan bajo la categoría «Sin clasificar».

### 3. Ventas por municipio, segmento y tipo de compra

Archivo: `consultas/oro/03_ventas_municipio_segmento.sql`

Agrupa la energía comercializada, el valor económico y los clientes reportados por municipio, segmento y modalidad de compra.

**Principales resultados:**

| Municipio | Segmento ID | Tipo de compra | Energía (kWh) | Valor (COP) |
|---|---:|---|---:|---:|
| 05001 | 4 | Contrato | 418.620.429 | 412.895.700.000 aprox. |
| 05001 | 2 | Contrato | 318.309.694 | 295.443.000.000 aprox. |
| 05001 | 1 | Contrato | 228.546.894 | 260.690.800.000 aprox. |
| 05001 | 4 | Bolsa | 117.494.391 | 116.368.900.000 aprox. |
| 05088 | 4 | Contrato | 105.056.354 | 103.984.200.000 aprox. |

El municipio 05001 concentra los primeros cuatro resultados del listado ordenado por valor económico. Los clientes corresponden a cantidades reportadas y acumuladas, no necesariamente a personas únicas.

### Ejecución de consultas

Las consultas se ejecutan sobre la base DuckDB generada por dbt en `data/observatorio.duckdb`. Primero se construye la capa Gold:

```powershell
dbt build --project-dir dbt --profiles-dir dbt
```

Posteriormente se pueden ejecutar los archivos SQL desde DuckDB.

### Documentación del modelo

- [Modelo dimensional](docs/modelo_dimensional.md).
- [Diccionario de datos](docs/diccionario_datos.md).
- [Reporte de calidad](docs/reporte_calidad.md).
