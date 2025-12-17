from pathlib import Path

# Imports relativos al paquete src
from src.data_loader import LOADER_FACTORY, ExcepcionCalidad
from src.data_preprocessor import DataPreprocessor

# -------------------------------
# Funcion principal
# -------------------------------

def carga_procesa(filepath, **kwargs):
    """
    Carga un archivo y aplica procesamiento estandar:
    - Limpieza de columnas
    - Conversion de vacios a NaN
    - Limpieza de montos, scores y fechas
    - Eliminacion de acentos
    - Creacion de columnas bandera de nulos
    """
    filepath = Path(filepath)
    ext = filepath.suffix.lower()
    if ext not in LOADER_FACTORY:
        raise ValueError(f"Formato no soportado: {ext}")

    # Carga del archivo usando el loader adecuado
    loader = LOADER_FACTORY[ext](filepath)
    df = loader.read_file(**kwargs)
    print(DataPreprocessor)
    print(type(DataPreprocessor))

    # Procesamiento de datos
    processor = DataPreprocessor(df)
    processor.clean_columns()
    processor.vacios_a_nulos()
    processor.limpieza_monto()
    processor.limpieza_num_cliente()
    processor.limpieza_score()
    processor.limpieza_fecha_registro()
    processor.eliminar_acentos()
    processor.ban_columnas_nulas()

    # Validacion critica de calidad de datos
    processor.validar_nulos_criticos(
        target_col="fraude",
        monto_col="monto",
        umbral=0.10
    )

    return processor.df, processor.calidad_df()


# -------------------------------
# Informacion global del DF
# -------------------------------

if __name__ == "__main__":
    ruta_archivo = input("Ingrese la ruta del archivo: ").strip()
    try:
        df, quality = carga_procesa(ruta_archivo, sep=",", encoding="utf-8")

        # Imprimir calidad de datos
        print("\nCalidad de datos (valores nulos por columna):")
        print(quality)

        # Muestra el DF tabulado
        print("\nVista del DataFrame final (primeras 5 filas):")
        print(df.head(5).to_markdown(index=False))

    except ExcepcionCalidad:
        print("\nProceso detenido por falla critica de calidad de datos.")
    except Exception as e:
        print(f"\nError: {e}")