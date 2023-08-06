from setuptools import setup

name = "types-mypy-extensions"
description = "Typing stubs for mypy-extensions"
long_description = '''
## Typing stubs for mypy-extensions

This is a PEP 561 type stub package for the `mypy-extensions` package.
It can be used by type-checking tools like mypy, PyCharm, pytype etc. to check code
that uses `mypy-extensions`. The source for this package can be found at
https://github.com/python/typeshed/tree/master/stubs/mypy-extensions. All fixes for
types and metadata should be contributed there.

See https://github.com/python/typeshed/blob/master/README.md for more details.
This package was generated from typeshed commit `ef5b4b6820ba7638d4749e9642a1d4bc2bc95707`.
'''.lstrip()

setup(name=name,
      version="0.4.6",
      description=description,
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/python/typeshed",
      install_requires=[],
      packages=['mypy_extensions-stubs'],
      package_data={'mypy_extensions-stubs': ['__init__.pyi', 'METADATA.toml']},
      license="Apache-2.0 license",
      classifiers=[
          "License :: OSI Approved :: Apache Software License",
          "Typing :: Typed",
      ]
)
