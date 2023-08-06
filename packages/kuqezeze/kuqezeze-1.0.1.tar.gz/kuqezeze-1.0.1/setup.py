from setuptools import setup, find_packages
import codecs
import os


VERSION = '1.0.1'

# Setting up
setup(
    name="kuqezeze",
    version=VERSION,
    author="Guido Xhindoli",
    author_email="<mail@gmail.com>",
    description='A package that guess the munber',
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=[],
    keywords=['kuqezeze', 'kuqe', 'zeze', 'sda'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)