import pandas as pd
from src.data_loader import DataLoader


def test_load_csv(tmp_path):
    # Crear archivo temporal
    file = tmp_path / "data.csv"
    file.write_text("a,b\n1,2")

    loader = DataLoader()
    df = loader.load_csv(file)

    assert isinstance(df, pd.DataFrame)
    assert df.shape == (1, 2)
