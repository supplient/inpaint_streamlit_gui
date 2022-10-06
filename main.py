import os.path
import sys
sys.path.insert(0, os.path.abspath("./diffusers/src"))

import json
import PIL
from PIL.PngImagePlugin import PngInfo

print("Loading pytorch...")
import torch

print("Loading pipe...")
from pipes.get_pipe import pipe


def random_filename():
	import uuid
	return str(uuid.uuid4())

def get_image_from_user(name, last_image_path):
	while True:
		print(f"Please specify {name}(empty if use the last one)(d to open a file explorer to select):")
		if not last_image_path is None:
			print(f"[{last_image_path}]")
		image_path = input(">>> ")

		if image_path == "d":
			import tkinter.filedialog
			image_path = tkinter.filedialog.askopenfilename(filetypes=[("Image", ".png .jpeg .bmp .gif")])
			if image_path == "":
				continue
			print(f"Select {image_path}.")
		elif image_path == "":
			image_path = last_image_path

		try:
			image = PIL.Image.open(image_path)
		except OSError:
			print("Cannot open file: " + image_path)
			continue
		break
	return (image, image_path)


last_config_filepath: str = None
last_sel_mode: str = None
last_inpaint_init_image_path: str = None
last_inpaint_mask_image_path: str = None
last_img2img_init_image_path: str = None
while True:
	####################################
	# Get config file
	####################################
	quit_flag = False
	while True:
		print("Please specify config file(empty if use the last one)(q for quit):")
		if not last_config_filepath is None:
			print(f"[{last_config_filepath}]")
		config_filepath = input(">>> ")
		if config_filepath == "":
			config_filepath = last_config_filepath
		elif config_filepath == "q":
			quit_flag = True
			break
		print("Using config file: " + config_filepath)
		last_config_filepath = config_filepath

		try:
			with open(config_filepath, mode="r", encoding="utf8") as f:
				configs = json.load(f)
		except OSError:
			print("Cannot open file " + config_filepath)
			continue
		break
	if quit_flag:
		break


	####################################
	# Select mode
	####################################
	while True:
		print('''Select mode(empty if use the last one):
0. txt2img
1. inpaint
2. img2img''')
		if not last_sel_mode is None:
			print(f"[{last_sel_mode}]")
		sel_mode = input(">>> ")
		if sel_mode == "":
			sel_mode = last_sel_mode
		if not sel_mode in ["0", "1", "2"]:
			print(f"Invalid mode: {sel_mode}")
			continue
		last_sel_mode = sel_mode
		break



	####################################
	# vars shared between modes
	####################################
	pipe_func: None
	kwargs: dict = {}
	

	####################################
	# Prepare evaluting for each mode
	####################################
	# txt2img
	if sel_mode == "0":
		import pipes.txt2img as txt2img
		pipe_func = txt2img.predict
	# inpaint
	elif sel_mode == "1":
		init_image, last_inpaint_init_image_path = get_image_from_user("init image", last_inpaint_init_image_path)
		kwargs["init_image"] = init_image

		mask_image, last_inpaint_mask_image_path = get_image_from_user("mask image", last_inpaint_mask_image_path)
		kwargs["mask_image"] = mask_image

		import pipes.inpaint as inpaint
		pipe_func = inpaint.predict
	# img2img
	elif sel_mode == "2":
		init_image, last_img2img_init_image_path = get_image_from_user("init image", last_img2img_init_image_path)
		kwargs["init_image"] = init_image

		import pipes.img2img as img2img
		pipe_func = img2img.predict



	#################################
	# Work on each config
	#################################
	for config_index in range(len(configs)):
		config = configs[config_index]
		print(f"Config {config_index}/{len(configs)}: {config.get('name', '')}")


		#################################
		# Set Seed
		#################################
		cuda_seed = torch.Generator(device='cuda')
		manual_seed = config["seed"]
		if manual_seed is None:
			config["seed"] = str(cuda_seed.seed())
		else:
			cuda_seed = cuda_seed.manual_seed(manual_seed)



		#################################
		# Fill arguments
		#################################
		for key in ["prompt", "height", "width", "keep_origin", "strength", "num_inference_steps", "guidance_scale", "eta"]:
			if key in config.keys():
				kwargs[key] = config[key]
		kwargs["pipe"] = pipe
		kwargs["generator"] = cuda_seed



		#################################
		# Build Png Metadata
		#################################
		metadata = PngInfo()
		metadata.add_text("stable diffusion", json.dumps(config))



		#################################
		# Save Results
		#################################
		# Output directory
		import os.path
		out_dir = "./out"

		# Save metadata
		metadata_filename:str = None
		if config["name"] is None:
			metadata_filename = random_filename()
		else:
			metadata_filename = config["name"]
		metadata_file = os.path.join(out_dir, metadata_filename+".txt")
		print("metadata_file: " + metadata_file)
		with open(metadata_file, mode="w") as f:
			json.dump(config, f, indent=4)

		# Evalute & Save Image
		for i in range(config["n"]):
			## Gen filename
			filename:str = None
			if config["name"] is None:
				filename = random_filename()
			else:
				filename = config["name"]
				if i != 0:
					filename += "_" + str(i)
			filepath = os.path.join(out_dir, filename+".png")
			print(f"{i}/{config['n']}: {filepath}")

			## Evaluate
			res_image: PIL.Image = pipe_func(**kwargs)
			
			## Save result image
			res_image.save(filepath, pnginfo=metadata)