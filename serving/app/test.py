import requests
'''
local 서버에서 파일을 받음
sc 서버 input 경로에 파일 저장
'''
file_path = "/opt/ml/final/serving/input/glory.mp4" 

with open(file_path, "wb") as f: # Upload된 input 데이터 저장
    f.write(video)

for server in rfServers:
    requests.post(f'http://{server}:30002/getfile/{count}', files=video)

count += 1
