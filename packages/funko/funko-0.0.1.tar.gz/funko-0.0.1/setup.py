from setuptools import setup

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="funko",
    version="0.0.1",
    description="Myfuncolandia",
    py_modules=["myfuncs"],
    package_dir={"": "src"},
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=["numpy ~= 1.19.5"],
    url="",
    author="",
    author_email="",
)
