import streamlit as st


btn = st.download_button(
	"Download",
	data="OKK",
	file_name="test.txt",
	mime="text/plain",
)

if btn:
	print("Downloaded")