# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['communauto']

package_data = \
{'': ['*']}

install_requires = \
['colorama>=0.4.4,<0.5.0',
 'httpx>=0.18.1,<0.19.0',
 'pydantic>=1.8.2,<2.0.0',
 'pytz>=2021.1,<2022.0',
 'structlog>=21.1.0,<22.0.0',
 'tabulate>=0.8.9,<0.9.0',
 'typer>=0.3.2,<0.4.0']

entry_points = \
{'console_scripts': ['communauto = communauto:main']}

setup_kwargs = {
    'name': 'communauto',
    'version': '0.1.4',
    'description': '',
    'long_description': '# communauto\n\nCalculate cost estimates against rentals extracted from invoices in pdf format.\nOutput extracted data & estimates in csv format.\n\n## Install using pip:\n\n```\n$ pip install communato\n```\n\n## Usage\n\n```\n$ communauto --output result.csv invoice1.pdf invoice2.pdf ...\n```\n',
    'author': 'Hadrien David',
    'author_email': 'hadrien@ectobal.com',
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
