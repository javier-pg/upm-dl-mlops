from flask import Flask, render_template, request
import requests
import os

app = Flask(__name__)

# Configuración de la URL base de la API
# Se puede configurar a través de variables de entorno (Docker) o por defecto localhost:8000 (se ejecuta sin Docker)
API_HOST = os.environ.get("API_HOST", "localhost")
API_PORT = os.environ.get("API_PORT", "8000")
API_URL = f"http://{API_HOST}:{API_PORT}/predict"

# Puerto de la aplicación web
WEB_APP_PORT = os.environ.get("WEB_APP_PORT", "8080")


@app.route("/", methods=["GET"])
def index():
    # Renderiza un formulario HTML
    return render_template("index.html")

@app.route("/predict_price", methods=["POST"])
def predict_price():
    # Recogemos los datos del formulario
    area = request.form.get("area")
    bedrooms = request.form.get("bedrooms")
    bathrooms = request.form.get("bathrooms")
    stories = request.form.get("stories")
    mainroad = request.form.get("mainroad")
    guestroom = request.form.get("guestroom")
    basement = request.form.get("basement")
    hotwaterheating = request.form.get("hotwaterheating")
    airconditioning = request.form.get("airconditioning")
    parking = request.form.get("parking")
    prefarea = request.form.get("prefarea")
    furnishingstatus = request.form.get("furnishingstatus")

    # Construimos la carga en JSON para la API
    payload = {
        "area": float(area),
        "bedrooms": int(bedrooms),
        "bathrooms": int(bathrooms),
        "stories": int(stories),
        "mainroad": mainroad,
        "guestroom": guestroom,
        "basement": basement,
        "hotwaterheating": hotwaterheating,
        "airconditioning": airconditioning,
        "parking": int(parking),
        "prefarea": prefarea,
        "furnishingstatus": furnishingstatus
    }

    # Hacemos la petición POST a la API
    response = requests.post(API_URL, json=payload)
    
    if response.status_code == 200:
        data = response.json()
        predicted_price = data["predicted_price"]
        return f"El precio estimado de la casa es: {predicted_price:.2f}"
    else:
        return "Error en la API. No se pudo obtener la predicción."

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=WEB_APP_PORT, debug=True)
