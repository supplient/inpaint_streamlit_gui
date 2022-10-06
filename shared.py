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

def img2bytes(image):
	# we have to convert PIL.Image to BytesIO for downloading.
	# see https://discuss.streamlit.io/t/how-to-download-image/3358/10
	from io import BytesIO
	image_buf = BytesIO()
	image.save(image_buf, format="png")
	return image_buf.getvalue()

def zip_bytes_or_strs(filenames, bytes_or_strs) -> bytes:
	assert(len(filenames) == len(bytes_or_strs))
	from zipfile import ZipFile
	import io
	zip_bytes_io = io.BytesIO()
	with ZipFile(zip_bytes_io, "w") as zip_file:
		for i in range(len(bytes_or_strs)):
			zip_file.writestr(filenames[i], bytes_or_strs[i])
	return zip_bytes_io.getvalue()

def make_image_download_btn(image, label, filename, key=None):
	return st.download_button(
		label=label,
		data=img2bytes(image) if image else "",
		file_name=filename,
		mime="image/png",
		disabled=image is None,
		key=key if key else label,
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