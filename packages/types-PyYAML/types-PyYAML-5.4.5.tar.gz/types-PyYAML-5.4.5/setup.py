from setuptools import setup

name = "types-PyYAML"
description = "Typing stubs for PyYAML"
long_description = '''
## Typing stubs for PyYAML

This is a PEP 561 type stub package for the `PyYAML` package.
It can be used by type-checking tools like mypy, PyCharm, pytype etc. to check code
that uses `PyYAML`. The source for this package can be found at
https://github.com/python/typeshed/tree/master/stubs/PyYAML. All fixes for
types and metadata should be contributed there.

See https://github.com/python/typeshed/blob/master/README.md for more details.
This package was generated from typeshed commit `8b9d771b67acf13a35905c7d4996382394f23181`.
'''.lstrip()

setup(name=name,
      version="5.4.5",
      description=description,
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/python/typeshed",
      install_requires=[],
      packages=['yaml-stubs'],
      package_data={'yaml-stubs': ['parser.pyi', 'dumper.pyi', '__init__.pyi', 'tokens.pyi', 'emitter.pyi', 'loader.pyi', 'events.pyi', 'nodes.pyi', 'composer.pyi', 'error.pyi', 'cyaml.pyi', 'resolver.pyi', 'representer.pyi', 'constructor.pyi', 'serializer.pyi', 'scanner.pyi', 'reader.pyi', 'METADATA.toml']},
      license="Apache-2.0 license",
      classifiers=[
          "License :: OSI Approved :: Apache Software License",
          "Typing :: Typed",
      ]
)
