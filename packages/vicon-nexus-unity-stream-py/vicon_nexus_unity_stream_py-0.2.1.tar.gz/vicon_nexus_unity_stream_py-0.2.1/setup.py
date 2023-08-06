# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['vicon_nexus_unity_stream_py', 'vicon_nexus_unity_stream_py.tests']

package_data = \
{'': ['*'], 'vicon_nexus_unity_stream_py': ['static/*']}

install_requires = \
['Flask-RESTful>=0.3.9,<0.4.0',
 'alive-progress>=2.4.1,<3.0.0',
 'click>=8.1.3,<9.0.0',
 'flask_restful>=0.3.8,<0.4.0',
 'loguru>=0.5.0,<0.6.0',
 'msgpack>=1.0.4,<2.0.0',
 'pandas>=1.5.1,<2.0.0']

entry_points = \
{'console_scripts': ['vicon-nexus-stream = '
                     'vicon_nexus_unity_stream_py.cli:_main']}

setup_kwargs = {
    'name': 'vicon-nexus-unity-stream-py',
    'version': '0.2.1',
    'description': 'Python script to stream data from vicon nexus to unity',
    'long_description': '# Overview\n\nPython script to stream data from vicon nexus to unity\n\n\n# Setup\n\n## Requirements\n\n* Python 3.8+\n\n## Installation\n\nInstall it directly into an activated virtual environment:\n\n```text\n$ pip install vicon_nexus_unity_stream_py\n```\n\nor add it to your [Poetry](https://poetry.eustace.io/) project:\n\n```text\n$ poetry add vicon_nexus_unity_stream_py\n```\n\n# Usage\n\nAfter installation, the package can be used as a cli tool:\n\n```text\n$ vicon-nexus-stream --help\n\nUsage: vicon-nexus-stream [OPTIONS] COMMAND [ARGS]...\n\nOptions:\n  --help  Show this message and exit.\n\nCommands:\n  server  Connects to the vicon and streams the data...\n  stream  Instead of connecting to vicon, streams data...\n  test    Test if connection is working\n```\n\n\n# Credits\nThis project was generated with [cookiecutter](https://github.com/audreyr/cookiecutter) using [jacebrowning/template-python](https://github.com/jacebrowning/template-python).\n',
    'author': 'Ahmed Shariff',
    'author_email': 'shariff.mfa@outlook.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://pypi.org/project/vicon_nexus_unity_stream_py',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
