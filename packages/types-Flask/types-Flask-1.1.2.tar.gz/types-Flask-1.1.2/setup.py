from setuptools import setup

name = "types-Flask"
description = "Typing stubs for Flask"
long_description = '''
## Typing stubs for Flask

This is a PEP 561 type stub package for the `Flask` package.
It can be used by type-checking tools like mypy, PyCharm, pytype etc. to check code
that uses `Flask`. The source for this package can be found at
https://github.com/python/typeshed/tree/master/stubs/Flask. All fixes for
types and metadata should be contributed there.

*Note:* The `Flask` package includes type annotations or type stubs
since version 2.0. Please uninstall the `types-Flask`
package if you use this or a newer version.


See https://github.com/python/typeshed/blob/master/README.md for more details.
This package was generated from typeshed commit `ef5b4b6820ba7638d4749e9642a1d4bc2bc95707`.
'''.lstrip()

setup(name=name,
      version="1.1.2",
      description=description,
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/python/typeshed",
      install_requires=['types-Jinja2', 'types-Werkzeug', 'types-click'],
      packages=['flask-stubs'],
      package_data={'flask-stubs': ['helpers.pyi', 'testing.pyi', 'ctx.pyi', 'blueprints.pyi', 'debughelpers.pyi', '__init__.pyi', 'logging.pyi', 'signals.pyi', 'app.pyi', 'views.pyi', 'config.pyi', 'templating.pyi', 'globals.pyi', 'sessions.pyi', 'cli.pyi', 'wrappers.pyi', 'json/__init__.pyi', 'json/tag.pyi', 'METADATA.toml']},
      license="Apache-2.0 license",
      classifiers=[
          "License :: OSI Approved :: Apache Software License",
          "Typing :: Typed",
      ]
)
