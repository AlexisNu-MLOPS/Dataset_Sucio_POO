import pandas as pd
from pathlib import Path

# -------------------------------
# Excepcion de calidad de datos
# -------------------------------

class ExcepcionCalidad(Exception):
    """Excepcion para problemas criticos en la calidad de los datos."""
    pass

# -------------------------------
# Loaders
# -------------------------------

class DataLoader:
    """
    Clase base para cargar datos desde un archivo.
    
    Parametros:
    -----------
    filepath : str o Path
        Ruta al archivo que se desea cargar.
    """
    def __init__(self, filepath):
        self.filepath = Path(filepath)

    def read_file(self, **kwargs):
        """
        Metodo base que debe ser sobrescrito por cada loader especifico.
        """
        raise NotImplementedError("Este metodo no esta implementado para el formato de archivo que se compartio")


class CargaCSV(DataLoader):
    """
    Carga archivos CSV.
    """
    def read_file(self, **kwargs):
        return pd.read_csv(self.filepath, **kwargs)


class CargaExcel(DataLoader):
    """
    Carga archivos Excel (.xls y .xlsx).
    """
    def read_file(self, **kwargs):
        return pd.read_excel(self.filepath, **kwargs)


class CargaJSON(DataLoader):
    """
    Carga archivos JSON.
    """
    def read_file(self, **kwargs):
        return pd.read_json(self.filepath, **kwargs)


# Asociacion entre extension y Loader
LOADER_FACTORY = {
    ".csv": CargaCSV,
    ".xlsx": CargaExcel,
    ".xls": CargaExcel,
    ".json": CargaJSON,
    ".txt": CargaCSV
}