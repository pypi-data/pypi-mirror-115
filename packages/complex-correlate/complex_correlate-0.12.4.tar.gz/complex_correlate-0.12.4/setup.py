# -*- coding: utf-8 -*-
"""
Created on Tue Jan  3 20:36:58 2017

@author: a
"""
package='complex_correlate'
version='0.12.4'

from setuptools import setup, Extension
import os

#排除掉 __开头的文件及文件夹 或在 resource 中的文件夹
paths=[package]+[i for i in os.listdir() if os.path.isdir(i) and not i.startswith('__')]
files=sum([[i+'/'+ii.replace('\\','/') for ii in os.listdir(i)] for i in paths],[])
py=[i for i in files if i.endswith('__init__.py')]
c=[i for i in files if i.endswith('.c')]

setup(
    #基本信息
    name = package,
    version = version,
    keywords = ("complex_correlate", ),
    description = "complex_correlate",  
    long_description = "complex_correlate",  
    url = "",  
    author = "",
    author_email = "",
    
    #环境依赖
    platforms = "any",
    
    #打包范围
    package_dir={package: package},
    py_modules=[i.replace('.py','') for i in py],
    ext_modules=[Extension(i.replace('.c','').replace('/','.'),sources=[i]) for i in c],
    include_package_data = False,
    )
