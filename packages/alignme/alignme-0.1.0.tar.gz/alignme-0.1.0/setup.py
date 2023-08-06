# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['alignme']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=5.4.1', 'biopython>=1.79,<2.0', 'click>=8.0.0', 'rich>=10.3.0']

entry_points = \
{'console_scripts': ['alignme = alignme.__main__:main']}

setup_kwargs = {
    'name': 'alignme',
    'version': '0.1.0',
    'description': 'Alignment Tool based on Biopython',
    'long_description': 'alignme\n===========================\n\n|PyPI| |Python Version| |License| |Read the Docs| |Build| |Tests| |Codecov| |pre-commit| |Black|\n\n.. |PyPI| image:: https://img.shields.io/pypi/v/alignme.svg\n   :target: https://pypi.org/project/alignme/\n   :alt: PyPI\n.. |Python Version| image:: https://img.shields.io/pypi/pyversions/alignme\n   :target: https://pypi.org/project/alignme\n   :alt: Python Version\n.. |License| image:: https://img.shields.io/github/license/wxicu/alignme\n   :target: https://opensource.org/licenses/MIT\n   :alt: License\n.. |Read the Docs| image:: https://img.shields.io/readthedocs/alignme/latest.svg?label=Read%20the%20Docs\n   :target: https://alignme.readthedocs.io/\n   :alt: Read the documentation at https://alignme.readthedocs.io/\n.. |Build| image:: https://github.com/wxicu/alignme/workflows/Build%20alignme%20Package/badge.svg\n   :target: https://github.com/wxicu/alignme/actions?workflow=Package\n   :alt: Build Package Status\n.. |Tests| image:: https://github.com/wxicu/alignme/workflows/Run%20alignme%20Tests/badge.svg\n   :target: https://github.com/wxicu/alignme/actions?workflow=Tests\n   :alt: Run Tests Status\n.. |Codecov| image:: https://codecov.io/gh/wxicu/alignme/branch/master/graph/badge.svg\n   :target: https://codecov.io/gh/wxicu/alignme\n   :alt: Codecov\n.. |pre-commit| image:: https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white\n   :target: https://github.com/pre-commit/pre-commit\n   :alt: pre-commit\n.. |Black| image:: https://img.shields.io/badge/code%20style-black-000000.svg\n   :target: https://github.com/psf/black\n   :alt: Black\n\n\nFeatures\n--------\n\n* TODO\n\n\nInstallation\n------------\n\nYou can install *alignme* via pip_ from PyPI_:\n\n.. code:: console\n\n   $ pip install alignme\n\n\nUsage\n-----\n\nPlease see the `Command-line Reference <Usage_>`_ for details.\n\n\nCredits\n-------\n\nThis package was created with cookietemple_ using Cookiecutter_ based on Hypermodern_Python_Cookiecutter_.\n\n.. _cookietemple: https://cookietemple.com\n.. _Cookiecutter: https://github.com/audreyr/cookiecutter\n.. _PyPI: https://pypi.org/\n.. _Hypermodern_Python_Cookiecutter: https://github.com/cjolowicz/cookiecutter-hypermodern-python\n.. _pip: https://pip.pypa.io/\n.. _Usage: https://alignme.readthedocs.io/en/latest/usage.html\n',
    'author': 'xichenwu',
    'author_email': 'xichenwu@outlook.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/wxicu/alignme',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8.0,<4.0.0',
}


setup(**setup_kwargs)
