#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import io
from setuptools import find_packages, setup
   
description1 = 'The project implements the Ascendfly Inference framework through the Ascend Compute Language Python (pyACL) API, and define a series of easy-to-use python interfaces. The purpose is to simplify the development process of users using pyACL and accelerate the migration and deployment of algorithms. The following is a brief description of ascendfly.'

description2 = str(' \
This software provides the following functions: \
\
1. Define the Context and Memory resource classes to simplify resource scheduling and allocation.\
2. Define the AscendArray class (like numpy.ndrray), and manage images and tensor on the device to achieve data unity. AscendArray automatically manages data memory without user operation.\
3. Define the VideoCapture and VideoWriter classes to obtain real-time H264 (MAIN LEVEL without B frame) protocol RTSP/RTMP stream, and hard-decode it through the Ascend310 chip, or encode the picture into a 264/265 stream frame by frame.\
4. Define the Image class to realize image processing functions such as image decoding, scaling, cutting, padding, etc.\
5. Define the Model class to perform model inference functions.\
6. Define Profiling class to facilitate model performance tuning.\
7. Other functions such as single operator call, post-processing and so on. ')

setup(
    name='ascendfly',
    version='0.2',
    description='Ascend inference framework',
    keywords='ascend detection and classification',
    packages=find_packages(exclude=('configs', 'tools', 'cv2', 'tests', 'docs')),
    include_package_data=True,
    long_description= description1+ description2,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Topic :: Software Development :: Libraries',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.7',
    ],
    url='https://gitee.com/ascend-fae/ascendfly',
    author='zhengguojian',
    author_email='kfengzheng@163.com',
    install_requires=['numpy>=1.14', 'av>=8.0.2', 'objgraph>=3.5.0', 'opencv-python>=3.4.2', 'prettytable>=2.1.0'],
    zip_safe=False)
