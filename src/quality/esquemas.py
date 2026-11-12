"""
Reglas de calidad de la capa plata, escritas con pandera.

Un ESQUEMA es la lista de condiciones que una tabla limpia DEBE cumplir:
que columnas tiene, de que tipo es cada una y que valores acepta.
Si una sola fila no cumple, pandera detiene el programa y dice cual fila
y cual regla fallo. Asi, ningun dato sucio llega a la capa oro.

Este archivo SOLO GUARDA las reglas: no revisa nada por si solo.
Los módulos de limpieza en src/silver/ validan sus tablas con estos esquemas
antes de devolverlas al proceso que las guarda. EnerAndes valida la tabla
consolidada antes de escribirla.

    from src.quality.esquemas import ESQUEMA_VENTAS
    ESQUEMA_VENTAS.validate(limpias, lazy=True)

  - La primera trae las reglas de este archivo (la variable ESQUEMA_VENTAS).
  - La segunda revisa la tabla limpia con esas reglas.
    Si una regla falla, el programa se detiene y la tabla NO se guarda.
    lazy=True: revisa toda la tabla y muestra TODOS los errores juntos
    (sin lazy=True, se detiene en el primer error y no se sabe si hay mas).

Las reglas van en un archivo aparte para escribirlas una sola vez:
las usan la limpieza (enerandes.py) y las pruebas (tests/).
"""
# ---------------------------------------------------------------------------
# IMPORTS
# ---------------------------------------------------------------------------
# pandera: libreria para revisar que una tabla de pandas cumpla reglas.
# .pandas es la parte de pandera para tablas de pandas; "as pa" le da el nombre corto pa
import pandera.pandas as pa
# Column: las reglas de UNA columna (su tipo y sus condiciones)
# Check: una condicion, por ejemplo ">= 0" o "esta en esta lista"
from pandera.pandas import Check, Column

# ---------------------------------------------------------------------------
# VALORES ACEPTADOS en las columnas de categorias
# ---------------------------------------------------------------------------
# Los unicos 4 valores que puede tener la columna segmento
SEGMENTOS = ["Residencial", "Comercial", "Industrial", "No informado"]
# Los unicos 2 valores que puede tener la columna tipo_compra
TIPOS_COMPRA = ["Bolsa", "Contrato"]

# ---------------------------------------------------------------------------
# EL ESQUEMA de la tabla limpia
# ---------------------------------------------------------------------------
# pa.DataFrameSchema(...) crea el esquema. Recibe un diccionario
# {nombre de columna: Column(tipo, condicion)} y algunas reglas de toda la tabla
ESQUEMA_VENTAS = pa.DataFrameSchema(
    {
        # periodo: texto (str) que cumpla el patron AAAA-MM con un mes de 01 a 12.
        # r"^\d{4}-(0[1-9]|1[0-2])$" es una expresion regular (un patron de texto):
        #   ^ inicio, \d{4} cuatro digitos, - un guion, (0[1-9]|1[0-2]) del 01 al 12, $ fin
        # Ejemplo: '2023-04' cumple; '2023-13' y 'TOTAL' no cumplen
        "periodo": Column(str, Check.str_matches(r"^\d{4}-(0[1-9]|1[0-2])$")),
        # divipola: texto de exactamente 5 digitos (^\d{5}$). '05001' cumple; '5001' no
        "divipola": Column(str, Check.str_matches(r"^\d{5}$")),
        # municipio: texto, sin condicion extra (el nombre oficial ya viene de MUNICIPIOS)
        "municipio": Column(str),
        # segmento: texto que este en la lista SEGMENTOS (.isin = "esta en")
        "segmento": Column(str, Check.isin(SEGMENTOS)),
        # tipo_compra: texto que este en la lista TIPOS_COMPRA: solo Bolsa o Contrato
        "tipo_compra": Column(str, Check.isin(TIPOS_COMPRA)),
        # energia_kwh: numero con decimales (float) mayor o igual a 0 (ge = greater or equal)
        "energia_kwh": Column(float, Check.ge(0)),
        # valor_cop: numero >= 0; nullable=True permite celdas vacias (regla 9 de la limpieza)
        "valor_cop": Column(float, Check.ge(0), nullable=True),
        # clientes: numero entero (int) mayor o igual a 0
        "clientes": Column(int, Check.ge(0)),
    },
    # unique: no puede haber dos filas con el mismo periodo, municipio, segmento y tipo
    # de compra; si las hay, es una venta repetida
    unique=["periodo", "divipola", "segmento", "tipo_compra"],
    # strict=True: la tabla no puede traer columnas que no esten en este esquema
    strict=True,
)

LINEAJE = {
    "_fuente": Column(str, nullable=False),
    "_origen": Column(str, nullable=False),
    "_extraido_en": Column(str, nullable=False),
}

_COLUMNAS_XM_HORARIO = {
    "Date": Column(pa.DateTime, nullable=False),
    "Id": Column(str, nullable=False),
    "code": Column(str, nullable=False),
    **LINEAJE,
    "valor": Column(pa.Float64, Check.ge(0), nullable=True),
    "hora": Column(pa.Int8, Check.in_range(1, 24), nullable=False),
}

ESQUEMA_XM_HORARIA = pa.DataFrameSchema(
    _COLUMNAS_XM_HORARIO,
    unique=["Date", "Id", "code", "hora"],
    strict=True,
)

ESQUEMA_XM_PRECIO_BOLSA = ESQUEMA_XM_HORARIA
ESQUEMA_XM_DEMANDA = ESQUEMA_XM_HORARIA
ESQUEMA_XM_GENERACION = ESQUEMA_XM_HORARIA

