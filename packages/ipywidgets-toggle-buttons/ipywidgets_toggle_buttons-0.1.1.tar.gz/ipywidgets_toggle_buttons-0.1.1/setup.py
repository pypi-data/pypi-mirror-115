# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['ipywidgets_toggle_buttons']

package_data = \
{'': ['*']}

install_requires = \
['ipywidgets>=7.6.3,<8.0.0']

setup_kwargs = {
    'name': 'ipywidgets-toggle-buttons',
    'version': '0.1.1',
    'description': 'PYPI package with better toggle buttons',
    'long_description': '==========================\nipywidgets_toggle_buttons\n==========================\n\n.. image:: https://img.shields.io/github/last-commit/stas-prokopiev/ipywidgets_toggle_buttons\n   :target: https://img.shields.io/github/last-commit/stas-prokopiev/ipywidgets_toggle_buttons\n   :alt: GitHub last commit\n\n.. image:: https://img.shields.io/github/license/stas-prokopiev/ipywidgets_toggle_buttons\n    :target: https://github.com/stas-prokopiev/ipywidgets_toggle_buttons/blob/master/LICENSE.txt\n    :alt: GitHub license<space><space>\n\n.. image:: https://readthedocs.org/projects/local-simple-database/badge/?version=latest\n    :target: https://local-simple-database.readthedocs.io/en/latest/?badge=latest\n    :alt: Documentation Status\n\n.. image:: https://travis-ci.org/stas-prokopiev/ipywidgets_toggle_buttons.svg?branch=master\n    :target: https://travis-ci.org/stas-prokopiev/ipywidgets_toggle_buttons\n\n.. image:: https://img.shields.io/pypi/v/ipywidgets_toggle_buttons\n   :target: https://img.shields.io/pypi/v/ipywidgets_toggle_buttons\n   :alt: PyPI\n\n.. image:: https://img.shields.io/pypi/pyversions/ipywidgets_toggle_buttons\n   :target: https://img.shields.io/pypi/pyversions/ipywidgets_toggle_buttons\n   :alt: PyPI - Python Version\n\n\n.. contents:: **Table of Contents**\n\nShort Overview.\n=========================\n\nipywidgets_toggle_buttons is a simple Python package(**py>=3.6**)\nwith the much nicer toggle buttons for ipywidgets\n\n\nLinks\n=====\n\n    * `PYPI <https://pypi.org/project/ipywidgets_toggle_buttons/>`_\n    * `readthedocs <https://local-simple-database.readthedocs.io/en/latest/>`_\n    * `GitHub <https://github.com/stas-prokopiev/ipywidgets_toggle_buttons>`_\n\nProject local Links\n===================\n\n    * `CONTRIBUTING <https://github.com/stas-prokopiev/ipywidgets_toggle_buttons/blob/master/CONTRIBUTING.rst>`_.\n\nContacts\n========\n\n    * Email: stas.prokopiev@gmail.com\n    * `vk.com <https://vk.com/stas.prokopyev>`_\n    * `Facebook <https://www.facebook.com/profile.php?id=100009380530321>`_\n\nLicense\n=======\n\nThis project is licensed under the MIT License.',
    'author': 'stanislav',
    'author_email': 'stas.prokopiev@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/stas-prokopiev/ipywidgets_toggle_buttons',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
