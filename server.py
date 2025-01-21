from flask import Flask, jsonify
import os
import importlib
import threading
import time

app = Flask(__name__)

# Diretório onde estão as rotas
ROUTES_DIR = "./routes"
PROTECTION_INTERVAL = 45  # Reinicia o servidor antes do limite de 50s

# Carregar rotas automaticamente
def load_routes():
    for filename in os.listdir(ROUTES_DIR):
        if filename.endswith(".py"):
            module_name = filename[:-3]
            module = importlib.import_module(f"routes.{module_name}")

            # Registra a rota com o mesmo nome do arquivo
            route_name = f"/{module_name}"
            app.route(route_name, methods=["GET"])(module.handle)

# Reinicia o servidor automaticamente
def restart_server():
    while True:
        time.sleep(PROTECTION_INTERVAL)
        os.execv(__file__, ["python"] + sys.argv)

# Endpoint padrão para testar
@app.route("/")
def index():
    return jsonify({"message": "Server is running"})

if __name__ == "__main__":
    load_routes()
    threading.Thread(target=restart_server, daemon=True).start()
    app.run(host="0.0.0.0", port=5000)
