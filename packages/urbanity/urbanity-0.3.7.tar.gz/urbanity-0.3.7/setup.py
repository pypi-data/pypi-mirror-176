# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['urbanity']

package_data = \
{'': ['*'],
 'urbanity': ['map_data/*',
              'svi_data/Bangkok.geojson',
              'svi_data/Bangkok.geojson',
              'svi_data/Bangkok.geojson',
              'svi_data/Bangkok.geojson',
              'svi_data/Bangkok.geojson',
              'svi_data/Bangkok.geojson',
              'svi_data/Chicago.geojson',
              'svi_data/Chicago.geojson',
              'svi_data/Chicago.geojson',
              'svi_data/Chicago.geojson',
              'svi_data/Chicago.geojson',
              'svi_data/Chicago.geojson',
              'svi_data/Paris.geojson',
              'svi_data/Paris.geojson',
              'svi_data/Paris.geojson',
              'svi_data/Paris.geojson',
              'svi_data/Paris.geojson',
              'svi_data/Paris.geojson',
              'svi_data/Seattle.geojson',
              'svi_data/Seattle.geojson',
              'svi_data/Seattle.geojson',
              'svi_data/Seattle.geojson',
              'svi_data/Seattle.geojson',
              'svi_data/Seattle.geojson',
              'svi_data/Singapore.geojson',
              'svi_data/Singapore.geojson',
              'svi_data/Singapore.geojson',
              'svi_data/Singapore.geojson',
              'svi_data/Singapore.geojson',
              'svi_data/Singapore.geojson',
              'svi_data/num_to_class.json',
              'svi_data/num_to_class.json',
              'svi_data/num_to_class.json',
              'svi_data/num_to_class.json',
              'svi_data/num_to_class.json',
              'svi_data/num_to_class.json']}

install_requires = \
['charset-normalizer==2.1.1',
 'geopandas==0.12.0',
 'ipykernel==6.16.2',
 'ipyleaflet==0.17.2',
 'networkit==10.0',
 'networkx==2.8.6',
 'numpy==1.23.3',
 'pyrobuf==0.9.3',
 'pyrosm==0.6.1',
 'rasterio==1.3.2',
 'rasterstats==0.17.0',
 'urllib3>=1.26.11,<2.0.0',
 'vt2geojson>=0.2.1,<0.3.0']

setup_kwargs = {
    'name': 'urbanity',
    'version': '0.3.7',
    'description': '',
    'long_description': None,
    'author': 'winstonyym',
    'author_email': 'winstonyym@u.nus.edu',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
