"""Limpieza de las fuentes meteorológicas IDEAM para la capa Silver."""

import pandas as pd

COLUMNAS_LINAJE = ["_fuente", "_origen", "_extraido_en"]

COLUMNAS_COMUNES = [
    "codigoestacion",
    "nombreestacion",
    "municipio",
    "latitud",
    "longitud",
    "fecha",
    "n_obs",
]


def _preparar_base(bronce: pd.DataFrame) -> pd.DataFrame:
    """Valida y normaliza los campos comunes de IDEAM."""
    resultado = bronce.copy()

    requeridas = COLUMNAS_COMUNES + COLUMNAS_LINAJE
    faltantes = set(requeridas) - set(resultado.columns)

    if faltantes:
        raise ValueError(
            f"Faltan columnas requeridas de IDEAM: {sorted(faltantes)}"
        )

    resultado["fecha"] = pd.to_datetime(
        resultado["fecha"], errors="coerce"
    )

    if resultado["fecha"].isna().any():
        raise ValueError("IDEAM contiene fechas inválidas.")

    numericas = ["latitud", "longitud", "n_obs"]

    for columna in numericas:
        resultado[columna] = pd.to_numeric(
            resultado[columna], errors="coerce"
        )

        if resultado[columna].isna().any():
            raise ValueError(
                f"IDEAM contiene valores no numéricos en {columna}."
            )

    if not resultado["latitud"].between(-90, 90).all():
        raise ValueError("IDEAM contiene latitudes fuera de rango.")

    if not resultado["longitud"].between(-180, 180).all():
        raise ValueError("IDEAM contiene longitudes fuera de rango.")

    if (resultado["n_obs"] <= 0).any():
        raise ValueError("IDEAM contiene cantidades de observaciones no positivas.")

    clave = ["codigoestacion", "fecha"]

    if resultado.duplicated(clave).any():
        raise ValueError("IDEAM contiene duplicados por estación y fecha.")

    for columna in ["codigoestacion", "nombreestacion", "municipio"]:
        resultado[columna] = resultado[columna].astype("string").str.strip()

        if resultado[columna].isna().any() or resultado[columna].eq("").any():
            raise ValueError(f"IDEAM contiene valores vacíos en {columna}.")

    return resultado


def limpiar_precipitacion(bronce: pd.DataFrame) -> pd.DataFrame:
    """Limpia y valida las observaciones diarias de precipitación."""
    requeridas = {"precipitacion_mm"}

    if not requeridas.issubset(bronce.columns):
        raise ValueError("Falta la columna precipitacion_mm en IDEAM.")

    resultado = _preparar_base(bronce)

    resultado["precipitacion_mm"] = pd.to_numeric(
        resultado["precipitacion_mm"], errors="coerce"
    )

    if resultado["precipitacion_mm"].isna().any():
        raise ValueError("IDEAM contiene precipitaciones no numéricas.")

    if (resultado["precipitacion_mm"] < 0).any():
        raise ValueError("IDEAM contiene precipitaciones negativas.")

    return resultado.reset_index(drop=True)


def limpiar_temperatura(bronce: pd.DataFrame) -> pd.DataFrame:
    """Limpia y valida las observaciones diarias de temperatura."""
    columnas = [
        "temperatura_media_c",
        "temperatura_minima_c",
        "temperatura_maxima_c",
    ]

    faltantes = set(columnas) - set(bronce.columns)

    if faltantes:
        raise ValueError(
            f"Faltan columnas de temperatura: {sorted(faltantes)}"
        )

    resultado = _preparar_base(bronce)

    for columna in columnas:
        resultado[columna] = pd.to_numeric(
            resultado[columna], errors="coerce"
        )

        if resultado[columna].isna().any():
            raise ValueError(
                f"IDEAM contiene valores no numéricos en {columna}."
            )

    if (resultado[columnas] < -10).any().any():
        raise ValueError("IDEAM contiene temperaturas inferiores a -10 °C.")

    if (resultado[columnas] > 60).any().any():
        raise ValueError("IDEAM contiene temperaturas superiores a 60 °C.")

    minimo_mayor_maximo = (
        resultado["temperatura_minima_c"]
        > resultado["temperatura_maxima_c"]
    )

    if minimo_mayor_maximo.any():
        raise ValueError("La temperatura mínima supera la máxima.")

    media_fuera_rango = (
        (resultado["temperatura_media_c"] < resultado["temperatura_minima_c"])
        | (resultado["temperatura_media_c"] > resultado["temperatura_maxima_c"])
    )

    if media_fuera_rango.any():
        raise ValueError("La temperatura media está fuera del intervalo mínimo-máximo.")

    return resultado.reset_index(drop=True)
