* 命令行：`python main.py`
* GUI: `streamlit run st_main.py`
* config生成：`python build_config.py`

# 部署
``` bash
mkdir /root/inpaint
git clone https://github.com/supplient/inpaint_streamlit_gui.git /root/inpaint
pip install /root/inpaint/requirements.txt
# Copy model to model_cache
bash /root/inpaint/install.bash
```

端口更改：修改`.streamlit/config.toml`