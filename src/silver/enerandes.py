"""Limpieza de las cuatro hojas de ventas de EnerAndes para la capa plata.

Uso:
    python -m src.silver.enerandes
"""
import json
import re
import unicodedata
from datetime import date, datetime
from pathlib import Path

import pandas as pd

from src import config
from src.quality.esquemas import ESQUEMA_VENTAS
from src.utils import log

LINAJE = ["_fuente", "_origen", "_extraido_en"]
ORDEN = [
    "periodo", "divipola", "municipio", "segmento", "tipo_compra",
    "energia_kwh", "valor_cop", "clientes",
]
CLAVES_NEGOCIO = ["periodo", "divipola", "segmento", "tipo_compra"]
COLUMNAS_REQUERIDAS = set(ORDEN) - {"divipola"}
COLUMNAS_CUARENTENA = [
    *ORDEN, "anio_fuente", "fila_excel", "motivo", "registro_original",
]

MUNICIPIOS = {
    "medellin": ("05001", "Medellín"),
    "santa fe de antioquia": ("05042", "Santa Fe de Antioquia"),
    "apartado": ("05045", "Apartadó"),
    "bello": ("05088", "Bello"),
    "caldas": ("05129", "Caldas"),
    "caucasia": ("05154", "Caucasia"),
    "copacabana": ("05212", "Copacabana"),
    "envigado": ("05266", "Envigado"),
    "girardota": ("05308", "Girardota"),
    "itagui": ("05360", "Itagüí"),
    "la estrella": ("05380", "La Estrella"),
    "marinilla": ("05440", "Marinilla"),
    "rionegro": ("05615", "Rionegro"),
    "sabaneta": ("05631", "Sabaneta"),
    "turbo": ("05837", "Turbo"),
}
ALIAS_MUNICIPIO = {
    "rio negro": "rionegro",
    "rionegro (ant)": "rionegro",
    "medellin d.e.": "medellin",
    "sta fe de antioquia": "santa fe de antioquia",
    "santafe de antioquia": "santa fe de antioquia",
}
SEGMENTOS = {
    "residencial": "Residencial",
    "resid.": "Residencial",
    "comercial": "Comercial",
    "industrial": "Industrial",
    "ind": "Industrial",
}
TIPOS_COMPRA = {"bolsa": "Bolsa", "contrato": "Contrato", "contratos": "Contrato"}
ALIAS_ENCABEZADOS = {
    "fecha": "periodo",
    "periodo": "periodo",
    "mes": "periodo",
    "fechacorte": "periodo",
    "municipio": "municipio",
    "ciudad": "municipio",
    "segmento": "segmento",
    "segmentocliente": "segmento",
    "tipocliente": "segmento",
    "tipocompra": "tipo_compra",
    "modalidad": "tipo_compra",
    "compra": "tipo_compra",
    "energiakwh": "energia_kwh",
    "energia": "energia_kwh",
    "consumokwh": "energia_kwh",
    "kwh": "energia_kwh",
    "unidad": "unidad",
    "valorcop": "valor_cop",
    "valor": "valor_cop",
    "facturado": "valor_cop",
    "totalfacturadocop": "valor_cop",
    "numclientes": "clientes",
    "clientes": "clientes",
    "usuarios": "clientes",
    "clientesactivos": "clientes",
}
MESES = {
    "jan": 1, "ene": 1,
    "feb": 2,
    "mar": 3,
    "apr": 4, "abr": 4,
    "may": 5,
    "jun": 6,
    "jul": 7,
    "aug": 8, "ago": 8,
    "sep": 9, "sept": 9, "set": 9,
    "oct": 10,
    "nov": 11,
    "dec": 12, "dic": 12,
}


def sin_tildes(texto: str) -> str:
    """Convierte texto a minúsculas, sin espacios laterales ni tildes."""
    letras = unicodedata.normalize("NFD", texto.strip().lower())
    return "".join(letra for letra in letras if unicodedata.category(letra) != "Mn")


def clave_municipio(texto: str | None) -> str | None:
    """Resuelve alias conocidos y normaliza el nombre de un municipio."""
    if pd.isna(texto):
        return None
    clave = sin_tildes(str(texto))
    return ALIAS_MUNICIPIO.get(clave, clave)


def _vacio(valor: object) -> bool:
    return pd.isna(valor) or (isinstance(valor, str) and not valor.strip())


