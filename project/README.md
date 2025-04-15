# MLOps para la predicción de precios de casas

Este repositorio contiene un **pipeline** básico de MLOps para un modelo de regresión que estima el precio de casas. Se incluyen scripts para entrenamiento, testeo y despliegue de inferencia con **FastAPI**, así como una interfaz web.

---

##  Opción 1: Entrenamiento e inferencia con Docker usando W&B

Ahora los artefactos del modelo se almacenan y leen desde **Weights & Biases (W&B)**. Ya **no es necesario montar volúmenes locales**.

### 1. Entrenamiento del modelo

Desde la carpeta `project/src/api`, ejecuta:

```bash
docker build -t house-price-mlops:latest .
```

Luego ejecuta el contenedor de entrenamiento con las variables necesarias:

```bash
docker run -it --rm \
  -e WANDB_API_KEY=<tu_api_key> \
  -e WANDB_ARTIFACT_PATH=<usuario/proyecto/modelo:version> \
  house-price-mlops:latest \
  python train.py
```

> 🎯 Esto entrenará el modelo y subirá los artefactos (`model.pkl`, `encoders.pkl`, `scaler.pkl`) a W&B automáticamente.

---

### 2. Despliegue de la API de inferencia

Desde `project/src/api`, ejecuta:

```bash
docker run -it --rm \
  -e WANDB_API_KEY=<tu_api_key> \
  -e WANDB_ARTIFACT_PATH=<usuario/proyecto/modelo:version> \
  -p 8000:8000 \
  house-price-mlops:latest
```

> 📦 La API se levantará en `http://localhost:8000` y descargará automáticamente los artefactos desde W&B.

---

### 3. Test de la API

Desde la carpeta `project/src/test`:

```bash
python3 test_inference_api.py
```

> Asegúrate de que el contenedor de la API esté corriendo antes de ejecutar los tests.

---

### 4. Despliegue de la aplicación web (frontend)

Desde `project/src/frontend`:

```bash
docker build -t web-house-price-mlops:latest .
docker run -it --rm -p 8080:8080 web-house-price-mlops:latest
```

> La aplicación estará disponible en `http://localhost:8080` para interactuar con la API.

---

##  Opción 2: Despliegue conjunto con docker-compose

**Importante:** Se asume que los artefactos ya están entrenados y subidos a W&B.

Desde la carpeta `project/src`, ejecuta:

```bash
WANDB_API_KEY=<tu_api_key> WANDB_ARTIFACT_PATH=<usuario/proyecto/modelo:version> docker-compose up
```

> Añade `--build` si hiciste cambios en los Dockerfiles o en los scripts.

---

##  Opción 3: Ejecución local (sin Docker)

### Requisitos

- **Python 3.8+**
- Librerías principales:
  - `pandas`
  - `numpy`
  - `scikit-learn`
  - `fastapi`
  - `uvicorn`
  - `joblib`
  - `wandb`

Puedes instalar los requerimientos desde la carpeta correspondiente:
```bash
pip install -r requirements.txt
```

Recomendado utilizar un entorno virtual:
```bash
python -m venv venv
source venv/bin/activate
```

---

### Entrenamiento del modelo

Desde la raíz del proyecto:

```bash
export WANDB_API_KEY=<tu_api_key>
export WANDB_ARTIFACT_PATH=mlops-house-price/artifacts
python3 project/src/api/train.py
```

---

### Despliegue de la API

```bash
export WANDB_API_KEY=<tu_api_key>
export WANDB_ARTIFACT_PATH=mlops-house-price/artifacts
python3 project/src/api/inference_api.py
```

> Acceder en `http://localhost:8000`

---

### Test de la API

```bash
python3 project/src/test/test_inference_api.py
```

---

### Despliegue del frontend

```bash
python3 project/src/frontend/web_app.py
```

> Acceder en `http://localhost:8080`

---

## 🌐 Variables de entorno obligatorias

| Variable             | Descripción                                           |
|----------------------|-------------------------------------------------------|
| `WANDB_API_KEY`      | Tu clave personal de acceso a Weights & Biases        |
| `WANDB_ARTIFACT_PATH`| Ruta completa al artefacto en W&B (ej. `mlops-house-price/artifacts`) |

---

## Referencias

- https://www.kaggle.com/datasets/yasserh/housing-prices-dataset/data
- https://www.kaggle.com/code/sahityasetu/house-pricing-regression