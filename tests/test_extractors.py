from datetime import date

from src import config
from src.extract.xm import aplanar, extraer_metrica
from src.utils import ventanas


def test_ventanas_divide_range_without_gaps_or_overlaps():
    resultado = list(ventanas(date(2024, 1, 1), date(2024, 1, 7), dias=3))

    assert resultado == [
        (date(2024, 1, 1), date(2024, 1, 3)),
        (date(2024, 1, 4), date(2024, 1, 6)),
        (date(2024, 1, 7), date(2024, 1, 7)),
    ]


def test_aplanar_hourly_expands_values_into_rows():
    respuesta = {
        "Items": [
            {
                "Date": "2024-01-01",
                "HourlyEntities": [
                    {"Id": "Sistema", "Values": {"Hour01": "10", "Hour02": "20"}},
                    {"Id": "Nacional", "Values": {"Hour01": "30", "Hour02": "40"}},
                ],
            }
        ]
    }

    assert aplanar(respuesta, "hourly") == [
        {"Date": "2024-01-01", "Id": "Sistema", "Hour01": "10", "Hour02": "20"},
        {"Date": "2024-01-01", "Id": "Nacional", "Hour01": "30", "Hour02": "40"},
    ]


def test_aplanar_daily_maps_value():
    respuesta = {
        "Items": [
            {
                "Date": "2024-01-01",
                "DailyEntities": [{"Id": "Sistema", "Value": "75.5"}],
            }
        ]
    }

    assert aplanar(respuesta, "daily") == [
        {"Date": "2024-01-01", "Id": "Sistema", "Value": "75.5"}
    ]


def test_extraer_metrica_skips_existing_output(tmp_path, monkeypatch):
    nombre = "xm_test_existente"
    monkeypatch.setattr(config, "DIR_BRONZE", tmp_path)
    (tmp_path / f"{nombre}.parquet").touch()

    def no_debe_hacer_peticion(*args, **kwargs):
        raise AssertionError("No debe consultar la API si el archivo ya existe")

    monkeypatch.setattr("src.extract.xm.http_json", no_debe_hacer_peticion)

    extraer_metrica("MetricId", "Sistema", "daily", nombre, forzar=False)
