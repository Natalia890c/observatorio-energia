import re
from pathlib import Path


def test_reporte_calidad_tiene_minimo_de_reglas_por_fuente():
    reporte = Path(__file__).resolve().parents[1] / "docs" / "reporte_calidad.md"
    contenido = reporte.read_text(encoding="utf-8")
    secciones = re.split(r"(?m)^## Fuente: ", contenido)[1:]
    reglas_por_fuente = {}

    for seccion in secciones:
        lineas = seccion.splitlines()
        fuente = lineas[0].strip()
        reglas_por_fuente[fuente] = sum(
            re.match(r"^\|\s*\d+\s*\|", linea) is not None
            for linea in lineas
        )

    assert set(reglas_por_fuente) == {"XM", "IDEAM", "NOAA (ONI)", "EPM (tarifas históricas)", "EnerAndes"}
    assert all(cantidad >= 15 for cantidad in reglas_por_fuente.values()), reglas_por_fuente
