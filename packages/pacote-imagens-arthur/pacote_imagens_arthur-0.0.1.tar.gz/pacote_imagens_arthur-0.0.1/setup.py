from setuptools import setup, find_packages

with open("README.md", "r") as f:
    page_description = f.read()

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup (
    name="pacote_imagens_arthur",
    version="0.0.1",
    author="Arthur Bernardes",
    author_email="arthur.feq.ufu@gmail.com",
    description="Image Processing Project",
    long_description=page_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ArthurrBernardes/image_processing_package",
    packages=find_packages(),
    install_requires=requirements,
    python_requires='>=3.8',
    
    )