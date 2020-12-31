from setuptools import setup
from Cython.Build import cythonize

setup(
    ext_modules=cythonize("efficient_face_recognition.pyx", annotate=True),
)