def _encabezado(valor: object) -> str | None:
    if _vacio(valor):
        return None
    normalizado = re.sub(r"[^a-z0-9]", "", sin_tildes(str(valor)))
    return ALIAS_ENCABEZADOS.get(normalizado)


def _buscar_encabezado(df: pd.DataFrame) -> tuple[int, dict[str, object]]:
    requeridas = COLUMNAS_REQUERIDAS
    for indice in range(min(len(df), 20)):
        columnas: dict[str, object] = {}
        for columna, valor in df.iloc[indice].items():
            nombre = _encabezado(valor)
            if nombre is not None:
                columnas.setdefault(nombre, columna)
        if requeridas.issubset(columnas):
            return indice, columnas
    raise ValueError("No se encontró una fila de encabezados reconocible en la hoja EnerAndes.")


def _periodo(valor: object) -> str | None:
    if _vacio(valor):
        return None
    if isinstance(valor, (date, datetime, pd.Timestamp)):
        return valor.strftime("%Y-%m")

    texto = str(valor).strip().lower()
    if re.fullmatch(r"\d{4}-(0[1-9]|1[0-2])", texto):
        return texto

    coincidencia = re.fullmatch(r"(0?[1-9]|1[0-2])/(\d{4})", texto)
    if coincidencia:
        return f"{coincidencia.group(2)}-{int(coincidencia.group(1)):02d}"

    coincidencia = re.fullmatch(r"(\d{1,2})/(\d{1,2})/(\d{4})", texto)
    if coincidencia:
        dia, mes, anio = map(int, coincidencia.groups())
        try:
            return datetime(anio, mes, dia).strftime("%Y-%m")
        except ValueError:
            return None

    coincidencia = re.fullmatch(r"([a-záéíóú]{3,4})-(\d{2}|\d{4})", texto)
    if coincidencia:
        mes = MESES.get(sin_tildes(coincidencia.group(1)))
        anio = int(coincidencia.group(2))
        if anio < 100:
            anio += 2000 if anio < 70 else 1900
        if mes is not None and 1 <= mes <= 12:
            return f"{anio:04d}-{mes:02d}"
    return None


def _numero(valor: object) -> float | None:
    if _vacio(valor):
        return None
    try:
        return float(str(valor).strip().replace(",", "."))
    except ValueError:
        return None


def _registro_original(fila: pd.Series) -> str:
    return json.dumps(fila.to_dict(), ensure_ascii=False, default=str)


