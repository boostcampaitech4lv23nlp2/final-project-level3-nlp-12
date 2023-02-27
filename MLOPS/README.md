# 목차
1. [Intro](#1-intro)
2. [아키텍처 설계 의도](#2-아키텍처-설계-의도)
3. [Kubernetes(K8s)](#3-kubernetesk8s)
4. [BACKEND](#4-backend)

# 1. Intro
![architecture](https://user-images.githubusercontent.com/113088158/218088271-670172ad-b43e-4f20-826c-e9cb15000ca2.png)
# 1.1. 저장소 구조
```
.
├── README.md
├── front                           - webapp frontend
|   └── BGM_project
|       ├── README.md
|       ├── node_modules
|       ├── package-lock.json
|       ├── package.json
|       ├── public
|       ├── src
|       └── Dockerfile              - Front Dockerfile for K8s deployment
├── kubernetes
|   ├── kubeflow
|   |   └── make_pipeline.py        - Kubeflow Pipeline 작성 코드
|   └── yaml
|       ├── back_deployment.yaml    - API 모델 서버 deployment
|       ├── back_service.yaml       - API 모델 서버 service
|       ├── front_deployment.yaml   - webapp deployment
|       ├── front_service.yaml      - webapp service
|       └── pod_pvc.yaml            - Kubeflow pvc 접근용 pod
└── serving
    ├── README.md
    ├── Dockerfile                  - Local Server Dockerfile for K8s deployment
    └── app
        ├── first_stage             - STT와 Sentiment Classifier 서버
        ├── local_main              - local API 서버, Kubeflow
        └── second_stage            - Riffusion 서버
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


# 2. 아키텍처 설계 의도
## 2.1. 모델에 요구되는 리소스가 크다.
* Required VRAM
  * Whisper-large : 10 GB
  * Riffusion : 30 GB
* 생성모델 특성 상 Riffusion 모델의 결과물이 일정하지 않기에 사용자에게 선택권을 주기 위해서는 결과물이 여러개 필요하다.

## 2.2. aistage GPU 서버 리소스 관리가 어렵다.
* 팀원에게 할당된 서버가 개별 컨테이너이기에 통합 리소스 관리가 어렵다.
* K8s를 통해 분리된 팀원들의 서버를 관리하고자 했으나 보안 정책으로 인해 컨테이너 권한을 받지 못하였다. 
  
## 2.3. 모델의 종류가 많으며 의존성이 있기에 관리가 필요함
* 선행 모델의 아웃풋이 후행 모델의 인풋으로 들어가는 의존성이 있기에 모델 파이프라인이 필요하다.
* 프로젝트 기간이 짧기에 유연한 아키텍처 설계가 필요하다. (3주)

## 2.4. 마이크로 서비스 아키텍처
### 2.4.1 특징
* 애플리케이션을 상호 독립적인 최소 구성 요소로 분할하며 API를 통해 서로 통신하는 아키텍처이다.
  * 단일 모듈의 장애에 대해 전체 어플리케이션은 크게 영향을 받지않는다.
  * 각 개별 서비스에서 새로운 기술 스택을 시험하고자 한다면 바로 시작할 수 있다. 
  * 의존 관계가 기존 Monolithic 아키텍처보다 적고 유연하다.

### 2.4.2 사용 이유
* 모델이 무겁고 종류가 많았던 문제 사항 $\to$ 마이크로서비스 아키텍처 적합
* 관리가 힘들고 테스트가 불편하다는 단점 $\to$ K8s로 보완

# 3. Kubernetes(K8s)
## 3.1 특징
- Reproducibility 실행 환경의 일관성 & 독립성
- Job Scheduling 스케줄 관리, 병렬 작업 관리, 유휴 작업 관리
- Auto-healing & Auto-scaling 장애 대응, 트래픽 대응
## 3.2 K8s와 마이크로 서비스
- 자동화된 bin packing : K8s는 컨테이너를 노드에 맞추어 자동으로 할당해주기에 리소스를 효율적으로 사용할 수 있다.
- 자동화된 복구 : K8s는 실패한 컨테이너를 다시 시작하고 교체하는 복구 기능을 지원하기에 마이크로 서비스와 같이 많은 서비스를 관리하기 적합하다.
  
## 3.3 클러스터 구성요소
### 3.3.1 WebFramework
* React, NodeJS, FastAPI 사용
  * 사용이 쉽고, 속도가 빠르기에 마이크로 서비스에 적합한 FastAPI를 사용하였다.
### 3.3.2 Cluster Heath Check
* Prometheus
  * 메트릭 수집, 시각화, 알림, 서비스 디스커버리 기능을 모두 제공하는 오픈 소스 모니터링 시스템
* Grafana
    * 시계열 메트릭 데이터 시각화 대시보드이며 Promethues 메트릭 대시보드로 사용
* OpenLens
    * kubenetes를 GUI로 관리 및 모니터링 가능

### 3.3.3. Kubeflow 
* Kubernetes 환경에서 ML 워크플로의 머신러닝 모델 학습부터 배포 단계까지 모든 작업에 필요한 도구와 환경을 제공하는 플랫폼
* **실행 환경의 일관성과 독립성을 유지하기 위해**
    * STT, Sentiment Classifier 모델과 Riffusion 모델이 2단계로 나뉘어져 여러개의 서버에서 동시에 실행이 되어야 한다.
* **다양한 실험을 쉽게 하기 위해**
    * model이 필요한 모든 작업을 재사용 가능한 component로 나누고 쿠버네티스 위에서 pod로 연결되는 과정을 자동화한다.

## 3.4. Kubeflow Pipeline
![pipeline](https://user-images.githubusercontent.com/113088158/218088118-77d6223f-29db-4b37-9689-480d10d104c7.png)
### 3.4.1. Pipeline
* 1st: STT → Sentiment Classifier 모델 실행
* 2nd: 4개의 Riffusion 모델을 병렬적으로 실행
    * 서로 다른 4개의 아웃풋 생성
* Pipeline은 Trigger가 되어 aistage 서버(Model 서버)를 실행한다.

## 3.5. 작동 흐름
### 3.5.1. Local Kubernetes (API 서버)
* 사용자 입력 → API 서버에서 request에 대한 sequence key 생성 → Input Video를 Model 서버에 업로드 → sequence key를 파라미터로 Kubeflow Pipeline 실행(Trigger)
### 3.5.2. aistage (Model 서버)
* Kubeflow Pipeline에 따른, Model 서버에 결과물 생성 → 생성된 결과물을 Model 서버에서 클라이언트로 response


# 4. BACKEND
## 4.1. 웹 서버 실행
serving 디렉토리에서 아래 명령어 수행
```
python -m {directory name}
```
## 4.2. 작동 방식
* sequence key를 통해 데이터 식별

# 5. FRONTEND
## 5.1 작동 흐름
* Axios를 통해 입력된 동영상 POST -> 로컬 서버에서 sequence key 반환 -> 해당 키를 통해 BGM이 합쳐진 동영상 GET
