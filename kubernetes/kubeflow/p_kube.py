import kfp
from kfp.components import create_component_from_func
from kfp import onprem

def first_stage(value_1: int) -> int:
    import paramiko
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect('101.101.209.53', username='root', port='2234', key_filename='/var/data/jd_key')

    stdin, stdout, stderr = ssh.exec_command(f'cd /opt/ml/code && python test.py {value_1}')
    ret = stdout.readlines()
    ret = int(*ret)
    stdin.close()
    ssh.close()

    return ret

def second_stage(value_1: int, ip: str, port: str, key: str, pw: str) -> str:
    import paramiko
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(ip, username='root', port=port, key_filename=f'/var/data/{key}_key',password=pw)

    stdin, stdout, stderr = ssh.exec_command('echo hi')
    ret = stdout.readlines()
    ret = str(ret)
    stdin.close()
    ssh.close()

    return ret

first_stage_op = create_component_from_func(first_stage, packages_to_install=['paramiko==3.0.0'])
second_stage_op = create_component_from_func(second_stage, packages_to_install=['paramiko==3.0.0'])

from kfp.dsl import pipeline
from kfp.dsl import ParallelFor

@pipeline(name="test_pipeline")
def my_pipeline(value_1: int):
    pvc_name="kfpvc"
    volume_name="pipeline"
    volume_mount_path="var/data"

    gw = {'ip': '118.67.133.154', 'port': '2239', 'key': 'gw', 'pw' : '1263'}
    yc = {'ip': '27.96.134.124', 'port': '2238', 'key': 'yc', 'pw' : '0801'}
    sol = {'ip': '118.67.133.198', 'port': '2242', 'key': 'sol', 'pw' : '1234'}
    dw = {'ip': '118.67.142.47', 'port': '2233', 'key': 'dw', 'pw' : 'eks3242'}
    my_dict = [gw,yc,sol,dw]

    task_1 = first_stage_op(value_1).apply(onprem.mount_pvc(pvc_name, volume_name=volume_name, volume_mount_path=volume_mount_path))
    
    with ParallelFor(my_dict) as item:
        second_stage_op(task_1.output, item.ip, item.port, item.key, item.pw).apply(onprem.mount_pvc(pvc_name, volume_name=volume_name, volume_mount_path=volume_mount_path))
        
if __name__ == '__main__':
    kfp.compiler.Compiler().compile(
        my_pipeline,
        "./kube_p_pipeline.yaml"
    )
    print("Compelete")