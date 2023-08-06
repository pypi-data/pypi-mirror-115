# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['sha_assist']
install_requires = \
['click>=8.0.1,<9.0.0']

setup_kwargs = {
    'name': 'sha-assist',
    'version': '0.1.1',
    'description': 'Easy SHA1, SHA256, SHA384, SHA512 and MD5 HTTPS domain fingerprinting',
    'long_description': '# SHA Assistant\n\n## Easy SHA1, SHA256, SHA384, SHA512, MD5 HTTPS domain fingerprinting\\*\\*.\n\nQuick zero dependency fingerprinting with one command. sha_assist produces algorithmic digests of certificate public keys.\n\nOut of box, sha_assist exposes 5 key digests i.e. (SHA1, SHA256, SHA384, SHA512 and MD5) but can be easily extended using `hashlib.algorithms_available`.\n\nSee [Extensibility](#Extensibility)\n\nCredit to [dlenski](https://gist.github.com/dlenski) for [ssl.SSLSocket patching](https://gist.github.com/dlenski/fc42156c00a615f4aa18a6d19d67e208)\n\n## Installation\n\n## Usage and Options\n\n`python3 sha_assist -d google.com -p 443`\n\nUsage: sha_assist.py [OPTIONS]\n\n| Options                   | Description                                                        |\n| ------------------------- | ------------------------------------------------------------------ |\n| -d or --domain [required] | [Text] Domain URL to be fingerprinted (eg. https://www.github.com) |\n| -p, --port [optional]     | [Integer] Port to establish connection on. Defaults to 443         |\n\n**NOTE: URL must be prefixed with https://**\n\n## Extensibility\n\nsha-assist produces algorithmic digests using hash-lib. By extension, all methods exposed by `hashlib.algorithms_available` can be used to produce required digests.\nOutput is by default hex but can be adapted to binary by replacing ~.digestHex().\n',
    'author': 'AndrewGlago',
    'author_email': 'andrewglago1@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/AndrewGlago/sha-assist',
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
