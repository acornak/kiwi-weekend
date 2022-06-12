"""
Handler for endpoint
"""
import uvicorn

from fastapi import FastAPI
from fastapi.responses import JSONResponse

from scraper.search_engine import call_search_engine


app = FastAPI()


@app.get("/v1/search")
def search(origin: str, destination: str, dateFrom: str) -> JSONResponse:
    result = call_search_engine(origin, destination, str(dateFrom))
    
    return JSONResponse(result)


if __name__ == "__main__":
    uvicorn.run("api_handler:app", host="127.0.0.1", port=8000, log_level="info")
