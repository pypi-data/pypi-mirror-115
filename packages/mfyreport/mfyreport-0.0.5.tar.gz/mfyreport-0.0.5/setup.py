#-*- coding:utf8 -*- #
#-----------------------------------------------------------------------------------
# ProjectName:   mfyreport
# FileName:     setup
# Author:      MingFeiyang
# Datetime:    2021/8/9 14:23
#-----------------------------------------------------------------------------------

import setuptools
from setuptools import setup, find_packages

"""
with open("README.md", "r",encoding="utf8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="mfyreport",
    version="0.0.5",
    author="MingFeiyang",
    author_email="mfy1102@163.com",
    description="打印报告的库",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mfy68/mfyreport.git",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
"""

with open("README.md", "r", encoding='utf8') as fh:
    long_description = fh.read()

setup(
    name='mfyreport',
    version='0.0.5',
    author='MingFeiyang',
    author_email='mfy1102@163.com',
    url='https://github.com/mfy68/mfyreport.git',
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=["Jinja2==2.10.1", "PyYAML==5.3.1","requests==2.24.0"],
    packages=find_packages(),
    package_data={
        "": ["*.html",'*.md'],
    },
    python_requires='>=3.6',
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
)