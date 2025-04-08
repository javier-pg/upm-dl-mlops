#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
test_inference_api.py: Tests para la API de inferencia de precios de casas.

⚠️ Requiere que el servidor FastAPI esté corriendo en http://api:8000,
por ejemplo ejecutando: uvicorn src.inference_api:app --reload
"""

import requests
import time
import os

# Configuración de la URL base de la API
# Se puede configurar a través de variables de entorno (Docker) o por defecto localhost:8000
API_HOST = os.environ.get("API_HOST", "localhost")
API_PORT = int(os.environ.get("API_PORT", 8000))
API_URL = f"http://{API_HOST}:{API_PORT}"


def check_server():
    """Verifica que el servidor esté corriendo antes de ejecutar los tests, 
    intentando hasta 3 veces con 5s de espera entre cada intento.
    """
    max_retries = 3
    sleep_time = 5

    for intento in range(max_retries):
        try:
            r = requests.get(f"{API_URL}/docs", timeout=2)
            if r.status_code == 200:
                print("✅ El servidor está disponible.")
                return
            else:
                print(f"⚠️ El servidor respondió con status {r.status_code}, reintentando...")
        except Exception as e:
            print(f"⚠️ Error de conexión: {e}, reintentando...")

        # Si no ha salido con éxito, esperamos 5 segundos antes de reintentar
        if intento < max_retries - 1:
            time.sleep(sleep_time)

    # Si tras 3 intentos sigue sin responder correctamente, lanzamos excepción
    raise RuntimeError("🚨 El servidor no respondió correctamente tras 3 intentos.")

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
    response = requests.post(f"{API_URL}/predict", json=payload)
    print("Test predict_success:")
    print("Payload enviado:", payload)
    print("Respuesta de la API:", response.json())
    assert response.status_code == 200
    assert "predicted_price" in response.json()
    print("✅ Test predict_success PASSED.\n")

def test_predict_validation_error():
    """Test para una petición con error de validación (tipo incorrecto)."""
    payload = {
        "area": "invalid",
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
    response = requests.post(f"{API_URL}/predict", json=payload)
    print("Test predict_validation_error:")
    print("Payload enviado (error):", payload)
    print("Respuesta de la API:", response.json())
    assert response.status_code == 422
    print("✅ Test predict_validation_error PASSED.\n")

def test_predict_missing_field():
    """Test para una petición con campo faltante."""
    payload = {
        "area": 5000.0,
        "bedrooms": 4,
        "bathrooms": 3,
        "stories": 2,
        # Falta 'mainroad'
        "guestroom": "yes",
        "basement": "yes",
        "hotwaterheating": "yes",
        "airconditioning": "no",
        "parking": 2,
        "prefarea": "no",
        "furnishingstatus": "semi-furnished"
    }
    response = requests.post(f"{API_URL}/predict", json=payload)
    print("Test predict_missing_field:")
    print("Payload enviado (faltante):", payload)
    print("Respuesta de la API:", response.json())
    assert response.status_code == 422
    print("✅ Test predict_missing_field PASSED.\n")

def test_predict_multiple_requests():
    """Test para múltiples peticiones exitosas."""
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
        response = requests.post(f"{API_URL}/predict", json=payload)
        print(f"Payload {i}:", payload)
        print(f"Respuesta {i}:", response.json())
        assert response.status_code == 200
        assert "predicted_price" in response.json()
    print("✅ Test predict_multiple_requests PASSED.\n")

if __name__ == "__main__":
    print("🧪 Verificando que el servidor esté levantado...")
    check_server()
    print("✅ Servidor activo. Ejecutando tests...\n")
    test_predict_success()
    test_predict_validation_error()
    test_predict_missing_field()
    test_predict_multiple_requests()
    print("🎉 Todos los tests han sido ejecutados exitosamente.")
