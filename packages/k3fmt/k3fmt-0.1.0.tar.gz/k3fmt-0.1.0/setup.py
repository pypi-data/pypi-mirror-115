# DO NOT EDIT!!! built with `python _building/build_setup.py`
import setuptools
setuptools.setup(
    name="k3fmt",
    packages=["k3fmt"],
    version="0.1.0",
    license='MIT',
    description='It provides with several string operation functions.',
    long_description='# k3fmt\n\n[![Action-CI](https://github.com/pykit3/k3fmt/actions/workflows/python-package.yml/badge.svg)](https://github.com/pykit3/k3fmt/actions/workflows/python-package.yml)\n[![Build Status](https://travis-ci.com/pykit3/k3fmt.svg?branch=master)](https://travis-ci.com/pykit3/k3fmt)\n[![Documentation Status](https://readthedocs.org/projects/k3fmt/badge/?version=stable)](https://k3fmt.readthedocs.io/en/stable/?badge=stable)\n[![Package](https://img.shields.io/pypi/pyversions/k3fmt)](https://pypi.org/project/k3fmt)\n\nIt provides with several string operation functions.\n\nk3fmt is a component of [pykit3] project: a python3 toolkit set.\n\n\n#   Name\n\nk3fmt\n\nIt provides with several string operation functions.\n\n#   Status\n\nThis library is considered production ready.\n\n\n\n\n# Install\n\n```\npip install k3fmt\n```\n\n# Synopsis\n\n```python\n\nimport k3fmt\n\nlines = [\n    \'hello\',\n    \'world\',\n]\n\n# add left padding to each line in a string\nk3fmt.line_pad(\'\\n\'.join(lines), \' \' * 4)\n# "    hello"\n# "    world"\n\n\n# format a multi-row line\nitems = [\'name:\',\n         [\'John\',\n          \'j is my nick\'\n          ],\n\n         \'age:\',\n         26,\n\n         \'experience:\',\n         [\'2000 THU\',\n          \'2006 sina\',\n          \'2010 other\'\n          ],\n         ]\n\nk3fmt.format_line(items, sep=\' | \', aligns=\'llllll\')\n# outputs:\n#    name: | John         | age: | 26 | experience: | 2000 THU\n#          | j is my nick |      |    |             | 2006 sina\n#          |              |      |    |             | 2010 other\n\n```\n\n#   Author\n\nZhang Yanpo (张炎泼) <drdr.xp@gmail.com>\n\n#   Copyright and License\n\nThe MIT License (MIT)\n\nCopyright (c) 2015 Zhang Yanpo (张炎泼) <drdr.xp@gmail.com>\n\n\n[pykit3]: https://github.com/pykit3',
    long_description_content_type="text/markdown",
    author='Zhang Yanpo',
    author_email='drdr.xp@gmail.com',
    url='https://github.com/pykit3/k3fmt',
    keywords=['python', 'string', 'fmt'],
    python_requires='>=3.0',

    install_requires=['k3ut>=0.1.15,<0.2', 'k3color>=0.1.0,<0.2', 'k3proc<0.3,>=0.2.0'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries',
    ] + ['Programming Language :: Python :: 3'],
)
