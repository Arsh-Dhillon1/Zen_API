from fastapi.testclient import TestClient
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "app"))

from main import app

client = TestClient(app)


def test_show_entries():
    response = client.get("/journals")

    assert response.status_code == 200