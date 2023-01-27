import kfp
from kfp.components import create_component_from_func
from kfp import onprem
import pickle

def first_stage() -> str:
    import paramiko
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect('101.101.209.53', username='root', port='2235', key_filename='/var/data/jd_key')

    stdin, stdout, stderr = ssh.exec_command(f'cd /opt/ml/final/model && python stt_sent_for_serving.py')
    sentiment_string = stdout.readline().strip()
    stdin.close()
    ssh.close()

    return sentiment_string

def second_stage(sentiment_string: str, ip: str, port: str, key: str, pw: str) -> str:
    import paramiko
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(ip, username='root', port=port, key_filename=f'/var/data/{key}_key',password=pw)
    
    stdin, stdout, stderr = ssh.exec_command(f'cd /opt/ml/final/model && python riffusion_pipeline_test.py --sentiment_string {sentiment_string}')
    ret = stdout.readlines()
    stdin.close()
    ssh.close()

    return ret

first_stage_op = create_component_from_func(first_stage, packages_to_install=['paramiko==3.0.0'])
second_stage_op = create_component_from_func(second_stage, packages_to_install=['paramiko==3.0.0'])

from kfp.dsl import pipeline
from kfp.dsl import ParallelFor

@pipeline(name="test_pipeline")
def my_pipeline():
    pvc_name="kfpvc"
    volume_name="pipeline"
    volume_mount_path="var/data"
    
    with open('server_secret_key.p', 'rb') as file:        # server_secret_key에서 ip, port, key, pw 읽기
        gw = pickle.load(file)
        yc = pickle.load(file)
        sol = pickle.load(file)
        dk = pickle.load(file)

    server_secret_key = [gw,yc,sol,dk]

    task_1 = first_stage_op().apply(onprem.mount_pvc(pvc_name, volume_name=volume_name, volume_mount_path=volume_mount_path))
    
    with ParallelFor(server_secret_key) as item:
        second_stage_op(task_1.output, item.ip, item.port, item.key, item.pw).apply(onprem.mount_pvc(pvc_name, volume_name=volume_name, volume_mount_path=volume_mount_path))
        
if __name__ == '__main__':
    kfp.compiler.Compiler().compile(
        my_pipeline,
        "./stt_sent_riffusion_kfp.yaml"
    )
    print("Compelete")