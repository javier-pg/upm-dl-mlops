# MLOps para la predicción de precios de casas

Este repositorio contiene un **pipeline** básico de MLOps para un modelo de regresión que estima el precio de casas. Se incluyen scripts para entrenamiento, testeo y despliegue de inferencia con **FastAPI**, así como una interfaz web.

---

##  Opción 1: Entrenamiento e inferencia con Docker

### 1. Entrenamiento del modelo

Desde la carpeta `src/api`, ejecuta el siguiente comando para construir la imagen de Docker y ejecutar el script de entrenamiento. Asegúrate de que el archivo `Housing.csv` esté en la carpeta `data/`.


1. **Construir la imagen de Docker**  
   Desde la carpeta `src/api`, ejecuta:
   ```bash
   docker build -t house-price-mlops:latest .
   ```
   * Esto creará una imagen de Docker con el nombre `house-price-mlops:latest`.

2. **Ejecutar el contenedor de entrenamiento**  
   ```bash
   docker run -it --rm -v .\artifacts\:/app/artifacts house-price-mlops:latest python train.py
   ```
   * Esto ejecutará el script de entrenamiento y guardará los artefactos en la carpeta `artifacts/`.
   * El contenedor se ejecutará y se detendrá automáticamente después de completar el entrenamiento.

3. **Verificar los artefactos**  
   Asegúrate de que los archivos `model.pkl`, `encoders.pkl` y `scaler.pkl` se encuentren en la carpeta `artifacts/`.
    
    ```bash 
    ls artifacts
    ```

### 2. Despliegue de la API de inferencia

Seguimos en la carpeta `src/api`:

4. **Ejecutar el script de la API desde project**  
   ```bash
   docker run -it --rm -v .\artifacts\:/app/artifacts -p 8000:8000 house-price-mlops:latest
   ```
    * La API estará disponible en `http://localhost:8000`.
    * El contenedor se ejecutará y se mantendrá activo para recibir peticiones.
    * Importante que el contenedor de entrenamiento se haya ejecutado previamente para que los artefactos estén disponibles (a través del volumen montado).


### 3. Test de la API

Nos movemos a la carpeta `src/test`:

5. **Ejecutar los tests de la API**  
   ```bash
   python3 test_inference_api.py
   ```
    * Esto ejecutará los tests de la API de inferencia.
    * Asegúrate de que el contenedor de la API esté en ejecución antes de ejecutar los tests.
   
    
### 4. Despliegue de la aplicación web (frontend)

Desde la carpeta `src/frontend`:

6. **Levantar aplicación web (frontend) para interactuar con la API de inferencia**  
   ```bash
   docker build -t web-house-price-mlops:latest .
   docker run -it --rm -p 8080:8080 web-house-price-mlops:latest
   ```
    * La aplicación estará disponible en `http://localhost:8080`.
    * El contenedor se ejecutará y se mantendrá activo para recibir peticiones.
    * Acceder a la aplicación web en `http://localhost:8080` para interactuar con la API de inferencia.


##  Opción 2: Despliegue conjunto con docker-compose 
Importante tener artifacts previos habiendo entrenado el modelo con los pasos 1 y 2 anteriores.

**Entrenamiento del modelo (si no tienes los artefactos ya)**  
Desde la carpeta `src/api`, ejecuta:

```bash
docker build -t house-price-mlops:latest .
docker run -it --rm -v .\artifacts\:/app/artifacts house-price-mlops:latest python train.py
```
* Esto ejecutará el script de entrenamiento y guardará los artefactos en la carpeta `artifacts/`.
* El contenedor se ejecutará y se detendrá automáticamente después de completar el entrenamiento.

**Lanzar docker-compose**  
   Desde la carpeta `src`, ejecuta:
   ```bash
   docker-compose up
   ```
   * Añade  --build al comando anterior si has realizado cambios en el Dockerfile o en los scripts de la API o frontend.
   * Esto levantará los servicios de la API de inferencia y la aplicación web (frontend).
   * La API estará disponible en `http://localhost:8000` y la aplicación web en `http://localhost:8080`.
   * El contenedor de la API se ejecutará y se mantendrá activo para recibir peticiones.


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

Puedes instalar los requerimientos de cada servicio desde la carpeta correspondiente:
> ```bash
> pip install -r requirements.txt
> ```

Recomendado utilizar un entorno virtual:
> ```bash
> python -m venv venv
> source venv/bin/activate
> ```

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
   python3 src/api/inference_api.py
   ```
    * La API estará disponible en `http://localhost:8000`.

2. **Test de la API**
    ```bash
    python3 src/test/test_inference_api.py
    ```
    * Se ejecutarán tests de la API de inferencia.

3. **Usar mediante petición POST**
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

4. Levantar aplicación web (frontend) para interactuar con la API de inferencia:
   ```bash
   python3 src/frontend/web_app.py
   ```
   * La aplicación estará disponible en `http://localhost:8080`.


## Referencias
* https://www.kaggle.com/datasets/yasserh/housing-prices-dataset/data

* https://www.kaggle.com/code/sahityasetu/house-pricing-regression