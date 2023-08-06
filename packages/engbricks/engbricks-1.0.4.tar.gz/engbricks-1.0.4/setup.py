from setuptools import setup, find_packages

setup(
    name="engbricks",
    version="1.0.4",
    license="MIT",
    author="Filipe Fraqueiro",
    author_email="fraqueirofilipe@gmail.com",
    packages=find_packages("engbricks"),
    package_dir={
        "": "engbricks",
        "src": "engbricks/src"
    },
    install_requires=[
        "selenium==4.5.0",
        "sympy==1.11.1",
    ],
    url="https://github.com/FilipeFraqueiro/engbricks",
    readme = "README.md"
)