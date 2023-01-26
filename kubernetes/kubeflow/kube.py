import kfp
from kfp.components import create_component_from_func
from kfp import onprem

def first_stage(value_1: int) -> int:
    import paramiko
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect('101.101.209.53', username='root', port='2234', key_filename='/var/data/first_stage_key')

    stdin, stdout, stderr = ssh.exec_command(f'cd /opt/ml/input/code && python test.py {value_1}')
    ret = stdout.readlines()
    ret = int(*ret)
    stdin.close()
    ssh.close()

    return ret

def second_stage(value_1: int) -> int:
    import paramiko
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect('118.67.133.198', username='root', port='2242', key_filename='/var/data/second_stage_key',password="1234")

    stdin, stdout, stderr = ssh.exec_command(f'cd /opt/ml/final/serving_test && python test.py {value_1}')
    ret = stdout.readlines()
    ret = int(*ret)
    stdin.close()
    ssh.close()

    return ret

first_stage_op = create_component_from_func(first_stage, packages_to_install=['paramiko==3.0.0'])
second_stage_op = create_component_from_func(second_stage, packages_to_install=['paramiko==3.0.0'])

from kfp.dsl import pipeline

@pipeline(name="test_pipeline")
def my_pipeline(value_1: int):
    pvc_name="kfpvc"
    volume_name="pipeline"
    volume_mount_path="var/data"
    task_1 = first_stage_op(value_1).apply(onprem.mount_pvc(pvc_name, volume_name=volume_name, volume_mount_path=volume_mount_path))
    task_2 = second_stage_op(task_1.output).apply(onprem.mount_pvc(pvc_name, volume_name=volume_name, volume_mount_path=volume_mount_path))

if __name__ == '__main__':
    kfp.compiler.Compiler().compile(
        my_pipeline,
        "./kube_pipeline.yaml"
    )
    print("Compelete")