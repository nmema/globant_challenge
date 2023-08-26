"""Main module for API."""
from typing import Optional

from fastapi import FastAPI

app = FastAPI()


@app.get('/')
def read_root():
    """Root of the App."""
    return {'Hello': 'World'}


@app.get('/items/{item_id}')
def read_item(item_id: int, query: Optional[str] = None):
    """Items endpoint."""
    return {'item_id': item_id, 'query': query}
