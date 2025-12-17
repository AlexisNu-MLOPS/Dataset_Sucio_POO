import pandas as pd
from src.preprocessor import DataPreprocessor


def test_clean_columns_headers():
    """
    Prueba unitaria del método clean_columns de DataPreprocessor.

    Verifica que los nombres de las columnas:
    - Se normalicen correctamente.
    - Se conviertan a minúsculas.
    - No contengan espacios ni caracteres especiales.
    """

    # Crear DataFrame de prueba con nombres de columnas desordenados
    df = pd.DataFrame({"Monto $$": [10], "Nombre Cliente": ["Ana"]})

    # Inicializar el preprocesador
    prep = DataPreprocessor()

    # Aplicar limpieza de columnas
    df_clean = prep.clean_columns(df)

    # Verificar que las columnas fueron renombradas correctamente
    assert "monto" in df_clean.columns
    assert "nombre_cliente" in df_clean.columns

    # Verificar reglas generales de normalización
    for col in df_clean.columns:
        assert col == col.lower()
        assert " " not in col


def test_add_null_flags_creates_flag_column():
    """
    Prueba unitaria del método add_null_flags de DataPreprocessor.

    Verifica que:
    - Se cree una columna bandera para identificar valores nulos.
    - Los valores de la bandera sean correctos (0 = no nulo, 1 = nulo).
    """

    # Crear DataFrame con valores nulos
    df = pd.DataFrame({"monto": [1, None]})

    # Inicializar el preprocesador
    prep = DataPreprocessor()

    # Generar columnas bandera de valores nulos
    df_flag = prep.add_null_flags(df)

    # Verificar la existencia de la columna bandera
    assert "monto_nan" in df_flag.columns

    # Verificar valores de la bandera
    assert df_flag.loc[0, "monto_nan"] == 0
    assert df_flag.loc[1, "monto_nan"] == 1


def test_quality_gate_fails_if_critical_nulls_exceed_threshold():
    """
    Prueba unitaria del método analyze_quality de DataPreprocessor.

    Verifica que el control de calidad:
    - Retorne False cuando el porcentaje de valores nulos
      excede el umbral permitido.
    """

    # Crear DataFrame con alto porcentaje de valores nulos
    df = pd.DataFrame({
        "monto": [None, None, 10, None, None],
        "es_fraude": [1, None, 0, None, None],
    })

    # Inicializar el preprocesador
    prep = DataPreprocessor()

    # Ejecutar análisis de calidad con umbral bajo
    ok = prep.analyze_quality(df, umbral=0.30)

    # Verificar que el DataFrame no cumpla el criterio de calidad
    assert ok is False
