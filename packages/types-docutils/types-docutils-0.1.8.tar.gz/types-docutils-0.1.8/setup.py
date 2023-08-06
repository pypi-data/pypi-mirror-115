from setuptools import setup

name = "types-docutils"
description = "Typing stubs for docutils"
long_description = '''
## Typing stubs for docutils

This is a PEP 561 type stub package for the `docutils` package.
It can be used by type-checking tools like mypy, PyCharm, pytype etc. to check code
that uses `docutils`. The source for this package can be found at
https://github.com/python/typeshed/tree/master/stubs/docutils. All fixes for
types and metadata should be contributed there.

See https://github.com/python/typeshed/blob/master/README.md for more details.
This package was generated from typeshed commit `ef5b4b6820ba7638d4749e9642a1d4bc2bc95707`.
'''.lstrip()

setup(name=name,
      version="0.1.8",
      description=description,
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/python/typeshed",
      install_requires=[],
      packages=['docutils-stubs'],
      package_data={'docutils-stubs': ['frontend.pyi', 'examples.pyi', '__init__.pyi', 'io.pyi', 'nodes.pyi', 'core.pyi', 'statemachine.pyi', 'writers/__init__.pyi', 'transforms/__init__.pyi', 'parsers/__init__.pyi', 'parsers/null.pyi', 'parsers/recommonmark_wrapper.pyi', 'parsers/rst/roles.pyi', 'parsers/rst/states.pyi', 'parsers/rst/__init__.pyi', 'parsers/rst/nodes.pyi', 'readers/__init__.pyi', 'readers/doctree.pyi', 'readers/pep.pyi', 'readers/standalone.pyi', 'languages/__init__.pyi', 'utils/__init__.pyi', 'METADATA.toml']},
      license="Apache-2.0 license",
      classifiers=[
          "License :: OSI Approved :: Apache Software License",
          "Typing :: Typed",
      ]
)
