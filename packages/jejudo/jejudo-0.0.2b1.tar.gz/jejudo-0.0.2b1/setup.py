import os
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="jejudo", ## 소문자 영단어
    version="0.0.2b1", ##
    author="月 ઇ 달토끼 。✿#6777", ## ex) Sunkyeong Lee
    author_email=None, ##
    description="discord is py-cord bot debug tools", ##
    long_description=long_description,
    long_description_content_type="text/markdown",
    url=None, ##
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.9',
)