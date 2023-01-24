import os
import sys
from fastapi import FastAPI, UploadFile
from fastapi.responses import FileResponse
from fastapi.templating import Jinja2Templates

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
INPUT_DIR = os.path.join(BASE_DIR, 'serving/input')
OUTPUT_DIR =os.path.join(BASE_DIR, 'serving/output')

sys.path.append(BASE_DIR)
from model import v2m_model

app = FastAPI()
templates = Jinja2Templates(directory="templates")


@app.get("/")
def main():
    return templates.TemplateResponse("index.html", {"request": {}})


@app.post("/")
async def upload(file: UploadFile):
    video = await file.read()  # 파일 읽기
    music = v2m_model.convert_to_music(video)  # 음악 파일로 변경
    file_name = file.filename
    file_path = os.path.join(INPUT_DIR, file_name)

    with open(file_path, "wb") as f:
        f.write(music)
    return templates.TemplateResponse("result.html", {"request": {"file_name": file_name}})


@app.get("/result/{file_name}")
def download(file_name: str):
    # file_name mp4 -> wav 형식으로 읽는 코드 수정 필요
    file_path = os.path.join(OUTPUT_DIR, file_name)
    return FileResponse(file_path)
