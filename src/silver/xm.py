import pandas as pd


def pasar_a_horario(bronce: pd.DataFrame) -> pd.DataFrame:
    horas = [f"Hour{i:02d}" for i in range(1, 25)]
    faltantes = set(horas) - set(bronce.columns)
    if faltantes:
        raise ValueError(f"Faltan columnas horarias de XM: {sorted(faltantes)}")

    columnas_id = [col for col in bronce.columns if col not in horas]
    largo = bronce.melt(
        id_vars=columnas_id,
        value_vars=horas,
        var_name="_hora_origen",
        value_name="valor",
    )

    texto = largo["valor"].astype("string")
    vacio = texto.isna() | texto.str.strip().eq("").fillna(False)
    valores = pd.to_numeric(texto.mask(vacio), errors="coerce")
    no_numericos = ~vacio & valores.isna()
    if no_numericos.any():
        ejemplos = texto[no_numericos].head(5).tolist()
        raise ValueError(f"Valores horarios no numéricos en XM: {ejemplos}")

    fechas = pd.to_datetime(largo["Date"], errors="coerce")
    if fechas.isna().any():
        raise ValueError("Hay fechas inválidas en los datos horarios de XM.")

    largo["Date"] = fechas
    largo["hora"] = largo["_hora_origen"].str.extract(r"(\d+)")[0].astype("int8")
    largo["valor"] = valores
    largo = largo.drop(columns="_hora_origen")

    return largo