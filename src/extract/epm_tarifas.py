"""Fuente adicional - tarifas históricas de energía eléctrica de EPM."""
import pandas as pd

from src import config
from src.utils import guardar_bronce, http_json, log, ya_existe

NOMBRE = "epm_tarifas_historicas"
PAGINA = 50000


def extraer(forzar: bool = False) -> None:
    """Descarga las filas publicadas por EPM y las guarda sin transformarlas."""
    log("EPM - tarifas históricas de energía (datos.gov.co)")
    if ya_existe(NOMBRE, forzar):
        return

    filas = []
    offset = 0
    while True:
        pagina = http_json(
            "GET",
            config.EPM_TARIFAS_URL,
            params={
                "$limit": PAGINA,
                "$offset": offset,
                "$order": (
                    "year, mes, tipodetarifa, nivel, rangodeconsumo, tipodedato, "
                    "propiedadepm, compartido, propiedaddelcliente, punta, fueradepunta"
                ),
            },
        )
        filas.extend(pagina)
        log(f"   filas recibidas: {len(filas)}")
        if len(pagina) < PAGINA:
            break
        offset += PAGINA

    if not filas:
        raise ValueError("datos.gov.co devolvió vacío el dataset histórico de tarifas de EPM.")

    guardar_bronce(
        pd.DataFrame(filas),
        NOMBRE,
        fuente="EPM/datos.gov.co",
        origen=config.EPM_TARIFAS_URL,
    )


if __name__ == "__main__":
    import sys

    extraer(forzar="--forzar" in sys.argv)
