from setuptools import setup, find_packages

with open("README.md", "r") as f:
    page_description = f.read()

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="img-processing-tm",
    version="0.0.1",
    author="thaiismeneses",
    author_email="thaisfmeneses@gmail.com",
    description="Image processing Package using Skimage",
    long_description=page_description,
    long_description_content_type="text/markdown",
    url="https://github.com/thaiismeneses/Bootcamp_DataScience/image_procesing_package",
    packages=find_packages(),
    install_requires=requirements,
    python_requires='>=3.8',
)
