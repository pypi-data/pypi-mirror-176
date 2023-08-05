from setuptools import setup

with open("README.md","r") as f:
  desc=f.read()

setup( 
  name="pydast",
  version="0.0.1",
  author="Kushagra Agarwal",
  author_email="kushagra.agarwal.2709@gmail.com",
  description="Python package providing powerful Data Structures for use",
  long_description=desc,
  long_description_content_type="text/markdown",
  url="https://github.com/ThinkWithKush/PyDaSt",
  classifiers=[
    "Programming Language :: Python :: 3",
    "Operating System :: OS Independent"
  ],
  packages=['pydast'],
  install_requires=[]
)