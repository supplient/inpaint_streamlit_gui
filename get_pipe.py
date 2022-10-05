import torch
from diffusers import StableDiffusionPipeline, DDIMScheduler

####################################
# Build pipe
####################################
model_id = "hakurei/waifu-diffusion"
device = "cuda"

pipe = StableDiffusionPipeline.from_pretrained(
    model_id,
	cache_dir="./model_cache",
    torch_dtype=torch.float16,
    revision="fp16",
    scheduler=DDIMScheduler(
        beta_start=0.00085,
        beta_end=0.012,
        beta_schedule="scaled_linear",
        clip_sample=False,
        set_alpha_to_one=False,
    ),
)
pipe = pipe.to(device)