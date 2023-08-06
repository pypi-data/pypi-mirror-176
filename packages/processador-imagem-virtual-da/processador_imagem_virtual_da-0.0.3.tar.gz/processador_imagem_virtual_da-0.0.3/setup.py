from setuptools import setup, find_packages

with open("README.md", "r") as f:
    page_description = f.read()

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="processador_imagem_virtual_da",
    version="0.0.3",
    author="Daniel Hisatugu",
    author_email="daniel.hisatugu@gmail.com",
    description="Pacote de processamento de imagem via Skimage",
    long_description=page_description,
    long_description_content_type="text/markdown",
    url="https://github.com/DanielHisatugu/desafio-python-processador-imagem-virtual",
    packages=find_packages(),
    install_requires=requirements,
    python_requires='>=3.8',
)