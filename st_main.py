from pydoc import getpager
import streamlit as st
from streamlit_drawable_canvas import st_canvas
import json
import hashlib
import os
import os.path
from PIL import Image
from PIL.PngImagePlugin import PngInfo
from io import BytesIO
from shared import random_filename

# Change work dir
root_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(root_dir)

# Gloabl Page Config
st.set_page_config(page_title="Inpaint", layout="wide")

# A place to information
info_bar = st.empty()

# Long time import
info_bar.info("Loading pytorch...")
import torch
info_bar.empty()

# Sidebar
## Mode
mode = st.sidebar.radio("mode", ["txt2img", "inpaint"], index=0)


# Mode Select
@st.experimental_singleton
def GetPipe():
	from pipes.get_pipe import pipe
	return pipe
st.session_state["pipe"] = GetPipe()


if mode == "inpaint":
	import st_inpaint
	st_inpaint.render()
elif mode == "txt2img":
	import st_txt2img
	st_txt2img.render()
