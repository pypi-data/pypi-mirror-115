from setuptools import setup

name = "types-PyMySQL"
description = "Typing stubs for PyMySQL"
long_description = '''
## Typing stubs for PyMySQL

This is a PEP 561 type stub package for the `PyMySQL` package.
It can be used by type-checking tools like mypy, PyCharm, pytype etc. to check code
that uses `PyMySQL`. The source for this package can be found at
https://github.com/python/typeshed/tree/master/stubs/PyMySQL. All fixes for
types and metadata should be contributed there.

See https://github.com/python/typeshed/blob/master/README.md for more details.
This package was generated from typeshed commit `ef5b4b6820ba7638d4749e9642a1d4bc2bc95707`.
'''.lstrip()

setup(name=name,
      version="1.0.1",
      description=description,
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/python/typeshed",
      install_requires=[],
      packages=['pymysql-stubs'],
      package_data={'pymysql-stubs': ['util.pyi', 'charset.pyi', 'converters.pyi', '__init__.pyi', 'cursors.pyi', 'times.pyi', 'connections.pyi', 'err.pyi', 'constants/__init__.pyi', 'constants/SERVER_STATUS.pyi', 'constants/FLAG.pyi', 'constants/FIELD_TYPE.pyi', 'constants/COMMAND.pyi', 'constants/CLIENT.pyi', 'constants/ER.pyi', 'METADATA.toml']},
      license="Apache-2.0 license",
      classifiers=[
          "License :: OSI Approved :: Apache Software License",
          "Typing :: Typed",
      ]
)
