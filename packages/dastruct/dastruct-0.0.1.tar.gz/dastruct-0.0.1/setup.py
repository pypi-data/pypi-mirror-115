import setuptools
from setuptools import setup

setup(
    name='dastruct',
    version='0.0.1',
    description='This package is a converter of different data structure we use. i.e. list, tuple, sets, collection etc to each other',
    author='Amun Timilsina',
    long_description_content_type='text/markdown',
    packages=setuptools.find_packages(),
    keywords=['Data structure converter', 'tuple to list'],
    classifiers=[
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.9.5',
    py_modules=['dastruct'],
    package_dir={'': 'src'}
)
