from flask import Flask, jsonify
import time

app = Flask(__name__)

@app.route("/procesar", methods=["POST"])
def procesar():
    print("Procesando tarea pesada...", flush=True)
    time.sleep(5)  # simulación
    print("Tarea terminada", flush=True)

    return jsonify({"status": "procesado"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
