import TNE
import codecs
from setuptools import setup
from pathlib import Path

TNE_VERSION = "0.0.1"
DOWNLOAD_URL = ""


setup(
    name="TNE",
    packages=['TNE'],
    version=TNE_VERSION,
    description="",
    long_description='''long''',
    license="MIT",
    author="Hou",
    author_email="hhhoujue@gmail.com",
    url="",
    download_url=DOWNLOAD_URL,
    keywords=["sick"],
    install_requires=[],
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Natural Language :: English",
    ],
    python_requires=">=3.7",
)
