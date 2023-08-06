import setuptools
import os

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="BBSpider",
    version="0.2.4",
    author="ZzxxH",
    author_email="654245529@qq.com",
    description="a web spider",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://www.dailyrecords.xyz/",
    project_urls={
        "Bug Tracker": "https://www.dailyrecords.xyz/",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires = ">=3.6"
)

try:
    import pandas as pd
except ImportError as err:
    print(f"{err}:::未安装模块 pandas ,现在将尝试安装")
    os.system("pip install pandas")

try:
    from bs4 import BeautifulSoup
except ImportError as err:
    print(f"{err}:::未安装模块 bs4 ,现在将尝试安装")
    os.system("pip install bs4")

try:
    import json
except ImportError as err:
    print(f"{err}:::未安装模块 json ,现在将尝试安装")
    os.system("pip install json")

try:
    import numpy as np
except ImportError as err:
    print(f"{err}:::未安装模块 numpy ,现在将尝试安装")
    os.system("pip install numpy")

try:
    import requests
except ImportError as err:
    print(f"{err}:::未安装模块 requests ,现在将尝试安装")
    os.system("pip install requests")

try:
    import time
except ImportError as err:
    print(f"{err}:::未安装模块 time ,现在将尝试安装")
    os.system("pip install time")

try:
    import re
except ImportError as err:
    print(f"{err}:::未安装模块 re ,现在将尝试安装")
    os.system("pip install re")

try:
    import random
except ImportError as err:
    print(f"{err}:::未安装模块 random ,现在将尝试安装")
    os.system("pip install random")

try:
    import jieba
except ImportError as err:
    print(f"{err}:::未安装模块 jieba ,现在将尝试安装")
    os.system("pip install jieba")

try:
    from pyecharts.charts import WordCloud
except ImportError as err:
    print(f"{err}:::未安装模块 pyecharts ,现在将尝试安装")
    os.system("pip install pyecharts")
