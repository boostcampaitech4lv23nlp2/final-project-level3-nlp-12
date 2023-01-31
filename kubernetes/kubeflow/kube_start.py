import kfp
import requests

def start():
    USERNAME = "user@example.com"
    PASSWORD = "12341234"
    NAMESPACE = "kubeflow-user-example-com"
    HOST = "http://localhost:8080" 

    session = requests.Session()
    response = session.get(HOST)

    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
    }

    data = {"login": USERNAME, "password": PASSWORD}
    session.post(response.url, headers=headers, data=data)
    session_cookie = session.cookies.get_dict()["authservice_session"]

    client = kfp.Client(
        host=f"{HOST}/pipeline",
        namespace=f"{NAMESPACE}",
        cookies=f"authservice_session={session_cookie}",
    )
    demo = 'c0342f52-2cb7-46ab-b0c7-49cd686b9fe1'

    exec_run = client.run_pipeline(experiment_id=demo, job_name="test", pipeline_package_path="./kube_p_pipeline.yaml", enable_caching=False, params={'value_1':1})

    # Run이 완료될 때까지 기다렸다가 결과를 리턴합니다.
    print(client.wait_for_run_completion(run_id=exec_run.id, timeout=345600))