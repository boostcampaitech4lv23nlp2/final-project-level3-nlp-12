# 1. LoRA
LoRA란 Low-Rank Adaption of Large Language Models로 Large Language Model의 효율적인 Fine Tuning을 위해 고안된 방법론입니다.
<br>
처음 LoRA는 LLM을 위해 고안되었지만 다양한 분야에 적용될 수 있음이 확인되었습니다. 
<br>
이는 Stable Diffusion 모델의 Image representation과 prompt를 연결하는 cross-attention layers에도 적용이 될 수 있었습니다.
<br>
이를 통해 Stable Diffusion with LoRA 모델은 다음과 같은 장점을 얻을 수 있습니다.
<br>
1. Training is much faster, as already discussed.
2. Compute requirements are lower. We could create a full fine-tuned model in a 2080 Ti with 11 GB of VRAM!
3. Trained weights are much, much smaller : Because the original model is frozen and we inject new layers to be trained, we can save the weights for the new layers as a single file that weighs in at ~3 MB in size. This is about one thousand times smaller than the original size of the UNet model!
<br>
발췌: https://huggingface.co/blog/lora

# 2. Riffusion with LoRA
Stable Diffusion 모델을 base로 하는 Riffusion 모델에도 이를 적용할 수있습니다.
~~~sh
# Train Riffusion with LoRA
./train.sh
~~~
해당 shell script를 통해 Riffusion Checkpoint를 저희가 만든 Dataset으로 학습할 수 있습니다.
<br>
이를 통해 만들어진 **"pytorch_lora_weights.bin"** 를 RiffusionPipeline의 unet에 붙임으로써 학습된 LoRA를 사용할 수 있습니다.
~~~python
pipeline.unet.load_attn_procs("pytorch_lora_weights.bin")
model = pipeline.to(device)
~~~
