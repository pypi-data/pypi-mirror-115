# DO NOT EDIT!!! built with `python _building/build_setup.py`
import setuptools
setuptools.setup(
    name="k3pattern",
    packages=["k3pattern"],
    version="0.1.0",
    license='MIT',
    description='Find common prefix of several `string`s, tuples of string, or other nested structure, recursively by default.',
    long_description="# k3pattern\n\n[![Action-CI](https://github.com/pykit3/k3pattern/actions/workflows/python-package.yml/badge.svg)](https://github.com/pykit3/k3pattern/actions/workflows/python-package.yml)\n[![Build Status](https://travis-ci.com/pykit3/k3pattern.svg?branch=master)](https://travis-ci.com/pykit3/k3pattern)\n[![Documentation Status](https://readthedocs.org/projects/k3pattern/badge/?version=stable)](https://k3pattern.readthedocs.io/en/stable/?badge=stable)\n[![Package](https://img.shields.io/pypi/pyversions/k3pattern)](https://pypi.org/project/k3pattern)\n\nFind common prefix of several `string`s, tuples of string, or other nested structure, recursively by default.\n\nk3pattern is a component of [pykit3] project: a python3 toolkit set.\n\n\nFind common prefix of several string, tuples of string, or other nested structure, recursively by default.\nIt returns the shortest prefix: empty string or empty tuple is removed.\n\n\n\n# Install\n\n```\npip install k3pattern\n```\n\n# Synopsis\n\n```python\n\nimport k3pattern\n\nk3pattern.common_prefix('abc', 'abd')                   # 'ab'\nk3pattern.common_prefix((1, 2, 'abc'), (1, 2, 'abd'))   # (1, 2, 'ab')\nk3pattern.common_prefix((1, 2, 'abc'), (1, 2, 'xyz'))   # (1, 2); empty prefix of 'abc' and 'xyz' is removed\nk3pattern.common_prefix((1, 2, (5, 6)), (1, 2, (5, 7))) # (1, 2, (5,) )\nk3pattern.common_prefix('abc', 'abd', 'abe')            # 'ab'; common prefix of more than two\n```\n\n#   Author\n\nZhang Yanpo (张炎泼) <drdr.xp@gmail.com>\n\n#   Copyright and License\n\nThe MIT License (MIT)\n\nCopyright (c) 2015 Zhang Yanpo (张炎泼) <drdr.xp@gmail.com>\n\n\n[pykit3]: https://github.com/pykit3",
    long_description_content_type="text/markdown",
    author='Zhang Yanpo',
    author_email='drdr.xp@gmail.com',
    url='https://github.com/pykit3/k3pattern',
    keywords=['python', 'pattern'],
    python_requires='>=3.0',

    install_requires=['k3ut<0.2,>=0.1.15'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries',
    ] + ['Programming Language :: Python :: 3'],
)
