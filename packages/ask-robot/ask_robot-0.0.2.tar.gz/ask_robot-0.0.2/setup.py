# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['ask_robot', 'ask_robot.local', 'ask_robot.utils', 'ask_robot.web']

package_data = \
{'': ['*']}

install_requires = \
['Flask==2.0.3',
 'Jinja2==3.0.3',
 'MarkupSafe==2.0.1',
 'Pygments==2.11.2',
 'Werkzeug==2.0.3',
 'asttokens==2.0.5',
 'beautifulsoup4==4.10.0',
 'certifi==2021.10.8',
 'cffi==1.15.0',
 'charset-normalizer==2.0.12',
 'cheap-repr==0.5.1',
 'cheroot==8.6.0',
 'click==8.0.4',
 'dataclasses==0.6',
 'executing==0.8.3',
 'flake8==4.0.1',
 'idna==3.3',
 'importlib-metadata==4.8.3',
 'itsdangerous==2.0.1',
 'jaraco.functools==3.4.0',
 'line-profiler-pycharm==1.1.0',
 'line-profiler==3.5.0',
 'mccabe==0.6.1',
 'more-itertools==8.12.0',
 'optionaldict==0.1.2',
 'pycodestyle==2.8.0',
 'pycparser==2.21',
 'pycryptodome==3.14.1',
 'pyflakes==2.4.0',
 'python-dateutil==2.8.2',
 'requests==2.27.1',
 'semantic-version==2.9.0',
 'setuptools-rust==1.1.2',
 'six==1.16.0',
 'snoop==0.4.1',
 'soupsieve==2.3.1',
 'typing-extensions==4.1.1',
 'urllib3==1.26.8',
 'wechatpy==1.8.18',
 'xmltodict==0.12.0',
 'zipp==3.6.0']

setup_kwargs = {
    'name': 'ask-robot',
    'version': '0.0.2',
    'description': 'the robot for chat system',
    'long_description': 'None',
    'author': 'idlewith',
    'author_email': 'newellzhou@163.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
