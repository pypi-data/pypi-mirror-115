from setuptools import setup
from setuptools import find_packages

# Setup keywords.
# https://setuptools.readthedocs.io/en/latest/references/keywords.html
setup(
    name="jax-extra",
    version="0.0.0",
    author="Andrei Nesterov",
    author_email="ae.nesterov@gmail.com",
    description="",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
)
