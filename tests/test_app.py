import os
import sys

os.environ["DB_PATH"] = "/tmp/test_db.sqlite"
os.environ.setdefault("SECRET_KEY", "test-only-value")
os.environ.setdefault("SECRET_KEY", "test-only-value")
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "app"))

from main import app  # noqa: E402

client = app.test_client()


def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.get_json()["status"] == "ok"


def test_user_lookup():
    r = client.get("/user?name=alice")
    assert b"alice" in r.data


def test_hello():
    r = client.get("/hello?name=Riadh")
    assert b"Riadh" in r.data


def test_hash():
    r = client.get("/hash?pw=test")
    assert r.data.decode() == "098f6bcd4621d373cade4e832627b4f6"
