from setuptools import setup, find_packages

with open("README.md", "r") as f:
    page_description = f.read()

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="image_manipulator_thx",
    version="0.0.1",
    author="Rafael Assis",
    author_email="rafa-assis@hotmail.com",
    description="pacote de manipulação de imagem - Projeto 2 DIO",
    long_description=page_description,
    long_description_content_type="text/markdown",
    url="https://github.com/rafanthx13/criar-pacote-python-process-de-imagens",
    packages=find_packages(),
    install_requires=requirements,
    python_requires='>=3.6',
)