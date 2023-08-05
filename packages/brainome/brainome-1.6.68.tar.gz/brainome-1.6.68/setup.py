#! /usr/bin/env python3
# Brainome Daimensions(tm)
#
# The Brainome Table Compiler setup.py
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

python_version = str(sys.version_info[0]) + "." + str(sys.version_info[1])
version = "1.006.68"
version_parts = version.split('.')
# define package name brainome-<OS>-python3.x
realname = 'brainome'
if sys.platform.startswith("lin"):
	realname += '-linux'
elif sys.platform.startswith("win"):
	realname += '-win'
else:
	realname += '-mac'
realname += '-python' + str(sys.version_info[0])+"."+str(sys.version_info[1])
# add version qualifier like ==1.4.*
realname += '==' + version_parts[0] + '.' + str(int(version_parts[1])) + '.*'

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
	name="brainome",
	version=version,
	scripts=['brainome'],
	package_dir={'': '.'},
	package_data={'': ['brainome.py', 'version.py']},
	description='Brainome Table Compiler',
	url='https://github.com/brainome/examples',
	author='Brainome, Inc',
	author_email='support@brainome.ai',
	license='BSD',
	install_requires=[
			realname,
			],
	classifiers=[
		'Development Status :: 5 - Production/Stable',
		'Environment :: Console',
		'Environment :: GPU :: NVIDIA CUDA',
		'Intended Audience :: Science/Research',
		'Intended Audience :: Developers',
		'Intended Audience :: Education',
		'License :: OSI Approved :: BSD License',   
		'Programming Language :: Python :: 3 :: Only',
		'Topic :: Scientific/Engineering :: Artificial Intelligence',
		'Topic :: Utilities',
		'Operating System :: Microsoft :: Windows :: Windows 10',
		'Operating System :: MacOS :: MacOS X',
		'Operating System :: POSIX :: Linux',
	],
	long_description_content_type='text/markdown',
	long_description=long_description,
)
