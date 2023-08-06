from setuptools import setup, find_packages

setup(
    name="engbricks",
    version="1.0.3",
    license="MIT",
    author="Filipe Fraqueiro",
    author_email="fraqueirofilipe@gmail.com",
    packages=find_packages("engbricks", "src"),
    package_dir={"": "engbricks"},
    install_requires=[
        "selenium==4.5.0",
        "sympy==1.11.1",
    ],
    url="https://github.com/FilipeFraqueiro/engbricks"
)