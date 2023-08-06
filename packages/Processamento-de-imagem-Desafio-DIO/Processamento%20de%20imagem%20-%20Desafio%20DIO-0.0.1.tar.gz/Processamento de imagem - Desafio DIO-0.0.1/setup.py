from setuptools import setup, find_packages

with open("README.md", "r") as f:
    page_description = f.read()

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="Processamento de imagem - Desafio DIO",
    version="0.0.1",
    author="Gabrielli",
    description="Image Processing Package using Skimage",
    long_description=page_description,
    long_description_content_type="text/markdown",
    url="https://github.com/gabriellivieira/Bootcamp_data_science/tree/main/desafios/Pacotes_Processamento_Imagem_Python",
    packages=find_packages(),
    install_requires=requirements,
    python_requires='>=3.8',
)