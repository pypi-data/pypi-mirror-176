# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pagemap']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.1,<9.0']

entry_points = \
{'console_scripts': ['pagemap = pagemap.entry:main']}

setup_kwargs = {
    'name': 'pagemap',
    'version': '0.1.1',
    'description': 'A tool for virtual memory.',
    'long_description': '# pagemap\n\nA tool for linux memory stats.\n\n## 依赖\n\n- Python 3.9+\n\n## 安装\n\n```terminal\npip install pagemap\n```\n\n## 使用Demo\n\n',
    'author': 'fffzlfk',
    'author_email': '1319933925qq@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
