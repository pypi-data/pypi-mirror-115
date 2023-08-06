# DO NOT EDIT!!! built with `python _building/build_setup.py`
import setuptools
setuptools.setup(
    name="k3shell",
    packages=["k3shell"],
    version="0.1.0",
    license='MIT',
    description='A python module to manage commands.',
    long_description='# k3shell\n\n[![Action-CI](https://github.com/pykit3/k3shell/actions/workflows/python-package.yml/badge.svg)](https://github.com/pykit3/k3shell/actions/workflows/python-package.yml)\n[![Build Status](https://travis-ci.com/pykit3/k3shell.svg?branch=master)](https://travis-ci.com/pykit3/k3shell)\n[![Documentation Status](https://readthedocs.org/projects/k3shell/badge/?version=stable)](https://k3shell.readthedocs.io/en/stable/?badge=stable)\n[![Package](https://img.shields.io/pypi/pyversions/k3shell)](https://pypi.org/project/k3shell)\n\nA python module to manage commands.\n\nk3shell is a component of [pykit3] project: a python3 toolkit set.\n\n\n#   Name\n\nk3shell\n\n#   Status\n\nThe library is considered production ready.\n\n\n\n\n# Install\n\n```\npip install k3shell\n```\n\n# Synopsis\n\n```python\n\nimport k3shell\nimport sys\narguments = {\n    \'echo_repr\': (\n        lambda x: sys.stdout.write(repr(x)),\n        (\'x\', {\'nargs\': \'+\', \'help\': \'just an input message\'}),\n    ),\n\n    \'foo\': {\n        \'bar\': lambda: sys.stdout.write(\'bar\'),\n\n        \'bob\': {\n            \'plus\': (\n                lambda x, y: sys.stdout.write(str(x + y)),\n                (\'x\', {\'type\': int, help: \'an int is needed\'}),\n                (\'y\', {\'type\': int, help: \'an int is needed\'}),\n            ),\n        },\n    },\n\n    \'__add_help__\': {\n        (\'echo_repr\',)           : \'output what is input.\',\n        (\'foo\', \'bar\',)          : \'print a "bar".\',\n        (\'foo\', \'bob\', \'plus\',)  : \'do addition operation with 2 numbers.\',\n    },\n\n    \'__description__\': \'this is an example command.\',\n}\n\nk3shell.command(**arguments)\n"""\n\nthen you can execute your command as:\n\npython demo.py echo_repr hello!\n# \'hello!\'\n\npython demo.py foo bar\n# \'bar\'\n\npython demo.py foo bob plus 1 2\n# 3\n\n\nand you can get a usage help message like:\n\n$ python demo.py -h\n---------------------------\nusage: demo.py [-h] {echo_repr, foo bar, foo bob plus} ...\n\nthis is an example command.\n\npositional arguments:\n  {echo_repr, foo bar, foo bob plus} commands to select ...\n    echo_repr            output what is input.\n    foo bar              print a "bar".\n    foo bob plus         do addition operation with 2 numbers.\n\noptional arguments:\n    -h, --help           show this help message and exit\n\n\n$ python demo.py foo bob plus -h\n--------------------------\nusage: demo.py foo bob plus [-h] x y\n\npositional arguments:\n    x   an int is need\n    y   an int is need\n\noptional arguments:\n    -h, --help           show this help message and exit\n\n"""\n```\n\n#   Author\n\nWenbo Li(李文博) <wenbo.li@baishancloud.com>\n\n#   Copyright and License\n\nThe MIT License (MIT)\n\nCopyright (c) 2017 Wenbo Li(李文博) <wenbo.li@baishancloud.com>\n\n\n[pykit3]: https://github.com/pykit3',
    long_description_content_type="text/markdown",
    author='Zhang Yanpo',
    author_email='drdr.xp@gmail.com',
    url='https://github.com/pykit3/k3shell',
    keywords=['python', 'shell'],
    python_requires='>=3.0',

    install_requires=['k3dict<0.2,>=0.1.0'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries',
    ] + ['Programming Language :: Python :: 3'],
)
