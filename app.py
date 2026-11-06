"""
Intentionally vulnerable Flask app — A.E.G.I.S. demo / benchmark target.

⚠️  DO NOT DEPLOY. This app contains DELIBERATE security holes so the
autonomous scanner can discover, exploit, verify, and patch them:

  VULN 1 — Insecure deserialization (RCE):
      /api/v1/user/preferences reads a base64 pickle from the `session_prefs`
      cookie and pickle.loads() it. An attacker controls the pickle, so this
      is arbitrary code execution.

  VULN 2 — Path traversal (arbitrary file read):
      /files/<filename> joins user input onto FILES_DIR without sanitization,
      so `..` sequences escape the served directory.
"""
import base64
import os
import pickle

from flask import Flask, Response, jsonify, request

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FILES_DIR = os.path.join(BASE_DIR, "public")


@app.route("/")
def index():
    return "Preferences service. Try /api/v1/user/preferences or /files/<name>."


@app.route("/api/v1/user/preferences", methods=["GET", "POST"])
def preferences():
    # VULN 1: insecure deserialization of an attacker-controlled cookie.
    raw = request.cookies.get("session_prefs")
    if raw:
        prefs = pickle.loads(base64.b64decode(raw))  # noqa: S301 (intentional)
        theme = prefs.get("theme", "default") if isinstance(prefs, dict) else "default"
        return jsonify({"active_theme": theme})
    return jsonify({"active_theme": "default"})


@app.route("/files/<path:filename>")
def get_file(filename):
    # VULN 2: path traversal — filename is joined without sanitization.
    full = os.path.join(FILES_DIR, filename)
    with open(full, "r", encoding="utf-8", errors="replace") as fh:
        return Response(fh.read(), mimetype="text/plain")


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=9999, debug=False)
