# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['scrcpy']

package_data = \
{'': ['*']}

install_requires = \
['adbutils>=0.11.0,<0.12.0',
 'av>=8.0.3,<9.0.0',
 'click>=8.0.1,<9.0.0',
 'opencv-python>=4.5.3,<5.0.0']

entry_points = \
{'console_scripts': ['py-scrcpy = scrcpy.ui:main']}

setup_kwargs = {
    'name': 'scrcpy-client',
    'version': '0.2.2',
    'description': 'A client of scrcpy',
    'long_description': '# Python Scrcpy Client\n<p>\n    <a href="https://pypi.org/project/scrcpy-client/" target="_blank">\n        <img src="https://img.shields.io/pypi/v/scrcpy-client" />\n    </a>\n    <a href="https://github.com/leng-yue/py-scrcpy-client/actions/workflows/ci.yml" target="_blank">\n        <img src="https://img.shields.io/github/workflow/status/leng-yue/py-scrcpy-client/CI" />\n    </a>\n    <a href="https://app.codecov.io/gh/leng-yue/py-scrcpy-client" target="_blank">\n        <img src="https://img.shields.io/codecov/c/github/leng-yue/py-scrcpy-client" />\n    </a>\n    <img src="https://img.shields.io/github/license/leng-yue/py-scrcpy-client" />\n    <a href="https://github.com/Genymobile/scrcpy/tree/v1.18" target="_blank">\n        <img src="https://img.shields.io/badge/scrcpy-v1.18-violet" />\n    </a>\n</p>\n\nThis package allows you to view and control android device in realtime. \n\n![demo gif](https://raw.githubusercontent.com/leng-yue/py-scrcpy-client/main/demo.gif)\n\n## How to use\nTo begin with, you need to install this package via pip:\n```shell\npip install scrcpy-client\n```\nThen, you can start `script/ui.py`:\n```shell\npy-scrcpy\n// or python script/ui.py\n```\n\n## Contribution & Development\nPlease check scrcpy server 1.18 source code: [Link](https://github.com/Genymobile/scrcpy/tree/v1.18/server)\n\n## Reference\n- [py-android-viewer](https://github.com/razumeiko/py-android-viewer)\n- [scrcpy](https://github.com/Genymobile/scrcpy)\n',
    'author': 'lengyue',
    'author_email': 'lengyue@lengyue.me',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/leng-yue/py-scrcpy-client',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
