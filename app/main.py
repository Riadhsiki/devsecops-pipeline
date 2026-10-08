import base64
import hashlib
import os
import pickle
import sqlite3
import subprocess

import requests
import yaml
from flask import Flask, request

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
    return {"status": "ok"}


# VULN: SQL injection
@app.route("/user")
def user():
    name = request.args.get("name", "")
    conn = sqlite3.connect(DB_PATH)
    query = f"SELECT id, name, role FROM users WHERE name = '{name}'"
    return str(conn.execute(query).fetchall())


# VULN: OS command injection
@app.route("/ping")
def ping():
    host = request.args.get("host", "127.0.0.1")
    return subprocess.getoutput("ping -c 1 " + host)


# VULN: reflected XSS
@app.route("/hello")
def hello():
    name = request.args.get("name", "world")
    return "<h1>Hello " + name + "</h1>"


# VULN: insecure deserialization
@app.route("/load")
def load():
    data = request.args.get("data", "")
    return str(pickle.loads(base64.b64decode(data)))


# VULN: unsafe YAML loading
@app.route("/yaml", methods=["POST"])
def parse_yaml():
    return str(yaml.load(request.data, Loader=yaml.Loader))


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
    return hashlib.md5(request.args.get("pw", "").encode()).hexdigest()


if __name__ == "__main__":
    # VULN: debug mode, all interfaces
    app.run(host="0.0.0.0", port=5000, debug=True)