def limpiar(
    bronce: pd.DataFrame,
    anio_fuente: int | None = None,
) -> tuple[pd.DataFrame, pd.DataFrame, list[dict]]:
    """Normaliza una hoja de bronce y devuelve ventas, cuarentena y métricas."""
    fuente = bronce.drop(columns=LINAJE, errors="ignore")
    indice_encabezado, columnas = _buscar_encabezado(fuente)
    filas = fuente.iloc[indice_encabezado + 1:]
    metricas: list[dict] = []

    def medir(problema: str, regla: str, antes: int, despues: int) -> None:
        metricas.append({
            "hoja": anio_fuente or "sin año",
            "problema": problema,
            "regla aplicada": regla,
            "antes": antes,
            "despues": despues,
        })

    medir("Títulos y notas antes del encabezado", "Ignorarlos como filas de datos",
          indice_encabezado, 0)

    ventas: list[dict] = []
    cuarentena: list[dict] = []
    totales = 0
    filas_vacias = 0
    segmentos_vacios = 0
    valores_facturados_vacios = 0
    for posicion, (_, fila) in enumerate(filas.iterrows(), start=indice_encabezado + 2):
        if all(_vacio(valor) for valor in fila):
            filas_vacias += 1
            continue

        originales = _registro_original(fila)
        valor_periodo = fila[columnas["periodo"]]
        if str(valor_periodo).strip().upper() == "TOTAL":
            totales += 1
            continue
        if _encabezado(valor_periodo) == "periodo":
            continue

        periodo = _periodo(valor_periodo)
        municipio_raw = fila[columnas["municipio"]]
        clave = clave_municipio(municipio_raw)
        municipio = MUNICIPIOS.get(clave) if clave is not None else None
        segmento_raw = fila[columnas["segmento"]]
        if _vacio(segmento_raw):
            segmento = "No informado"
            segmentos_vacios += 1
        else:
            segmento = SEGMENTOS.get(sin_tildes(str(segmento_raw)))
        tipo_raw = fila[columnas["tipo_compra"]]
        tipo_compra = (
            TIPOS_COMPRA.get(sin_tildes(str(tipo_raw)))
            if not _vacio(tipo_raw) else None
        )

        energia = _numero(fila[columnas["energia_kwh"]])
        unidad = fila[columnas["unidad"]] if "unidad" in columnas else "kWh"
        unidad_normalizada = sin_tildes(str(unidad)) if not _vacio(unidad) else ""
        if "unidad" in columnas and not unidad_normalizada:
            factor = None
        elif unidad_normalizada == "kwh":
            factor = 1
        elif unidad_normalizada == "mwh":
            factor = 1000
        else:
            factor = None
        if energia is not None and factor is not None:
            energia *= factor

        valor_cop_raw = fila[columnas["valor_cop"]]
        valor_cop = _numero(valor_cop_raw)
        if _vacio(valor_cop_raw):
            valores_facturados_vacios += 1
        clientes_raw = fila[columnas["clientes"]]
        clientes_numero = _numero(clientes_raw)

        razones: list[str] = []
        if periodo is None:
            razones.append("Periodo vacío o con formato no reconocido")
        elif anio_fuente is not None and int(periodo[:4]) != anio_fuente:
            razones.append(f"El periodo no corresponde a la hoja {anio_fuente}")
        if municipio is None:
            razones.append("Municipio vacío o no reconocido")
        if segmento is None:
            razones.append("Segmento no reconocido")
        if tipo_compra is None:
            razones.append("Tipo de compra vacío o no reconocido")
        if factor is None:
            razones.append("Unidad de energía vacía o no reconocida")
        if energia is None:
            razones.append("Energía vacía o no numérica")
        elif energia < 0:
            razones.append("Energía negativa")
        if not _vacio(valor_cop_raw) and valor_cop is None:
            razones.append("Valor facturado no numérico")
        elif valor_cop is not None and valor_cop < 0:
            razones.append("Valor facturado negativo")
        if clientes_numero is None:
            razones.append("Clientes vacíos o no numéricos")
        elif clientes_numero < 0:
            razones.append("Clientes negativos")
        elif not clientes_numero.is_integer():
            razones.append("Número de clientes no entero")

        campos = {
            "periodo": periodo if periodo is not None else valor_periodo,
            "divipola": municipio[0] if municipio else None,
            "municipio": municipio[1] if municipio else municipio_raw,
            "segmento": segmento if segmento is not None else segmento_raw,
            "tipo_compra": tipo_compra if tipo_compra is not None else tipo_raw,
            "energia_kwh": energia,
            "valor_cop": valor_cop,
            "clientes": int(clientes_numero) if clientes_numero is not None else None,
        }
        if razones:
            cuarentena.append({
                **campos,
                "anio_fuente": anio_fuente or (int(periodo[:4]) if periodo else None),
                "fila_excel": posicion,
                "motivo": "; ".join(razones),
                "registro_original": originales,
            })
        else:
            ventas.append({**campos, "_registro_original": originales, "_fila_excel": posicion})

    medir("Filas de totales", "Excluirlas del conjunto de ventas", totales, 0)
    medir("Filas completamente vacías", "Excluirlas del conjunto de ventas", filas_vacias, 0)
    medir("Segmentos vacíos", "Asignar 'No informado'", segmentos_vacios, 0)
    medir("Valores facturados vacíos", "Conservar vacío; no inferir el dato",
          valores_facturados_vacios, valores_facturados_vacios)

    # Una venta duplicada con los mismos valores se consolida; las colisiones
    # con medidas distintas se conservan en cuarentena para revisión manual.
    ventas_unicas: list[dict] = []
    primeras_por_clave: dict[tuple, dict] = {}
    duplicados = 0
    colisiones = 0
    for venta in ventas:
        clave_venta = tuple(venta[columna] for columna in CLAVES_NEGOCIO)
        primera = primeras_por_clave.get(clave_venta)
        if primera is None:
            primeras_por_clave[clave_venta] = venta
            ventas_unicas.append(venta)
            continue
        medidas = ("energia_kwh", "valor_cop", "clientes")
        if all(primera[columna] == venta[columna] for columna in medidas):
            duplicados += 1
            continue
        colisiones += 1
        cuarentena.append({
            **{columna: venta[columna] for columna in ORDEN},
            "anio_fuente": anio_fuente,
            "fila_excel": venta["_fila_excel"],
            "motivo": "Clave de venta duplicada con valores diferentes",
            "registro_original": venta["_registro_original"],
        })
    medir("Ventas duplicadas", "Conservar una sola copia", duplicados, 0)
    medir("Claves duplicadas con valores distintos", "Enviar la colisión a cuarentena",
          colisiones, 0)

    limpias = pd.DataFrame(ventas_unicas, columns=[*ORDEN, "_registro_original", "_fila_excel"])
    limpias = limpias[ORDEN]
    for columna in ("periodo", "divipola", "municipio", "segmento", "tipo_compra"):
        limpias[columna] = limpias[columna].astype(str)
    limpias["energia_kwh"] = pd.to_numeric(limpias["energia_kwh"], errors="raise").astype(float)
    limpias["valor_cop"] = pd.to_numeric(limpias["valor_cop"], errors="raise").astype(float)
    limpias["clientes"] = pd.to_numeric(limpias["clientes"], errors="raise").astype("int64")
    tabla_cuarentena = pd.DataFrame(cuarentena, columns=COLUMNAS_CUARENTENA)
    return limpias.reset_index(drop=True), tabla_cuarentena, metricas


