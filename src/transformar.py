"""Ejecuta la limpieza de las fuentes Bronze y guarda sus tablas Silver.

Uso:
    python -m src.transformar
    python -m src.transformar --sin-dbt
"""

import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import pandas as pd

from src import config
from src.quality.esquemas import ESQUEMA_VENTAS
from src.silver import enerandes, epm, ideam, noaa, xm
from src.utils import log

ARCHIVOS_BRONCE = [
    "enerandes_ventas_2023",
    "enerandes_ventas_2024",
    "enerandes_ventas_2025",
    "enerandes_ventas_2026",
    "xm_precio_bolsa",
    "xm_demanda",
    "xm_generacion",
    "xm_embalses",
    "xm_aportes_energia",
    "xm_listado_recursos",
    "ideam_precipitacion_diaria",
    "ideam_temperatura_diaria",
    "noaa_oni",
    "epm_tarifas_historicas",
]


def _leer_bronce(nombre: str) -> pd.DataFrame:
    """Lee un Parquet Bronze y falla con una instrucción clara si no existe."""
    ruta = config.DIR_BRONZE / f"{nombre}.parquet"
    if not ruta.is_file():
        raise FileNotFoundError(
            f"No se encontró {ruta}. Ejecute primero python -m src.pipeline."
        )
    return pd.read_parquet(ruta)


