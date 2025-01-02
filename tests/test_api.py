from fastapi.testclient import TestClient
from app.models import TwoLineElementRecord, TwoLineElementRecordParsed
from app.helpers import parse_tle, parse_mutliple_tles
from app.main import app

client = TestClient(app)

def test_root_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "NASA TLE API"}