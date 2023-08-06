from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.0.1'
DESCRIPTION = 'Pure Python neural network package.'
LONG_DESCRIPTION = 'easyNeuron is a lightweight neural network framework that is easy to use and simple to understand.'

# Setting up
setup(
    name="easyNeuron",
    version=VERSION,
    author="Password-Classified",
    author_email="user@example.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    # install_requires=['timeit', 'decimal', 'csv'],
    keywords=['python', 'neural', 'networks', 'AI', 'ML', 'machine learning', 'easy', 'neuron', 'easyneuron', 'easyNeuron'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)