# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['stltovoxel']

package_data = \
{'': ['*']}

install_requires = \
['Pillow>=9.3,<10.0',
 'matplotlib>=3.6,<4.0',
 'numpy-stl>=2.17,<3.0',
 'numpy>=1.13,<2.0']

entry_points = \
{'console_scripts': ['stltovoxel = stltovoxel.__main__:main']}

setup_kwargs = {
    'name': 'stl-to-voxel',
    'version': '0.9.3',
    'description': 'Turn STL files into voxels, images, and videos',
    'long_description': '# stl-to-voxel\nTurn STL files into voxels, images, and videos\n## Main Features\n* Convert stl files into a voxel representation\n* Output to (a series of) .pngs, .xyz, .svx\n* Command line interface\n\n## How to run\n### Run in command line\n```\npip install stl-to-voxel\nstltovoxel input.stl output.png\n```\n\n### Generating a higher resolution\n```bash\nstltovoxel input.stl output.png --resolution 200\n```\n\n### Specifying voxel size\n```bash\nstltovoxel input.stl output.png --voxel-size .5\n```\n\n### Multiple materials\n```bash\nstltovoxel input1.stl input2.stl output.png --colors "red,green"\n```\nHex color values are also supported\n```bash\nstltovoxel input1.stl input2.stl output.png --colors "#FF0000,#00FF00"\n```\n\n### Integrate into your code\n```python3\nimport stltovoxel\nstltovoxel.convert_file(\'input.stl\', \'output.png\')\n```\n\n### Run for development\n```bash\ncd stl-to-voxel\npython3 -m stltovoxel input.stl output.png\n```\n\n### Run unit tests\n```bash\ncd stl-to-voxel\nPYTHONPATH=./ python3 test/test_slice.py\n```\n\n<!--- https://commons.wikimedia.org/wiki/File:Stanford_Bunny.stl --->\n\nThe resolution is optional and defaults to 100.\n\n### Example:\n![alt text](https://github.com/cpederkoff/stl-to-voxel/raw/master/data/stanford_bunny.png "STL version of the stanford bunny")\n![alt text](https://github.com/cpederkoff/stl-to-voxel/raw/master/data/stanford_bunny.gif "voxel version of the stanford bunny")\n### Multi-color Example:\n<p float="left">\n  <img src="https://github.com/cpederkoff/stl-to-voxel/raw/master/data/traffic_cone_1.png" width="300" alt="STL version of the orange part of the model">\n  <img src="https://github.com/cpederkoff/stl-to-voxel/raw/master/data/traffic_cone_2.png" width="300" alt="STL version of the white part of the model">\n  <img src="https://github.com/cpederkoff/stl-to-voxel/raw/master/data/traffic_cone.gif" width="300" alt="voxel version of the traffic cone">\n</p>\n\n[Model credit](https://www.thingiverse.com/thing:21773)\n',
    'author': 'Christian Pederkoff',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/cpederkoff/stl-to-voxel',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
