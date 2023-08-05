========
Overview
========

.. start-badges

|  |docs| |tests| |requires|
|  |license|

.. list-table::
    :stub-columns: 1

    * - docs
      - |docs|
    * - tests
      - | |tests| |requires|
        |
    * - package
      - | |version| |wheel| |supported-versions| |supported-implementations|
        | |commits-since|
.. |docs| image:: https://github.com/BAMresearch/jupyter_analysis_tools/actions/workflows/docs.yml/badge.svg
    :target: https://bamresearch.github.io/jupyter_analysis_tools/
    :alt: Documentation Status

.. |tests| image:: https://github.com/BAMresearch/jupyter_analysis_tools/actions/workflows/tests.yml/badge.svg
    :alt: GitHub Actions Build Status
    :target: https://github.com/BAMresearch/jupyter_analysis_tools/actions

.. |requires| image:: https://requires.io/github/BAMresearch/jupyter_analysis_tools/requirements.svg?branch=main
    :alt: Requirements Status
    :target: https://requires.io/github/BAMresearch/jupyter_analysis_tools/requirements/?branch=main

.. |version| image:: https://img.shields.io/pypi/v/jupyter-analysis-tools.svg
    :alt: PyPI Package latest release
    :target: https://pypi.org/project/jupyter-analysis-tools

.. |license| image:: https://img.shields.io/pypi/l/jupyter-analysis-tools.svg
    :target: https://pypi.org/project/jupyter-analysis-tools/
    :alt: License

.. |wheel| image:: https://img.shields.io/pypi/wheel/jupyter-analysis-tools.svg
    :alt: PyPI Wheel
    :target: https://pypi.org/project/jupyter-analysis-tools

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/jupyter-analysis-tools.svg
    :alt: Supported versions
    :target: https://pypi.org/project/jupyter-analysis-tools

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/jupyter-analysis-tools.svg
    :alt: Supported implementations
    :target: https://pypi.org/project/jupyter-analysis-tools

.. |commits-since| image:: https://img.shields.io/github/commits-since/BAMresearch/jupyter_analysis_tools/v0.1.0.svg
    :alt: Commits since latest release
    :target: https://github.com/BAMresearch/jupyter_analysis_tools/compare/v0.1.0...main



.. end-badges

Common Python helpers used in data analysis notebooks (.ipynb) with GIT

* Free software: MIT license

Installation
============

::

    pip install jupyter-analysis-tools

You can also install the in-development version with::

    pip install https://github.com/BAMresearch/jupyter_analysis_tools/archive/main.zip


Documentation
=============

https://bamresearch.github.io/jupyter_analysis_tools/

Development
===========

To run all the tests run::

    tox

Note, to combine the coverage data from all the tox environments run:

.. list-table::
    :widths: 10 90
    :stub-columns: 1

    - - Windows
      - ::

            set PYTEST_ADDOPTS=--cov-append
            tox

    - - Other
      - ::

            PYTEST_ADDOPTS=--cov-append tox
