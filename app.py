from flask import Flask, render_template, jsonify, request
from core.data_store import cargar_info, guardar_info
from core.agent import procesar_correos

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/run")
def run_bot():
    return jsonify(procesar_correos())

@app.route("/config", methods=["GET", "POST"])
def config_data():
    if request.method == "GET":
        return jsonify(cargar_info())

    data = request.json
    guardar_info(data)
    return jsonify({"status": "ok"})

# ❌ NO app.run() en Vercel
