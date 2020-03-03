# -*- coding=utf-8 -*-
import setuptools

from Cython.Build import cythonize

from setuptools.extension import Extension

# mit/log.py是文件的位置，比如某个文件夹。mit.log是import的时候模块的名字
# python setup.py build_ext --inplace

# 编译成pyc python3 -m compileall -b run.py

setuptools.setup(
    ext_modules=cythonize("toybrick/*.py")
)
setuptools.setup(
    ext_modules=cythonize("webapp/*.py")
)
setuptools.setup(
    ext_modules=cythonize("webapp/factoryTest/*.py")
)
import inspect
import os
# get now path
filename = inspect.getframeinfo(inspect.currentframe()).filename
BASE_DIR = os.path.dirname(os.path.abspath(filename))

# clean toybrick
os.system('find %s/toybrick/  -maxdepth 1 -name "*.py*" -type f  ! -name "__init__.pyc"  |xargs rm -rf' % BASE_DIR)
os.system('find %s/toybrick/  -maxdepth 1 -name "*.c"  |xargs rm -rf' % BASE_DIR)
os.system('find %s/toybrick/  -maxdepth 1 -name "__init__.so"  |xargs rm -rf' % BASE_DIR)


# clean webapp
os.system('find %s/webapp/  -maxdepth 1 -name "*.py*" -type f  ! -name "__init__.pyc"  |xargs rm -rf' % BASE_DIR)
os.system('find %s/webapp/  -maxdepth 1 -name "*.c"  |xargs rm -rf' % BASE_DIR)
os.system('find %s/webapp/  -maxdepth 1 -name "__init__.so"  |xargs rm -rf' % BASE_DIR)

# clean webapp/factoryTest
os.system('find %s/webapp/factoryTest/  -maxdepth 1 -name "*.py*" -type f  ! -name "__init__.pyc"  |xargs rm -rf' % BASE_DIR)
os.system('find %s/webapp/factoryTest/  -maxdepth 1 -name "*.c"  |xargs rm -rf' % BASE_DIR)
os.system('find %s/webapp/factoryTest/  -maxdepth 1 -name "__init__.so"  |xargs rm -rf' % BASE_DIR)


# find ./  -maxdepth 1 -name '*py*' -type f  ! -name "__init__.pyc"  |xargs rm -rf
