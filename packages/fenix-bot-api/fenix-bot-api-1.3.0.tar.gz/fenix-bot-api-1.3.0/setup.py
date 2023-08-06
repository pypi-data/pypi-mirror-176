from setuptools import find_packages, setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="fenix-bot-api",
    version="1.3.0",
    author="Carlettos",
    author_email="carlettos.fem@gmail.com",
    description="Common methods and classes used between fenix's bots",
    license="GNU GPL v3",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitarra.cl/kako3000/fenix-bot-api",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent"],
    packages=find_packages(),
    pythor_requires=">=3.7"
)