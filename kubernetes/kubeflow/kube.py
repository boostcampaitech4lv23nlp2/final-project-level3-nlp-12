import kfp
from kfp.components import create_component_from_func
from kfp import onprem

def jd(value_1: int) -> int:
    import paramiko
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect('101.101.209.53', username='root', port='2234', key_filename='/var/data/jd_key')

    stdin, stdout, stderr = ssh.exec_command(f'cd /opt/ml/input/code && python test.py {value_1}')
    ret = stdout.readlines()
    ret = int(*ret)
    stdin.close()
    ssh.close()

    return ret

def sol(value_1: int) -> int:
    import paramiko
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect('118.67.133.198', username='root', port='2242', key_filename='/var/data/sol_key',password="1234")

    stdin, stdout, stderr = ssh.exec_command(f'cd /opt/ml/final/serving_test && python test.py {value_1}')
    ret = stdout.readlines()
    ret = int(*ret)
    stdin.close()
    ssh.close()

    return ret

jd_op = create_component_from_func(jd, packages_to_install=['paramiko==3.0.0'])
sol_op = create_component_from_func(sol, packages_to_install=['paramiko==3.0.0'])

from kfp.dsl import pipeline

@pipeline(name="test_pipeline")
def my_pipeline(value_1: int):
    pvc_name="kfpvc"
    volume_name="pipeline"
    volume_mount_path="var/data"
    task_1 = jd_op(value_1).apply(onprem.mount_pvc(pvc_name, volume_name=volume_name, volume_mount_path=volume_mount_path))
    task_2 = sol_op(task_1.output).apply(onprem.mount_pvc(pvc_name, volume_name=volume_name, volume_mount_path=volume_mount_path))

if __name__ == '__main__':
    kfp.compiler.Compiler().compile(
        my_pipeline,
        "./kube_pipeline.yaml"
    )
    print("Compelete")