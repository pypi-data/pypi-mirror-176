from setuptools import setup, find_packages

with open("README.md", "r") as f:
    page_description = f.read()

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="equacao_segundo_grau",
    version="0.0.1",
    author="Genildo",
    author_email="genildo.praca@gmail.com",
    description="Calcula o resultado para equações do segundo grau",
    long_description=page_description,
    long_description_content_type="text/markdown",
    url="https://github.com/GenildoPraca/equacao-segundo-grau-package.git",
    packages=find_packages(),
    install_requires=requirements,
    python_requires='>=3.8',
)