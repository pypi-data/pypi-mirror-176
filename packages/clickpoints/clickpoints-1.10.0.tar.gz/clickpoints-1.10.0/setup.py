# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['clickpoints',
 'clickpoints.addons',
 'clickpoints.addons.CellDetector',
 'clickpoints.addons.CellMeasure',
 'clickpoints.addons.DetectorTester',
 'clickpoints.addons.DistanceMeasurement',
 'clickpoints.addons.DriftCorrection',
 'clickpoints.addons.Dronpa',
 'clickpoints.addons.ExportForFlow',
 'clickpoints.addons.ExportToExcel',
 'clickpoints.addons.FineContrastAdjust',
 'clickpoints.addons.GrabPlotData',
 'clickpoints.addons.Kymograph',
 'clickpoints.addons.LayerSorter',
 'clickpoints.addons.MeasureTool',
 'clickpoints.addons.PersistentMarkers',
 'clickpoints.addons.PolygonAddon',
 'clickpoints.addons.TileViewer',
 'clickpoints.addons.Track',
 'clickpoints.addons.TrackManager',
 'clickpoints.addons.imageio_plugin',
 'clickpoints.includes',
 'clickpoints.includes.qextendedgraphicsview',
 'clickpoints.modules']

package_data = \
{'': ['*'], 'clickpoints': ['icons/*']}

install_requires = \
['Pillow',
 'PyQt5',
 'QtAwesome',
 'QtPy',
 'imagecodecs',
 'imageio-ffmpeg',
 'imageio>=2.0.1',
 'matplotlib',
 'natsort',
 'peewee>=3.1',
 'psutil',
 'python-dateutil>=2.8.1',
 'qasync',
 'qimage2ndarray',
 'scikit-image>=0.14',
 'scipy==1.9.3',
 'sortedcontainers',
 'tifffile>=2020.2.16']

extras_require = \
{'docs': ['sphinx-rtd-theme>=1.1.1,<2.0.0',
          'sphinxcontrib-bibtex>=2.5.0,<3.0.0',
          'sphinxcontrib-svg2pdfconverter>=1.2.1,<2.0.0',
          'nbsphinx>=0.8.9,<0.9.0',
          'mock>=4.0.3,<5.0.0']}

entry_points = \
{'console_scripts': ['clickpoints = clickpoints.launch:main']}

setup_kwargs = {
    'name': 'clickpoints',
    'version': '1.10.0',
    'description': 'Scientific toolbox for manual and automatic image evaluation.',
    'long_description': '.. -*- mode: rst -*-\n\n|ClickPoints|\n\n.. |ClickPoints| image:: https://github.com/fabrylab/clickpoints/blob/master/docs/images/Logo.png\n\n|DOC|_  |Python36| |License|_ |DOI|_\n\n.. |DOC| image:: https://readthedocs.org/projects/clickpoints/badge/\n.. _DOC: http://clickpoints.readthedocs.io\n\n.. |Python36| image:: https://img.shields.io/badge/python-3.6-blue.svg\n\n.. |License| image:: https://img.shields.io/badge/License-GPLv3-blue.svg\n.. _License: http://www.gnu.org/licenses/gpl-3.0.html\n\n.. |DOI| image:: https://img.shields.io/badge/DOI-10.1111/2041--210X.12702-blue.svg\n.. _DOI: http://onlinelibrary.wiley.com/doi/10.1111/2041-210X.12702/full\n\nClick Points is a program written in the Python programming language, which serves on the one hand as an image viewer and on the other hand as an data display and annotation tool. Every frame can be annotated by a description, marked points/tracks, or marked areas (paint brush). This helps to view image data, do manual evaluation of data, helps to create semi-automatic evaluation or display the results of automatic image evaluation.\n\nPlease refere to our `Documentation <http://clickpoints.readthedocs.io/en/latest/>`_ for more information and instructions on installing it.\n',
    'author': 'Richard Gerum',
    'author_email': 'richard.gerum@fau.de',
    'maintainer': 'Alexander Winterl',
    'maintainer_email': 'alexander.winterl@fau.de',
    'url': 'https://github.com/fabrylab/clickpoints',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
