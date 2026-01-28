from flask import Flask, render_template, jsonify, request
from core.data_store import cargar_info, guardar_info
from core.agent import procesar_correos

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")


# ✅ Endpoint llamado por Google Apps Script
@app.route("/run", methods=["POST"])
def run_bot():
    data = request.get_json()

    if not data:
        return jsonify({"error": "No data received"}), 400

    return jsonify(procesar_correos(data))


@app.route("/config", methods=["GET", "POST"])
def config_data():
    if request.method == "GET":
        return jsonify(cargar_info())

    data = request.json
    guardar_info(data)
    return jsonify({"status": "ok"})
