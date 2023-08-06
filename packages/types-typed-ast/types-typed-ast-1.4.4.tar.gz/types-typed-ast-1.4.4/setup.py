from setuptools import setup

name = "types-typed-ast"
description = "Typing stubs for typed-ast"
long_description = '''
## Typing stubs for typed-ast

This is a PEP 561 type stub package for the `typed-ast` package.
It can be used by type-checking tools like mypy, PyCharm, pytype etc. to check code
that uses `typed-ast`. The source for this package can be found at
https://github.com/python/typeshed/tree/master/stubs/typed-ast. All fixes for
types and metadata should be contributed there.

See https://github.com/python/typeshed/blob/master/README.md for more details.
This package was generated from typeshed commit `8b9d771b67acf13a35905c7d4996382394f23181`.
'''.lstrip()

setup(name=name,
      version="1.4.4",
      description=description,
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/python/typeshed",
      install_requires=[],
      packages=['typed_ast-stubs'],
      package_data={'typed_ast-stubs': ['ast3.pyi', '__init__.pyi', 'ast27.pyi', 'conversions.pyi', 'METADATA.toml']},
      license="Apache-2.0 license",
      classifiers=[
          "License :: OSI Approved :: Apache Software License",
          "Typing :: Typed",
      ]
)