def _separar_conflictos_catalogo(
    bronce: pd.DataFrame,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Retira códigos con atributos distintos y conserva esas filas en cuarentena."""
    sin_repetidos = bronce.drop_duplicates().copy()
    conflictos_mask = sin_repetidos.duplicated("Code", keep=False)
    conflictos = sin_repetidos.loc[conflictos_mask].copy()
    catalogo = sin_repetidos.loc[~conflictos_mask].copy()

    if conflictos.empty:
        conflictos["motivo"] = pd.Series(dtype="string")
        conflictos["registro_original"] = pd.Series(dtype="string")
        return catalogo, conflictos

    conflictos["motivo"] = "Código repetido con atributos distintos"
    conflictos["registro_original"] = conflictos.apply(
        lambda fila: json.dumps(fila.to_dict(), ensure_ascii=False, default=str),
        axis=1,
    )
    return catalogo, conflictos.reset_index(drop=True)


def _a_plata_horaria(bronce: pd.DataFrame) -> pd.DataFrame:
    """Limpia una serie horaria y usa `fecha` como nombre común en Silver."""
    resultado = xm.pasar_a_horario(bronce)
    return resultado.rename(columns={"Date": "fecha"})


def _a_plata_diaria(bronce: pd.DataFrame) -> pd.DataFrame:
    """Limpia una serie diaria XM y normaliza los nombres de fecha e indicador."""
    resultado = xm.limpiar_diaria(bronce)
    return resultado.rename(
        columns={"Date": "fecha", "Id": "id", "Value": "valor"}
    )


def _guardar_temporal(df: pd.DataFrame, carpeta: Path, nombre: str) -> int:
    """Escribe una tabla en el área temporal de la ejecución."""
    ruta = carpeta / f"{nombre}.parquet"
    df.to_parquet(ruta, index=False)
    filas = len(df)
    del df
    return filas


def _ejecutar_dbt() -> None:
    """Construye Gold y ejecuta sus pruebas de calidad."""
    nombre_ejecutable = "dbt.exe" if sys.platform == "win32" else "dbt"
    dbt = Path(sys.executable).parent / nombre_ejecutable
    if not dbt.is_file():
        encontrado = shutil.which("dbt")
        if encontrado is None:
            raise FileNotFoundError(
                "No se encontró el comando dbt. Instale las dependencias del "
                "proyecto o ejecute python -m src.transformar --sin-dbt."
            )
        dbt = Path(encontrado)

    subprocess.run(
        [
            str(dbt),
            "build",
            "--project-dir",
            str(config.RAIZ / "dbt"),
            "--profiles-dir",
            str(config.RAIZ / "dbt"),
        ],
        cwd=config.RAIZ,
        check=True,
    )


def transformar(ejecutar_dbt: bool = True) -> dict[str, int]:
    """Limpia todas las fuentes Bronze, guarda Silver y opcionalmente construye Gold."""
    faltantes = [
        config.DIR_BRONZE / f"{nombre}.parquet"
        for nombre in ARCHIVOS_BRONCE
        if not (config.DIR_BRONZE / f"{nombre}.parquet").is_file()
    ]
    if faltantes:
        rutas = "\n".join(f"- {ruta}" for ruta in faltantes)
        raise FileNotFoundError(
            "Faltan archivos Bronze requeridos. Ejecute primero "
            f"python -m src.pipeline:\n{rutas}"
        )

    config.DIR_SILVER.mkdir(parents=True, exist_ok=True)
    conteos: dict[str, int] = {}

    with tempfile.TemporaryDirectory(
        prefix="transformar_", dir=config.DIR_SILVER
    ) as temporal:
        carpeta_temporal = Path(temporal)

        ventas: list[pd.DataFrame] = []
        cuarentenas_enerandes: list[pd.DataFrame] = []
        for anio in range(2023, 2027):
            bronce = _leer_bronce(f"enerandes_ventas_{anio}")
            limpias, cuarentena, _ = enerandes.limpiar(
                bronce, anio_fuente=anio
            )
            ventas.append(limpias)
            cuarentenas_enerandes.append(cuarentena)

        ventas_plata = pd.concat(ventas, ignore_index=True)
        ESQUEMA_VENTAS.validate(ventas_plata, lazy=True)
        cuarentena_enerandes_plata = pd.concat(
            cuarentenas_enerandes, ignore_index=True
        )
        conteos["enerandes_ventas"] = _guardar_temporal(
            ventas_plata, carpeta_temporal, "enerandes_ventas"
        )
        conteos["enerandes_cuarentena"] = _guardar_temporal(
            cuarentena_enerandes_plata,
            carpeta_temporal,
            "enerandes_cuarentena",
        )

        for nombre in ("xm_precio_bolsa", "xm_demanda", "xm_generacion"):
            resultado = _a_plata_horaria(_leer_bronce(nombre))
            conteos[nombre] = _guardar_temporal(
                resultado, carpeta_temporal, nombre
            )

        for nombre in ("xm_embalses", "xm_aportes_energia"):
            resultado = _a_plata_diaria(_leer_bronce(nombre))
            conteos[nombre] = _guardar_temporal(
                resultado, carpeta_temporal, nombre
            )

        catalogo_bronce = _leer_bronce("xm_listado_recursos")
        catalogo_sin_conflictos, cuarentena_catalogo = (
            _separar_conflictos_catalogo(catalogo_bronce)
        )
        catalogo_plata = xm.limpiar_catalogo(catalogo_sin_conflictos)
        conteos["xm_listado_recursos"] = _guardar_temporal(
            catalogo_plata, carpeta_temporal, "xm_listado_recursos"
        )
        conteos["xm_listado_recursos_cuarentena"] = _guardar_temporal(
            cuarentena_catalogo,
            carpeta_temporal,
            "xm_listado_recursos_cuarentena",
        )

        for nombre, limpiar in (
            ("ideam_precipitacion_diaria", ideam.limpiar_precipitacion),
            ("ideam_temperatura_diaria", ideam.limpiar_temperatura),
        ):
            resultado = limpiar(_leer_bronce(nombre))
            conteos[nombre] = _guardar_temporal(
                resultado, carpeta_temporal, nombre
            )

        oni = noaa.limpiar_oni(_leer_bronce("noaa_oni"))
        conteos["noaa_oni"] = _guardar_temporal(
            oni, carpeta_temporal, "noaa_oni"
        )

        tarifas, cuarentena_epm = epm.limpiar_epm(
            _leer_bronce("epm_tarifas_historicas")
        )
        conteos["epm_tarifas_historicas"] = _guardar_temporal(
            tarifas, carpeta_temporal, "epm_tarifas_historicas"
        )
        conteos["epm_tarifas_historicas_cuarentena"] = _guardar_temporal(
            cuarentena_epm,
            carpeta_temporal,
            "epm_tarifas_historicas_cuarentena",
        )

        for temporal_parquet in carpeta_temporal.glob("*.parquet"):
            destino = config.DIR_SILVER / temporal_parquet.name
            temporal_parquet.replace(destino)

    log("Archivos Silver guardados:")
    for nombre, filas in conteos.items():
        log(f"   {nombre}.parquet: {filas:,} filas")

    if ejecutar_dbt:
        log("Construyendo modelos Gold y ejecutando pruebas de dbt")
        _ejecutar_dbt()

    return conteos


def main() -> None:
    ejecutar_dbt = "--sin-dbt" not in sys.argv
    log("Iniciando transformación de Bronze a Silver")
    conteos = transformar(ejecutar_dbt=ejecutar_dbt)
    log(f"Transformación completa: {len(conteos)} archivos Silver")


if __name__ == "__main__":
    main()
