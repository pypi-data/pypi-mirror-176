
from setuptools import setup
import re
import os
import sys


setup(
    name="torch-nets",
    version="0.0.0",
    python_requires=">3.7.0",
    author="Michael E. Vinyard - Harvard University - Broad Institute of MIT and Harvard - Massachussetts General Hospital",
    author_email="mvinyard@broadinstitute.org",
    url=None,
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    description="PyTorch Neural Networks",
    packages=[
        "torch_nets"
    ],
    
    install_requires=[
        "torch>=1.12",
    ],
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Programming Language :: Python :: 3.7",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Bio-Informatics",
    ],
    license="MIT",
)
