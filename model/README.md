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
