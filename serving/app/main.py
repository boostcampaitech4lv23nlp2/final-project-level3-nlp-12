import os
import sys

from typing import List
from fastapi import FastAPI, UploadFile, Form, File
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
INPUT_DIR = os.path.join(BASE_DIR, "serving/input")
OUTPUT_DIR = os.path.join(BASE_DIR, "serving/output")

# TODO: 다른 서버로 옮긴 후 모델을 실행하고, 다시 웹 서버로 받는 과정 필요
# sys.path.append(BASE_DIR)
# from model import v2m_model
# TODO: STT - sentiment 모델 연결
# TODO: 4개 output 선택지 버튼. 버튼 선택 - 해당 데이터를 local DB에서 가져오기
############################################옵션#################################################
# TODO: file name을 고유한 ID로 받기
# TODO: DB 용량을 위해 하나의 서비스 끝나면 데이터 지워주기


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
    with open(file_path, "wb") as f: # 다른 서버로 넘겨주기 위해 input 데이터 저장
        f.write(video)

    return FileResponse(file_path)
    # music = v2m_model.convert_to_music(video)  # 음악 파일로 변경

@app.get("/result/{file_name}") # 결과
def download(file_name: str):
    # output에 있는 파일은 model을 통해 변환된 음악 파일
    # TODO: file_name mp4 -> wav 형식으로 읽는 코드 수정 필요
    file_path = os.path.join(OUTPUT_DIR, file_name) # output 경로 + 파일 이름 

    return FileResponse(file_path)

@app.post("/getfile")
async def getfile(file: UploadFile):
    result = await file.read()

    file_name = file.filename
    file_path = os.path.join(OUTPUT_DIR, file_name) # 저장 경로
    with open(file_path, "wb") as f: 
        f.write(result)

