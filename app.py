import base64
import os
import json

from flask import Flask, Response, jsonify, request

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FILES_DIR = os.path.join(BASE_DIR, "public")


@app.route("/")
def index():
    return "Preferences service. Try /api/v1/user/preferences or /files/<name>."


@app.route("/api/v1/user/preferences", methods=["GET", "POST"])
def preferences():
    # Secure deserialization by using JSON instead of pickle.
    raw = request.cookies.get("session_prefs")
    if raw:
        try:
            prefs = json.loads(base64.b64decode(raw).decode('utf-8'))
            theme = prefs.get("theme", "default") if isinstance(prefs, dict) else "default"
        except (json.JSONDecodeError, UnicodeDecodeError):
            theme = "default"
        return jsonify({"active_theme": theme})
    return jsonify({"active_theme": "default"})


@app.route("/files/<path:filename>")
def get_file(filename):
    # Prevent path traversal by ensuring the path is within FILES_DIR.
    safe_filename = os.path.normpath(os.path.join(FILES_DIR, filename))
    if not safe_filename.startswith(FILES_DIR):
        return Response("Access Denied", status=403)
    try:
        with open(safe_filename, "r", encoding="utf-8", errors="replace") as fh:
            return Response(fh.read(), mimetype="text/plain")
    except FileNotFoundError:
        return Response("File Not Found", status=404)


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=9999, debug=False)
