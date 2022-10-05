import os
import os.path

root_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(root_dir)

import pathlib

pathlib.Path("./model_cache").mkdir(parents=True, exist_ok=True)
pathlib.Path("./out").mkdir(parents=True, exist_ok=True)