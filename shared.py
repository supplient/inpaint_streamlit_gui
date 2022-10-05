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