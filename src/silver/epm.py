
"""Limpieza de tarifas históricas EPM para la capa Silver."""

import pandas as pd

from src.quality.esquemas import ESQUEMA_EPM_TARIFAS

LINAJE = ["_fuente", "_origen", "_extraido_en"]

MESES = {
    "enero": 1, "febrero": 2, "marzo": 3, "abril": 4,
    "mayo": 5, "junio": 6, "julio": 7, "agosto": 8,
    "septiembre": 9, "octubre": 10, "noviembre": 11,
    "diciembre": 12,
}

NUMERICAS = [
    "propiedadepm", "compartido", "propiedaddelcliente",
    "punta", "fueradepunta",
]


def limpiar_epm(bronce: pd.DataFrame):
    """Retorna datos Silver y registros incompletos en cuarentena."""
    resultado = bronce.copy()

    requeridas = [
        "tipodeinformacion", "tipodetarifa", "tipodedato",
        "rangodeconsumo", "nivel", *NUMERICAS, "year", "mes", *LINAJE
    ]

    faltantes = set(requeridas) - set(resultado.columns)
    if faltantes:
        raise ValueError(f"Faltan columnas EPM: {sorted(faltantes)}")

    antes = len(resultado)
    resultado = resultado.drop_duplicates().copy()
    duplicados = antes - len(resultado)

    for columna in [
        "tipodeinformacion", "tipodetarifa", "tipodedato",
        "rangodeconsumo", "nivel"
    ]:
        resultado[columna] = resultado[columna].astype("string").str.strip()

    resultado["year"] = pd.to_numeric(resultado["year"], errors="coerce")
    resultado["mes_nombre"] = resultado["mes"].astype("string").str.strip()
    resultado["mes_numero"] = (
        resultado["mes_nombre"].str.lower().map(MESES)
    )

    for columna in NUMERICAS:
        resultado[columna] = pd.to_numeric(
            resultado[columna], errors="coerce"
        )

    incompletos = (
        resultado[NUMERICAS + ["year", "mes_numero"]].isna().any(axis=1)
    )

    cuarentena = resultado.loc[incompletos].copy()
    cuarentena["motivo_cuarentena"] = (
        "Valores tarifarios, año o mes incompletos o inválidos"
    )

    limpias = resultado.loc[~incompletos].copy()

    if not limpias["year"].between(1900, 2100).all():
        raise ValueError("EPM contiene años fuera del rango esperado.")

    limpias["year"] = limpias["year"].astype("int16")
    limpias["mes_numero"] = limpias["mes_numero"].astype("int8")
    limpias["mes_nombre"] = limpias["mes_nombre"].str.capitalize()
    limpias[NUMERICAS] = limpias[NUMERICAS].astype("float64")

    limpias = limpias.drop(columns=["mes"])
    limpias = limpias.rename(columns={"mes_numero": "mes"})

    limpias = limpias.reset_index(drop=True)
    cuarentena = cuarentena.reset_index(drop=True)
    limpias = ESQUEMA_EPM_TARIFAS.validate(limpias, lazy=True)

    print(f"Bronze: {antes:,}")
    print(f"Duplicados exactos eliminados: {duplicados:,}")
    print(f"Cuarentena: {len(cuarentena):,}")
    print(f"Silver: {len(limpias):,}")

    return limpias, cuarentena
