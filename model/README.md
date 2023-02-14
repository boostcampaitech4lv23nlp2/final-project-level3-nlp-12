# 1. 저장소 구조
~~~
.
|-- README.md
|-- _interpolation.py         - Riffusion model interpolation stage
|-- _sum_by_sent.py           - Sentimental analysis stage
|-- oneway_pipeline.py        - Oneyway pipeline for testing
|-- pre_to_stt.py             - First stage of model, input: video | output: sentiments
|-- stt_to_rif.py             - Second stage of model, input: sentiments | output: video with new_bgm
`-- utils.py                  - Utils for model
~~~

# 2. 모델 설명

[ Riffusion ](https://github.com/boostcampaitech4lv23nlp2/final-project-level3-nlp-12/tree/main/riffusion)
- stable diffusion 기반 음악 생성 모델

[ Whisper ](https://github.com/boostcampaitech4lv23nlp2/final-project-level3-nlp-12/tree/main/whisper)
- openai 가 공개한 open-source neural net 으로 speech recognition 부분에서 우수한 성능을 보임

[ Lora ](https://github.com/boostcampaitech4lv23nlp2/final-project-level3-nlp-12/tree/main/LoRA)
- 사전 훈련된 모델 가중치를 동결하고 transformer architecture의 각 계층에 훈련 가능한 rank decomposition matrix를 주입하여 다운스트림 작업에서 피라미터의 수를 크게 줄이는 방법
