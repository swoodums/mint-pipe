# project/test/test_api.py

import pytest
from fastapi.testclient import TestClient
import json
from datetime import datetime
import sys
from pathlib import Path

# Add the app directory to the Python path
app_path = Path(__file__).parent.parent / "app"
sys.path.append(str(app_path))

from app.main import app
from app.models import TwoLineElementRecord, TwoLineElementRecordParsed
from app.helpers import parse_tle, modify_payload

client = TestClient(app)

# Sample TLE data for testing
SAMPLE_TLE_RESPONSE = {
    "@context": "https://www.ivanstanojevic.me/tle/docs.jsonld",
    "@id": "/api/tle",
    "@type": "TleCollection",
    "totalItems": 1,
    "member": [
        {
            "@id": "/api/tle/25544",
            "@type": "Tle",
            "satelliteId": 25544,
            "name": "ISS (ZARYA)",
            "date": "2024-01-02T12:00:00.000Z",
            "line1": "1 25544U 98067A   24002.50000000  .00020000  00000+0  36000-3 0  9995",
            "line2": "2 25544  51.6416 243.8493 0006000  47.4000 313.2000 15.50000000    00"
        }
    ],
    "parameters": {
        "page": 1,
        "size": 1
    },
    "view": {
        "first": "/api/tle?page=1",
        "last": "/api/tle?page=1",
        "next": None,
        "previous": None
    }
}

def test_proxy_endpoint_success():
    """Test successful API proxy request"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    
    # Check basic structure
    assert "context" in data
    assert "member" in data
    assert isinstance(data["member"], list)
    
    # Check transformation of TLE data
    if data["member"]:
        member = data["member"][0]
        assert "satellite_catalog_number" in member
        assert "classification" in member
        assert "epoch_year" in member
        assert "bstar" in member
        assert isinstance(member["eccentricity"], float)

def test_proxy_endpoint_with_params():
    """Test API proxy with query parameters"""
    response = client.get("/?page=1&size=1")
    assert response.status_code == 200
    data = response.json()
    assert data["parameters"]["page"] == 1
    assert data["parameters"]["size"] == 1

def test_specific_satellite():
    """Test getting data for a specific satellite"""
    # ISS NORAD ID
    response = client.get("/25544")
    assert response.status_code == 200
    data = response.json()
    assert data["member"][0]["satelliteId"] == 25544

def test_parse_tle_function():
    """Test the TLE parsing function directly"""
    sample_tle = TwoLineElementRecord(
        id="/api/tle/25544",
        type="Tle",
        satelliteId=25544,
        name="ISS (ZARYA)",
        date="2024-01-02T12:00:00.000Z",
        line1="1 25544U 98067A   24002.50000000  .00020000  00000+0  36000-3 0  9995",
        line2="2 25544  51.6416 243.8493 0006000  47.4000 313.2000 15.50000000    00"
    )
    
    parsed = parse_tle(sample_tle)
    
    assert isinstance(parsed, TwoLineElementRecordParsed)
    assert parsed.satellite_catalog_number == "25544"
    assert parsed.classification == "U"
    assert parsed.epoch_year == "24"
    assert isinstance(parsed.eccentricity, float)
    assert parsed.eccentricity == 0.0006000
    assert parsed.inclination == "  51.6416"

def test_modify_payload_function():
    """Test the payload modification function"""
    # Convert sample response to appropriate input type
    source_payload = json.loads(json.dumps(SAMPLE_TLE_RESPONSE))
    modified = modify_payload(source_payload)
    
    assert modified.totalItems == 1
    assert len(modified.member) == 1
    assert modified.member[0].satelliteId == 25544
    assert isinstance(modified.member[0].eccentricity, float)

def test_error_handling():
    """Test error handling for invalid requests"""
    response = client.get("/invalid_satellite_id")
    assert response.status_code in [404, 400]  # Depending on API implementation

@pytest.mark.asyncio
async def test_async_functionality():
    """Test async functionality of the API"""
    # Make multiple concurrent requests
    import asyncio
    import httpx
    
    async with httpx.AsyncClient(app=app, base_url="http://test") as ac:
        tasks = [ac.get("/") for _ in range(3)]
        responses = await asyncio.gather(*tasks)
        
        for response in responses:
            assert response.status_code == 200

def test_response_headers():
    """Test response headers"""
    response = client.get("/")
    assert "content-type" in response.headers
    assert "application/json" in response.headers["content-type"]