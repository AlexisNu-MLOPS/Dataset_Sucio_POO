import pandas as pd
import pytest

from src.data_preprocessor import DataPreprocessor
from src.data_loader import ExcepcionCalidad


def test_clean_columns():
    df = pd.DataFrame(columns=["Score (1-5)", "¿Es_Fraude?", "Notes & Comments"])
    result = DataPreprocessor(df).clean_columns()
    assert list(result.columns) == ["score", "fraude", "comentarios"]


def test_vacios_a_nulos():
    df = pd.DataFrame({"col": ["", "   ", "nan", "texto"]})
    result = DataPreprocessor(df).vacios_a_nulos()
    assert result["col"].isna().sum() == 3


def test_limpieza_monto():
    df = pd.DataFrame({"monto": ["$1,000", "2000", "texto"]})
    result = DataPreprocessor(df).limpieza_monto()
    assert result["monto"].tolist()[0:2] == [1000, 2000]
    assert pd.isna(result["monto"].iloc[2])


def test_limpieza_score():
    df = pd.DataFrame({"score": ["uno", "dos", "tres", "cuatro", "cinco"]})
    result = DataPreprocessor(df).limpieza_score()
    assert result["score"].tolist() == [1, 2, 3, 4, 5]


def test_eliminar_acentos():
    df = pd.DataFrame({
        "nombre": pd.Series(["José", "María"], dtype="string")
    })
    result = DataPreprocessor(df).eliminar_acentos()
    assert result["nombre"].tolist() == ["Jose", "Maria"]


def test_ban_columnas_nulas():
    df = pd.DataFrame({"a": [1, None], "b": ["x", None]})
    result = DataPreprocessor(df).ban_columnas_nulas()
    assert result["a_nan"].tolist() == [0, 1]
    assert result["b_nan"].tolist() == [0, 1]


def test_validar_nulos_criticos_falla():
    df = pd.DataFrame({
        "fraude": [None, None, 1],
        "monto": [100, None, None]
    })
    with pytest.raises(ExcepcionCalidad):
        DataPreprocessor(df).validar_nulos_criticos(umbral=0.3)


def test_validar_nulos_criticos_ok():
    df = pd.DataFrame({
        "fraude": [0, 1, 0],
        "monto": [100, 200, 300]
    })
    assert DataPreprocessor(df).validar_nulos_criticos() is True


def test_calidad_df():
    df = pd.DataFrame({
        "a": [1, None],
        "a_nan": [0, 1]
    })
    result = DataPreprocessor(df).calidad_df()
    assert "a_nan" not in result.index
    assert result["a"] == 1