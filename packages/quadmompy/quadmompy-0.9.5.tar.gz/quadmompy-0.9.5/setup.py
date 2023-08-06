from setuptools import setup


with open("README.rst", 'r') as fh:
    long_description = fh.read()


setup( \
    name='quadmompy', \
    version='0.9.5', \
    author="Michele Puetz", \
    url="https://gitlab.com/puetzm/quadmompy.git", \
    description='Tools for moments, Gaussian quadrature, orthogonal polynomials and quadrature-based moment methods for the numerical solution of spatially homogeneous population balance equations.', \
    long_description=long_description, \
    py_modules="quadmompy", \
    package_dir={'': '.'}, \
    classifiers=[ \
        "Programming Language :: Python :: 3", \
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)", \
        "Operating System :: OS Independent", \
        ], \
    install_requires=[ \
        "numpy ~= 1.21.5", \
        "scipy ~= 1.8.0", \
        ], \
    extras_require={ \
        "dev": [ \
            "pytest>=6.2.5", \
            "Sphinx==4.3.2", \
            "sphinxcontrib-bibtex==2.5.0", \
            "sphinxcontrib-packages==1.0.1", \
            ] \
        } \
)
