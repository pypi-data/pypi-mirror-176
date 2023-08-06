import setuptools
from setuptools import find_packages
  
with open("README.md", "r") as fh:
    description = fh.read()
  
setuptools.setup(
    name="simplepygamemenus",
    version="0.1.3",
    author="Leonardo Ferrisi",
    author_email="ferrisil@union.edu",
    packages=find_packages(where='src'),
    include_package_data=True,
    description="A package for making simple menus for your python games!",
    long_description=description,
    long_description_content_type="text/markdown",
    url="https://github.com/LeonardoFerrisi/simplepygamemenus-gitrepo",
    license='MIT',
    python_requires='>=3.8',
    install_requires=["pygame"]
)