ESQUEMA_XM_DIARIA = pa.DataFrameSchema(
    {
        "Date": Column(pa.DateTime, nullable=False),
        "Id": Column(str, nullable=False),
        "Value": Column(pa.Float64, Check.ge(0), nullable=False),
        **LINEAJE,
    },
    unique=["Date", "Id"],
    strict=True,
)

ESQUEMA_XM_EMBALSES = ESQUEMA_XM_DIARIA
ESQUEMA_XM_APORTES = ESQUEMA_XM_DIARIA

ESQUEMA_XM_CATALOGO = pa.DataFrameSchema(
    {
        "fecha_catalogo": Column(pa.DateTime, nullable=False),
        "id_sistema": Column(str, nullable=False),
        "codigo_recurso": Column(str, Check.str_length(min_value=1), nullable=False),
        "nombre_recurso": Column(str, Check.str_length(min_value=1), nullable=False),
        "tipo_recurso": Column(str, Check.str_length(min_value=1), nullable=False),
        "tipo_despacho": Column(str, Check.str_length(min_value=1), nullable=False),
        "tipo_recurso_operativo": Column(str, Check.str_length(min_value=1), nullable=False),
        "codigo_empresa": Column(str, Check.str_length(min_value=1), nullable=False),
        "fuente_energia": Column(str, Check.str_length(min_value=1), nullable=False),
        "fecha_inicio_operacion": Column(pa.DateTime, nullable=False),
        "estado": Column(str, Check.str_length(min_value=1), nullable=False),
        **LINEAJE,
    },
    unique=["codigo_recurso"],
    strict=True,
)

_COLUMNAS_IDEAM_COMUNES = {
    "codigoestacion": Column(str, Check.str_length(min_value=1), nullable=False),
    "nombreestacion": Column(str, Check.str_length(min_value=1), nullable=False),
    "municipio": Column(str, Check.str_length(min_value=1), nullable=False),
    "latitud": Column(pa.Float64, Check.in_range(-90, 90), nullable=False),
    "longitud": Column(pa.Float64, Check.in_range(-180, 180), nullable=False),
    "fecha": Column(pa.DateTime, nullable=False),
    "n_obs": Column(pa.Int64, Check.gt(0), nullable=False),
    **LINEAJE,
}

ESQUEMA_IDEAM_PRECIPITACION = pa.DataFrameSchema(
    {
        **_COLUMNAS_IDEAM_COMUNES,
        "precipitacion_mm": Column(pa.Float64, Check.ge(0), nullable=False),
    },
    unique=["codigoestacion", "fecha"],
    strict=True,
)

ESQUEMA_IDEAM_TEMPERATURA = pa.DataFrameSchema(
    {
        **_COLUMNAS_IDEAM_COMUNES,
        "temperatura_media_c": Column(pa.Float64, Check.in_range(-10, 60), nullable=False),
        "temperatura_minima_c": Column(pa.Float64, Check.in_range(-10, 60), nullable=False),
        "temperatura_maxima_c": Column(pa.Float64, Check.in_range(-10, 60), nullable=False),
    },
    checks=[
        Check(
            lambda df: df["temperatura_minima_c"] <= df["temperatura_maxima_c"],
            error="La temperatura mínima no puede superar la máxima.",
        ),
        Check(
            lambda df: df["temperatura_media_c"].between(
                df["temperatura_minima_c"], df["temperatura_maxima_c"]
            ),
            error="La temperatura media debe estar entre la mínima y la máxima.",
        ),
    ],
    unique=["codigoestacion", "fecha"],
    strict=True,
)

ESQUEMA_NOAA_ONI = pa.DataFrameSchema(
    {
        "fecha": Column(pa.DateTime, nullable=False),
        "anio": Column(pa.Int16, Check.in_range(1950, 2100), nullable=False),
        "mes": Column(pa.Int8, Check.in_range(1, 12), nullable=False),
        "temporada": Column(
            str,
            Check.isin([
                "DJF", "JFM", "FMA", "MAM", "AMJ", "MJJ",
                "JJA", "JAS", "ASO", "SON", "OND", "NDJ",
            ]),
            nullable=False,
        ),
        "temperatura_oceanica_total": Column(pa.Float64, nullable=False),
        "anomalia_oni": Column(pa.Float64, nullable=False),
        "fase_enso": Column(
            str, Check.isin(["El Niño", "La Niña", "Neutral"]), nullable=False
        ),
        **LINEAJE,
    },
    unique=["fecha"],
    strict=True,
)

ESQUEMA_EPM_TARIFAS = pa.DataFrameSchema(
    {
        "tipodeinformacion": Column(str, Check.str_length(min_value=1), nullable=False),
        "tipodetarifa": Column(str, Check.str_length(min_value=1), nullable=False),
        "tipodedato": Column(str, Check.str_length(min_value=1), nullable=False),
        "rangodeconsumo": Column(str, Check.str_length(min_value=1), nullable=False),
        "nivel": Column(str, Check.str_length(min_value=1), nullable=False),
        "propiedadepm": Column(pa.Float64, nullable=False),
        "compartido": Column(pa.Float64, nullable=False),
        "propiedaddelcliente": Column(pa.Float64, nullable=False),
        "punta": Column(pa.Float64, nullable=False),
        "fueradepunta": Column(pa.Float64, nullable=False),
        "year": Column(pa.Int16, Check.in_range(1900, 2100), nullable=False),
        **LINEAJE,
        "mes_nombre": Column(
            str,
            Check.isin([
                "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
                "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre",
                "Diciembre",
            ]),
            nullable=False,
        ),
        "mes": Column(pa.Int8, Check.in_range(1, 12), nullable=False),
    },
    strict=True,
)
