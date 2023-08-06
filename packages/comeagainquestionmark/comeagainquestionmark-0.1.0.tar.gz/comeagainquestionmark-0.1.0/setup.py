# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['comeagainquestionmark']

package_data = \
{'': ['*']}

install_requires = \
['SpeechRecognition>=3.8.1,<4.0.0',
 'alive-progress>=1.6.2,<2.0.0',
 'moviepy>=1.0.3,<2.0.0']

setup_kwargs = {
    'name': 'comeagainquestionmark',
    'version': '0.1.0',
    'description': 'Transcription tool for video to text',
    'long_description': None,
    'author': 'Henry Bergström',
    'author_email': 'henrybergstrom@protonmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
