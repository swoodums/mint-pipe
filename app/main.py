from fastapi import FastAPI

app = FastAPI(      #create FastAPI instance
    title="Earth-Orbit Objects API",        # Provide a title
    description="API for transforming earth-orbit objects TLE data to JSON",        #Provide a description
    version="0.1.0",
    summary="Consumes TLE data and transforms it into a flattened JSON.  Validates datatypes."
)

@app.get("/")       #Define a path operation decorator.  This tells FastAPI that the function below is in charge of handling requests that go to the path / using the get operation
async def root():         #define the path operation function
    return {"message": "NASA TLE API"}       #return the content