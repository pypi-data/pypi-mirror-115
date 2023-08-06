from setuptools import setup

name = "types-cachetools"
description = "Typing stubs for cachetools"
long_description = '''
## Typing stubs for cachetools

This is a PEP 561 type stub package for the `cachetools` package.
It can be used by type-checking tools like mypy, PyCharm, pytype etc. to check code
that uses `cachetools`. The source for this package can be found at
https://github.com/python/typeshed/tree/master/stubs/cachetools. All fixes for
types and metadata should be contributed there.

See https://github.com/python/typeshed/blob/master/README.md for more details.
This package was generated from typeshed commit `ef5b4b6820ba7638d4749e9642a1d4bc2bc95707`.
'''.lstrip()

setup(name=name,
      version="0.1.10",
      description=description,
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/python/typeshed",
      install_requires=[],
      packages=['cachetools-stubs'],
      package_data={'cachetools-stubs': ['lru.pyi', 'ttl.pyi', '__init__.pyi', 'lfu.pyi', 'rr.pyi', 'func.pyi', 'abc.pyi', 'decorators.pyi', 'cache.pyi', 'METADATA.toml']},
      license="Apache-2.0 license",
      classifiers=[
          "License :: OSI Approved :: Apache Software License",
          "Typing :: Typed",
      ]
)
