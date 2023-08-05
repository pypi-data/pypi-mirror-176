# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['adtsdk']

package_data = \
{'': ['*']}

install_requires = \
['pandas>=1.3.5,<1.4.0', 'requests>=2.28.1,<3.0.0']

entry_points = \
{'console_scripts': ['add-datasource = adtsdk.cli:add_datasource',
                     'delete-datasource = adtsdk.cli:delete_datasource',
                     'upload-data = adtsdk.cli:upload_data']}

setup_kwargs = {
    'name': 'adt-sdk',
    'version': '1.0.0a1',
    'description': 'ADT SDK',
    'long_description': None,
    'author': 'Hellen',
    'author_email': 'hellen@datamole.cz',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/datamole-ai/adt-sdk',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7.9,<3.11',
}


setup(**setup_kwargs)
