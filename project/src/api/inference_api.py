#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
inference_api.py: API para servir predicciones del modelo de precios de casas utilizando FastAPI.
Carga los artefactos (modelo, encoders y scaler) y define un endpoint para recibir datos en JSON
y retornar la predicción.
"""

import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
import joblib
import os
import wandb

API_PORT = int(os.environ.get("API_PORT", 8000))


# Definir el esquema de datos para la petición de inferencia
class HouseData(BaseModel):
    area: float
    bedrooms: int
    bathrooms: int
    stories: int
    mainroad: str
    guestroom: str
    basement: str
    hotwaterheating: str
    airconditioning: str
    parking: int
    prefarea: str
    furnishingstatus: str

# Función para transformar variables categóricas usando los encoders guardados
def transform_new_data_ohe(df, columns, encoders):
    """
    Transforma las columnas categóricas de nuevos datos usando los encoders ya ajustados.
    Elimina las columnas originales y concatena las columnas dummy generadas.
    """
    df_transformed = df.copy()
    
    for col in columns:
        encoder = encoders[col]
        encoded_array = encoder.transform(df_transformed[[col]])
        col_names = encoder.get_feature_names_out([col])
        temp = pd.DataFrame(encoded_array, columns=col_names, index=df_transformed.index)
        df_transformed = pd.concat([df_transformed, temp], axis=1)
        df_transformed.drop(col, axis=1, inplace=True)
        
    return df_transformed




# Inicializar wandb (no inicia un run de tracking)
api = wandb.Api()

# Definir el nombre del artefacto y usuario/proyecto
artifact_path = os.getenv("WANDB_ARTIFACT_PATH", "javierpg-universidad-de-murcia/house-price-regression/house_price_model:v0")

# Descargar artefacto
artifact = api.artifact(artifact_path, type="model")
artifact_dir = artifact.download()

# Cargar artefactos guardados
model = joblib.load(os.path.join(artifact_dir, "model.pkl"))
encoders = joblib.load(os.path.join(artifact_dir, "encoders.pkl"))
scaler = joblib.load(os.path.join(artifact_dir, "scaler.pkl"))


# Columnas categóricas y numéricas (según el preprocesamiento)
categorical_columns = [
    'mainroad', 
    'guestroom', 
    'hotwaterheating', 
    'basement', 
    'airconditioning', 
    'prefarea', 
    'furnishingstatus'
]
numerical_columns = ['area', 'bedrooms', 'bathrooms', 'stories', 'parking']

# Inicializar la aplicación FastAPI
app = FastAPI(title="API de Inferencia - Precio de Casas")

@app.post("/predict")
async def predict_house(data: HouseData):
    """
    Endpoint para recibir datos de una casa y retornar la predicción del precio.
    """
    # Convertir el objeto recibido a DataFrame con model_dump
    input_data = pd.DataFrame([data.model_dump()])
    
    
    # Transformar variables categóricas usando los encoders guardados
    input_data = transform_new_data_ohe(input_data, categorical_columns, encoders)
    
    # Escalar las variables numéricas usando el scaler guardado
    input_data[numerical_columns] = scaler.transform(input_data[numerical_columns])
    
    # Realizar la predicción
    pred = model.predict(input_data)

    # Retornar la predicción
    return {"predicted_price": float(pred[0])}


# Ejecutar la API (ejecutar este script directamente)
if __name__ == "__main__":
    # Ejecutar la API en el puerto especificado
    uvicorn.run(app, host="0.0.0.0", port=API_PORT)
