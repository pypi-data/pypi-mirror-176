# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['stlinmc']

package_data = \
{'': ['*']}

install_requires = \
['joblib>=1.1,<2.0',
 'mcpi>=1.2,<2.0',
 'numpy-stl>=2.17,<3.0',
 'numpy>=1.22,<2.0',
 'poetry>=1.2.2,<2.0.0',
 'pre-commit>=2.20,<3.0',
 'stl-to-voxel>=0.9,<0.10',
 'validators>=0.19,<0.20']

entry_points = \
{'console_scripts': ['stlinmc = stlinmc.__main__:main']}

setup_kwargs = {
    'name': 'stl-in-mc',
    'version': '0.1.6',
    'description': 'Import STL files into Minecraft',
    'long_description': '# stl-in-mc\nImport STL files into Minecraft via Raspberry Juice server plugin\n\n## Usage\n### Command line\n```\npip install stl-in-mc\nstlinmc input.stl example.minecraft.server --port 4711\n```\n',
    'author': 'Martin Miglio',
    'author_email': 'code@martinmiglio.dev',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/marmig0404/stl-in-mc',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
