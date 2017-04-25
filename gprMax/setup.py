# Copyright (C) 2015-2016: The University of Edinburgh
#                 Authors: Craig Warren and Antonis Giannopoulos
#
# This file is part of gprMax.
#
# gprMax is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# gprMax is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with gprMax.  If not, see <http://www.gnu.org/licenses/>.

try:
    from setuptools import setup, Extension
except ImportError:
    from distutils.core import setup
    from distutils.extension import Extension

try:
    import numpy as np
except ImportError:
    raise ImportError('gprMax requires the NumPy package.')

import glob, os, shutil, sys

# Python version
if sys.version_info[:2] < (3, 4):
    print('gprMax requires Python 3.4 or newer')
    sys.exit(-1)

import gprMax

# Package name
packagename = gprMax.__name__

# Package version
version = gprMax.__version__

# Process 'install' command line argument
if 'install' in sys.argv:
    print("'install' is not required for this package, running 'build_ext --inplace' instead.")
    sys.argv.remove('install')
    sys.argv.append('build_ext')
    sys.argv.append('--inplace')

# Process 'build' command line argument
if 'build' in sys.argv:
    print("'build' is not required for this package, running 'build_ext --inplace' instead.")
    sys.argv.remove('build')
    sys.argv.append('build_ext')
    sys.argv.append('--inplace')

# Process '--no-cython' command line argument - either Cythonize or just compile the .c files
if '--no-cython' in sys.argv:
    USE_CYTHON = False
    sys.argv.remove('--no-cython')
else:
    USE_CYTHON = True

# Build a list of all the files that need to be Cythonized looking in gprMax directory and user_libs
cythonfiles = []
for root, dirs, files in os.walk(os.path.join(os.getcwd(), packagename)):
    for file in files:
        if file.endswith('.pyx'):
            cythonfiles.append(os.path.join(packagename, file))
for root, dirs, files in os.walk(os.path.join(os.getcwd(), 'user_libs')):
    for file in files:
        if file.endswith('.pyx'):
            cythonfiles.append(os.path.join('user_libs', file))

# Process 'cleanall' command line argument - cleanup Cython files
if 'cleanall' in sys.argv:
    USE_CYTHON = False
    print('Deleting Cython files...')
    for file in cythonfiles:
        filebase = os.path.splitext(file)[0]
        # Remove Cython C files
        if os.path.isfile(filebase + '.c'):
            try:
                os.remove(filebase + '.c')
                print('Removed: {}'.format(filebase + '.c'))
            except OSError:
                print('Could not remove: {}'.format(filebase + '.c'))
        # Remove compiled Cython modules
        libfile = glob.glob(os.path.join(os.getcwd(), os.path.splitext(file)[0]) + '*.pyd') + glob.glob(os.path.join(os.getcwd(), os.path.splitext(file)[0]) + '*.so')
        if libfile:
            libfile = libfile[0]
            try:
                os.remove(libfile)
                print('Removed: {}'.format(os.path.join(packagename, os.path.split(libfile)[-1])))
            except OSError:
                print('Could not remove: {}'.format(os.path.join(packagename, os.path.split(libfile)[-1])))
    # Remove build directory
    shutil.rmtree(os.path.join(os.getcwd(), 'build'), ignore_errors=True)
    # Now do a normal clean
    sys.argv[1] = 'clean'  # this is what distutils understands

# Set compiler options
# Windows
if sys.platform == 'win32':
    compile_args = ['/O2', '/openmp', '/w']
    linker_args = []
    extra_objects = []
# Mac OS X - needs gcc (usually via HomeBrew) because the default compiler LLVM (clang) does not support OpenMP
elif sys.platform == 'darwin':
    gccpath = glob.glob('/usr/local/bin/gcc-[4-5]*')
    if gccpath:
        os.environ['CC'] = gccpath[0].split(os.sep)[-1]
    else:
        raise('Cannot find gcc 4.x or gcc 5.x in /usr/local/bin. gprMax requires gcc to be installed - easily done through the Homebrew package manager (http://brew.sh). Note: gcc with OpenMP support must be installed')
    compile_args = ['-O3', '-w', '-fstrict-aliasing', '-fno-common', '-fopenmp']
    linker_args = ['-fopenmp']
    extra_objects = []
    
    # If user is cwarren do static linking as this is for binaries uploaded to GitHub
#    if os.getlogin() == 'cwarren':
#        linker_args = ['-static-libgcc']
#        extra_objects = ['/usr/local/opt/gcc/lib/gcc/5/libgomp.a']
# Linux
else:
    compile_args = ['-O3', '-w', '-fopenmp']
    linker_args = ['-fopenmp']
    extra_objects = []

# Build a list of all the extensions
extensions = []
for file in cythonfiles:
    tmp = os.path.splitext(file)
    if USE_CYTHON:
        fileext = tmp[1]
    else:
        fileext = '.c'
    extension = Extension(tmp[0].replace(os.sep, '.'),
                          [tmp[0] + fileext],
                          language='c',
                          include_dirs=[np.get_include()],
                          extra_compile_args=compile_args,
                          extra_link_args=linker_args,
                          extra_objects = extra_objects)
    extensions.append(extension)

# Cythonize (build .c files)
if USE_CYTHON:
    from Cython.Build import cythonize
    extensions = cythonize(extensions,
                           compiler_directives={
                               'boundscheck': False,
                               'wraparound': False,
                               'initializedcheck': False,
                               'embedsignature': True,
                               'language_level': 3
                           },
                           annotate=False)

setup(name=packagename,
      version=version,
      author='Craig Warren and Antonis Giannopoulos',
      url='http://www.gprmax.com',
      description='Electromagnetic Modelling Software based on the Finite-Difference Time-Domain (FDTD) method',
      license='GPLv3+',
      classifiers=[
                   'Environment :: Console',
                   'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
                   'Operating System :: MacOS :: MacOS X',
                   'Operating System :: Microsoft :: Windows :: Windows 7',
                   'Operating System :: POSIX :: Linux',
                   'Programming Language :: Cython',
                   'Programming Language :: Python :: 3.4',
                   'Topic :: Scientific/Engineering'
                   ],
      ext_modules=extensions,
      include_dirs=[np.get_include()])
