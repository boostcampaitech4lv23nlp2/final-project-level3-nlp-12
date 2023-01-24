import os
import sys

from fastapi import FastAPI, UploadFile
from fastapi.responses import FileResponse
from fastapi.templating import Jinja2Templates

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
INPUT_DIR = os.path.join(BASE_DIR, "serving/input")
OUTPUT_DIR = os.path.join(BASE_DIR, "serving/output")

# TODO: 다른 서버로 옮긴 후 모델을 실행하고, 다시 웹 서버로 받는 과정 필요
# sys.path.append(BASE_DIR)
# from model import v2m_model


app = FastAPI()
templates = Jinja2Templates(directory="templates")


@app.get("/") # 시작
def main():
    return templates.TemplateResponse("index.html", {"request": {}})


@app.post("/")
async def upload(file: UploadFile):
    video = await file.read()  # 파일 읽기
    
    file_name = file.filename # 파일 이름 저장
    file_path = os.path.join(INPUT_DIR, file_name) # input 경로
    with open(file_path, "wb") as f: # 다른 서버로 넘겨주기 위해 input 데이터 저장
        f.write(video)
    # music = v2m_model.convert_to_music(video)  # 음악 파일로 변경
    return templates.TemplateResponse("result.html", {"request": {"file_name": file_name}}) 


@app.get("/result/{file_name}") # 결과
def download(file_name: str):
    # output에 있는 파일은 model을 통해 변환된 음악 파일
    # TODO: file_name mp4 -> wav 형식으로 읽는 코드 수정 필요
    file_path = os.path.join(OUTPUT_DIR, file_name) # output 경로 + 파일 이름 
    return FileResponse(file_path)
