from setuptools import setup

name = "types-python-dateutil"
description = "Typing stubs for python-dateutil"
long_description = '''
## Typing stubs for python-dateutil

This is a PEP 561 type stub package for the `python-dateutil` package.
It can be used by type-checking tools like mypy, PyCharm, pytype etc. to check code
that uses `python-dateutil`. The source for this package can be found at
https://github.com/python/typeshed/tree/master/stubs/python-dateutil. All fixes for
types and metadata should be contributed there.

See https://github.com/python/typeshed/blob/master/README.md for more details.
This package was generated from typeshed commit `ef5b4b6820ba7638d4749e9642a1d4bc2bc95707`.
'''.lstrip()

setup(name=name,
      version="0.1.5",
      description=description,
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/python/typeshed",
      install_requires=[],
      packages=['dateutil-stubs'],
      package_data={'dateutil-stubs': ['parser.pyi', 'rrule.pyi', '__init__.pyi', 'relativedelta.pyi', 'utils.pyi', '_common.pyi', 'easter.pyi', 'tz/__init__.pyi', 'tz/tz.pyi', 'tz/_common.pyi', 'METADATA.toml']},
      license="Apache-2.0 license",
      classifiers=[
          "License :: OSI Approved :: Apache Software License",
          "Typing :: Typed",
      ]
)
