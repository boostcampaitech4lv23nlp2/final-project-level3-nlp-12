import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

ssh.connect('101.101.209.53', username='root', port='2234', key_filename='/Users/jd/PG/code/Boost/MRC/jd_key')
v = 1
stdin, stdout, stderr = ssh.exec_command(f'cd /opt/ml/input/code && python test.py {v}')
a = stdout.readlines()
a = int(*a)
print(f'first test {a}')

stdin.close()
ssh.close()

# ssh = paramiko.SSHClient()
# ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

ssh.connect('118.67.133.198', username='root', port='2242', key_filename='/Users/jd/PG/code/Boost/MRC/sol_key',password="1234")
v = a
stdin, stdout, stderr = ssh.exec_command(f'cd /opt/ml/final/serving_test && python test.py {v}')
b = stdout.readlines()
b = int(*b)
print(f"second test is {b}")

stdin.close()
ssh.close()
