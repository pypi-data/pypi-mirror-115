from setuptools import setup

name = "types-paramiko"
description = "Typing stubs for paramiko"
long_description = '''
## Typing stubs for paramiko

This is a PEP 561 type stub package for the `paramiko` package.
It can be used by type-checking tools like mypy, PyCharm, pytype etc. to check code
that uses `paramiko`. The source for this package can be found at
https://github.com/python/typeshed/tree/master/stubs/paramiko. All fixes for
types and metadata should be contributed there.

See https://github.com/python/typeshed/blob/master/README.md for more details.
This package was generated from typeshed commit `8b9d771b67acf13a35905c7d4996382394f23181`.
'''.lstrip()

setup(name=name,
      version="0.1.9",
      description=description,
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/python/typeshed",
      install_requires=['types-cryptography'],
      packages=['paramiko-stubs'],
      package_data={'paramiko-stubs': ['ecdsakey.pyi', 'util.pyi', 'pipe.pyi', 'pkey.pyi', 'common.pyi', 'rsakey.pyi', 'ssh_exception.pyi', 'kex_curve25519.pyi', 'buffered_pipe.pyi', '__init__.pyi', '_winapi.pyi', 'py3compat.pyi', 'proxy.pyi', 'transport.pyi', 'kex_ecdh_nist.pyi', 'sftp_file.pyi', 'kex_gss.pyi', 'ber.pyi', 'primes.pyi', 'ssh_gss.pyi', 'hostkeys.pyi', 'sftp_handle.pyi', 'channel.pyi', 'packet.pyi', 'sftp_server.pyi', 'dsskey.pyi', 'win_pageant.pyi', 'kex_group14.pyi', 'sftp.pyi', 'client.pyi', 'sftp_attr.pyi', 'kex_group1.pyi', 'message.pyi', 'config.pyi', 'file.pyi', 'ed25519key.pyi', 'compress.pyi', 'server.pyi', 'sftp_si.pyi', 'agent.pyi', 'kex_group16.pyi', 'kex_gex.pyi', '_version.pyi', 'auth_handler.pyi', 'sftp_client.pyi', 'METADATA.toml']},
      license="Apache-2.0 license",
      classifiers=[
          "License :: OSI Approved :: Apache Software License",
          "Typing :: Typed",
      ]
)
