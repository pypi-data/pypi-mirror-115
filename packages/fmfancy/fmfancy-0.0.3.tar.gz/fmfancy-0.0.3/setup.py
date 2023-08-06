from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.0.3'
DESCRIPTION = 'Test_pkg'
LONG_DESCRIPTION = 'A package that allows to build simple microservices with fastapi and mongoDB'

# Setting up
setup(
    name="fmfancy",
    version=VERSION,
    author="Tobiasz Gleba",
    author_email="tobiasz.gleba24@gmail.com",
    description=DESCRIPTION,
    # long_description=long_description,
    # long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=['fastapi', 'motor'],
    keywords=['python', 'fastapi', 'workflow'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6"
)