
"""Limpieza del índice ONI de NOAA para la capa Silver."""

import pandas as pd

LINAJE = ["_fuente", "_origen", "_extraido_en"]

MESES_CENTRALES = {
    "DJF": 1, "JFM": 2, "FMA": 3, "MAM": 4,
    "AMJ": 5, "MJJ": 6, "JJA": 7, "JAS": 8,
    "ASO": 9, "SON": 10, "OND": 11, "NDJ": 12,
}


def limpiar_oni(bronce: pd.DataFrame) -> pd.DataFrame:
    """Convierte ONI a observaciones mensuales y clasifica la fase ENSO."""
    requeridas = ["SEAS", "YR", "TOTAL", "ANOM"] + LINAJE
    faltantes = set(requeridas) - set(bronce.columns)

    if faltantes:
        raise ValueError(f"Faltan columnas NOAA: {sorted(faltantes)}")

    resultado = bronce.copy()
    resultado["SEAS"] = resultado["SEAS"].astype("string").str.strip()

    if not resultado["SEAS"].isin(MESES_CENTRALES).all():
        raise ValueError("NOAA contiene temporadas no reconocidas.")

    for columna in ["YR", "TOTAL", "ANOM"]:
        resultado[columna] = pd.to_numeric(
            resultado[columna], errors="coerce"
        )
        if resultado[columna].isna().any():
            raise ValueError(f"NOAA contiene valores inválidos en {columna}.")

    if not resultado["YR"].between(1950, 2100).all():
        raise ValueError("NOAA contiene años fuera del rango esperado.")

    if resultado.duplicated(["YR", "SEAS"]).any():
        raise ValueError("NOAA contiene temporadas duplicadas por año.")

    resultado["YR"] = resultado["YR"].astype("int16")
    resultado["mes"] = resultado["SEAS"].map(MESES_CENTRALES).astype("int8")
    resultado["fecha"] = pd.to_datetime({
        "year": resultado["YR"],
        "month": resultado["mes"],
        "day": 1,
    })

    resultado["fase_enso"] = "Neutral"
    resultado.loc[resultado["ANOM"] >= 0.5, "fase_enso"] = "El Niño"
    resultado.loc[resultado["ANOM"] <= -0.5, "fase_enso"] = "La Niña"

    resultado = resultado.rename(columns={
        "YR": "anio",
        "SEAS": "temporada",
        "TOTAL": "temperatura_oceanica_total",
        "ANOM": "anomalia_oni",
    })

    return resultado[
        [
            "fecha", "anio", "mes", "temporada",
            "temperatura_oceanica_total", "anomalia_oni",
            "fase_enso", *LINAJE,
        ]
    ].reset_index(drop=True)
