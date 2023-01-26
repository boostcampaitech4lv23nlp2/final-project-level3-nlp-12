# TODO : pickle 파일 생성 후 develop 브랜치에 merge 할 때는 삭제 필요
import pickle

gw = {'ip': '118.67.133.154', 'port': '6023', 'key': 'gw', 'pw' : '1263'}
yc = {'ip': '27.96.134.124', 'port': '2238', 'key': 'yc', 'pw' : '0801'}
sol = {'ip': '118.67.133.198', 'port': '2242', 'key': 'sol', 'pw' : '1234'}
dk = {'ip': '118.67.142.47', 'port': '6006', 'key': 'dk', 'pw' : 'eks3242'}


with open('server_secret_key.p', 'wb') as file:    # server_secret_key 생성
    pickle.dump(gw, file)
    pickle.dump(yc, file)
    pickle.dump(sol, file)
    pickle.dump(dk, file)

with open('server_secret_key.p', 'rb') as file:    # server_secret_key 읽기
    gw = pickle.load(file)
    yc = pickle.load(file)
    sol = pickle.load(file)
    dk = pickle.load(file)
    print(gw)
    print(yc)
    print(sol)
    print(dk)
server_secret_key = [gw,yc,sol,dk]
print(server_secret_key)