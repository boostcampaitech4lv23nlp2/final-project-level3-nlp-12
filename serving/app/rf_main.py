from fastapi import FastAPI, UploadFile
import uvicorn
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
INPUT_DIR = os.path.join(BASE_DIR, "serving/input")

app = FastAPI()


@app.post("/getfile")
async def getfile(file: UploadFile):
    result = await file.read()
    file_name = file.filename
    file_path = os.path.join(INPUT_DIR, file_name)
    with open(file_path, "wb") as f:
        f.write(result)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=30002)
