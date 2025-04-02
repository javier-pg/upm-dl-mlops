#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
test_inference_api.py: Script de tests para la API de inferencia de precios de casas.
Utiliza TestClient de FastAPI para enviar peticiones y validar respuestas, 
incluyendo casos de éxito, errores de validación y peticiones con campos faltantes.
"""
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from fastapi.testclient import TestClient
from src.inference_api import app  # Asegúrate de que en inference_api.py la variable 'app' es la instancia FastAPI

# Crear el cliente de test pasándole la aplicación FastAPI
client = TestClient(app)

def test_predict_success():
    """Test para una petición exitosa de predicción."""
    payload = {
        "area": 5000.0,
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
    }
    response = client.post("/predict", json=payload)
    print("Test predict_success:")
    print("Payload enviado:", payload)
    print("Respuesta de la API:", response.json())
    assert response.status_code == 200, f"Se esperaba status 200, se obtuvo {response.status_code}"
    data = response.json()
    assert "predicted_price" in data, "La respuesta debe contener 'predicted_price'"
    print("Test predict_success PASSED.\n")

def test_predict_validation_error():
    """Test para una petición con error de validación (tipo de dato incorrecto)."""
    payload = {
        "area": "invalid",  # Debería ser float, no string
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
    }
    response = client.post("/predict", json=payload)
    print("Test predict_validation_error:")
    print("Payload enviado (error):", payload)
    print("Respuesta de la API:", response.json())
    assert response.status_code == 422, f"Se esperaba status 422, se obtuvo {response.status_code}"
    print("Test predict_validation_error PASSED.\n")

def test_predict_missing_field():
    """Test para una petición con campo faltante."""
    payload = {
        "area": 5000.0,
        "bedrooms": 4,
        "bathrooms": 3,
        "stories": 2,
        # Falta el campo 'mainroad'
        "guestroom": "yes",
        "basement": "yes",
        "hotwaterheating": "yes",
        "airconditioning": "no",
        "parking": 2,
        "prefarea": "no",
        "furnishingstatus": "semi-furnished"
    }
    response = client.post("/predict", json=payload)
    print("Test predict_missing_field:")
    print("Payload enviado (con campo faltante):", payload)
    print("Respuesta de la API:", response.json())
    assert response.status_code == 422, f"Se esperaba status 422, se obtuvo {response.status_code}"
    print("Test predict_missing_field PASSED.\n")

def test_predict_multiple_requests():
    """Test para enviar múltiples peticiones y verificar que todas responden correctamente."""
    payloads = [
        {
            "area": 4000.0,
            "bedrooms": 3,
            "bathrooms": 2,
            "stories": 1,
            "mainroad": "no",
            "guestroom": "no",
            "basement": "no",
            "hotwaterheating": "yes",
            "airconditioning": "yes",
            "parking": 1,
            "prefarea": "yes",
            "furnishingstatus": "furnished"
        },
        {
            "area": 5500.0,
            "bedrooms": 5,
            "bathrooms": 4,
            "stories": 3,
            "mainroad": "yes",
            "guestroom": "yes",
            "basement": "yes",
            "hotwaterheating": "no",
            "airconditioning": "no",
            "parking": 2,
            "prefarea": "no",
            "furnishingstatus": "semi-furnished"
        }
    ]
    
    print("Test predict_multiple_requests:")
    for i, payload in enumerate(payloads, start=1):
        response = client.post("/predict", json=payload)
        print(f"Payload {i} enviado:", payload)
        print(f"Respuesta de la API para payload {i}:", response.json())
        assert response.status_code == 200, f"Payload {i}: Se esperaba status 200, se obtuvo {response.status_code}"
        data = response.json()
        assert "predicted_price" in data, f"Payload {i}: La respuesta debe contener 'predicted_price'"
    print("Test predict_multiple_requests PASSED.\n")

if __name__ == "__main__":
    print("Ejecutando tests para inference_api...\n")
    test_predict_success()
    test_predict_validation_error()
    test_predict_missing_field()
    test_predict_multiple_requests()
    print("Todos los tests han sido ejecutados exitosamente.")