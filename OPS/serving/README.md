# 1. 웹 서버 실행
serving 디렉토리에서 아래 명령어 수행
```
python -m {directory name}
```

# 2. 저장소 구조


```
.
├── README.md
├── app
|   ├── first_stage             - STT와 Sentiment Clssifier 서버
|   |   ├── __main__.py
|   |   └── main.py
|   ├── local_main              - local API 서버
|   |   ├── __main__.py
|   |   ├── kubestart.py        - kubeflow 실행
|   |   ├── main.py
|   |   └── pipeline.yaml       - kubeflow pipeline
|   └── second_stage            - Riffusion 서버
|       ├── __main__.py
|       └── main.py
├── input                       - 데이터 upload 경로
└── output                      - 모델 output 경로
```