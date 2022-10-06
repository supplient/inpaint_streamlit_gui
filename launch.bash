#!/bin/bash
cd /root/inpaint
/root/miniconda3/bin/python /root/inpaint/init.py
/root/miniconda3/bin/python -m streamlit run /root/inpaint/st_main.py