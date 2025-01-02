import requests

from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from .models import SourcePayload
from .helpers import modify_payload, create_robust_session

app = FastAPI(      #create FastAPI instance
    title="Earth-Orbit Objects API",        # Provide a title
    description="API for transforming earth-orbit objects TLE data to JSON",        #Provide a description
    version="0.2.0"
)

SOURCE_API_URL = 'https://tle.ivanstanojevic.me/api/tle/'

@app.api_route("/{path:path}", methods=["GET"])
async def proxy(request: Request, path: str):
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "en-US,en;q=0.5",
        "Connection": "keep-alive",
        "DNT": "1",
        "Host": "tle.ivanstanojevic.me",
        "Priority":	"u=0, i",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-User": "?1",
        "Sec-GPC": "1",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:133.0) Gecko/20100101 Firefox/133.0"
    }
    session = create_robust_session()

    try:
        with session.request(
            method=request.method,
            url=f"{SOURCE_API_URL}{path}",
            headers=headers,
            data=await request.body(),
            cookies=request.cookies,
            allow_redirects=False,
            stream=True
        ) as response:
            
            if response.status_code != 200:
                raise HTTPException(
                    status_code=response.status_code,
                    detail=response.json()
                )

            # Parse the response payload
            source_payload = SourcePayload.model_validate_json(response.content)

            # Modify the payload
            modified_payload = modify_payload(source_payload)

            # Return the modified response
            return JSONResponse(content=modified_payload.model_dump(by_alias=True), status_code=response.status_code) 

    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=str(e))

    # # Print the response content for debugging
    # print("Reponse from base API for debugging:")
    # print(response.content)

    # # Parse the response payload
    # source_payload = SourcePayload.model_validate_json(response.content)

    # # Modify the payload
    # modified_payload = modify_payload(source_payload)

    # # Return the modified response
    # return JSONResponse(content=modified_payload.model_dump(by_alias=True), status_code=response.status_code) 