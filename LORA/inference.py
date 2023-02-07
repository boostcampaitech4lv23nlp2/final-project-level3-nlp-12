from riffusion.riffusion import riffusion_pipeline
import torch

ck_pt = "asd"
model = riffusion_pipeline.load_checkpoint(
    checkpoint=ck_pt,
    torch_dtype=torch.float16
)
