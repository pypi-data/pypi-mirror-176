# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ifly_atp',
 'ifly_atp.pretrain',
 'ifly_atp.pretrain.av2vec',
 'ifly_atp.pretrain.voice2vec',
 'ifly_atp.utils']

package_data = \
{'': ['*']}

install_requires = \
['jsonpath_rw>=1.4.0', 'requests>=2.26.0']

setup_kwargs = {
    'name': 'ifly-atp',
    'version': '1.0.0',
    'description': 'an sdk for iflytek atp',
    'long_description': None,
    'author': 'ybyang',
    'author_email': 'ybyang7@iflytek.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6',
}


setup(**setup_kwargs)
