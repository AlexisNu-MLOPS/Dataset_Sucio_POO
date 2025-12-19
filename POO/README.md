
---
## Enfoque Modular

El proyecto esta diseñado de forma **modular**, separando las
responsabilidades de cada etapa del pipeline:

### DataLoader (`data_loader.py`)
Encargado de la **carga de archivos** y su conversion a `pandas.DataFrame`.

Características:
- Implementa un patron **Factory**
- Selecciona el cargador segun la extension del archivo
- Soporta los siguientes formatos:
  - CSV
  - Excel (`.xls`, `.xlsx`)
  - JSON
  - TXT

---

### DataPreprocessor (`data_preprocessor.py`)
Encargado de la **limpieza y estandarizacion de los datos**.

Funciones principales:
- Limpieza de nombres de columnas
- Conversion de valores vacíos a nulos
- Limpieza de montos monetarios
- Conversion de scores de texto a valores numericos
- Eliminacion de acentos
- Creacion de columnas bandera (`_nan`)
- Validacion de nulos criticos mediante umbrales
- Generacion de un resumen de calidad del DataFrame

---

### Main (`main.py`)
Orquesta el flujo completo del pipeline:

1. Carga del archivo de entrada
2. Preprocesamiento del DataFrame
3. Validacion de calidad de los datos
4. Retorno del DataFrame limpio y su estado de calidad

---

## Pruebas

El proyecto incluye **pruebas unitarias** y **pruebas de integracion**,
implementadas con `pytest`.

### Pruebas Unitarias

- **`test_data_loader.py`**
  - Valida la carga correcta de archivos
  - Verifica el patrón Factory
  - Comprueba el manejo de formatos no soportados

- **`test_data_preprocessor.py`**
  - Valida la limpieza y estandarizacion de columnas
  - Verifica la conversion de valores nulos
  - Prueba la limpieza de montos y scores
  - Evalúa la validacion de calidad del DataFrame

### Prueba de Integración

- **`test_main.py`**
  - Valida el funcionamiento end-to-end del pipeline
  - Comprueba que los modulos trabajen en conjunto
  - Verifica la correcta salida del DataFrame y su evaluacion de calidad

---

## Ejecucion del Proyecto

Desde la carpeta `POO`:

```bash
python src/main.py

## Autores

Proyecto desarrollado como practica academica  
para el modulo de **Programacion Orientada a Objetos**.

**Equipo:**
- Alexis Nuñez  
- Jose Benjamin Flores  
- Sonia Avilés Sacoto