from setuptools import setup
from distutils.extension import Extension
from Cython.Build import cythonize
import numpy

ext_modules = [
    Extension(
        r'main',
        [r'efficient_face_recognition.pyx'],
        include_dirs=[numpy.get_include()]
    ),
]

setup(
    ext_modules=cythonize("efficient_face_recognition.pyx", annotate=True),
    include_dirs=[numpy.get_include()]
)