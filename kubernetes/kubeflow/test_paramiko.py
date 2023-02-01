


# ssh.connect('118.67.133.198', username='root', port='2242', password="1234", key_filename="C:/Users/seokhee/boostcamp/final/key")
# ssh.connect('118.67.133.154', username='root', port='2240', key_filename='key',password='0000')
# ssh.connect('27.96.134.124', username='root', port='2238', key_filename='key',password='0801')
# conda = 'gw'
# conda = 'whisper'

# stdin, stdout, stderr = ssh.exec_command(f'cd /opt/ml/final/model && pwd')
# stdin, stdout, stderr = ssh.exec_command(f'cd /opt/ml/final/model && conda activate {conda} && python riffusion_pipeline_test.py')

def first_stage(cnt):
    import paramiko
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect('101.101.209.53', username='root', port='2235', key_filename='key',password='1234')
    stdin, stdout, stderr = ssh.exec_command(f'cd /opt/ml/final/model && conda activate JD && python stt_sent_test.py --input_file /opt/ml/final/serving/input/video_{cnt}.mp4')
    sentiment_string = stdout.readline().strip()
    # print(type(sentiment_string))
    stdin.close()
    ssh.close()
    # print(sentiment_string)
    return sentiment_string

# stage 2

def second_stage(name, cnt, sentiment_string):
    import paramiko
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    # sentiment_string = '80 94 fear 118 124 surprise'
    # cnt = 1
    # cnt = str(cnt)
    if name == 'sh':
        conda = 'final'
        ssh.connect('118.67.133.198', username='root', port='2243', key_filename='key',password='1234')
    elif name == 'gw':
        conda = 'gw'
        ssh.connect('118.67.133.154', username='root', port='2240', key_filename='key',password='0000')
    elif name == 'yc':
        conda = 'whisper'
        ssh.connect('27.96.134.124', username='root', port='2238', key_filename='key',password='0801')
    elif name == 'dk':
        conda = 'lv3'
        ssh.connect('118.67.142.47', username='root', port='2234', key_filename='key',password='0214')
    stdin, stdout, stderr = ssh.exec_command(f'cd /opt/ml/final/model && conda activate {conda} && python riffusion_pipeline_test.py --sentiment_string "{sentiment_string}" --code "{cnt}"')    
    results = stdout.readlines()
    filepath = 'No result in second stage'
    for result in results:
        result = result.strip()
        if result.startswith('/opt/ml/final/tmp'):
            filepath = result
            break
    # result = results[0]
    # result = stdout.readline()
    print(filepath)
    stdin.close()
    ssh.close()
# server = ['sh', 'gw', 'yc', 'dk']
# for s in server:
#     print("server :", s, " start")
#     second_stage(s)

count = 1
# task_1_output= first_stage(count)
# print(task_1_output)
task_1_output ="12 30 None"
second_stage('yc', count, task_1_output)