from setuptools import setup

name = "types-maxminddb"
description = "Typing stubs for maxminddb"
long_description = '''
## Typing stubs for maxminddb

This is a PEP 561 type stub package for the `maxminddb` package.
It can be used by type-checking tools like mypy, PyCharm, pytype etc. to check code
that uses `maxminddb`. The source for this package can be found at
https://github.com/python/typeshed/tree/master/stubs/maxminddb. All fixes for
types and metadata should be contributed there.

See https://github.com/python/typeshed/blob/master/README.md for more details.
This package was generated from typeshed commit `ef5b4b6820ba7638d4749e9642a1d4bc2bc95707`.
'''.lstrip()

setup(name=name,
      version="0.1.3",
      description=description,
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/python/typeshed",
      install_requires=['types-ipaddress'],
      packages=['maxminddb-stubs'],
      package_data={'maxminddb-stubs': ['decoder.pyi', '__init__.pyi', 'extension.pyi', 'compat.pyi', 'errors.pyi', 'const.pyi', 'reader.pyi', 'METADATA.toml']},
      license="Apache-2.0 license",
      classifiers=[
          "License :: OSI Approved :: Apache Software License",
          "Typing :: Typed",
      ]
)
