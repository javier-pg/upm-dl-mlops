#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
train.py: Script para entrenar el modelo de regresión de precios de casas.
Realiza el preprocesamiento (OneHotEncoding para variables categóricas y escalado
para variables numéricas), entrena el modelo y guarda los artefactos en la carpeta artifacts.
"""

import os
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.preprocessing import MinMaxScaler, OneHotEncoder
import joblib

# Crear carpeta para guardar artefactos si no existe
os.makedirs("artifacts", exist_ok=True)

# Función para ajustar y transformar variables categóricas
def fit_transform_ohe(df, columns, drop='first'):
    """
    Ajusta un OneHotEncoder para cada columna en 'columns' y transforma la columna.
    Elimina la columna original y retorna el DataFrame transformado junto con
    un diccionario que contiene los encoders ajustados.
    """
    encoders = {}
    df_transformed = df.copy()
    
    for col in columns:
        encoder = OneHotEncoder(drop=drop, sparse_output=False, handle_unknown='ignore')
        # Ajusta y transforma la columna (se espera un array 2D)
        encoded_array = encoder.fit_transform(df_transformed[[col]])
        # Obtiene nombres de columnas dummy generadas
        col_names = encoder.get_feature_names_out([col])
        temp = pd.DataFrame(encoded_array, columns=col_names, index=df_transformed.index)
        # Concatena las columnas dummy y elimina la original
        df_transformed = pd.concat([df_transformed, temp], axis=1)
        df_transformed.drop(col, axis=1, inplace=True)
        # Guarda el encoder ajustado
        encoders[col] = encoder
        
    return df_transformed, encoders

# Cargar dataset
df = pd.read_csv("data/Housing.csv")

# Definir columnas categóricas a transformar
categorical_columns = [
    'mainroad', 
    'guestroom', 
    'hotwaterheating', 
    'basement', 
    'airconditioning', 
    'prefarea', 
    'furnishingstatus'
]

# Ajustar y transformar las variables categóricas
df, encoders = fit_transform_ohe(df, categorical_columns)

# Escalar variables numéricas con MinMaxScaler
numerical_columns = ['area', 'bedrooms', 'bathrooms', 'stories', 'parking']
scaler = MinMaxScaler()
df[numerical_columns] = scaler.fit_transform(df[numerical_columns])

# Separar características (X) y variable objetivo (y)
X = df.drop("price", axis=1)
y = df["price"]

# División de datos en entrenamiento y test
X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=0.75, random_state=42)

# Entrenar el modelo de regresión lineal
model = LinearRegression()
model.fit(X_train, y_train)

# Evaluar el modelo en el conjunto de test
preds = model.predict(X_test)
mae = mean_absolute_error(y_test, preds)
mse = mean_squared_error(y_test, preds)
rmse = np.sqrt(mse)
r2 = r2_score(y_test, preds)

print("Métricas de evaluación:")
print("MAE:", mae)
print("MSE:", mse)
print("RMSE:", rmse)
print("R²:", r2)

# Guardar modelo, encoders y scaler en la carpeta artifacts
joblib.dump(model, "artifacts/model.pkl")
joblib.dump(encoders, "artifacts/encoders.pkl")
joblib.dump(scaler, "artifacts/scaler.pkl")
print("Artefactos guardados en la carpeta artifacts.")