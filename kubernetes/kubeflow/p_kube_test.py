import kfp
from kfp import onprem
from kfp.components import create_component_from_func
from kfp.dsl import pipeline, ParallelFor
import pickle

def first_stage() -> str:
    '''
    backend 서버와 연결
    stt-sc model 실행 
    return: sentiment_string output
    '''
    import paramiko
    ssh = paramiko.SSHClient() # ssh client 실행
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect('101.101.209.53', username='root', port='2235', key_filename='/var/data/jd_key',password='1234') # 서버 연결

    stdin, stdout, stderr = ssh.exec_command(f'cd /opt/ml/final/model && conda activate JD && python stt_sent_test.py')
    sentiment_string = stdout.readline().strip()
    stdin.close()
    ssh.close()

    return sentiment_string

def second_stage(sentiment_string: str, ip: str, port: str, key: str, pw: str, conda: str) -> str:
    '''
    sentiment_string을 input으로 받음
    riffusion model 실행
    return: video output 경로 
    '''
    import paramiko
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy()) # ssh client 실행
    ssh.connect(ip, username='root', port=port, key_filename=f'/var/data/{key}_key',password=pw) # 서버 연결
    
    # stdin, stdout, stderr = ssh.exec_command(f'cd /opt/ml/final/model && conda activate {conda} && python riffusion_pipeline_test.py --sentiment_string "{sentiment_string}"')
    # ret = stdout.readlines()
    # stdin.close()
    # ssh.close()
    
    stdin, stdout, stderr = ssh.exec_command(f'cd /opt/ml/final/model && conda activate {conda} && python riffusion_pipeline_test.py --sentiment_string "{sentiment_string}"')
    filepath = stdout.readlines() # 파일 이름 포함 파일 경로
    stdin.close()
    ssh.close()
    
    return filepath

# component 생성
first_stage_op = create_component_from_func(first_stage, packages_to_install=['paramiko==3.0.0'])
second_stage_op = create_component_from_func(second_stage, packages_to_install=['paramiko==3.0.0'])


@pipeline(name="test_pipeline")
def my_pipeline():
    pvc_name="kfpvc"
    volume_name="pipeline"
    volume_mount_path="var/data"
    
    with open('server_secret_key.p', 'rb') as file:        # server_secret_key에서 ip, port, key, pw, conda 읽기
        # gw = pickle.load(file)
        # yc = pickle.load(file)
        sol = pickle.load(file)
        # dw = pickle.load(file)

    # server_secret_key = [gw,yc,sol,dw]
    server_secret_key = [sol]

    task_1 = first_stage_op().apply(onprem.mount_pvc(pvc_name, volume_name=volume_name, volume_mount_path=volume_mount_path))
    
    with ParallelFor(server_secret_key) as item:
        second_stage_op(task_1.output, item.ip, item.port, item.key, item.pw, item.conda).apply(onprem.mount_pvc(pvc_name, volume_name=volume_name, volume_mount_path=volume_mount_path))
        
if __name__ == '__main__':
    kfp.compiler.Compiler().compile(
        my_pipeline,
        "./kube_p_pipeline.yaml"
    )
    print("Compelete")