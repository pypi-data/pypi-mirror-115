# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['blenderless']

package_data = \
{'': ['*']}

install_requires = \
['bpy==2.91a0',
 'click>=8.0.1,<9.0.0',
 'hydra-core>=1.0.7,<2.0.0',
 'imageio',
 'pillow',
 'tqdm>=4.61.2,<5.0.0',
 'trimesh>=3.9.24,<4.0.0',
 'xvfbwrapper>=0.2.9,<0.3.0']

entry_points = \
{'console_scripts': ['blenderless = blenderless.cli:cli']}

setup_kwargs = {
    'name': 'blenderless',
    'version': '0.1.3',
    'description': 'Blenderless is the python package for easy headless rendering using blender.',
    'long_description': "# Blenderless\n\nBlenderless is the Python package for easy headless rendering using Blender.\n\n## How to use this\n\n### Python module\n\nCreate image from mesh:\n\n```python\nimport blenderless\npath_to_foo_png = blenderless.render('foo.stl')\n```\n\n### CLI\n\nrender geometry to image\n\n```sh\nblenderless image foo.stl\n```\n\nrender geometry to gif\n\n```sh\nblenderless gif foo.stl\n```\n\nrender config to image\n\n```sh\nblenderless config scene.yml\n```\n\n## Install\n\n```buildoutcfg\nsudo apt-get install xvfb\npipx install poetry==1.1.5\nmake .venv\n```\n\n### Testing\n\n```sh\nmake test\n```\n",
    'author': 'Axel Vlaminck',
    'author_email': 'axel.vlaminck@oqton.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/oqton/blenderless',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<3.8',
}


setup(**setup_kwargs)
