from setuptools import setup
from Cython.Build import cythonize

setup(
    name="TempMail",
    ext_modules=cythonize("tempmail.py", compiler_directives={'language_level': 3}),
)
