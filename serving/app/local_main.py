from typing import Optional
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from kube_start import start

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"],
)

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}

# 쿠버네티스 kubestart
@app.get("/start")
def kubestart():
    start()