from setuptools import setup

name = "types-Markdown"
description = "Typing stubs for Markdown"
long_description = '''
## Typing stubs for Markdown

This is a PEP 561 type stub package for the `Markdown` package.
It can be used by type-checking tools like mypy, PyCharm, pytype etc. to check code
that uses `Markdown`. The source for this package can be found at
https://github.com/python/typeshed/tree/master/stubs/Markdown. All fixes for
types and metadata should be contributed there.

See https://github.com/python/typeshed/blob/master/README.md for more details.
This package was generated from typeshed commit `ef5b4b6820ba7638d4749e9642a1d4bc2bc95707`.
'''.lstrip()

setup(name=name,
      version="3.3.1",
      description=description,
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/python/typeshed",
      install_requires=[],
      packages=['markdown-stubs'],
      package_data={'markdown-stubs': ['util.pyi', 'inlinepatterns.pyi', '__init__.pyi', 'blockparser.pyi', '__meta__.pyi', 'serializers.pyi', 'blockprocessors.pyi', 'treeprocessors.pyi', 'core.pyi', 'postprocessors.pyi', 'preprocessors.pyi', 'pep562.pyi', 'extensions/wikilinks.pyi', 'extensions/legacy_em.pyi', 'extensions/extra.pyi', 'extensions/fenced_code.pyi', 'extensions/toc.pyi', 'extensions/__init__.pyi', 'extensions/codehilite.pyi', 'extensions/legacy_attrs.pyi', 'extensions/tables.pyi', 'extensions/meta.pyi', 'extensions/smarty.pyi', 'extensions/def_list.pyi', 'extensions/sane_lists.pyi', 'extensions/footnotes.pyi', 'extensions/attr_list.pyi', 'extensions/md_in_html.pyi', 'extensions/abbr.pyi', 'extensions/nl2br.pyi', 'extensions/admonition.pyi', 'METADATA.toml']},
      license="Apache-2.0 license",
      classifiers=[
          "License :: OSI Approved :: Apache Software License",
          "Typing :: Typed",
      ]
)
