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
python -m src.consultar         # consultas SQL de BI con DuckDB
python -m pytest                # ejecuta las pruebas automáticas
```

El pipeline ejecuta los extractores de XM, IDEAM, NOAA, EnerAndes y las tarifas históricas de EPM. Los archivos existentes se omiten cuando corresponde, salvo que se solicite una nueva extracción con --forzar.
El Excel de EnerAndes requerido por el pipeline está incluido en `data/insumos/ventas_enerandes_2023_2026.xlsx`. Se necesita conexión a internet para descargar las fuentes externas.

Para volver a descargar todo: `python -m src.pipeline --forzar`. El rango de fechas se cambia en `src/config.py`.
La precipitación y la temperatura del IDEAM se consultan desde el 1 de enero de 2025. Ambas se filtran por Antioquia y se agregan por estación y día directamente en SoQL; la temperatura incluye promedio, mínimo y máximo diarios.
Para generar o actualizar únicamente estos dos archivos: `python -m src.extract.ideam --forzar`.

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

## 🤖 Uso de IA

Se utilizó ChatGPT como herramienta de apoyo para analizar mensajes de error Y organizar tareas técnicas Las modificaciones se verificaron mediante comandos y ejecuciones en el entorno local.
