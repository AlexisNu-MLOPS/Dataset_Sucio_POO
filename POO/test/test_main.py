import pandas as pd
import pytest
from src.main import carga_procesa

@pytest.fixture
def prueba_csv(tmp_path):
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
    df, quality = carga_procesa(prueba_csv, sep=",", encoding="utf-8")

    # Columnas críticas que deben existir
    for col in ["monto", "score", "fraude"]:
        assert col in df.columns

    # Columnas bandera '_nan' deben existir
    for col in ["monto", "score", "fraude"]:
        assert f"{col}_nan" in df.columns

    # Verificar tipos de datos básicos
    assert pd.api.types.is_numeric_dtype(df["monto"])
    assert pd.api.types.is_numeric_dtype(df["score"])
    assert pd.api.types.is_numeric_dtype(df["fraude"])

    # Calidad del DataFrame (nulos) debe devolver un Series
    assert isinstance(quality, pd.Series)