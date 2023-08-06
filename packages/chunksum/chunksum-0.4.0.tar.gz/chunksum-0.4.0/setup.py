# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['chunksum']

package_data = \
{'': ['*']}

install_requires = \
['fastcdc>=1.4.2,<2.0.0', 'tqdm>=4.64.1,<5.0.0']

entry_points = \
{'console_scripts': ['chunksum = chunksum.cli:main']}

setup_kwargs = {
    'name': 'chunksum',
    'version': '0.4.0',
    'description': 'Print FastCDC rolling hash chunks and checksums.',
    'long_description': '# chunksum\n\n[![test](https://github.com/xyb/chunksum/actions/workflows/test.yml/badge.svg)](https://github.com/xyb/chunksum/actions/workflows/test.yml)\n[![codecov](https://codecov.io/gh/xyb/chunksum/branch/main/graph/badge.svg?token=LR3ET0TBK2)](https://codecov.io/gh/xyb/chunksum)\n[![Maintainability](https://api.codeclimate.com/v1/badges/9bd0a3b4fcefb196b2f8/maintainability)](https://codeclimate.com/github/xyb/chunksum/maintainability)\n[![Latest version](https://img.shields.io/pypi/v/chunksum.svg)](https://pypi.org/project/chunksum/)\n[![Support python versions](https://img.shields.io/pypi/pyversions/chunksum)](https://pypi.org/project/chunksum/)\n\nPrint FastCDC rolling hash chunks and checksums.\n\n```\nUsage: chunksum <dir> [<alg_name>] [<prev_chunksums_file>]\n\nalg_name:\n  Format "fc[k|m|g][0-9][sha2|blake2b|blake2s][32]".\n\n  For example, "fck4sha2", means using FastCDC("fc") with an\n  average chunk size of 2**8=256KB("k8") and using sha256("sha2")\n  to calculate the checksum.\n\n  "fcm4blake2b32" means using FastCDC with an average chunk size\n  of 2**4=16MB("m4") and using "blake2b" to calculate and output\n  a checksum of length "32" bytes(save storage).\n\n  For large files, you may using large chunk size, such as "m4",\n  to reduce the number of chunks.\n\n  (default: fck4sha2)\n\nprev_chunksums_file:\n  You can specify the previous chunksums file if you want to\n  resume a previous check, or if you want to find the incremental\n  updates (new files) of the directory.\n\n\nExamples:\n\n  $ chunksum /etc > ~/etc.chunksums\n\n  $ chunksum ~/Videos fcm4blake2b32 > ~/Videos/chunksums\n\n  $ chunksum ~/Videos fcm4blake2b32 ~/chunksums > ~/chunksums.incr\n```\n',
    'author': 'Xie Yanbo',
    'author_email': 'xieyanbo@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/xyb/chunksum',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
