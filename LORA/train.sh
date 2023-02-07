#!/bin/bash
echo "Trainer running"
accelerate launch text_to_image_lora.py \
  --pretrained_model_name_or_path="riffusion/riffusion-model-v1" \
  --dataset_name=$DATASET_NAME \
  --validation_prompt="Validation ON" \
  --output_dir="/opt/ml/final/LORA/output" \
  --train_batch_size=2 \
  --gradient_accumulation_steps=4 \
  --gradient_checkpointing \
  --lr_scheduler="cosine_with_restarts" \
  --lr_warmup_steps=0 \
  --seed=42 \
  --mixed_precision="fp16" \
  --report_to="wandb" \    
