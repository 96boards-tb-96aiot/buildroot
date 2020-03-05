# -*- coding=utf-8 -*-
import setuptools

from Cython.Build import cythonize

from setuptools.extension import Extension

# python setup.py build_ext --inplace

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