def escribir_reporte(
    metricas: list[dict],
    filas_bronce: int,
    filas_plata: int,
    filas_cuarentena: int,
) -> None:
    """Escribe el reporte agregado de calidad de las cuatro hojas."""
    lineas = [
        "# Reporte de calidad: ventas de EnerAndes (2023-2026)\n",
        f"- Filas en bronce: {filas_bronce:,}",
        f"- Filas en plata: {filas_plata:,}",
        f"- Filas en cuarentena: {filas_cuarentena:,}\n",
        "| Hoja | Problema | Regla aplicada | Antes | Después |",
        "|---:|---|---|---:|---:|",
    ]
    for metrica in metricas:
        lineas.append(
            f"| {metrica['hoja']} | {metrica['problema']} | "
            f"{metrica['regla aplicada']} | {metrica['antes']} | {metrica['despues']} |"
        )
    config.DIR_DOCS.mkdir(parents=True, exist_ok=True)
    (config.DIR_DOCS / "reporte_calidad.md").write_text(
        "\n".join(lineas) + "\n", encoding="utf-8"
    )


def main() -> None:
    tablas_limpias: list[pd.DataFrame] = []
    tablas_cuarentena: list[pd.DataFrame] = []
    metricas: list[dict] = []
    archivos: list[Path] = []

    for anio in range(2023, 2027):
        archivo = config.DIR_BRONZE / f"enerandes_ventas_{anio}.parquet"
        if not archivo.exists():
            raise FileNotFoundError(
                f"No se encontró {archivo}. Ejecute primero python -m src.extract.enerandes."
            )
        bronce = pd.read_parquet(archivo)
        log(f"Bronce {anio}: {len(bronce):,} filas")
        limpias, cuarentena, metricas_hoja = limpiar(bronce, anio_fuente=anio)
        tablas_limpias.append(limpias)
        tablas_cuarentena.append(cuarentena)
        metricas.extend(metricas_hoja)
        archivos.append(bronce)

    limpias = pd.concat(tablas_limpias, ignore_index=True)
    cuarentena = pd.concat(tablas_cuarentena, ignore_index=True)
    ESQUEMA_VENTAS.validate(limpias, lazy=True)
    log("Validación con pandera: OK")

    config.DIR_SILVER.mkdir(parents=True, exist_ok=True)
    limpias.to_parquet(config.DIR_SILVER / "enerandes_ventas.parquet", index=False)
    cuarentena.to_parquet(config.DIR_SILVER / "enerandes_cuarentena.parquet", index=False)
    escribir_reporte(
        metricas, sum(len(tabla) for tabla in archivos), len(limpias), len(cuarentena)
    )

    log(
        f"Plata: {len(limpias):,} filas limpias y "
        f"{len(cuarentena):,} en cuarentena"
    )
    log("Archivos en data/silver/ y reporte en docs/reporte_calidad.md")


if __name__ == "__main__":
    main()
