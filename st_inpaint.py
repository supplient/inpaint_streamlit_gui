import streamlit as st
from streamlit_drawable_canvas import st_canvas
import json
import hashlib
from PIL import Image
from PIL.PngImagePlugin import PngInfo
from io import BytesIO
from random_filename import random_filename

# Gloabl Page Config
st.set_page_config(page_title="Inpaint", layout="wide")

# A place to information
info_bar = st.empty()

# Long time import
info_bar.info("Loading pytorch...")
import torch
info_bar.empty()

# Sidebar
## Server
def LoadConfig(config_filepath):
	with open(config_filepath, mode="r", encoding="utf8") as f:
		configs = json.load(f)
	config = configs[0]
	return config
st.session_state.setdefault("config", LoadConfig(r".\config\inpaint.json"))
with st.sidebar.expander("Server", expanded=False):
	config_filepath = st.text_input("config_filepath", value=r".\config\inpaint.json",
		help="The config file's path on server.")
	do_load_config = st.button("Load Config")
	if do_load_config:
		st.session_state["config"] = LoadConfig(config_filepath)
		st.info("Config loaded.")

	out_dir = st.text_input("out_dir", value="./out/progress", 
		help="The directory address on server to save selected pictures.") 
config = st.session_state["config"]

## Input
with st.sidebar.expander("Input", expanded=True):
	clear_canvas = st.button("clear_canvas")
	with st.form(key="upload_init_image_form", clear_on_submit=True):
		upload_image = st.file_uploader("init_image", type=["png", "jpg", "bmp"], key="upload_init_image_uploader")
		submitted = st.form_submit_button("Submit")
		if submitted:
			st.session_state["sel_image"] = None
			st.session_state["upload_image"] = upload_image
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
	save_metadata = st.checkbox("save_metadata", value=True,
		help="If True, a json file containing the config when generating the image will be saved, with .meta.json extension.")

## Inpaint Settings
@st.experimental_singleton
def get_check_prompt_func():
	from check_prompt import check_prompt_length
	return check_prompt_length

with st.sidebar.expander("Inpaint", expanded=True):
	### Prompt Setting
	prompt = st.text_area("prompt", value=config["prompt"], key="prompt",
		help="Prompt to guide AI.")
	isvalid, prompt_len, max_prompt_len = get_check_prompt_func()(prompt)
	if isvalid:
		st.success(f"Prompt has {prompt_len} tokens <= {max_prompt_len}.")
	else:
		st.warning(f"Prompt has {prompt_len} tokens > {max_prompt_len}!!!")

	### Other Settings
	n = st.number_input("n", min_value=1, value=config["n"], step=1, format="%i", key="n",
		help="How many pictures to generate?")
	if all_mask:
		keep_origin = False
	else:
		keep_origin = st.checkbox("keep_origin", value=config["keep_origin"], key="keep_origin",
			help="If False, the unmasked part will also be modified. Though the change is small, it may be significant after multiple iterations.")
	strength = st.slider("strength", min_value=0.0, max_value=1.0, value=config["strength"], step=0.05, key="strength",
		help="Repaint strength.")
	num_inference_steps = st.slider("num_inference_steps", min_value=0, max_value=100, value=config["num_inference_steps"], step=5, format="%i", key="num_inference_steps")
	guidance_scale = st.slider("guidance_scale", min_value=1.0, max_value=50.0, value=config["guidance_scale"], step=0.5, format="%f", key="guidance_scale")
	eta = st.slider("eta", min_value=0.0, max_value=1.0, value=config["eta"], step=0.05, key="eta")
	seed = st.number_input("seed", min_value=0, value=0 if config["seed"] is None else config["seed"], step=1, format="%i", key="seed", 
		help="0 means to use random seed.")



# Work area
## get init_image
upload_image = st.session_state.get("upload_image", default=None)
sel_image = st.session_state.get("sel_image", default=None)

init_image = None
if sel_image:
	init_image = sel_image
elif upload_image:
	init_image = Image.open(upload_image)

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

## Convert mask_image to PIL.Image with mode of 'RGB'
mask_image = None
if not canvas_result.image_data is None:
	mask_image = canvas_result.image_data
	mask_image = Image.fromarray(mask_image, mode="RGBA")
	mask_image = mask_image.convert("RGB")

## Buttons to inpaint and download
work_btn_cols = st.columns(4)
with work_btn_cols[0]:
	do_inpaint = st.button(
		label="Inpaint",
	)
with work_btn_cols[1]:
	# we have to convert PIL.Image to BytesIO for downloading.
	# see https://discuss.streamlit.io/t/how-to-download-image/3358/10
	init_image_buf_im = ""
	if init_image:
		init_image_buf = BytesIO()
		init_image.save(init_image_buf, format="png")
		init_image_buf_im = init_image_buf.getvalue()
	st.download_button(
		label="Download bg",
		data=init_image_buf_im,
		file_name=random_filename()+".png",
		mime="image/png",
		disabled=init_image is None,
	)
with work_btn_cols[2]:
	mask_image_buf_im = ""
	if mask_image:
		mask_image_buf = BytesIO()
		mask_image.save(mask_image_buf, format="png")
		mask_image_buf_im = mask_image_buf.getvalue()
	st.download_button(
		label="Download mask image",
		data=mask_image_buf_im,
		file_name=random_filename()+".mask.png",
		mime="image/png",
		disabled=mask_image is None,
	)
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
@st.experimental_singleton
def GetPipe():
	from pipes.get_pipe import pipe
	return pipe
import pipes.inpaint

if do_inpaint:
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
				pipe=GetPipe(),
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
		# Rerun to remove the progress bar
		st.experimental_rerun()



# Results
res_images = st.session_state.get("res_images", default=[])
sel_btns = [False] * len(res_images)
if len(res_images) > 0:
	col_number = len(res_images)
	row_number = int((col_number-1) / col_per_row) + 1

	img_index = 0
	for row_ind in range(row_number):
		cols = st.columns(min(col_per_row, col_number))
		col_number -= len(cols)

		for col in cols:
			col.image(res_images[img_index], use_column_width="never")
			sel_btns[img_index] = col.button("Select", key=f"sel_btn_{img_index}")
			img_index += 1


# Save & Select
for i in range(len(sel_btns)):
	if sel_btns[i]:
		img = res_images[i]

		# Save concerned common
		import os.path
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
		if save_metadata:
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
