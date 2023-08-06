from setuptools import setup, find_packages
import codecs
import os


VERSION = '0.0.1'
DESCRIPTION = 'A basic List Shift Operation package'

# Setting up
setup(
    name="listshiftoperationpkg",
    version=VERSION,
    author="Prabhat Ale",
    author_email="<srv.ale52@gmail.com>",
    description=DESCRIPTION,
    packages=find_packages(),
    install_requires=[],
    keywords=['python', 'list', 'shift opeartion', 'left shift', 'right shift'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)