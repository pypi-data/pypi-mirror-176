#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import io
import re
from glob import glob
from os.path import basename
from os.path import dirname
from os.path import join
from os.path import splitext

from setuptools import find_packages
from setuptools import setup


def read(*names, **kwargs):
    with io.open(join(dirname(__file__), *names), encoding=kwargs.get('encoding', 'utf8')) as fh:
        return fh.read()


setup(
    name='jupyter-analysis-tools',
    version='0.1.0',
    license='MIT',
    description='Common Python helpers used in data analysis notebooks (.ipynb) with GIT',
    long_description='{}\n{}'.format(
        re.compile('^.. start-badges.*^.. end-badges', re.M | re.S).sub('', read('README.rst')),
        re.sub(':[a-z]+:`~?(.*?)`', r'``\1``', read('CHANGELOG.rst')),
    ),
    author='Ingo Breßler',
    author_email='dev@ingobressler.net',
    url='https://github.com/BAMresearch/jupyter_analysis_tools',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    py_modules=[splitext(basename(path))[0] for path in glob('src/*.py')],
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        # complete classifier list: http://pypi.python.org/pypi?%3Aaction=list_classifiers
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Unix',
        'Operating System :: POSIX',
        'Operating System :: MacOS',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: Implementation :: CPython',
        'Framework :: Jupyter :: JupyterLab',
        'Topic :: Utilities',
        'Topic :: Scientific/Engineering',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
    ],
    project_urls={
        'Documentation': 'https://bamresearch.github.io/jupyter_analysis_tools/',
        'Changelog': 'https://bamresearch.github.io/jupyter_analysis_tools/changelog.html',
        'Issue Tracker': 'https://github.com/BAMresearch/jupyter_analysis_tools/issues',
    },
    keywords=[
        # eg: 'keyword1', 'keyword2', 'keyword3',
    ],
    python_requires='>=3.7',
    install_requires=[
        # eg: 'aspectlib==1.1.1', 'six>=1.7',
    ],
    extras_require={
        # eg:
        #   'rst': ['docutils>=0.11'],
        #   ':python_version=="2.6"': ['argparse'],
    },
)
