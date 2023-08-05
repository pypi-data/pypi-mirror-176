from setuptools import setup, find_packages

with open("README.md", "r") as f:
    page_description = f.read()

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="package_skimage",
    version="0.0.1",
    author="leody",
    author_email="leody@outlook.com.br",
    description="Image Processing Package using Skimage Dio_me",
    long_description=page_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Leody100/dio-bootcamp-unimedbh-projeto-pacotes-processamento-imagens-python.git",
    packages=find_packages(),
    install_requires=requirements,
    python_requires='>=3.8',
)
