from fastapi import FastAPI, Query
from typing import Annotated
from urllib.parse import urljoin

from app.models import SourcePayload, ModifiedPayload, TwoLineElementRecord, TwoLineElementRecordParsed, QueryParams
from app.helpers import parse_tle, modify_payload, make_source_api_call, parse_query_params_to_str

tags_metadata = [
    {
        "name": "TLE",
        "description": "Operations for TLE records",
    }
]

app = FastAPI(
    title="Earth-Orbit Objects API",
    description="API for transforming earth-orbit objects TLE data to JSON",
    version="0.3.0",
    openapi_tags=tags_metadata
)

base_url = 'https://tle.ivanstanojevic.me/'
path = 'api/tle/'

@app.get("/tle", tags = ["TLE"])
async def get_collection(query_params: Annotated[QueryParams, Query()]) -> ModifiedPayload:
    
    parsed_query_params= parse_query_params_to_str(query_params)
    url= f"{urljoin(base_url, path)}?{parsed_query_params}"

    response_content_dict = await make_source_api_call(url) # Calls the API with the query parameters in the URL
    source_payload = SourcePayload.model_validate(response_content_dict) # This returns a Pydantic Model, which is used for validation.
    
    #This part takes the source payload, which is some metadata and a collection of TLEs, parses the TLE lines into distinct key-value pairs, and returns the modified payload.
    modified_payload = modify_payload(source_payload)
    return(modified_payload)
    
@app.get("/tle/{id}", tags = ["TLE"])
async def get_tle_record(id: int) -> TwoLineElementRecordParsed:

    url = f"{urljoin(base_url, path)}{id}"
    response_content_dict = await make_source_api_call(url)
    source_tle = TwoLineElementRecord.model_validate(response_content_dict) # This returns an object from a Pydantic Model, which is used for validation.

    #This part takes the source payload, which is a single TLE, parses the TLE lines into distinct key-value pairs, and returns the modified payload.
    parsed_tle = parse_tle(source_tle)
    return parsed_tle