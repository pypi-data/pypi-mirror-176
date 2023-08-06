from setuptools import setup

name = "types-tzlocal"
description = "Typing stubs for tzlocal"
long_description = '''
## Typing stubs for tzlocal

This is a PEP 561 type stub package for the `tzlocal` package.
It can be used by type-checking tools like mypy, PyCharm, pytype etc. to check code
that uses `tzlocal`. The source for this package can be found at
https://github.com/python/typeshed/tree/main/stubs/tzlocal. All fixes for
types and metadata should be contributed there.

See https://github.com/python/typeshed/blob/main/README.md for more details.
This package was generated from typeshed commit `1733c460582e6bf83a3592e5b24f9fd0e3fdeddc`.
'''.lstrip()

setup(name=name,
      version="4.2.2.2",
      description=description,
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/python/typeshed",
      project_urls={
          "GitHub": "https://github.com/python/typeshed",
          "Changes": "https://github.com/typeshed-internal/stub_uploader/blob/main/data/changelogs/tzlocal.md",
          "Issue tracker": "https://github.com/python/typeshed/issues",
          "Chat": "https://gitter.im/python/typing",
      },
      install_requires=['types-pytz'],
      packages=['tzlocal-stubs'],
      package_data={'tzlocal-stubs': ['__init__.pyi', 'utils.pyi', 'windows_tz.pyi', 'METADATA.toml']},
      license="Apache-2.0 license",
      classifiers=[
          "License :: OSI Approved :: Apache Software License",
          "Programming Language :: Python :: 3",
          "Typing :: Stubs Only",
      ]
)
