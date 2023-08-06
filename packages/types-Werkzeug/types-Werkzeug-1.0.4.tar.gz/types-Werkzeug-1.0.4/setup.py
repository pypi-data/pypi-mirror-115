from setuptools import setup

name = "types-Werkzeug"
description = "Typing stubs for Werkzeug"
long_description = '''
## Typing stubs for Werkzeug

This is a PEP 561 type stub package for the `Werkzeug` package.
It can be used by type-checking tools like mypy, PyCharm, pytype etc. to check code
that uses `Werkzeug`. The source for this package can be found at
https://github.com/python/typeshed/tree/master/stubs/Werkzeug. All fixes for
types and metadata should be contributed there.

*Note:* The `Werkzeug` package includes type annotations or type stubs
since version 2.0. Please uninstall the `types-Werkzeug`
package if you use this or a newer version.


See https://github.com/python/typeshed/blob/master/README.md for more details.
This package was generated from typeshed commit `8b9d771b67acf13a35905c7d4996382394f23181`.
'''.lstrip()

setup(name=name,
      version="1.0.4",
      description=description,
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/python/typeshed",
      install_requires=[],
      packages=['werkzeug-stubs'],
      package_data={'werkzeug-stubs': ['serving.pyi', 'wsgi.pyi', '_compat.pyi', 'filesystem.pyi', '_reloader.pyi', '__init__.pyi', 'exceptions.pyi', 'security.pyi', 'routing.pyi', 'urls.pyi', 'testapp.pyi', 'local.pyi', 'utils.pyi', '_internal.pyi', 'useragents.pyi', 'http.pyi', 'datastructures.pyi', 'test.pyi', 'formparser.pyi', 'script.pyi', 'posixemulation.pyi', 'wrappers.pyi', 'middleware/http_proxy.pyi', 'middleware/dispatcher.pyi', 'middleware/__init__.pyi', 'middleware/shared_data.pyi', 'middleware/profiler.pyi', 'middleware/lint.pyi', 'middleware/proxy_fix.pyi', 'debug/__init__.pyi', 'debug/tbtools.pyi', 'debug/console.pyi', 'debug/repr.pyi', 'contrib/iterio.pyi', 'contrib/fixers.pyi', 'contrib/__init__.pyi', 'contrib/securecookie.pyi', 'contrib/testtools.pyi', 'contrib/jsrouting.pyi', 'contrib/profiler.pyi', 'contrib/lint.pyi', 'contrib/limiter.pyi', 'contrib/atom.pyi', 'contrib/cache.pyi', 'contrib/sessions.pyi', 'contrib/wrappers.pyi', 'METADATA.toml']},
      license="Apache-2.0 license",
      classifiers=[
          "License :: OSI Approved :: Apache Software License",
          "Typing :: Typed",
      ]
)
