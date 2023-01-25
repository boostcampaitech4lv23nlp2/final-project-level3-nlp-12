import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

ssh.connect('101.101.209.53', username='root', port='2234', key_filename='/Users/jd/PG/code/Boost/MRC/jd_key')
v = 1
stdin, stdout, stderr = ssh.exec_command(f'cd /opt/ml/input/code && python test.py {v}')
a = stdout.readlines()
print(int(*a))

stdin.close()
ssh.close()


