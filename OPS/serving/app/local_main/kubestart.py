import kfp
import requests

def start(count: int):
    USERNAME = ""
    PASSWORD = ""
    NAMESPACE = ""
    HOST = ""

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

    demo = ""
    path = ""
    exec_run = client.run_pipeline(
        experiment_id=demo, job_name="signal", pipeline_package_path=path, enable_caching=False, params={"count": count}
    )

    # Run이 완료될 때까지 기다렸다가 결과를 리턴합니다.
    client.wait_for_run_completion(run_id=exec_run.id, timeout=345600)
