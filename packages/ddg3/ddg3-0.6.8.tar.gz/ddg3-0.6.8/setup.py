"""
pip setup.py for ddg3
"""
from setuptools import setup


__library__ = "ddg3"
__version__ = "0.6.8"

with open("README.md") as readme:
    LONG_DESCRIPTION = readme.read()

with open("requirements.txt") as requirements:
    INSTALL_REQUIRES = requirements.read().split("\n")
    INSTALL_REQUIRES = [x.strip() for x in INSTALL_REQUIRES if x.strip()]

setup(
    name=__library__,
    version=__version__,
    py_modules=["ddg3"],
    description="Library for querying the Duck Duck Go API, updated for python3",
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    author="Michael Stephens, Jacobi Petrucciani",
    author_email="jacobi@mimirhq.com",
    license="BSD",
    url="https://github.com/jpetrucciani/python-duckduckgo",
    platforms=["any"],
    install_requires=INSTALL_REQUIRES,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Topic :: Internet :: WWW/HTTP :: Indexing/Search",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    entry_points={"console_scripts": ["ddg3 = ddg3:main"]},
)
