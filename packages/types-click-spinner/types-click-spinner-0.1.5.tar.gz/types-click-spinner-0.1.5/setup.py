from setuptools import setup

name = "types-click-spinner"
description = "Typing stubs for click-spinner"
long_description = '''
## Typing stubs for click-spinner

This is a PEP 561 type stub package for the `click-spinner` package.
It can be used by type-checking tools like mypy, PyCharm, pytype etc. to check code
that uses `click-spinner`. The source for this package can be found at
https://github.com/python/typeshed/tree/master/stubs/click-spinner. All fixes for
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
      packages=['click_spinner-stubs'],
      package_data={'click_spinner-stubs': ['__init__.pyi', 'METADATA.toml']},
      license="Apache-2.0 license",
      classifiers=[
          "License :: OSI Approved :: Apache Software License",
          "Typing :: Typed",
      ]
)
