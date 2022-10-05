import torch
import PIL
from diffusers import StableDiffusionImg2ImgPipeline, DDIMScheduler

####################################
# Build pipe
####################################
model_id = "hakurei/waifu-diffusion"
device = "cuda"

pipe = StableDiffusionImg2ImgPipeline.from_pretrained(
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


####################################
# Interface for predicting
####################################
def predict(prompt: str, init_image: PIL.Image, strength: float, num_inference_steps: int, guidance_scale: float, eta: float, generator: torch.Generator, **kwargs) -> PIL.Image:
	''' Args (copied from StableDiffusionInpaintPipeline.__call__):
		prompt (`str` or `List[str]`):
			The prompt or prompts to guide the image generation.
		init_image (`torch.FloatTensor` or `PIL.Image.Image`):
			`Image`, or tensor representing an image batch, that will be used as the starting point for the
			process. This is the image whose masked region will be inpainted.
		strength (`float`, *optional*, defaults to 0.8):
			Conceptually, indicates how much to inpaint the masked area. Must be between 0 and 1. When `strength`
			is 1, the denoising process will be run on the masked area for the full number of iterations specified
			in `num_inference_steps`. `init_image` will be used as a reference for the masked area, adding more
			noise to that region the larger the `strength`. If `strength` is 0, no inpainting will occur.
		num_inference_steps (`int`, *optional*, defaults to 50):
			The reference number of denoising steps. More denoising steps usually lead to a higher quality image at
			the expense of slower inference. This parameter will be modulated by `strength`, as explained above.
		guidance_scale (`float`, *optional*, defaults to 7.5):
			Guidance scale as defined in [Classifier-Free Diffusion Guidance](https://arxiv.org/abs/2207.12598).
			`guidance_scale` is defined as `w` of equation 2. of [Imagen
			Paper](https://arxiv.org/pdf/2205.11487.pdf). Guidance scale is enabled by setting `guidance_scale >
			1`. Higher guidance scale encourages to generate images that are closely linked to the text `prompt`,
			usually at the expense of lower image quality.
		eta (`float`, *optional*, defaults to 0.0):
			Corresponds to parameter eta (η) in the DDIM paper: https://arxiv.org/abs/2010.02502. Only applies to
			[`schedulers.DDIMScheduler`], will be ignored for others.
		generator (`torch.Generator`, *optional*):
			A [torch generator](https://pytorch.org/docs/stable/generated/torch.Generator.html) to make generation
			deterministic.
		output_type (`str`, *optional*, defaults to `"pil"`):
			The output format of the generate image. Choose between
			[PIL](https://pillow.readthedocs.io/en/stable/): `PIL.Image.Image` or `nd.array`.
		return_dict (`bool`, *optional*, defaults to `True`):
			Whether or not to return a [`~pipelines.stable_diffusion.StableDiffusionPipelineOutput`] instead of a
			plain tuple.
	'''
	with torch.autocast("cuda"):
		image = pipe(
			prompt, 
			init_image,
			strength=strength,
			num_inference_steps=num_inference_steps, 
			guidance_scale=guidance_scale, 
			eta=eta, 
			generator=generator,
		)["images"][0]
	return image



