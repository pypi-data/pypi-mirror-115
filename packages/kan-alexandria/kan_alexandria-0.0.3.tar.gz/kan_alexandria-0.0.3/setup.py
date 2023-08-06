# -*- coding: utf-8 -*-

try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup, find_packages

def read(path):
    """Build a file path from *paths* and return the contents."""
    with open(path) as f:
        return f.read()


description = """
Kan_Alexandria is Python 3.5+ library for searching book details using Google
Books API. It's based on the original Kan module but optimized for consumption
of more data and returns the data in a more usable format (Python dicts).
"""

long_description = '\n\n'.join(
    [
        read('README.rst'),
        #read('HISTORY.rst')
    ])

license = read('LICENSE.md')

setup(
    name='kan_alexandria',
    description=description,
    long_description=long_description,
    author='Sang Han, João Rodrigues',
    license=license,
    url='https://github.com/joaodath/kan_alexandria',
    download_url='https://github.com/joaodath/kan_alexandria.git',
    author_email='joaorodriguesdiasneto@gmail.com',
    include_package_data=True,
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    python_requires=">=3.6",
    version='0.0.3',
    tests_require=['nose'],
    entry_points={
        'console_scripts': [
            'kan = kan.__main__:main'
            ]
        },
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Unix Shell',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Text Processing :: Linguistic',
        'Topic :: Utilities',
    ],
)
