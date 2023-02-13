import time

from typing import Optional

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .kubestart import start

app = FastAPI()
count = 0

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"hello": "world"}


@app.get("/signal")
def signal_root():
    global count
    count += 1
    start(count)
    return f"{count}"
