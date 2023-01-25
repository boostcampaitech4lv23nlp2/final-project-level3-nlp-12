import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

ssh.connect('118.67.133.198', username='root', port='2242', key_filename='/Users/jd/PG/code/Boost/MRC/sol_key',password="1234")
v = 2
stdin, stdout, stderr = ssh.exec_command(f'cd /opt/ml/final/serving_test && python test.py {v}')
a = stdout.readlines()

print(int(*a))

stdin.close()
ssh.close()