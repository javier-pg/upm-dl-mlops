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


import time
import requests

API_URL = "http://localhost:8000"  # Asegurate de definir esto fuera si no está

def check_server(api_url=API_URL, retries=3, delay=5, timeout=2):
    """
    Verifica que el servidor esté disponible antes de ejecutar los tests.

    Intenta conectarse a la ruta /docs del servidor especificado. Reintenta hasta
    'retries' veces con una espera de 'delay' segundos entre intentos.

    Args:
        api_url (str): URL base de la API a verificar.
        retries (int): Número máximo de intentos.
        delay (int): Segundos de espera entre intentos.
        timeout (int): Tiempo máximo de espera por intento de conexión (segundos).

    Raises:
        RuntimeError: Si el servidor no responde correctamente después de todos los intentos.
    """
    print(f"🔍 Verificando disponibilidad del servidor en {api_url}...")

    for attempt in range(1, retries + 1):
        try:
            response = requests.get(f"{api_url}/docs", timeout=timeout)
            if response.status_code == 200:
                print("✅ El servidor está disponible.")
                return
            else:
                print(f"⚠️ Respuesta inesperada (status {response.status_code}), intento {attempt}/{retries}")
        except requests.RequestException as err:
            print(f"⚠️ Error al conectar: {err}, intento {attempt}/{retries}")

        if attempt < retries:
            time.sleep(delay)

    raise RuntimeError(f"🚨 El servidor no respondió correctamente tras {retries} intentos.")


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
