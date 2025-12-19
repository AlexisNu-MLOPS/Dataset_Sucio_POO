import pandas as pd
import pytest

from src.data_loader import (
    DataLoader,
    CargaCSV,
    CargaExcel,
    CargaJSON,
    EXTENSION_COMPATIBLE
)

def test_dataloader_read_file_lanza_error():
    loader = DataLoader("archivo.fake")
    with pytest.raises(NotImplementedError):
        loader.read_file()


def test_carga_csv(tmp_path):
    archivo = tmp_path / "dataset_sucio_ventas.csv"
    archivo.write_text("a,b\n1,2\n3,4")

    loader = CargaCSV(archivo)
    df = loader.read_file()

    assert df.shape == (2, 2)

def test_loader_factory():
    assert EXTENSION_COMPATIBLE[".csv"] is CargaCSV
    assert EXTENSION_COMPATIBLE[".xlsx"] is CargaExcel
    assert EXTENSION_COMPATIBLE[".json"] is CargaJSON