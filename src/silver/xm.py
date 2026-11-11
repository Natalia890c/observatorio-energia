import pandas as pd

LINAJE = ["_fuente", "_origen", "_extraido_en"]
HORAS = [f"Hour{i:02d}" for i in range(1, 25)]


def _validar_fechas(df: pd.DataFrame) -> pd.DataFrame:
    """Normaliza las fechas y rechaza registros con fechas inválidas."""
    resultado = df.copy()
    fechas = pd.to_datetime(resultado["Date"], errors="coerce")

    if fechas.isna().any():
        raise ValueError(
            f"Se encontraron {fechas.isna().sum()} fechas inválidas en XM."
        )

    resultado["Date"] = fechas
    return resultado


def _validar_numericos(
    serie: pd.Series,
    nombre: str,
    permitir_vacios: bool = False,
) -> pd.Series:
    """Convierte una columna a numérica y detecta valores no válidos."""
    texto = serie.astype("string").str.strip()
    vacios = texto.isna() | texto.eq("")
    valores = pd.to_numeric(texto.mask(vacios), errors="coerce")

    invalidos = ~vacios & valores.isna()

    if invalidos.any():
        ejemplos = texto[invalidos].head(5).tolist()
        raise ValueError(
            f"Valores no numéricos en {nombre}: {ejemplos}"
        )

    if not permitir_vacios and valores.isna().any():
        raise ValueError(
            f"Se encontraron {valores.isna().sum()} valores vacíos en {nombre}."
        )

    return valores


def pasar_a_horario(bronce: pd.DataFrame) -> pd.DataFrame:
    """Convierte las 24 columnas horarias en registros por fecha y hora.

    Las observaciones vacías se excluyen y no se convierten en cero.
    """
    faltantes = set(HORAS) - set(bronce.columns)

    if faltantes:
        raise ValueError(
            f"Faltan columnas horarias de XM: {sorted(faltantes)}"
        )

    columnas_id = [
        columna
        for columna in bronce.columns
        if columna not in HORAS
    ]

    largo = bronce.melt(
        id_vars=columnas_id,
        value_vars=HORAS,
        var_name="_hora_origen",
        value_name="valor",
    )

    texto = largo["valor"].astype("string").str.strip()
    vacios = texto.isna() | texto.eq("")
    valores = pd.to_numeric(texto.mask(vacios), errors="coerce")

    invalidos = ~vacios & valores.isna()

    if invalidos.any():
        ejemplos = texto[invalidos].head(5).tolist()
        raise ValueError(
            f"Valores horarios no numéricos en XM: {ejemplos}"
        )

    fechas = pd.to_datetime(largo["Date"], errors="coerce")

    if fechas.isna().any():
        raise ValueError("Hay fechas inválidas en los datos horarios de XM.")

    # Se conservan únicamente observaciones con valores numéricos.
    validos = ~vacios
    largo = largo.loc[validos].copy()
    largo["Date"] = fechas.loc[validos]
    largo["valor"] = valores.loc[validos]

    largo["hora"] = (
        largo["_hora_origen"]
        .str.extract(r"(\d+)")[0]
        .astype("int8")
    )

    return largo.drop(columns="_hora_origen").reset_index(drop=True)


def limpiar_diaria(bronce: pd.DataFrame) -> pd.DataFrame:
    """Limpia las fuentes diarias de embalses y aportes de energía."""
    requeridas = {"Date", "Id", "Value"}
    faltantes = requeridas - set(bronce.columns)

    if faltantes:
        raise ValueError(
            f"Faltan columnas en fuente diaria XM: {sorted(faltantes)}"
        )

    resultado = _validar_fechas(bronce)
    resultado["Value"] = _validar_numericos(
        resultado["Value"],
        "Value",
    )

    return resultado


def limpiar_catalogo(bronce: pd.DataFrame) -> pd.DataFrame:
    """Normaliza el catálogo y consolida duplicados exactos."""
    resultado = bronce.copy()

    columnas = {
        "Date": "fecha_catalogo",
        "Id": "id_sistema",
        "Code": "codigo_recurso",
        "Name": "nombre_recurso",
        "Type": "tipo_recurso",
        "Disp": "tipo_despacho",
        "RecType": "tipo_recurso_operativo",
        "CompanyCode": "codigo_empresa",
        "EnerSource": "fuente_energia",
        "OperStartdate": "fecha_inicio_operacion",
        "State": "estado",
    }

    faltantes = set(columnas) - set(resultado.columns)

    if faltantes:
        raise ValueError(
            f"Faltan columnas en catálogo XM: {sorted(faltantes)}"
        )

    resultado = resultado.rename(columns=columnas)

    resultado["fecha_catalogo"] = pd.to_datetime(
        resultado["fecha_catalogo"],
        errors="coerce",
    )

    resultado["fecha_inicio_operacion"] = pd.to_datetime(
        resultado["fecha_inicio_operacion"],
        errors="coerce",
    )

    if resultado["fecha_catalogo"].isna().any():
        raise ValueError("Hay fechas inválidas en el catálogo XM.")

    if resultado["fecha_inicio_operacion"].isna().any():
        raise ValueError("Hay fechas de operación inválidas en el catálogo XM.")

    columnas_texto = [
        "codigo_recurso",
        "nombre_recurso",
        "tipo_recurso",
        "tipo_despacho",
        "tipo_recurso_operativo",
        "codigo_empresa",
        "fuente_energia",
        "estado",
    ]

    for columna in columnas_texto:
        resultado[columna] = resultado[columna].astype("string").str.strip()

        if resultado[columna].isna().any() or resultado[columna].eq("").any():
            raise ValueError(
                f"Hay valores vacíos en {columna} del catálogo XM."
            )

    # Consolidar únicamente duplicados idénticos en todas sus columnas.
    resultado = resultado.drop_duplicates(keep="first")

    # Un código repetido con información diferente requiere revisión.
    conflictos = resultado[
        resultado.duplicated(subset=["codigo_recurso"], keep=False)
    ]

    if not conflictos.empty:
        codigos = conflictos["codigo_recurso"].unique().tolist()
        raise ValueError(
            f"Códigos de recurso con información contradictoria: {codigos[:10]}"
        )

    return resultado.reset_index(drop=True)