import setuptools
import simplex

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="simplex",
    version=simplex.__version__,
    author=simplex.__author__.split(' <')[0],
    author_email=simplex.__author__.split(' <')[1][:-1],
    description="Solver using simplex algorithm.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Oprax/simplex",
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "Topic :: Scientific/Engineering :: Mathematics",
    ),
)