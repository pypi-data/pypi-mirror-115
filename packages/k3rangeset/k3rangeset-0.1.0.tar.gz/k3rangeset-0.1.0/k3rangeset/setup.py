# DO NOT EDIT!!! built with `python _building/build_setup.py`
import setuptools
setuptools.setup(
    name="k3rangeset",
    packages=["k3rangeset"],
    version="0.1.0",
    license='MIT',
    description='segmented range which is represented in a list of sorted interleaving range.',
    long_description="# k3rangeset\n\n[![Action-CI](https://github.com/pykit3/k3rangeset/actions/workflows/python-package.yml/badge.svg)](https://github.com/pykit3/k3rangeset/actions/workflows/python-package.yml)\n[![Build Status](https://travis-ci.com/pykit3/k3rangeset.svg?branch=master)](https://travis-ci.com/pykit3/k3rangeset)\n[![Documentation Status](https://readthedocs.org/projects/k3rangeset/badge/?version=stable)](https://k3rangeset.readthedocs.io/en/stable/?badge=stable)\n[![Package](https://img.shields.io/pypi/pyversions/k3rangeset)](https://pypi.org/project/k3rangeset)\n\nsegmented range which is represented in a list of sorted interleaving range.\n\nk3rangeset is a component of [pykit3] project: a python3 toolkit set.\n\n\nSegmented range which is represented in a list of sorted interleaving range.\n\nA range set can be thought as: `[[1, 2], [5, 7]]`.\n\n\n\n\n# Install\n\n```\npip install k3rangeset\n```\n\n# Synopsis\n\n```python\n\nimport k3rangeset\n\na = k3rangeset.RangeSet([[1, 5], [10, 20]])\na.has(1)  # True\na.has(8)  # False\na.add([5, 7])  # [[1, 7], [10, 20]]\n\ninp = [\n    [0, 1, [['a', 'b', 'ab'],\n            ['b', 'd', 'bd'],\n            ]],\n    [1, 2, [['a', 'c', 'ac'],\n            ['c', 'd', 'cd'],\n            ]],\n]\n\nr = k3rangeset.RangeDict(inp, dimension=2)\nprint(r.get(0.5, 'a'))  # 'ab'\nprint(r.get(1.5, 'a'))  # 'ac'\n\n```\n\n#   Author\n\nZhang Yanpo (张炎泼) <drdr.xp@gmail.com>\n\n#   Copyright and License\n\nThe MIT License (MIT)\n\nCopyright (c) 2015 Zhang Yanpo (张炎泼) <drdr.xp@gmail.com>\n\n\n[pykit3]: https://github.com/pykit3",
    long_description_content_type="text/markdown",
    author='Zhang Yanpo',
    author_email='drdr.xp@gmail.com',
    url='https://github.com/pykit3/k3rangeset',
    keywords=['python', 'set'],
    python_requires='>=3.0',

    install_requires=['k3ut<0.2,>=0.1.15'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries',
    ] + ['Programming Language :: Python :: 3'],
)
