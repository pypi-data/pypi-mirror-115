from os import path

import yaml
from setuptools import setup

name = path.abspath(path.dirname(__file__)).split("/")[-1]

with open("README.md", "r") as fh:
    long_description = fh.read()

if path.exists("requirements.txt"):
    with open("requirements.txt", "r") as f:
        requirements = f.readlines()
else:
    requirements = []

with open("config.yml", "r") as stream:
    configs = yaml.safe_load(stream)

setup(
    name=name,
    long_description=long_description,
    long_description_content_type="text/markdown",
    url=f"https://github.com/mariotaddeucci/packages/python/{name}/",
    author="Mario Taddeucci",
    author_email="mariotaddeucci@gmx.com",
    license="MIT",
    packages=[name],
    zip_safe=False,
    install_requires=requirements,
    **configs,
)
