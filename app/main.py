import json
from httpx import AsyncClient, RequestError

from fastapi import FastAPI, HTTPException
from urllib.parse import urlencode

from app.models import SourcePayload, ModifiedPayload
from app.helpers import modify_payload

app = FastAPI(
    title="Earth-Orbit Objects API",        # Provide a title
    description="API for transforming earth-orbit objects TLE data to JSON",        #Provide a description
    version="0.3.0"
)
client = AsyncClient()

@app.get("/")
async def root():
    return {"message": "Hello World!"}

# search: str | None = "*", sort: str | None = "popularity", sort-dir: str | None = "desc", page: int | None = 1, page-size: int | None = 20

@app.get("/tle")
async def get_collection(
    search: str | None = "*",
    sort: str | None = "popularity",
    sort_dir: str | None = "desc",
    page: int | None = 1,
    page_size: int | None = 20
) -> ModifiedPayload:
    
    base_url = 'https://tle.ivanstanojevic.me/api'
    function_parameters = {
        'search': search,
        'sort': sort,
        'sort-dir': sort_dir,
        'page': page,
        'page_size': page_size
    }
    query_parameters = urlencode({k: v for k, v in function_parameters.items() if v is not None})
    request_headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:133.0) Gecko/20100101 Firefox/133.0"
    }
    path = '/tle/'
    try:
        response = await client.get(
            url = f"{base_url}{path}?{query_parameters}",
            headers = request_headers)
        response.raise_for_status()
        response_content = response.content # This returns a byte array containing the json.
        response_content_string = response_content.decode("utf-8") # This returns a string.

        # Hi Sam!  Sam here.  Come back to this problem.  Seems like a good fundamentals for understanding types and how to read them.
        response_content_dict = json.loads(response_content_string) # This returns a dict, not a json.  Not sure why.
        source_payload = SourcePayload.model_validate(response_content_dict) # This returns a Pydantic Model, which is used for validation.

        #Now that we have the API response in a useable format, we can test and validate it better.  But we'll get the bones set up first.
        #This part takes the source payload, parses the TLE lines into distinct key-value pairs, and returns the modified payload.
        modified_payload = modify_payload(source_payload)
        return modified_payload
    except RequestError as e:
        raise HTTPException(status_code=503, detail=f"External API error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")