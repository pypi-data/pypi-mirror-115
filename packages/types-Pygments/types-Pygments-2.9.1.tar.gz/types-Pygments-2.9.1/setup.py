from setuptools import setup

name = "types-Pygments"
description = "Typing stubs for Pygments"
long_description = '''
## Typing stubs for Pygments

This is a PEP 561 type stub package for the `Pygments` package.
It can be used by type-checking tools like mypy, PyCharm, pytype etc. to check code
that uses `Pygments`. The source for this package can be found at
https://github.com/python/typeshed/tree/master/stubs/Pygments. All fixes for
types and metadata should be contributed there.

See https://github.com/python/typeshed/blob/master/README.md for more details.
This package was generated from typeshed commit `ef5b4b6820ba7638d4749e9642a1d4bc2bc95707`.
'''.lstrip()

setup(name=name,
      version="2.9.1",
      description=description,
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/python/typeshed",
      install_requires=['types-docutils'],
      packages=['pygments-stubs'],
      package_data={'pygments-stubs': ['modeline.pyi', 'util.pyi', 'plugin.pyi', '__init__.pyi', 'regexopt.pyi', 'sphinxext.pyi', 'token.pyi', 'formatter.pyi', 'style.pyi', 'console.pyi', 'lexer.pyi', 'cmdline.pyi', 'filter.pyi', 'scanner.pyi', 'unistring.pyi', 'lexers/__init__.pyi', 'formatters/__init__.pyi', 'formatters/rtf.pyi', 'formatters/_mapping.pyi', 'formatters/bbcode.pyi', 'formatters/terminal.pyi', 'formatters/latex.pyi', 'formatters/img.pyi', 'formatters/svg.pyi', 'formatters/irc.pyi', 'formatters/other.pyi', 'formatters/terminal256.pyi', 'formatters/html.pyi', 'formatters/pangomarkup.pyi', 'filters/__init__.pyi', 'styles/__init__.pyi', 'METADATA.toml']},
      license="Apache-2.0 license",
      classifiers=[
          "License :: OSI Approved :: Apache Software License",
          "Typing :: Typed",
      ]
)
