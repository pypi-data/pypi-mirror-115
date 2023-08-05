#! /usr/bin/env python3
# Brainome Daimensions(tm)
#
# The Brainome setup.py
#
# Copyright (c) 2019 - 2021 Brainome Incorporated. All Rights Reserved.
# BSD license, all text above must be included in any redistribution.     
# See LICENSE.TXT for more information.
#
# This program may use Brainome's servers for cloud computing. Server use
# is subject to separate license agreement. 
#
# Contact: support@brainome.ai                                              
# for questions and suggestions. 
#

import sys
from setuptools import setup
from btc_version import BtcVersion
import sys
python_version = str(sys.version_info[0]) + "." + str(sys.version_info[1])
btcv = BtcVersion()
version = btcv.get_version_pep()

platform = 'Operating System :: Microsoft :: Windows :: Windows 10' if sys.platform.startswith("win") else 'Operating System :: MacOS :: MacOS X' if sys.platform.startswith("dar") else  'Operating System :: POSIX :: Linux'

# define package name daimensions-<OS>-python3.x
name = 'brainome'
if sys.platform.startswith("lin"):
	name += '-linux'
elif sys.platform.startswith("win"):
	name += '-win'
else:
	name += '-mac'
name += '-python' + python_version

long_description = """
# Brainome(tm) 

## Project description

Brainome is a **data compiler** that automatically solves supervised machine learning problems with repeatable and reproducible results and creates **standalone python predictors**. 

Brainome’s philosophy is that data science should be accessible to all:

* Run on your machine or in your cloud.
* Keep your data local.
* Own your model python code - run it anywhere.
* Single “compiler like” command to convert you data in a model in a single step. 
* Automatic data format conversion (text, numbers, etc..).
* No hyper-parameter tuning through measurements.
* Unlimited dimensionality (premium).

Brainome offer unique data insight and helps answer:

* Do I have enough data and the right feature? 
* What features are important (attribute ranking)?
* What model type will work best?
* Is my model overfitting?

Brainome’s predictors: 

* Run as executable or import as library.
* Are hardware independent.
* Are self contained in a single python file and integrate easily in standard CI/CD flow, Github, etc…

Brainome is free for personal use or evaluation. 
"""


setup(
	name=name,
	version=version,
	scripts=['btc'],  
	packages=[''],
	package_dir={'': '.'},
	package_data={'': ['btc.pyd']} if sys.platform.startswith("win") else {'': ['btc.so', 'lib/libomp.dylib', 'lib/libxgboost.dylib']} if sys.platform.endswith("win") else {'': ['btc.so']},
	description='Brainome Table Compiler',
	url='https://github.com/brainome/examples',
	author='Brainome, Inc',
	author_email='support@brainome.ai',
	license='BSD',
	install_requires=[
					'requests',
					'numpy>=1.20.0',
					'scikit-learn>=0.22.1',
					'torch>=1.4.0',
					'Jinja2>=3.0.0',
					'xgboost==1.4.2',
					],
	classifiers=[
		'Development Status :: 5 - Production/Stable',
		'Environment :: Console',
		'Environment :: GPU :: NVIDIA CUDA',
		'Intended Audience :: Science/Research',
		'Intended Audience :: Developers',
		'Intended Audience :: Education',
		'License :: OSI Approved :: BSD License',
		platform,       
		'Programming Language :: Python :: 3 :: Only',
		'Topic :: Scientific/Engineering :: Artificial Intelligence',
		'Topic :: Utilities'
	],
	long_description_content_type='text/markdown',
	long_description=long_description
)
