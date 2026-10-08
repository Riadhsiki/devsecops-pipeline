import base64
import hashlib
import os
import sqlite3
import subprocess

import requests
import yaml
from flask import Flask, jsonify, request
from markupsafe import escape

from config import SECRET_KEY

app = Flask(__name__)
app.secret_key = SECRET_KEY

DB_PATH = os.environ.get("DB_PATH", "db.sqlite")


def init_db():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT, role TEXT)")
    if conn.execute("SELECT COUNT(*) FROM users").fetchone()[0] == 0:
        conn.executemany("INSERT INTO users (name, role) VALUES (?, ?)",
                         [("alice", "admin"), ("bob", "user")])
    conn.commit()
    conn.close()


init_db()


@app.route("/")
def index():
    return "DevSecOps demo app"


@app.route("/health")
def health():
    return jsonify(status="ok")


# VULN: SQL injection
@app.route("/user")
def user():
    name = request.args.get("name", "")
    conn = sqlite3.connect(DB_PATH)
    return str(conn.execute("SELECT id, name, role FROM users WHERE name = ?", (name,)).fetchall())


# VULN: OS command injection
@app.route("/ping")
def ping():
    host = request.args.get("host", "127.0.0.1")
    return subprocess.run(["ping", "-c", "1", host], capture_output=True, text=True).stdout


# VULN: reflected XSS
@app.route("/hello")
def hello():
    name = request.args.get("name", "world")
    return "<h1>Hello " + escape(name) + "</h1>"


# VULN: unsafe YAML loading
@app.route("/yaml", methods=["POST"])
def parse_yaml():
    return str(yaml.safe_load(request.data))


# VULN: path traversal
@app.route("/file")
def read_file():
    name = request.args.get("name", "")
    try:
        with open(os.path.join("files", name)) as f:
            return f.read()
    except Exception as e:
        return "Error: " + str(e), 500


# VULN: SSRF
@app.route("/fetch")
def fetch():
    return requests.get(request.args.get("url", ""), timeout=5).text[:500]


# VULN: weak hashing
@app.route("/hash")
def hash_pw():
    return hashlib.sha256(request.args.get("pw", "").encode()).hexdigest()


if __name__ == "__main__":
    # VULN: debug mode, all interfaces
    app.run(host=os.environ.get("APP_HOST", "127.0.0.1"), port=5000, debug=False)
