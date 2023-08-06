from setuptools import setup

name = "types-waitress"
description = "Typing stubs for waitress"
long_description = '''
## Typing stubs for waitress

This is a PEP 561 type stub package for the `waitress` package.
It can be used by type-checking tools like mypy, PyCharm, pytype etc. to check code
that uses `waitress`. The source for this package can be found at
https://github.com/python/typeshed/tree/master/stubs/waitress. All fixes for
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
      packages=['waitress-stubs'],
      package_data={'waitress-stubs': ['runner.pyi', 'trigger.pyi', 'parser.pyi', 'buffers.pyi', 'rfc7230.pyi', '__init__.pyi', 'receiver.pyi', 'task.pyi', 'compat.pyi', 'channel.pyi', 'utilities.pyi', 'wasyncore.pyi', 'proxy_headers.pyi', 'adjustments.pyi', 'server.pyi', 'METADATA.toml']},
      license="Apache-2.0 license",
      classifiers=[
          "License :: OSI Approved :: Apache Software License",
          "Typing :: Typed",
      ]
)
