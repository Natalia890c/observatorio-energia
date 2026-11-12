
import pandas as pd

from src.silver.xm import pasar_a_horario, limpiar_diaria
from src.silver.xm import limpiar_catalogo
from src.silver.ideam import limpiar_precipitacion, limpiar_temperatura
from src.silver.noaa import limpiar_oni
from src.silver.epm import limpiar_epm


def linaje():
    return {
        "_fuente": "PRUEBA",
        "_origen": "test",
        "_extraido_en": "2026-11-11T00:00:00+00:00",
    }


def test_xm_convierte_24_horas_a_formato_largo():
    fila = {
        "Date": "2026-01-01",
        "Id": "Sistema",
        "code": "DEMANDA",
        **{f"Hour{i:02d}": str(i) for i in range(1, 25)},
        **linaje(),
    }
    resultado = pasar_a_horario(pd.DataFrame([fila]))
    assert len(resultado) == 24
    assert resultado["hora"].tolist() == list(range(1, 25))


def test_xm_diario_convierte_valor_a_numerico():
    df = pd.DataFrame([{
        "Date": "2026-01-01",
        "Id": "Sistema",
        "Value": "12.5",
        **linaje(),
    }])
    resultado = limpiar_diaria(df)
    assert len(resultado) == 1
    assert resultado["Value"].iloc[0] == 12.5


def test_xm_catalogo_valida_campos_y_codigo_unico():
    df = pd.DataFrame([{
        "Date": "2026-11-10",
        "Id": "Sistema",
        "Code": "R001",
        "Name": "Recurso de prueba",
        "Type": "HIDRAULICA",
        "Disp": "DESPACHADO CENTRALMENTE",
        "RecType": "NORMAL",
        "CompanyCode": "EMPR",
        "EnerSource": "AGUA",
        "OperStartdate": "2020-01-01",
        "State": "OPERACION",
        **linaje(),
    }])

    resultado = limpiar_catalogo(df)

    assert len(resultado) == 1
    assert resultado.loc[0, "codigo_recurso"] == "R001"
    assert pd.api.types.is_datetime64_any_dtype(resultado["fecha_catalogo"])


def test_ideam_precipitacion_convierte_campos_numericos():
    df = pd.DataFrame([{
        "codigoestacion": "123",
        "nombreestacion": "Estación prueba",
        "municipio": "Medellín",
        "latitud": "6.25",
        "longitud": "-75.56",
        "fecha": "2026-06-01",
        "precipitacion_mm": "0",
        "n_obs": "24",
        **linaje(),
    }])
    resultado = limpiar_precipitacion(df)
    assert len(resultado) == 1
    assert resultado["precipitacion_mm"].iloc[0] == 0
    assert resultado["latitud"].iloc[0] == 6.25


def test_ideam_temperatura_rechaza_media_fuera_del_intervalo():
    df = pd.DataFrame([{
        "codigoestacion": "123",
        "nombreestacion": "Estación prueba",
        "municipio": "Medellín",
        "latitud": "6.25",
        "longitud": "-75.56",
        "fecha": "2026-06-01",
        "temperatura_media_c": "30",
        "temperatura_minima_c": "15",
        "temperatura_maxima_c": "25",
        "n_obs": "24",
        **linaje(),
    }])
    try:
        limpiar_temperatura(df)
        assert False, "Debió rechazar la temperatura media fuera del intervalo"
    except ValueError as error:
        assert "fuera del intervalo" in str(error)


def test_noaa_clasifica_los_tres_estados_enso():
    filas = []
    for temporada, anomalia in [
        ("DJF", "0.5"), ("JFM", "-0.5"), ("FMA", "0.49")
    ]:
        filas.append({
            "SEAS": temporada,
            "YR": "2026",
            "TOTAL": "27.5",
            "ANOM": anomalia,
            **linaje(),
        })

    resultado = limpiar_oni(pd.DataFrame(filas))
    assert resultado["fase_enso"].tolist() == [
        "El Niño", "La Niña", "Neutral"
    ]
    assert resultado["mes"].tolist() == [1, 2, 3]


def test_epm_envia_registro_incompleto_a_cuarentena():
    base = {
        "tipodeinformacion": "Monomia",
        "tipodetarifa": "Costo Unitario",
        "tipodedato": "Costo compra: Gm, i",
        "rangodeconsumo": "N/A",
        "nivel": "I",
        "propiedadepm": "10.0",
        "compartido": "10.0",
        "propiedaddelcliente": "10.0",
        "punta": "0",
        "fueradepunta": "0",
        "year": "2020",
        "mes": "Enero",
        **linaje(),
    }
    incompleta = {**base, "year": None, "mes": None,
                  "propiedadepm": None, "compartido": None,
                  "propiedaddelcliente": None, "punta": None,
                  "fueradepunta": None}

    silver, cuarentena = limpiar_epm(pd.DataFrame([base, incompleta]))
    assert len(silver) == 1
    assert len(cuarentena) == 1
    assert "motivo_cuarentena" in cuarentena.columns


def test_epm_conserva_componentes_negativos_de_restricciones():
    fila = {
        "tipodeinformacion": "Monomia",
        "tipodetarifa": "Costo Unitario",
        "tipodedato": "Restricciones: Rm",
        "rangodeconsumo": "N/A",
        "nivel": "I",
        "propiedadepm": "-0.25",
        "compartido": "-0.25",
        "propiedaddelcliente": "-0.25",
        "punta": "0",
        "fueradepunta": "0",
        "year": "2020",
        "mes": "Enero",
        **linaje(),
    }
    silver, cuarentena = limpiar_epm(pd.DataFrame([fila]))
    assert len(silver) == 1
    assert len(cuarentena) == 0
    assert silver["propiedadepm"].iloc[0] == -0.25
