import os.path
from setuptools import setup

HERE = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(HERE, "README.md")) as fid:
    README = fid.read()

setup(
    name="FSCLI",
    version="3.0.0",
    description="FSCLI is a module that simplifies starting, stopping & deleting servers based on server_id and email.",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/fluidstackio/fscli.git",
    author="Abhisar Anand, Srinivas Sriram",
    author_email="abhisar.muz@gmail.com, srinivassriram06@gmail.com",
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
    ],
    packages=["fscli"],
    include_package_data=True,
    install_requires=[
        "requests"
    ],
    entry_points={"console_scripts": ["fscli=fscli.__main__:main"]},
)
