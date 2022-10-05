from faulthandler import disable
import streamlit as st
from streamlit_drawable_canvas import st_canvas
import json
import hashlib
import os
import os.path
from PIL import Image
from PIL.PngImagePlugin import PngInfo
from io import BytesIO
from shared import load_config, make_prompt_area, random_filename
import torch


def render():
	## Server
	st.session_state.setdefault("config", load_config("./config/txt2img.json"))
	with st.sidebar.expander("Server", expanded=False):
		config_filepath = st.text_input("config_filepath", value="./config/txt2img.json",
			help="The config file's path on server.")
		do_load_config = st.button("Load Config")
		if do_load_config:
			st.session_state["config"] = load_config(config_filepath)
			st.info("Config loaded.")
	config = st.session_state["config"]
	pipe = st.session_state["pipe"]

	## Tool settings
	with st.sidebar.expander("Tool", expanded=True):
		col_per_row = st.number_input("col_per_row", min_value=1, value=3, step=1, format="%i", key="col_per_row",
			help="How many pictures are shown in the result row?")
		save_metadata = st.checkbox("save_metadata", value=True,
			help="If True, a json file containing the config when generating the image will be saved, with .meta.json extension.")
		show_result = st.checkbox("show_result", value=False,
			help="If True, all generated images will shown.")

	## txt2img Settings
	with st.sidebar.expander("Inpaint", expanded=True):
		n = st.number_input("n", min_value=1, value=config["n"], step=1, format="%i", key="n",
			help="How many pictures to generate?")
		width = st.number_input("width", min_value=64, value=config["width"], step=64, format="%i", key="width")
		height = st.number_input("height", min_value=64, value=config["height"], step=64, format="%i", key="height")
		num_inference_steps = st.slider("num_inference_steps", min_value=0, max_value=100, value=config["num_inference_steps"], step=5, format="%i", key="num_inference_steps")
		guidance_scale = st.slider("guidance_scale", min_value=1.0, max_value=50.0, value=config["guidance_scale"], step=0.5, format="%f", key="guidance_scale")
		eta = st.slider("eta", min_value=0.0, max_value=1.0, value=config["eta"], step=0.05, key="eta")
		seed = st.number_input("seed", min_value=0, value=0 if config["seed"] is None else config["seed"], step=1, format="%i", key="seed", 
			help="0 means to use random seed.")


	# Work area
	## Prompt
	prompt = make_prompt_area(config["prompt"])

	## Button to draw
	do_draw = st.button(
		label="Draw",
	)
	
	import pipes.txt2img

	if do_draw:
		# Set Seed
		cuda_seed = torch.Generator(device='cuda')
		manual_seed = seed
		if manual_seed == 0:
			seed = str(cuda_seed.seed())
		else:
			cuda_seed = cuda_seed.manual_seed(manual_seed)

		# Evaluate
		st.session_state["res_images"] = []
		with st.spinner(f"Drawing... (seed:{seed})"):
			prog_bar = st.progress(0)
			for i in range(n):
				st.session_state["res_images"].append(pipes.txt2img.predict(
					pipe=pipe,
					prompt=prompt,
					height=height,
					width=width,
					num_inference_steps=num_inference_steps,
					guidance_scale=guidance_scale,
					eta=eta,
					generator=cuda_seed,
				))
				prog_bar.progress((i+1)/n)
			# Clear zip_file to trigger rezip
			st.session_state["zip_file"] = None
	res_images = st.session_state.get("res_images", default=[])


	# Zip result images
	def ZipImages(images):
		## Build metadata
		metadata = {
			"n": n,
			"prompt": prompt,
			"height": height,
			"width": width,
			"num_inference_steps": num_inference_steps,
			"guidance_scale": guidance_scale,
			"eta": eta,
			"seed": seed,
		}

		## zip images & metadata
		from zipfile import ZipFile
		import io
		zip_bytes_io = io.BytesIO()
		with ZipFile(zip_bytes_io, "w") as zip_file:
			# metadata
			if save_metadata:
				zip_file.writestr(f"{random_filename()}.meta.json", json.dumps(metadata, indent=4))

			# imgs
			for i in range(len(images)):
				imgname = random_filename() + ".png"
				img = images[i]

				# PIL.Image => io.BytesIO
				img_bytes_io = io.BytesIO()
				img.save(img_bytes_io, "PNG")

				# Write to zip
				zip_file.writestr(imgname, img_bytes_io.getvalue())
		return zip_bytes_io.getvalue()

	if len(res_images) > 0 and st.session_state.get("zip_file", None) is None:
		st.session_state["zip_file"] = ZipImages(res_images)

	# Button to download
	st.download_button(
		"Save",
		data=st.session_state.get("zip_file", ""),
		file_name="images.zip",
		mime="application/zip",
		disabled=st.session_state.get("zip_file", None) is None,
	)


	# Result Images
	if len(res_images) > 0 and show_result:
		col_number = len(res_images)
		row_number = int((col_number-1) / col_per_row) + 1

		img_index = 0
		for row_ind in range(row_number):
			cols = st.columns(min(col_per_row, col_number))
			col_number -= len(cols)

			for col in cols:
				col.image(res_images[img_index], use_column_width="never")
				img_index += 1

