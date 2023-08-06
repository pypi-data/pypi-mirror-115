# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ciel',
 'ciel.classifier',
 'ciel.collection',
 'ciel.gamerule',
 'ciel.recognizer',
 'ciel.transition',
 'ciel.util',
 'ciel.video']

package_data = \
{'': ['*']}

install_requires = \
['asai-abyss>=0.3.2,<0.4.0',
 'click>=7.0',
 'colorama>=0.4.4,<0.5.0',
 'opencv-python-headless>=4.0,<5.0',
 'pandas>=1.3.1,<2.0.0',
 'scikit-learn>=0.24.2,<0.25.0',
 'tensorflow>=2.5.0,<3.0.0',
 'tqdm>=4.62.0,<5.0.0']

entry_points = \
{'console_scripts': ['analyze_video = scripts.analyze_video:main']}

setup_kwargs = {
    'name': 'asai-ciel',
    'version': '1.0.3',
    'description': '',
    'long_description': None,
    'author': 'haripo',
    'author_email': 'haripo@users.noreply.github.com',
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
