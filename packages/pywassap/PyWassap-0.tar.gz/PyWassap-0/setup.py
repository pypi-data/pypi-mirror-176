# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pywassap']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.8.3,<4.0.0']

setup_kwargs = {
    'name': 'pywassap',
    'version': '0',
    'description': 'PyWassap is a python library for sending WhatsApp messages using the WhatsApp Business API.',
    'long_description': '<p align="center">\n  <a href="https://pywassap.netlify.app"><img src="https://pywassap.netlify.app/img/logo-margin/pywassap-logo.png" alt="pywassap"></a>\n</p>\n<p align="center">\n    <em> A simple asynchronous Python library for WhatsApp Web.</em>\n</p>\n<p align="center">\n<a href="https://github.com/Aarif1430/pywassap/actions/workflows/test.yml" target="_blank">\n    <img src="https://github.com/Aarif1430/pywassap/actions/workflows/test.yml/badge.svg" alt="Test">\n</a>\n<a href="https://github.com/Aarif1430/pywassap/pulse" alt="Activity">\n    <img src="https://img.shields.io/github/commit-activity/m/Aarif1430/pywassap" /></a>\n<a href="https://github.com/Aarif1430/pywassap/actions/workflows/smokeshow.yml" target="_blank">\n    <img src="https://github.com/Aarif1430/pywassap/actions/workflows/smokeshow.yml/badge.svg" alt="Coverage">\n</p>\n</p>\n\n---\n\n**Documentation**: <a href="https://pywassap.netlify.app" target="_blank">https://pywassap.netlify.app</a>\n\n**Source Code**: <a href="https://github.com/Aarif1430/pywassap" target="_blank">https://github.com/Aarif1430/pywassap</a>\n\n---\n**PyWassap** is a python library for sending WhatsApp messages using the WhatsApp Business API. It is a wrapper around the WhatsApp Business API. The library is built on top of the [aiohttp](https://pypi.org/project/aiohttp/) library for asynchronous HTTP requests.\n\n**PyWassap** supports the following features:\n\n**1. Send WhatsApp messages** - Send WhatsApp messages to a single or multiple recipients.\n\n```Python\nfrom pywassap import PyWassap\n\nclient = WhatsApp(number, token)\nclient.send_message(\n    message="Hello World",\n    recipient_id="919999999999"\n    recipient_type="individual"\n)\n```\n\n**2. Send WhatsApp messages to multiple recipients** - Send WhatsApp messages to multiple recipients.\n\n```Python\nfrom pywassap import WhatsApp\n\nclient = WhatsApp(number, token)\nclient.send_message(\n    message="Hello World",\n    recipient_id=["919999999999", "919999999998"]\n    recipient_type="individual"\n)\n```\n\n\n## Requirements\nFor development, the following requirements are needed:\n```console\npython\naiohttp\n```\n\n## Installation\n\n<div class="termy">\n\n```console\n$ pip install pywassap\n---> 100%\nSuccessfully installed pywassap\n```\n\n</div>\n\n## License\n\nThis project is licensed under the terms of the [MIT license](https://github.com/Aarif1430/pywassap/blob/main/LICENSE).\n',
    'author': 'Aarif Malik',
    'author_email': 'malikarif13@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Aarif1430/pywassap',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
