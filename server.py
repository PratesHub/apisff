import os
import sys
import importlib
import threading
import time
from flask import Flask, jsonify

# Configurações principais
ROUTES_DIR = "./routes"  # Diretório base das rotas
PROTECTION_INTERVAL = 45  # Tempo antes de reiniciar o servidor (em segundos)

# Inicialização do aplicativo Flask
app = Flask(__name__)

def clear_console():
    """
    Limpa o console antes de exibir as rotas.
    Funciona em sistemas Windows e Unix.
    """
    os.system('cls' if os.name == 'nt' else 'clear')

def load_routes():
    """
    Carrega automaticamente os módulos de rotas do diretório especificado,
    incluindo subdiretórios como v1, v2, etc., e registra no Flask.
    """
    available_routes = []
    failed_routes = []

    for root, dirs, files in os.walk(ROUTES_DIR):
        for filename in files:
            if filename.endswith(".py"):
                try:
                    # Construir o nome do módulo
                    relative_path = os.path.relpath(root, ROUTES_DIR)
                    module_name = filename[:-3]
                    route_prefix = f"/{relative_path.replace(os.sep, '/')}"
                    module = importlib.import_module(f"routes.{relative_path.replace(os.sep, '.')}.{module_name}")

                    # Define o nome da rota
                    route_name = f"{route_prefix}/{module_name}".rstrip("/")
                    
                    # Registra a rota no Flask
                    app.route(route_name, methods=["GET"])(module.handle)
                    available_routes.append(route_name)
                except Exception as e:
                    failed_routes.append(f"{route_prefix}/{module_name}".rstrip("/"))
                    print(f"Erro ao carregar rota {module_name}: {e}")
    
    # Exibe as rotas carregadas
    clear_console()
    print("Rotas disponíveis e indisponíveis:")
    for route in available_routes:
        print(f"🟢 {route}")
    for route in failed_routes:
        print(f"🔴 {route}")

    return available_routes, failed_routes

def restart_server():
    """
    Reinicia automaticamente o servidor para evitar limite de tempo da host.
    """
    while True:
        time.sleep(PROTECTION_INTERVAL)
        os.execv(sys.executable, [sys.executable] + sys.argv)

# Rota padrão para verificar se o servidor está ativo
@app.route("/")
def index():
    return jsonify({
        "message": "API server is running",
        "routes_base": "/routes",
    })

if __name__ == "__main__":
    try:
        # Carregar rotas dinamicamente
        load_routes()

        # Iniciar thread de reinício automático
        threading.Thread(target=restart_server, daemon=True).start()

        # Iniciar o servidor Flask
        app.run(host="0.0.0.0", port=5000)
    except Exception as e:
        print(f"Erro ao iniciar o servidor: {e}")
