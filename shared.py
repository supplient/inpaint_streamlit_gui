import streamlit as st

def random_filename():
	import uuid
	return str(uuid.uuid4())


def load_config(config_filepath):
	import json
	with open(config_filepath, mode="r", encoding="utf8") as f:
		configs = json.load(f)
	config = configs[0]
	return config

@st.experimental_singleton
def get_check_prompt_func():
	from check_prompt import check_prompt_length
	return check_prompt_length

def make_image_download_btn(image, label, filename):
	# we have to convert PIL.Image to BytesIO for downloading.
	# see https://discuss.streamlit.io/t/how-to-download-image/3358/10
	from io import BytesIO

	image_buf_im = ""
	if image:
		image_buf = BytesIO()
		image.save(image_buf, format="png")
		image_buf_im = image_buf.getvalue()
	return st.download_button(
		label=label,
		data=image_buf_im,
		file_name=filename,
		mime="image/png",
		disabled=image is None,
	)

def make_prompt_area(default_prompt):
	prompt = st.text_area("prompt", value=default_prompt, key="prompt",
		help="Prompt to guide AI.")
	isprompt_valid, prompt_len, max_prompt_len = get_check_prompt_func()(prompt)
	if isprompt_valid:
		st.success(f"Prompt has {prompt_len} tokens <= {max_prompt_len}.")
	else:
		st.warning(f"Prompt has {prompt_len} tokens > {max_prompt_len}!!!")
	return prompt