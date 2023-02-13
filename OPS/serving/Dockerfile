FROM python:3.8-slim-buster
# container의 usr/src 경로에서 진행
WORKDIR /usr/src
# requirements.txt를 복사해서 넣기
COPY ./requirements.txt /usr/src/requirements.txt
# app 디렉토리를 복사해서 넣기
COPY ./app /usr/src/app
# pip install requirements.txt 실행
RUN pip install --no-cache-dir --upgrade -r requirements.txt
RUN pip install kfp

CMD [ "python3", "-m" , "app"]
