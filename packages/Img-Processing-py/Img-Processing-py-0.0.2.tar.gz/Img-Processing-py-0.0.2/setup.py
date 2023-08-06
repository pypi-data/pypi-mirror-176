from setuptools import setup, find_packages

with open("README.md", "r") as f:
    page_description = f.read()

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="Img-Processing-py",
    version="0.0.2",
    author="VagnerF",    
    description="Image Processing Package using Skimage", 
    long_description=page_description,
    long_description_content_type="text/markdown",
    url="https://github.com/VagnerF/Pacotes_processamento_imagens_com_python",
    packages=find_packages(),
    install_requires=requirements,
    python_requires='>=3.7',
)
