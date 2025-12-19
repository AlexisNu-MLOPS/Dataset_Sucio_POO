
---
## Enfoque Modular

El proyecto está diseñado de forma **modular**, separando claramente las
responsabilidades de cada etapa del pipeline:

### DataLoader (`data_loader.py`)
Encargado de la **carga de archivos** y su conversión a `pandas.DataFrame`.

Características:
- Implementa un patrón **Factory**
- Selecciona dinámicamente el cargador según la extensión del archivo
- Soporta los siguientes formatos:
  - CSV
  - Excel (`.xls`, `.xlsx`)
  - JSON
  - TXT

---

### DataPreprocessor (`data_preprocessor.py`)
Encargado de la **limpieza y estandarización de los datos**.

Funciones principales:
- Limpieza de nombres de columnas
- Conversión de valores vacíos a nulos
- Limpieza de montos monetarios
- Conversión de scores de texto a valores numéricos
- Eliminación de acentos
- Creación de columnas bandera (`_nan`)
- Validación de nulos críticos mediante umbrales
- Generación de un resumen de calidad del DataFrame

---

### Main (`main.py`)
Orquesta el flujo completo del pipeline:

1. Carga del archivo de entrada
2. Preprocesamiento del DataFrame
3. Validación de calidad de los datos
4. Retorno del DataFrame limpio y su estado de calidad

---

## Pruebas

El proyecto incluye **pruebas unitarias** y **pruebas de integración**,
implementadas con `pytest`.

### Pruebas Unitarias

- **`test_data_loader.py`**
  - Valida la carga correcta de archivos
  - Verifica el patrón Factory
  - Comprueba el manejo de formatos no soportados

- **`test_data_preprocessor.py`**
  - Valida la limpieza y estandarización de columnas
  - Verifica la conversión de valores nulos
  - Prueba la limpieza de montos y scores
  - Evalúa la validación de calidad del DataFrame

### Prueba de Integración

- **`test_main.py`**
  - Valida el funcionamiento end-to-end del pipeline
  - Comprueba que los módulos trabajen correctamente en conjunto
  - Verifica la correcta salida del DataFrame y su evaluación de calidad

---

## Ejecución del Proyecto

Desde la carpeta `POO`:

```bash
python src/main.py

## Autores

Proyecto desarrollado como práctica académica  
para el módulo de **Programación Orientada a Objetos**.

**Equipo:**
- Alexis Nuñez  
- Jose Benjamin Flores  
- Sonia Avilés Sacoto