#!/bin/bash
echo "Trainer running"
accelerate launch --mixed_precision="fp16" text_to_image_lora.py \
  --pretrained_model_name_or_path="riffusion/riffusion-model-v1" \
  --dataset_name='gwkim22/et_test' \
  --validation_prompt="Validation ON" \
  --output_dir="/opt/ml/final/LORA/output" \
  --train_batch_size=4 \
  --gradient_accumulation_steps=2 \
  --gradient_checkpointing \
  --lr_scheduler="cosine_with_restarts" \
  --lr_warmup_steps=0 \
  --seed=42 \
  --report_to="wandb" 
