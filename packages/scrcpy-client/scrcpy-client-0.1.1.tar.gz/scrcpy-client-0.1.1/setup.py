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
    'version': '0.1.1',
    'description': 'A client of scrcpy',
    'long_description': '# Python Scrcpy Client\n\nThis package allows you to view and control android device in realtime. \n\nDocument is not finished, you can check `demo.py` for detail.\n\n## Reference\n- [py-android-viewer](https://github.com/razumeiko/py-android-viewer)\n- [scrcpy](https://github.com/Genymobile/scrcpy)\n\n## Add ability\nPlease check scrcpy 1.12.1 document: [Link](https://github.com/Genymobile/scrcpy/blob/v1.12.1/server/src/main/java/com/genymobile/scrcpy/ControlMessageReader.java)\n\n## TODO:\n- [ ] Update scrcpy to 1.19\n- [ ] Add control unit test',
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
