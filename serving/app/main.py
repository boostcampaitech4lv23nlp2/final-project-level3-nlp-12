from fastapi import FastAPI, UploadFile
from fastapi.responses import FileResponse
import uvicorn
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
INPUT_DIR = os.path.join(BASE_DIR, "serving/input")
OUTPUT_DIR = os.path.join(BASE_DIR, "serving/output")

app = FastAPI()


@app.post("/getfile/{count}")
async def getfile(file: UploadFile):
    '''
    sc 서버에서 video 파일을 받음
    rf 서버 input 경로에 파일 저장
    '''
    result = await file.read()
    file_name = f"video_{count}.mp4"
    file_path = os.path.join(INPUT_DIR, file_name)
    with open(file_path, "wb") as f:
        f.write(result)

@app.get("/file/{count}")
def download(count: int):
    '''
    local 서버에서 count를 받으면 output 경로를 local로 return
    '''
    # file_name = f"video_{count}.mp4"
    file_name = f"audio_{count}.mp3"
    file_path = os.path.join(OUTPUT_DIR, file_name)
    return FileResponse(file_path)


# if __name__ == "__main__":
#     uvicorn.run(app, host="0.0.0.0", port=30002)