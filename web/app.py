from flask import Flask, render_template, jsonify
from core.agent import procesar_correos

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html", logs=[])

@app.route("/run")
def run_bot():
    logs = procesar_correos()
    return jsonify(logs)

if __name__ == "__main__":
    app.run(debug=True)
