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
    'version': '0.0.3',
    'description': 'the robot for chat system',
    'long_description': "\n# Ask robot\n\n**using cloud functions to do soma daily things**\n\n# todo\n\n**main todo**\n\n- [ ] update docs to use cloud functions to connect wechat platform\n- [ ] delete local operations, like files\n\n\n# install python\n\n\n## build from source\n\n```shell\nwget https://www.python.org/ftp/python/3.9.7/Python-3.9.7.tar.xz\ntar -xzvf Python-3.9.7.tar.xz\n\ncd Python-3.9.7\n./configure --prefix=/opt/idlepig/apps/python397\nmake\nmake altinstall\n\ncd ~/code/venv\n/opt/idlepig/apps/python397/bin/python3.9 -m venv wx\nsource ~/code/venv/wx/bin/activate\n\ncd ~/code/wx\npip install -r requirements.txt\n```\n\n\n## create environment\n\nin centos\n\n```shell\nyum install python36u\n```\n\ncreate virtual environment and source\n\n```shell\nmkdir -p ~/code/venv\ncd ~/code/venv\npython3 -m venv wx\nsource ~/code/venv/wx/bin/activate\n```\n\ncopy files in this project to server.\n\nfirstly, login in your server, then, clone github repository\n\n**todo: push code to github**\n\n```shell\nmkdir -p ~/code\ncd ~/code\ngit clone https://github.com/idlepig/wx.git\ncd wx\n```\n\ninstall third requirement\n```shell\npip install -r requirements.txt\n```\n\n## start flask service\n\nyou need set actual info for token, aes_key, appid\n\nif you are in plaintext mode, just set token is ok.\n\n```shell\nexport token=''\nexport app_id=''\nexport aes_key=''\nexport secret=''\nexport email_from=''\nexport email_password=''\nexport email_to=''\n```\n\n```shell\nsh auto.sh\n```\n\nthe http://0.0.0.0:8081 will work\n\n# install nginx\n\n\n```shell\nyum install nginx\n```\n\nvi /etc/nginx/nginx.conf\n\n```shell\nhttp {\n...\nupstream idlepig {\n    server 127.0.0.1:8081;\n  }\n...\n}\n```\n\nvi /etc/nginx/conf.d/default.conf\n\n```shell\nserver {\n    listen 80;\n    server_name _;\n    location / {\n      proxy_pass http://idlepig;\n    }\n}\n```\n\nso, we map 80 port to 8081 port\n\nstart nginx\n\n```shell\nnginx\n```\n\n# for WeChat platform\n\n[article_for_wx.py](article_for_wx.py) has chinese comment is only for WeChat platform\n\n这个脚本是微信公众号里面都脚本文件\n\n# logs file location\n\n/opt/idlewith/logs/output.log\n",
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
