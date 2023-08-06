from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '1.1.0'
DESCRIPTION = "Locate the path you're in and append it to sys"
LONG_DESCRIPTION = 'A package that allows you to locate your modules imports when you run an script from the console.'

# Setting up
setup(
    name="encontrar",
    version=VERSION,
    author="tmorales (Tomas Morales Vera)",
    author_email="<moralesveratomas@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=[''],
    keywords=['python', 'path', 'locate', 'locator', 'pathLocator', 'pathLocate'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Programming Language :: Python :: 3.10"
    ]
)
