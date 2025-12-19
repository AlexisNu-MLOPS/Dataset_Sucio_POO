"""
Pruebas unitarias para el modulo DataPreprocessor.

Este archivo valida las distintas etapas de limpieza,
estandarizacion y validacion de calidad de un DataFrame.

Las pruebas cubren:
- Limpieza de nombres de columnas
- Conversion de valores vacíos a nulos
- Limpieza de columnas numericas (montos)
- Conversion de scores de texto a valores numericos
- Eliminacion de acentos
- Creacion de columnas bandera para valores nulos
- Validacion de nulos críticos según un umbral definido
- Resumen de calidad del DataFrame

Estas pruebas aseguran que los datos esten listos
para su uso posterior en análisis o modelos.
"""
import pandas as pd
import pytest

from src.data_preprocessor import DataPreprocessor
from src.data_loader import ExcepcionCalidad


def test_clean_columns():
    """
    Verifica que los nombres de las columnas sean limpiados y
    estandarizados correctamente.

    Se valida que:
    - Se eliminen caracteres especiales
    - Se utilicen minusculas
    - Se reemplacen nombres a un formato estandar
    """
    df = pd.DataFrame(columns=["Score (1-5)", "¿Es_Fraude?", "Notes & Comments"])
    result = DataPreprocessor(df).clean_columns()
    assert list(result.columns) == ["score", "fraude", "comentarios"]


def test_vacios_a_nulos():
    """
    Verifica que los valores vacíos, espacios en blanco y
    cadenas de texto 'nan' sean convertidos correctamente a NaN.
    """
    df = pd.DataFrame({"col": ["", "   ", "nan", "texto"]})
    result = DataPreprocessor(df).vacios_a_nulos()
    assert result["col"].isna().sum() == 3


def test_limpieza_monto():
    """
    Verifica que la limpieza de la columna monto:
    - Elimine simbolos de moneda y separadores
    - Convierta los valores a tipo numerico
    - Asigne NaN a valores no convertibles
    """
    df = pd.DataFrame({"monto": ["$1,000", "2000", "texto"]})
    result = DataPreprocessor(df).limpieza_monto()
    assert result["monto"].tolist()[0:2] == [1000, 2000]
    assert pd.isna(result["monto"].iloc[2])


def test_limpieza_score():
    """
    Verifica la conversion de scores expresados en texto
    (uno, dos, tres, etc.) a valores numericos enteros.
    """
    df = pd.DataFrame({"score": ["uno", "dos", "tres", "cuatro", "cinco"]})
    result = DataPreprocessor(df).limpieza_score()
    assert result["score"].tolist() == [1, 2, 3, 4, 5]


def test_eliminar_acentos():
    """
    Verifica que los acentos sean eliminados correctamente
    de columnas de tipo string.
    """
    df = pd.DataFrame({
        "nombre": pd.Series(["José", "María"], dtype="string")
    })
    result = DataPreprocessor(df).eliminar_acentos()
    assert result["nombre"].tolist() == ["Jose", "Maria"]


def test_ban_columnas_nulas():
    """
    Verifica la creacion de columnas bandera (_nan) que indican
    la presencia de valores nulos en el DataFrame.
    """
    df = pd.DataFrame({"a": [1, None], "b": ["x", None]})
    result = DataPreprocessor(df).ban_columnas_nulas()
    assert result["a_nan"].tolist() == [0, 1]
    assert result["b_nan"].tolist() == [0, 1]


def test_validar_nulos_criticos_falla():
    """
    Verifica que se lance una excepcion cuando el porcentaje
    de valores nulos en columnas criticas supera el umbral definido.
    """
    df = pd.DataFrame({
        "fraude": [None, None, 1],
        "monto": [100, None, None]
    })
    with pytest.raises(ExcepcionCalidad):
        DataPreprocessor(df).validar_nulos_criticos(umbral=0.3)


def test_validar_nulos_criticos_ok():
    """
    Verifica que el DataFrame pase la validacion de calidad
    cuando el porcentaje de valores nulos está dentro del umbral permitido.
    """
    df = pd.DataFrame({
        "fraude": [0, 1, 0],
        "monto": [100, 200, 300]
    })
    assert DataPreprocessor(df).validar_nulos_criticos() is True


def test_calidad_df():
    """
    Verifica que el resumen de calidad del DataFrame:
    - Excluya las columnas bandera
    - Devuelva correctamente el conteo de nulos por columna
    """
    df = pd.DataFrame({
        "a": [1, None],
        "a_nan": [0, 1]
    })
    result = DataPreprocessor(df).calidad_df()
    assert "a_nan" not in result.index
    assert result["a"] == 1