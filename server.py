from flask import Flask, jsonify
import os
import importlib.util
from termcolor import colored
import threading
import time
import requests

app = Flask(__name__)
routes = []

def load_routes(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.py'):
                module_path = os.path.join(root, file)
                module_name = os.path.splitext(file)[0]
                spec = importlib.util.spec_from_file_location(module_name, module_path)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                
                relative_path = os.path.relpath(root, directory)
                endpoint = f"/{relative_path}/{module_name}".replace('\\', '/').rstrip('/')
                if endpoint.endswith('.py'):
                    endpoint = endpoint[:-3]  # Remove .py extension
                
                if hasattr(module, 'route_function'):
                    app.add_url_rule(endpoint, f"{module_name}_endpoint", module.route_function)
                    routes.append(endpoint)
                    print(f"Loaded route: {endpoint}")

def print_routes():
    print("\nAvailable routes:")
    for route in routes:
        status = colored('🟢', 'green')
        print(f"{status} {route}")
    
    for root, dirs, files in os.walk('routes'):
        for file in files:
            if file.endswith('.py'):
                module_path = os.path.join(root, file)
                relative_path = os.path.relpath(module_path, 'routes')
                potential_route = f"/{os.path.splitext(relative_path)[0]}".replace('\\', '/')
                if potential_route not in routes:
                    status = colored('🔴', 'red')
                    print(f"{status} {potential_route} (No route_function found)")

@app.route('/')
def home():
    return jsonify({"message": "Welcome to the API server"})

@app.route('/health')
def health_check():
    return jsonify({"status": "healthy"}), 200

def keep_alive():
    while True:
        time.sleep(30)
        try:
            requests.get('http://localhost:8080/health')
            print("Heartbeat sent")
        except:
            print("Failed to send heartbeat")

if __name__ == '__main__':
    from waitress import serve
    
    load_routes('routes')
    print_routes()
    
    keep_alive_thread = threading.Thread(target=keep_alive, daemon=True)
    keep_alive_thread.start()
    
    print("\nServer is running on http://localhost:8080")
    serve(app, host='0.0.0.0', port=8080)
