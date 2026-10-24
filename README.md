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
| IDEAM – datos.gov.co | API Socrata (SoQL) | `ideam_precipitacion_diaria` |
| NOAA – índice ONI | Archivo de texto | `noaa_oni` |
| EnerAndes | Excel interno | `enerandes_ventas_2023`, `enerandes_ventas_2024`, `enerandes_ventas_2025` … `enerandes_ventas_2026` |

## ⚙️ Cómo ejecutar

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
# copiar ventas_enerandes_2023_2026.xlsx en data/insumos/
python -m src.pipeline          # descarga las 4 fuentes a data/bronze/ (unos 3 minutos)
python -m src.pipeline --forzar # Para solicitar una nueva extracción
python -m src.consultar         # consultas SQL de BI con DuckDB
```

El pipeline ejecuta los extractores de XM, IDEAM, NOAA y EnerAndes. Los archivos existentes se omiten cuando corresponde, salvo que se solicite una nueva extracción con --forzar.

Para volver a descargar todo: `python -m src.pipeline --forzar`. El rango de fechas se cambia en `src/config.py`.

## 🏗️ Arquitectura

```
Fuentes -> BRONCE (dato tal cual + linaje) -> PLATA (limpio) -> ORO (modelo estrella) -> Dashboard
```
## Estructura

```
observatorio-energia/
├── data/
│   ├── insumos/
│   └── bronze/
├── src/
│   ├── config.py
│   ├── pipeline.py
│   ├── utils.py
│   └── extract/
│       ├── xm.py
│       ├── ideam.py
│       ├── noaa.py
│       └── enerandes.py
├── consultas/
├── requirements.txt
└── README.md
```

## 🤖 Uso de IA

Se utilizó ChatGPT como herramienta de apoyo para analizar mensajes de error Y organizar tareas técnicas Las modificaciones se verificaron mediante comandos y ejecuciones en el entorno local.
