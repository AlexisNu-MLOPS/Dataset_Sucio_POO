import pandas as pd
from src.preprocessor import DataPreprocessor


def test_full_pipeline_runs_end_to_end():
    """
    Prueba de integración del pipeline de preprocesamiento de datos.

    Este test valida que el flujo completo de procesamiento funcione
    correctamente de inicio a fin, utilizando un DataFrame de ejemplo.
    Se verifica que:
    - Las columnas se limpien correctamente.
    - Se generen las columnas bandera de valores nulos.
    - El análisis de calidad retorne un valor booleano.
    """

    # Crear un DataFrame de prueba simulando datos reales
    df = pd.DataFrame({
        "Monto $$": [10, None, 5],
        "Es Fraude?": [1, 0, None],
        "Score Cliente": [800, None, 650],
    })

    # Inicializar el preprocesador de datos
    prep = DataPreprocessor()

    # Aplicar limpieza de nombres de columnas
    df = prep.clean_columns(df)

    # Generar columnas bandera para identificar valores nulos
    df = prep.add_null_flags(df)

    # Verificar que las columnas bandera fueron creadas correctamente
    assert "monto_nan" in df.columns
    assert "es_fraude_nan" in df.columns

    # Ejecutar el análisis de calidad del DataFrame
    decision = prep.analyze_quality(df, umbral=0.50)

    # Verificar que el resultado del análisis sea un valor booleano
    assert isinstance(decision, bool)
