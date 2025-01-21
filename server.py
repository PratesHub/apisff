from flask import Flask, jsonify
import os
import importlib.util

app = Flask(__name__)

def load_routes(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.py'):
                module_path = os.path.join(root, file)
                module_name = os.path.splitext(file)[0]
                spec = importlib.util.spec_from_file_location(module_name, module_path)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                
                # Remove 'routes' from the path and create the endpoint
                relative_path = os.path.relpath(root, directory)
                endpoint = f"/{relative_path}/{module_name}".replace('\\', '/').rstrip('/')
                if endpoint.endswith('.py'):
                    endpoint = endpoint[:-3]  # Remove .py extension
                
                if hasattr(module, 'route_function'):
                    app.add_url_rule(endpoint, f"{module_name}_endpoint", module.route_function)
                    print(f"Loaded route: {endpoint}")

# Load routes from the 'routes' directory
load_routes('routes')

@app.route('/')
def home():
    return jsonify({"status": "online"})

if __name__ == '__main__':
    from waitress import serve
    print("🟢")
    serve(app, host='0.0.0.0', port=8080)
