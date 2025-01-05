import json
from httpx import AsyncClient, RequestError

from fastapi import FastAPI, HTTPException, Query
from urllib.parse import urlencode
from typing import Annotated

from app.models import SourcePayload, ModifiedPayload, TwoLineElementRecord, TwoLineElementRecordParsed, QueryParams
from app.helpers import parse_tle, modify_payload, parse_query_params_to_str

app = FastAPI(
    title="Earth-Orbit Objects API",        # Provide a title
    description="API for transforming earth-orbit objects TLE data to JSON",        #Provide a description
    version="0.3.0"
)

client = AsyncClient()
base_url = 'https://tle.ivanstanojevic.me/api'
request_headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:133.0) Gecko/20100101 Firefox/133.0"
}
path = '/tle/'

# @app.get("/")
# async def root():
#     return {"message": "Hello World!"}

@app.get("/tle")
async def get_collection(query_params: Annotated[QueryParams, Query()]) -> ModifiedPayload:
    
    parsed_query_params= parse_query_params_to_str(query_params)

    try:
        response = await client.get(
            url = f"{base_url}{path}?{parsed_query_params}",
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
    
@app.get("/tle/{id}")
async def get_tle_record(id) -> TwoLineElementRecordParsed:
    try:
        response = await client.get(
            url = f"{base_url}{path}{id}",
            headers = request_headers)
        print(f"\n\n Sent request to: {base_url}{path}{id}")
        response.raise_for_status()
        response_content = response.content # This returns a byte array containing the json.
        response_content_string = response_content.decode("utf-8") # This returns a string.

        # Hi Sam!  Sam here.  Come back to this problem.  Seems like a good fundamentals for understanding types and how to read them.
        response_content_dict = json.loads(response_content_string) # This returns a dict, not a json.  Not sure why.
        source_tle = TwoLineElementRecord.model_validate(response_content_dict) # This returns a Pydantic Model, which is used for validation.

        #Now that we have the API response in a useable format, we can test and validate it better.  But we'll get the bones set up first.
        #This part takes the source payload, parses the TLE lines into distinct key-value pairs, and returns the modified payload.
        parsed_tle = parse_tle(source_tle)
        return parsed_tle
    except RequestError as e:
        raise HTTPException(status_code=503, detail=f"External API error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")