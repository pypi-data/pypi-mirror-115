# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['scrcpy']

package_data = \
{'': ['*']}

install_requires = \
['av>=8.0.3,<9.0.0', 'opencv-python>=4.5.3,<5.0.0']

setup_kwargs = {
    'name': 'scrcpy-client',
    'version': '0.1.2',
    'description': 'A client of scrcpy',
    'long_description': '# Python Scrcpy Client\n\n![pypi package](https://img.shields.io/pypi/v/scrcpy-client)\n![build](https://img.shields.io/github/workflow/status/leng-yue/py-scrcpy-client/CI)\n![build](https://img.shields.io/github/license/leng-yue/py-scrcpy-client)\n\nThis package allows you to view and control android device in realtime. \n\n## How to use\nTo begin with, you need to install this package via pip:\n```shell\npip install scrcpy-client\n```\nThen, you can start `demo.py`:\n```shell\npython demo.py\n```\nNote: You need to install adb by yourself.\n\n## Contribution & Development\nPlease check scrcpy server 1.18 source code: [Link](https://github.com/Genymobile/scrcpy/tree/v1.18/server)\n\n## TODO:\n- [x] Support all KeyCodes\n- [x] Update scrcpy to 1.18\n- [ ] Add control unit test\n\n## Reference\n- [py-android-viewer](https://github.com/razumeiko/py-android-viewer)\n- [scrcpy](https://github.com/Genymobile/scrcpy)\n',
    'author': 'lengyue',
    'author_email': 'lengyue@lengyue.me',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/leng-yue/py-scrcpy-client',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
