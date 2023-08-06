import os
import setuptools
from jejudo._version import __version__

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="jejudo", ## 소문자 영단어
    version=__version__, ##
    author="月 ઇ 달토끼 。✿#6777, gawi#9537", ## ex) Sunkyeong Lee
    author_email=None, ##
    description="discord is py-cord bot debug tools", ##
    long_description=long_description,
    long_description_content_type="text/markdown",
    url=None, ##
    packages=["jejudo","jejudo.core","jejudo.repl","jejudo.core.shim","jejudo.core.work"],
    classifiers=[
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    keywords="jishkucord, py-cord, discord, cog, repl, extension, jishku",
    python_requires='>=3.9',
)