import pandas as pd

from src.transformar import _separar_conflictos_catalogo


def test_catalogo_repetido_con_atributos_distintos_va_a_cuarentena():
    bronce = pd.DataFrame([
        {"Code": "R001", "Name": "Recurso válido"},
        {"Code": "R001", "Name": "Recurso válido"},
        {"Code": "PRG1", "Name": "PROELECTRICA"},
        {"Code": "PRG1", "Name": "PROELECTRICA 1"},
    ])

    catalogo, cuarentena = _separar_conflictos_catalogo(bronce)

    assert catalogo.to_dict("records") == [
        {"Code": "R001", "Name": "Recurso válido"}
    ]
    assert cuarentena["Code"].tolist() == ["PRG1", "PRG1"]
    assert cuarentena["motivo"].eq(
        "Código repetido con atributos distintos"
    ).all()
    assert cuarentena["registro_original"].notna().all()
