from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="is-string",
    version="0.0.6",
    author="Przemek Kaminski",
    author_email="przemyslaw.m.kaminski@gmail.com",
    description="A small Python library to determine if something is a string",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/przemo199/is-string",
    packages=find_packages(),
    install_requires=[],
    keywords=["python", "str", "string"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ]
)
