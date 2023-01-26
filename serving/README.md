# 1. 웹 서버 실행
serving 디렉토리에서 아래 명령어 수행
```
python -m app 
```
# 2. 데모 페이지 접속 URL
```
http://0.0.0.0:9000
```
# 3. 저장소 구조
```
serving
|-- app
|   |-- __main__.py
|   `-- main.py          - fast api 실행
|-- input                - input video(mp4) 데이터의 storage
|   `-- test_video.mp4
|-- output               - output music(wav, mp3, ...) 데이터의 storage
|   |-- test_sound.wav
|   `-- test_video.mp4
`-- templates            - html 템플릿
    |-- index.html
    `-- result.html
```