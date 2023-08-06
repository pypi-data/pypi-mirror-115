#!/usr/bin/env python
# -*- coding: utf-8 -*-

# version: 1.0
# author: Qian Yang
# Contact: dtzxyangq@foxmail.com

import os,sys,io
from setuptools import setup,find_packages

VERSION = '1.1'

tests_require= []
install_requires = ['numpy', 
                    'scipy',
                    'pandas',
                    'matplotlib',
                    'seaborn',
                    'matplotlib_venn'
                   ]

setup(name='HiSTra',
      version=VERSION,
      author="Q.Yang",
      author_email='dtzxyangq@foxmail.com',
      keywords='HiC genome structure variation translocation',
      description='Spectral translocation detection of HiC matrices.',
      license='MIT',
      url='https://github.com/dtzxyangq/HiSTra',
      classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
#       package_dir={"":"HiSTra"},
      packages=find_packages(),
#       package_data={'':['deDoc/*','juice/*']},
#       include_package_data=True,
      scripts=['./HiST'],
      install_requires=install_requires,
      tests_require=tests_require,
#       packages_dir={"":"HiSTra"},
#       packages=find_packages(where="HiSTra"),
      python_requires=">=3.6",
     )