import torch
import streamlit as st
from diffusers import StableDiffusionPipeline, DDIMScheduler

####################################
# Build pipe
####################################
model_id = "hakurei/waifu-diffusion"
device = "cuda"

import os.path
model_cache_dir = "./model_cache"

pipe = StableDiffusionPipeline.from_pretrained(
    model_id,
	cache_dir=model_cache_dir,
    torch_dtype=torch.float16,
    revision="fp16",
    local_files_only=True,
    scheduler=DDIMScheduler(
        beta_start=0.00085,
        beta_end=0.012,
        beta_schedule="scaled_linear",
        clip_sample=False,
        set_alpha_to_one=False,
    ),
)
pipe = pipe.to(device)