"""
Prueba de integracion para el modulo main.

Este archivo valida el funcionamiento end-to-end del pipeline completo,
asegurando que los distintos modulos trabajen en conjunto.

Se prueba el flujo completo:
1. Carga del archivo CSV
2. Limpieza y estandarizacion de columnas
3. Conversion de tipos de datos
4. Generacion de columnas bandera para valores nulos
5. Evaluacion de la calidad del DataFrame

A diferencia de las pruebas unitarias, aqui se valida la integracion
entre DataLoader, DataPreprocessor y la función principal del pipeline.
"""
import pandas as pd
import pytest
from src.main import carga_procesa

#Se genera un csv para la prueba del correcto funcionamiento del main.py
@pytest.fixture
def prueba_csv(tmp_path):
    """
    Fixture genera un archivo CSV temporal con datos simulados
    para probar el correcto funcionamiento del pipeline completo.

    El archivo contiene columnas con:
    - Nombres sucios
    - Valores monetarios con simbolos
    - Scores en texto
    - Valores nulos y vacios

    Retorna la ruta al archivo CSV generado.
    """
    df = pd.DataFrame({
        "Transaction ID #": [1, 2, 3],
        "Fech@_Registro": ["2025-01-01", "2025-01-02", "2025-01-03"],
        "Nombre Cliente (RAW)": ["Cliente1", "Cliente2", "Cliente3"],
        "Monto $$": ["$1000", "$2000", "$3000"],
        "Categoría_Producto/Tipo": ["A", "B", "C"],
        "Score (1-5)": ["Uno", "Dos", "Tres"],
        "Notes & Comments": ["", "Comentario", None],
        "¿Es_Fraude?": [0, 1, 0]
    })
    file_path = tmp_path / "archivo_prueba.csv"
    df.to_csv(file_path, index=False)
    return file_path

def test_carga_procesa_csv(prueba_csv):
    """
    Verifica que la funcion principal del pipeline (carga_procesa)
    procese un archivo CSV y retorne:

    - Un DataFrame limpio y estandarizado
    - Un resumen de calidad del DataFrame

    Se validan:
    - Existencia de columnas criticas
    - Creacion de columnas bandera (_nan)
    - Conversion correcta de tipos de datos
    - Tipo de retorno del resumen de calidad
    """
    df, quality = carga_procesa(prueba_csv, sep=",", encoding="utf-8")

    # Columnas criticas que deben existir tras el procesamiento
    for col in ["monto", "score", "fraude"]:
        assert col in df.columns

    # Columnas bandera '_nan' que indican valores nulos
    for col in ["monto", "score", "fraude"]:
        assert f"{col}_nan" in df.columns

    # Verificar tipos de datos de columnas clave sean numéricas
    assert pd.api.types.is_numeric_dtype(df["monto"])
    assert pd.api.types.is_numeric_dtype(df["score"])
    assert pd.api.types.is_numeric_dtype(df["fraude"])

    # Calidad del DataFrame (nulos) debe devolver una serie de Pandas
    assert isinstance(quality, pd.Series)
