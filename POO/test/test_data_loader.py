"""
Pruebas unitarias para el módulo DataLoader.

Este archivo valida el comportamiento del sistema de carga de datos,
asegurando que:

- Se lance un error cuando se intenta cargar un archivo
  sin una implementación concreta.
- Los archivos CSV se carguen correctamente en un DataFrame.
- El mecanismo de fábrica (factory) seleccione la clase correcta
  según la extensión del archivo.

Estas pruebas garantizan que la entrada de datos al pipeline
sea consistente y controlada.
"""
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
    """
    Verifica que la clase base DataLoader lance un error
    cuando se intenta usar el método read_file sin
    una implementación concreta.

    Esto asegura que DataLoader actúe como clase abstracta
    y obligue a usar una subclase específica.
    """
    loader = DataLoader("archivo.fake")
    with pytest.raises(NotImplementedError):
        loader.read_file()


def test_carga_csv(tmp_path):
    """
    Verifica que un archivo CSV válido se cargue correctamente
    en un DataFrame de pandas.

    Se crea un archivo CSV temporal y se comprueba
    que el DataFrame resultante tenga la forma esperada.
    """
    archivo = tmp_path / "dataset_sucio_ventas.csv"
    archivo.write_text("a,b\n1,2\n3,4")

    loader = CargaCSV(archivo)
    df = loader.read_file()

    assert df.shape == (2, 2)

def test_loader_factory():
    """
    Verifica que el diccionario EXTENSION_COMPATIBLE
    asocie correctamente cada extensión de archivo
    con su clase de carga correspondiente.

    Esto valida el patrón Factory implementado
    para seleccionar dinámicamente el cargador adecuado.
    """
    assert EXTENSION_COMPATIBLE[".csv"] is CargaCSV
    assert EXTENSION_COMPATIBLE[".xlsx"] is CargaExcel
    assert EXTENSION_COMPATIBLE[".json"] is CargaJSON