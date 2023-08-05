# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['melange',
 'melange.drivers',
 'melange.drivers.aws',
 'melange.drivers.rabbitmq',
 'melange.helpers',
 'melange.infrastructure',
 'melange.tests']

package_data = \
{'': ['*']}

install_requires = \
['boto3>=1.11.5,<2.0.0',
 'funcy>=1.14,<2.0',
 'marshmallow>=3.3.0,<4.0.0',
 'methoddispatch>=3.0.2,<4.0.0',
 'pika>=1.1.0,<2.0.0',
 'pyopenssl>=19.1.0,<20.0.0',
 'pytz>=2019.3,<2020.0',
 'redis-simple-cache-py3>=0.0.7,<0.0.8',
 'singleton-py3>=0.2.1,<0.3.0']

setup_kwargs = {
    'name': 'melange',
    'version': '6.0.1',
    'description': 'A messaging library for an easy inter-communication in distributed and microservices architectures',
    'long_description': None,
    'author': 'David Jiménez (Rydra)',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.0,<4.0.0',
}


setup(**setup_kwargs)
