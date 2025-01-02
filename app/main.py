import datetime

from enum import Enum
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from .models import TwoLineElementRecord, TwoLineElementRecordParsed
from .helpers import parse_tle, parse_mutliple_tles

app = FastAPI(      #create FastAPI instance
    title="Earth-Orbit Objects API",        # Provide a title
    description="API for transforming earth-orbit objects TLE data to JSON",        #Provide a description
    version="0.1.0"
)

test_tle = {
    "@id": "https://tle.ivanstanojevic.me/api/tle/694",
    "@type": "Tle",
    "satelliteId": 694,
    "name": "ATLAS CENTAUR 2",
    "date": "2024-12-30T16:44:23+00:00",
    "line1": "1 00694U 63047A   24365.69749068  .00009556  00000+0  11813-2 0  9998",
    "line2": "2 00694  30.3575  96.7654 0557567 222.2164 133.4191 14.09575246 70287"
}

test_tle_from_class = TwoLineElementRecord(
    id=test_tle["@id"],
    type=test_tle["@type"],
    satelliteId=test_tle["satelliteId"],
    name=test_tle["name"],
    date=test_tle["date"],
    line1=test_tle["line1"],
    line2=test_tle["line2"]
)


@app.get("/")       #Define a path operation decorator.  This tells FastAPI that the function below is in charge of handling requests that go to the path / using the get operation
async def index():         #define the path operation function
    return {"message": "NASA TLE API"}       #return the content


@app.get("/tle")
def query_tle():
    return parse_tle(test_tle_from_class)