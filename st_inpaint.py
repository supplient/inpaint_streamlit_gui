import streamlit as st
from streamlit_drawable_canvas import st_canvas
import json
import hashlib
import os
import os.path
from PIL import Image
from PIL.PngImagePlugin import PngInfo
from io import BytesIO
from shared import img2bytes, random_filename, load_config, make_prompt_area, make_image_download_btn, zip_bytes_or_strs
import torch

default_configfile_path = os.path.join(st.session_state["root_dir"], "config/inpaint.json")
default_out_path = os.path.join(st.session_state["root_dir"], "out")

def render():
	## Server
	st.session_state.setdefault("config", load_config(default_configfile_path))
	with st.sidebar.expander("Server", expanded=False):
		config_filepath = st.text_input("config_filepath", value=default_configfile_path,
			help="The config file's path on server.")
		do_load_config = st.button("Load Config")
		if do_load_config:
			st.session_state["config"] = load_config(config_filepath)
			st.info("Config loaded.")

		st.session_state["out_dir"] = st.text_input("out_dir", value=default_out_path, key="out_dir_input",
			help="The directory address on server to save selected pictures.") 
		save_on_select_server = st.checkbox("save_on_select_server", value=False,
			help="If True, image will be saved in `out_dir` when `Select` button is pressed.")
		if save_on_select_server:
			save_metadata_server = st.checkbox("save_metadata_server", value=True,
				help="If True, a json file containing the config when generating the image will be saved, with .meta.json extension.")
	config = st.session_state["config"]
	out_dir = st.session_state["out_dir"]
	pipe = st.session_state["pipe"]

	## Input
	with st.sidebar.expander("Input", expanded=True):
		clear_canvas = st.button("clear_canvas")
		with st.form(key="upload_init_image_form", clear_on_submit=True):
			upload_init_image = st.file_uploader("init_image", type=["png", "jpg", "bmp"], key="upload_init_image_uploader")
			submitted = st.form_submit_button("Submit")
			if submitted:
				st.session_state["sel_image"] = None
				st.session_state["upload_image"] = upload_init_image
		init_mask_json = st.file_uploader("mask_json", type=["json"], key="upload_mask_json_uploader")

		if clear_canvas:
			st.session_state["sel_image"] = None
			st.session_state["upload_image"] = None

	## Tool settings
	with st.sidebar.expander("Tool", expanded=True):
		all_mask = st.checkbox("all_mask", value=False, 
			help="If true, all the picture will be inpainted. i.e. become img2img")
		stroke_width = st.slider("stroke_width", min_value=1, max_value=100, value=30, step=1, key="stroke_width")
		stroke_color = st.radio("stroke_color", options=["white", "black"], index=0, horizontal=True,
			help="White: mask this.  Black: unmask this.  Only the masked part will be inpainted.")
		col_per_row = st.number_input("col_per_row", min_value=1, value=3, step=1, format="%i", key="col_per_row",
			help="How many pictures are shown in the result row?")
		save_on_select = st.checkbox("save_on_select", value=True,
			help="If True, image will be saved upon `Select` is pressed.")

	## Inpaint Settings
	with st.sidebar.expander("Inpaint", expanded=True):
		n = st.number_input("n", min_value=1, value=config["n"], step=1, format="%i", key="n",
			help="How many pictures to generate?")
		if all_mask:
			keep_origin = False
		else:
			keep_origin = st.checkbox("keep_origin", value=config["keep_origin"], key="keep_origin",
				help="If False, the unmasked part will also be modified. Though the change is small, it may be significant after multiple iterations.")
		strength = st.number_input("strength", min_value=0.0, max_value=1.0, value=config["strength"], step=0.01, key="strength",
			help="Repaint strength.")
		num_inference_steps = st.number_input("num_inference_steps", min_value=0, value=config["num_inference_steps"], step=5, format="%i", key="num_inference_steps")
		guidance_scale = st.slider("guidance_scale", min_value=1.0, max_value=50.0, value=config["guidance_scale"], step=0.1, format="%f", key="guidance_scale")
		eta = st.slider("eta", min_value=0.0, max_value=1.0, value=config["eta"], step=0.05, key="eta")
		seed = st.number_input("seed", min_value=0, value=0 if config["seed"] is None else config["seed"], step=1, format="%i", key="seed", 
			help="0 means to use random seed.")



	# Work area
	## Prompt
	prompt = make_prompt_area(config["prompt"])

	## get init_image
	upload_init_image = st.session_state.get("upload_image", default=None)
	sel_init_image = st.session_state.get("sel_image", default=None)

	init_image = None
	if sel_init_image:
		init_image = sel_init_image
	elif upload_init_image:
		init_image = Image.open(upload_init_image)

	## get init_mask_json
	if init_mask_json is None:
		init_mask_json = {}
	else:
		init_mask_json = json.load(init_mask_json)

	## use image's hash to enforce the canvas to re-render
	## see https://github.com/andfanilo/streamlit-drawable-canvas/issues/73
	init_image_hash = hashlib.sha256(init_image.tobytes()).hexdigest() if init_image else "sadjfiojeio"

	## canvas to draw the mesh
	canvas_result = st_canvas(
		fill_color="rgba(0, 0, 0, 0)",  # Fixed fill color with some opacity
		stroke_width=stroke_width,
		stroke_color=stroke_color,
		background_image=init_image,
		background_color="rgba(0, 0, 0, 255)",
		update_streamlit=True,
		width=512 if init_image is None else init_image.size[0],
		height=512 if init_image is None else init_image.size[1],
		initial_drawing=init_mask_json,
		drawing_mode="freedraw",
		display_toolbar=True,
		key="canvas" + init_image_hash,
	)



	# Mask Image
	mask_image = None
	upload_mask_image = st.file_uploader("mask_image", type=["png", "jpg", "bmp"], key="upload_mask_image_uploader")
	if upload_mask_image:
		st.info("Using uploaded mask_image.")
		mask_image = Image.open(upload_mask_image)
		st.image(mask_image, use_column_width="never")
	elif not canvas_result.image_data is None:
		## Convert canvas's mask_image to PIL.Image with mode of 'RGB'
		mask_image = canvas_result.image_data
		mask_image = Image.fromarray(mask_image, mode="RGBA")
		mask_image = mask_image.convert("RGB")



	# Buttons to inpaint and download
	work_btn_cols = st.columns(4)
	with work_btn_cols[0]:
		do_inpaint = st.button(
			label="Inpaint",
		)
	with work_btn_cols[1]:
		make_image_download_btn(init_image, "Download bg", random_filename()+".png")
	with work_btn_cols[2]:
		make_image_download_btn(mask_image, "Download mask image", random_filename()+".png")
	with work_btn_cols[3]:
		json_str = json.dumps(canvas_result.json_data) if canvas_result.json_data else ""
		st.download_button(
			label="Download mask json",
			data= json_str,
			file_name=random_filename()+".mask.json",
			mime="application/json",
			disabled=canvas_result.json_data is None,
		)



	# Inpaint
	if do_inpaint:
		import pipes.inpaint
		# Set Seed
		cuda_seed = torch.Generator(device='cuda')
		manual_seed = seed
		if manual_seed == 0:
			seed = str(cuda_seed.seed())
		else:
			cuda_seed = cuda_seed.manual_seed(manual_seed)

		# Set mask to all white if all_mask is True
		if all_mask:
			mask_image = Image.new(mode="RGB", size=init_image.size, color=(255, 255, 255))

		# Evaluate
		st.session_state["res_images"] = []
		with st.spinner(f"Inpainting... (seed:{seed})"):
			prog_bar = st.progress(0)
			for i in range(n):
				st.session_state["res_images"].append(pipes.inpaint.predict(
					pipe=pipe,
					prompt=prompt,
					init_image=init_image,
					mask_image=mask_image,
					keep_origin=keep_origin,
					strength=strength,
					num_inference_steps=num_inference_steps,
					guidance_scale=guidance_scale,
					eta=eta,
					generator=cuda_seed,
				))
				prog_bar.progress((i+1)/n)

		# Clear zip_file to trigger rezip
		st.session_state["zip_file"] = None
	res_images = st.session_state.get("res_images", default=[])



	# Give download button
	## If there are result images & no zip_file cache
	if len(res_images) > 0 and st.session_state.get("zip_file", None) is None:
		# Do zip
		## Build metadata
		metadata = {
			"n": n,
			"prompt": prompt,
			"strength": strength,
			"num_inference_steps": num_inference_steps,
			"guidance_scale": guidance_scale,
			"eta": eta,
			"seed": seed,
		}
		metadata_str = json.dumps(metadata, indent=4)
		metadata_filename = f"{random_filename()}.meta.json"

		# PIL.Image => bytes
		img_bytes = []
		img_names = []
		for i in range(len(res_images)):
			img_names.append(random_filename() + ".png")
			img_bytes.append(img2bytes(res_images[i]))

		# Make zip
		zip_bytes = zip_bytes_or_strs([*img_names, metadata_filename], [*img_bytes, metadata_str])
		st.session_state["zip_file"] = zip_bytes


	# Buttons to download & Control whether to show results
	cols = st.columns(2)
	with cols[0]:
		st.download_button(
			"Save Results",
			data=st.session_state.get("zip_file", ""),
			file_name="images.zip",
			mime="application/zip",
			disabled=st.session_state.get("zip_file", None) is None,
		)
	with cols[1]:
		show_result = st.checkbox("show_result", value=True,
			help="If True, all generated images will shown.")

	# Show results
	if show_result:
		# Show Results
		sel_btns = [False] * len(res_images)
		if len(res_images) > 0:
			col_number = len(res_images)
			row_number = int((col_number-1) / col_per_row) + 1

			img_index = 0
			for row_ind in range(row_number):
				cols = st.columns(min(col_per_row, col_number))
				col_number -= len(cols)

				for col in cols:
					image = res_images[img_index]
					with col:
						st.image(image, use_column_width="never")
						if save_on_select:
							sel_btns[img_index] = make_image_download_btn(image, "Select & Save", f"{random_filename()}.png", key=f"sel_download_btn_{img_index}")
						else:
							sel_btns[img_index] = st.button("Select", key=f"sel_btn_{img_index}")
						img_index += 1


		# Save & Select
		for i in range(len(sel_btns)):
			# The i-th image is selected
			if sel_btns[i]:
				img = res_images[i]

				if save_on_select_server:
					# Save concerned common
					filename:str = random_filename()

					# Save metadata
					## Build metadata
					metadata = {
						"n": n,
						"prompt": prompt,
						"keep_origin": keep_origin,
						"strength": strength,
						"num_inference_steps": num_inference_steps,
						"guidance_scale": guidance_scale,
						"eta": eta,
						"seed": seed,
					}

					## Save metadata
					if save_metadata_server:
						metadata_file = os.path.join(out_dir, filename+".meta.json")
						st.text("Save metadata_file: " + metadata_file)
						print("Save metadata_file: " + metadata_file)
						with open(metadata_file, mode="w") as f:
							json.dump(metadata, f, indent=4)

					# Save Image
					## Gen filename
					filepath = os.path.join(out_dir, filename+".png")

					## Build Png Metadata
					png_metadata = PngInfo()
					png_metadata.add_text("stable diffusion", json.dumps(metadata))
					
					## Save selected image
					st.text(f"Save image {filepath}")
					print(f"Save image {filepath}")
					img.save(filepath, pnginfo=png_metadata)

				# Select
				st.session_state["sel_image"] = img
				st.session_state["upload_image"] = None
				st.experimental_rerun()
	else: # show_result == False
		# Do not show result
		pass
