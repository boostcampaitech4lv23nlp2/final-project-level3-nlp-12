# 목차
1. 아키텍처 설계 의도
2. Kubernetes
3. BACKEND
   
# 1. 아키텍처 설계 의도
## 1.1. 모델에 요구되는 리소스가 크다.
* Required VRAM
  * Whisper-large : 10 GB
  * Riffusion : 30 GB
* 생성모델 특성 상 Riffusion 모델의 결과물이 일정하지 않기에 사용자에게 선택권을 주기 위해서는 결과물이 여러개 필요하다.

## 1.2. aistage GPU 서버 리소스 관리가 어렵다.
* 팀원에게 할당된 서버가 개별 컨테이너이기에 통합 리소스 관리가 어렵다.
* K8s를 통해 분리된 팀원들의 서버를 관리하고자 했으나 보안 정책으로 인해 컨테이너 권한을 받지 못하였다. 
  
## 1.3. 모델의 종류가 많으며 의존성이 있기에 관리가 필요함
* 선행 모델의 아웃풋이 후행 모델의 인풋으로 들어가는 의존성이 있기에 모델 파이프라인이 필요하다.
* 프로젝트 기간이 짧기에 유연한 아키텍처 설계가 필요하다. (3주)

## 1.4. 마이크로 서비스 아키텍처
### 1.4.1 특징
* 애플리케이션을 상호 독립적인 최소 구성 요소로 분할하며 API를 통해 서로 통신하는 아키텍처이다.
  * 단일 모듈의 장애에 대해 전체 어플리케이션은 크게 영향을 받지않는다.
  * 각 개별 서비스에서 새로운 기술 스택을 시험하고자 한다면 바로 시작할 수 있다. 
  * 의존 관계가 기존 Monolithic 아키텍처보다 적고 유연하다.

### 1.4.2 사용 이유
* 모델이 무겁고 종류가 많았던 문제 사항 $\to$ 마이크로서비스 아키텍처 적합
* 관리가 힘들고 테스트가 불편하다는 단점 $\to$ K8s로 보완

# 2. Kubernetes(K8s)
## 2.1 특징
- Reproducibility 실행 환경의 일관성 & 독립성
- Job Scheduling 스케줄 관리, 병렬 작업 관리, 유휴 작업 관리
- Auto-healing & Auto-scaling 장애 대응, 트래픽 대응
## 2.2 K8s와 마이크로 서비스
- 자동화된 bin packing : K8s는 컨테이너를 노드에 맞추어 자동으로 할당해주기에 리소스를 효율적으로 사용할 수 있다.
- 자동화된 복구 : K8s는 실패한 컨테이너를 다시 시작하고 교체하는 복구 기능을 지원하기에 마이크로 서비스와 같이 많은 서비스를 관리하기 적합하다.
  
## 2.3 클러스터 구성요소
### 2.3.1 WebFramework
* React, NodeJS, FastAPI 사용
  * 사용이 쉽고, 속도가 빠르기에 마이크로 서비스에 적합한 FastAPI를 사용하였다.
### 2.3.2 Cluster Heath Check
* Prometheus
  * asdf
* Grafana
* OpenLens

# 1.1. 저장소 구조
```
.
├── README.md
├── kubeflow
|   └── make_pipeline.py
└── yaml
    ├── back_deployment.yaml
    ├── back_service.yaml
    ├── front_deployment.yaml
    ├── front_service.yaml
    └── pod_pvc.yaml
```
# 1.2. Prerequisites
- 환경 
    - hardware : M1 MacBook Pro 13
    - RAM : 16GB
- `minikube` : `v1.21.12`
- `kubectl` : `v1.21.12`
- `kustomize` : `v3.2.0`
- `helm` : `v3.10.3`
- `Prometheus` : `v2.43.0`
- `Grafana` : `v6.40.4`
- `Kubeflow` : `v1.6`

# 2. BACKEND
## 2.1. 웹 서버 실행
serving 디렉토리에서 아래 명령어 수행
```
python -m {directory name}
```
## 2.2. 저장소 구조
```
.
├── README.md
├── app
|   ├── first_stage             - STT와 Sentiment Clssifier 서버
|   |   ├── __main__.py
|   |   └── main.py
|   ├── local_main              - local API 서버
|   |   ├── __main__.py
|   |   ├── kubestart.py        - kubeflow 실행
|   |   ├── main.py
|   |   └── pipeline.yaml       - kubeflow pipeline
|   └── second_stage            - Riffusion 서버
|       ├── __main__.py
|       └── main.py
├── input                       - 데이터 upload 경로
└── output                      - 모델 output 경로
```