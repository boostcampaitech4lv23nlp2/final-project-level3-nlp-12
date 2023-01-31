import os
import sys

from typing import List
from fastapi import FastAPI, UploadFile, Form, File
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import requests

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
INPUT_DIR = os.path.join(BASE_DIR, "serving/input")
OUTPUT_DIR = os.path.join(BASE_DIR, "serving/output")

# TODO: file name을 고유한 ID로 받기
# TODO: DB 용량을 위해 하나의 서비스 끝나면 데이터 지워주기

rfServers = [ 
    "118.67.133.154:30001",
    "27.96.134.124:30001",
    "118.67.142.47:30001",
    "118.67.133.198:30001",
]

app = FastAPI()

origins = ["*"]

# origins = {
#     "http://localhost",
#     "http://localhost:3000",
# }

app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"],
)

@app.post("/upload")
async def upload(file: UploadFile = Form()):
    video = await file.read()  # 파일 읽기
    
    file_name = file.filename # 파일 이름 저장
    file_path = os.path.join(INPUT_DIR, file_name) # input 경로
    
    with open(file_path, "wb") as f: # Upload된 input 데이터 저장
        f.write(video)

    for server in rfServers:
        requests.post(f'{server}:30002/getfile', files=video)

    return FileResponse(file_path)

@app.get("/result/{file_name}") # 결과
def download(file_name: str):
    file_path = os.path.join(OUTPUT_DIR, file_name) # output 경로 + 파일 이름 

    return FileResponse(file_path)

@app.post("/getfile")
async def getfile(file: UploadFile):
    result = await file.read()

    file_name = file.filename
    file_path = os.path.join(OUTPUT_DIR, file_name) # 저장 경로
    with open(file_path, "wb") as f: 
        f.write(result)

