from flask import jsonify

def handle():
    return jsonify({"status": "ok", "message": "Server is live."})
