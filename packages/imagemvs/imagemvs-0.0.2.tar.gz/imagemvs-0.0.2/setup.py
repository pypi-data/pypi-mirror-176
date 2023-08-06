from setuptools import setup, find_packages

with open("README.md", "r") as f:
    page_description = f.read()

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="imagemvs",
    version="0.0.2",
    author="Marcos Vinicius",
    author_email="marcos_mvs99@hotmail.com",
    description="DIO project process",
    long_description=page_description,
    long_description_content_type="text/markdown",
    url="https://github.com/marcosmvsfut/Dio_Unimed_Bootcamp",
    packages=find_packages(),
    install_requires=requirements,
    python_requires='>=3.8',
)