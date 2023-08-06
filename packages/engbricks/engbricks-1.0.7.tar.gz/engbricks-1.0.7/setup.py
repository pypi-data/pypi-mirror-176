from setuptools import setup, find_packages, find_namespace_packages

# read the contents of your README file
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name="engbricks",
    version="1.0.7",
    license="MIT",
    author="Filipe Fraqueiro",
    author_email="fraqueirofilipe@gmail.com",
    packages=find_namespace_packages(include=['src.*']),
    install_requires=[
        "selenium==4.5.0",
        "sympy==1.11.1",
    ],
    url="https://github.com/FilipeFraqueiro/engbricks",
    long_description=long_description,
    long_description_content_type='text/markdown'
)