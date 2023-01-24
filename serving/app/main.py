# from fastapi import FastAPI, Form, File, UploadFile
# from fastapi.responses import HTMLResponse
# import uuid
# from typing import List
# from fastapi.templating import Jinja2Templates
# import uvicorn
# import os
# from pathlib import Path
# from datetime import timedelta, datetime

# # from transformers import pipeline

# time_ = datetime.now() + timedelta(hours=9)
# time_now = time_.strftime("%m%d%H%M")

# app = FastAPI()
# templates = Jinja2Templates(directory="templates")

# qa_pipeline = pipeline("question-answering")



# @app.post("/files")
# async def create_files(files: List[bytes] = File(...)):
#     return {"file_sizes": [len(file) for file in files]}


# @app.post("/uploadfiles")
# async def create_upload_files(files: List[UploadFile] = File(...)):
#     UPLOAD_DIRECTORY = "/opt/ml/final/input"
#     for file in files:
#         contents = await file.read()
#         with open(os.path.join(UPLOAD_DIRECTORY, time_now+'_'+file.filename), "wb") as fp:
#             fp.write(contents)
#         print(time_now+'_'+file.filename)
#     return {"filenames": [time_now+'_'+file.filename for file in files]}

# @app.get("/uploadfiles")
# async def create_files(filenames):
#     return {"filenames": filenames}

####################################################################

# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# STATIC_DIR = os.path.join(BASE_DIR,'static/')
# IMG_DIR = os.path.join(STATIC_DIR,'images/')
# SERVER_IMG_DIR = os.path.join('http://localhost:9000/','static/','images/')

# @app.post('/uploadfiles')
# async def upload_board(in_files: List[UploadFile] = File(...)):
#     file_urls=[]
#     for file in in_files:
#         currentTime = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
#         saved_file_name = ''.join([currentTime,secrets.token_hex(16)])
#         print(saved_file_name)
#         file_location = os.path.join(IMG_DIR,saved_file_name)
#         with open(file_location, "wb+") as file_object:
#             file_object.write(file.file.read())
#         file_urls.append(SERVER_IMG_DIR+saved_file_name)
#     result={'fileUrls' : file_urls}
#     return result

# @app.get('/images/{file_name}')
# def get_image(file_name:str):
#     return FileResponse(''.join([IMG_DIR,file_name]))

# @app.get("/")
# async def main():
#     content = """
# <body>
# <form action="/files/" enctype="multipart/form-data" method="post">
# <input name="files" type="file" multiple>
# <input type="submit">
# </form>
# <form action="/uploadfiles/" enctype="multipart/form-data" method="post">
# <input name="files" type="file" multiple>
# <input type="submit">
# </form>
# </body>
#     """
#     return HTMLResponse(content=content)

# @app.get("/")
# def read_root():
#     return templates.TemplateResponse("index.html", {"request": {}})

# @app.post("/answer")
# def answer_question(question: str = Form(...), context: str = Form(...)):
#     result = qa_pipeline({
#         'question': question,
#         'context': context
#     })
#     return templates.TemplateResponse("answer.html", {"request": result})

#############################################
# import os
# import uuid

# from fastapi import FastAPI, Form, File, UploadFile
# from fastapi.responses import HTMLResponse, FileResponse
# from fastapi.templating import Jinja2Templates
# from pathlib import Path

# app = FastAPI()
# templates = Jinja2Templates(directory="templates")


# @app.get("/convert")
# def convert_video_to_audio_form():
#     return templates.TemplateResponse("convert.html", {"request": {}})

# @app.post("/convert")
# async def convert_video_to_audio(file: UploadFile):
#     # 영상 파일을 읽어들임
#     video = await file.read()
#     # 영상 파일을 음성 파일로 변환
#     audio = convert_to_audio(video)
    
#     UPLOAD_DIRECTORY = "/opt/ml/final/serving/output"
#     file_name = file.filename
#     # 음성 파일을 로컬에 저장
#     file_path = save_to_local(audio, UPLOAD_DIRECTORY, file_name)
#     return templates.TemplateResponse("audio.html", {"request": {"file_path": file_path}})

# @app.get("/audio/{file_path}")
# def download_audio(file_path: str):
#     return FileResponse(file_path)

# def convert_to_audio(video: bytes) -> bytes:
#     # 영상 파일을 음성 파일로 변환하는 코드
#     # pass
#     return video # 음성 파일이라고 가정

# def save_to_local(audio: bytes, UPLOAD_DIRECTORY: str , file_name: str):
#     # 음성 파일을 로컬에 저장하는 코드
#     file_path = os.path.join(UPLOAD_DIRECTORY, file_name)
#     with open(file_path, "wb") as f:
#         f.write(audio)
#     return file_path
###########################################################
import os
from fastapi import FastAPI, File, UploadFile, Path
from fastapi.responses import FileResponse
from fastapi.templating import Jinja2Templates
from pathlib import Path
app = FastAPI()
templates = Jinja2Templates(directory="templates")

INPUT_DIRECTORY = "/opt/ml/final/serving/input"
OUTPUT_DIRECTORY = "/opt/ml/final/serving/output"


@app.get("/")
def main():
    return templates.TemplateResponse("index.html", {"request": {}})

@app.post("/")
async def upload(file: UploadFile): 
    video = await file.read() # 파일 읽기
    music = convert_to_music(video) # 
    file_name = file.filename
    file_path = os.path.join(INPUT_DIRECTORY, file_name)

    with open(file_path, "wb") as f:
        f.write(music)
    return templates.TemplateResponse("result.html", {"request": {"file_name":file_name}})

def convert_to_music(video: bytes) -> bytes:
    # 영상 파일을 음악 파일로 변환하는 코드
    # pass
    return video # 음악 파일이라고 가정

@app.get("/result/{file_name}")
def download(file_name: str):
    file_path = os.path.join(OUTPUT_DIRECTORY, file_name)
    return FileResponse(file_path)