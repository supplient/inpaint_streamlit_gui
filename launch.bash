#!/bin/bash
cd /root/inpaint
python init.py
nohup python -m streamlit run st_main.py &