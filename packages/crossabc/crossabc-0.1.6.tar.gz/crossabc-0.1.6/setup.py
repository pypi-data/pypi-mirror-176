# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['crossabc']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.21.1', 'pandas>=1.1.5']

entry_points = \
{'console_scripts': ['crossabc = crossabc.crossabc:main']}

setup_kwargs = {
    'name': 'crossabc',
    'version': '0.1.6',
    'description': 'Easily CrossABC analyzer',
    'long_description': '# crossabc\n[![PyPI](https://img.shields.io/pypi/v/crossabc)](https://pypi.org/project/crossabc/)\n[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/crossabc)](https://pypi.org/project/crossabc/)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n[![license](https://img.shields.io/github/license/hrt0809/crossabc)](https://github.com/hrt0809/crossabc/blob/main/LICENSE)\n\nEasily CrossABC analyzer\n\n## Usage\n```Python\nfrom crossabc import CrossABC\nimport pandas as pd\n\ndf = pd.DataFrame(\n    data={\n        "sales": {"item_1": 30750, "item_2": 29000},\n        "profit": {"item_1": 8900, "item_2": 3430}\n        }\n    )\nc = CrossABC(df=df, indicators=["sales", "profit"])\nans_df = c.get_df()\n```\nWhen ```df``` is\n\n| | sales | profit |\n| :--- | ---: | ---: |\nitem_1 | 30750 | 8900 |\nitem_2 | 29000 | 3430 |\n\nand use ```CrossABC(df, ["sales", "profit"])```, now ```ans_df``` is\n\n| | sales | profit | rank_sales | rank_profit |\n| :--- | ---: | ---: | ---: | ---: |\nitem_1 | 30750 | 8900 | 6 | 8 |\nitem_2 | 29000 | 3430 | 10 | 10 |\n\n## Build\nThe source code is currently hosted on GitHub at: https://github.com/hrt0809/crossabc. Binary installers for the latest released version are available at the [PyPI](https://pypi.org/project/crossabc/).\n\n```\npip install crossabc\n```\n\n## Dependencies\n1. https://numpy.org\n1. https://pandas.pydata.org\n',
    'author': 'Hiroto Ueda',
    'author_email': 'hrt.ueda0809@gmail.com',
    'maintainer': 'Hiroto Ueda',
    'maintainer_email': 'hrt.ueda0809@gmail.com',
    'url': 'https://github.com/hrt0809/crossabc',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7',
}


setup(**setup_kwargs)
