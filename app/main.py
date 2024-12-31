import datetime
from enum import Enum
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from helpers import parse_tle, parse_mutliple_tles

app = FastAPI(      #create FastAPI instance
    title="Earth-Orbit Objects API",        # Provide a title
    description="API for transforming earth-orbit objects TLE data to JSON",        #Provide a description
    version="0.1.0"
)

class TwoLineElementRecord(BaseModel):
    id: str
    type: str
    satelliteId: int
    name: str
    date: str
    line1: str
    line2: str

class TwoLineElementRecordParsed(BaseModel):
    id: str
    type: str
    satelliteId: int
    name: str
    date: str
    line1: str
    line2: str

class Category(Enum):
    TOOLS = "tools"
    CONSUMABLES = "consumables"

class Item(BaseModel):
    name: str
    price: float
    count: int
    id: int
    category: Category

# Using items as an example; this will be conceptually the same as the TLE data you will pas.
items = {
    0: Item(name="Hammer", price=9.99, count=20, id=0, category=Category.TOOLS),
    1: Item(name="Pliers", price=5.99, count=20, id=1, category=Category.TOOLS),
    2: Item(name="Nails", price=1.99, count=100, id=2, category=Category.CONSUMABLES)
}

test_tle = {
    "@id": "https://tle.ivanstanojevic.me/api/tle/694",
    "@type": "Tle",
    "satelliteId": 694,
    "name": "ATLAS CENTAUR 2",
    "date": "2024-12-30T16:44:23+00:00",
    "line1": "1 00694U 63047A   24365.69749068  .00009556  00000+0  11813-2 0  9998",
    "line2": "2 00694  30.3575  96.7654 0557567 222.2164 133.4191 14.09575246 70287"
}

@app.get("/")       #Define a path operation decorator.  This tells FastAPI that the function below is in charge of handling requests that go to the path / using the get operation
async def index() -> dict[str, dict[int, Item]]:         #define the path operation function
    return {"items": items}       #return the content

@app.get("/items/{item_id}")
def query_item_by_id(item_id: int) -> Item:
    if item_id not in items:
        raise HTTPException(
            tatus_code=404, detail=f"Item with {item_id=} does not exist."
            )
    return items[item_id]