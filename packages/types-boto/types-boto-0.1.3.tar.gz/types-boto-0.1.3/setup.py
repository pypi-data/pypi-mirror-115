from setuptools import setup

name = "types-boto"
description = "Typing stubs for boto"
long_description = '''
## Typing stubs for boto

This is a PEP 561 type stub package for the `boto` package.
It can be used by type-checking tools like mypy, PyCharm, pytype etc. to check code
that uses `boto`. The source for this package can be found at
https://github.com/python/typeshed/tree/master/stubs/boto. All fixes for
types and metadata should be contributed there.

See https://github.com/python/typeshed/blob/master/README.md for more details.
This package was generated from typeshed commit `ef5b4b6820ba7638d4749e9642a1d4bc2bc95707`.
'''.lstrip()

setup(name=name,
      version="0.1.3",
      description=description,
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/python/typeshed",
      install_requires=['types-six'],
      packages=['boto-stubs'],
      package_data={'boto-stubs': ['plugin.pyi', '__init__.pyi', 'auth.pyi', 'exception.pyi', 'compat.pyi', 'utils.pyi', 'connection.pyi', 'regioninfo.pyi', 'auth_handler.pyi', 'kms/layer1.pyi', 'kms/__init__.pyi', 'kms/exceptions.pyi', 'elb/__init__.pyi', 's3/multidelete.pyi', 's3/__init__.pyi', 's3/bucket.pyi', 's3/bucketlogging.pyi', 's3/prefix.pyi', 's3/key.pyi', 's3/lifecycle.pyi', 's3/tagging.pyi', 's3/user.pyi', 's3/connection.pyi', 's3/cors.pyi', 's3/keyfile.pyi', 's3/bucketlistresultset.pyi', 's3/acl.pyi', 's3/multipart.pyi', 's3/website.pyi', 's3/deletemarker.pyi', 'ec2/__init__.pyi', 'METADATA.toml']},
      license="Apache-2.0 license",
      classifiers=[
          "License :: OSI Approved :: Apache Software License",
          "Typing :: Typed",
      ]
)
