"""Main module for API."""
from api.upload import upload_router
from fastapi import FastAPI

app = FastAPI()

app.include_router(upload_router)


@app.get('/')
def read_root():
    """Root of the App."""
    return {"Title': 'Globant's Data Engineer Challenge"}
