# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['viburnum', 'viburnum.application', 'viburnum.cli', 'viburnum.deployer']

package_data = \
{'': ['*']}

extras_require = \
{'cdk': ['aws-cdk-lib==2.50.0'],
 'constructs': ['constructs>=10.0.0,<11.0.0'],
 'deployer': ['constructs>=10.0.0,<11.0.0', 'aws-cdk-lib==2.50.0']}

setup_kwargs = {
    'name': 'viburnum',
    'version': '0.1.1',
    'description': "It's abstraction on top of AWS CDK, that helps in building serverless web applications.",
    'long_description': "# Viburnum\n\n**Viburum** - it's a small framework built on top of AWS CDK to simplify development and deploying AWS Serverless web applications.\n",
    'author': 'Yaroslav Martynenko',
    'author_email': 'stikblacklabel@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'extras_require': extras_require,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
