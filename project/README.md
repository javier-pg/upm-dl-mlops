# MLOps para la predicción de precios de casas

Este repositorio contiene un **pipeline** básico de MLOps para un modelo de regresión que estima el precio de casas. Se incluyen scripts para entrenamiento, testeo y despliegue de inferencia con **FastAPI**. A continuación, se describe la estructura principal y las instrucciones de uso.

---

## Estructura de Directorios
```project
├── artifacts
│   ├── encoders.pkl      # Encoders de variables categóricas
│   ├── model.pkl         # Modelo entrenado (LinearRegression)
│   └── scaler.pkl        # Scaler para variables numéricas
├── data
│   └── Housing.csv       # Dataset de ejemplo
├── notebooks
│   └── modeling.ipynb    # Notebook con análisis y experimentos
├── src
│   ├── inference_api.py  # Script FastAPI para servir inferencias
│   └── train.py          # Script para entrenar y guardar el modelo
└── test
    └── test_inference_api.py  # Tests de la API de inferencia
```

## Requisitos

- **Python 3.8+**
- Librerías principales:
  - `pandas`
  - `numpy`
  - `scikit-learn`
  - `fastapi`
  - `uvicorn`
  - `joblib`

Puedes instalar los requerimientos con:
> ```bash
> pip install -r requirements.txt
> ```

Recomendado utilizar un entorno virtual:
> ```bash
> python -m venv venv
> source venv/bin/activate
> ```


##  Opción 1: Entrenamiento e inferencia con Docker (RECOMENDADO)






##  Opción 2: Ejecución local (sin Docker)

### Entrenamiento del modelo

1. **Ubicar los datos**  
   Asegúrate de que el archivo `Housing.csv` se encuentre en la carpeta `data/`.
   
2. **Ejecutar el script de entrenamiento desde project**  
   ```bash
   python3 src/train.py
   ```
    * Se leerá el dataset, se preprocesarán las variables categóricas y numéricas, y se entrenará un modelo de regresión lineal.
    * Los artefactos resultantes (model.pkl, encoders.pkl y scaler.pkl) se actualizarán/guardarán en la carpeta `artifacts/`.

### Despliegue de la API de inferencia

1. **Ejecutar el script de la API desde project**  
   ```bash
   python3 src/inference_api.py
   ```
    * La API estará disponible en `http://localhost:8000`.

2. **Test de la API**
    ```bash
    python3 test/test_inference_api.py
    ```
    * Se ejecutarán tests de la API de inferencia.

2. **Usar mediante petición POST**
    ```bash
    curl -X POST \
     -H "Content-Type: application/json" \
     -d '{
           "area": 5000,
           "bedrooms": 4,
           "bathrooms": 3,
           "stories": 2,
           "mainroad": "yes",
           "guestroom": "yes",
           "basement": "yes",
           "hotwaterheating": "yes",
           "airconditioning": "no",
           "parking": 2,
           "prefarea": "no",
           "furnishingstatus": "semi-furnished"
         }' \
     http://localhost:8000/predict
    ```

## Referencias
* https://www.kaggle.com/datasets/yasserh/housing-prices-dataset/data

* https://www.kaggle.com/code/sahityasetu/house-pricing-regression