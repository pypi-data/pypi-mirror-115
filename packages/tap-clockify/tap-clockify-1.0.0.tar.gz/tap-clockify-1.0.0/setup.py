# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tap_clockify']

package_data = \
{'': ['*'], 'tap_clockify': ['schemas/*']}

install_requires = \
['requests>=2.26.0,<3.0.0', 'singer-python==5.9.0']

setup_kwargs = {
    'name': 'tap-clockify',
    'version': '1.0.0',
    'description': 'Singer tap for extracting data from Clockify',
    'long_description': '# tap-clockify\n\n**Author**: Stephen Bailey (sbailey@immuta.com)\n\nThis is a [Singer](http://singer.io) tap that produces JSON-formatted data following the [Singer spec](https://github.com/singer-io/getting-started/blob/master/SPEC.md).\n\nIt can generate a catalog of available data in Clockify and extract the following resources:\n\n- clients\n- projects\n- tags\n- tasks\n- time entries\n- users\n- workspaces\n\n### Configuration\n\n```\n{\n  "api_key": "string",\n  "workspace": "string",\n  "start_date": "2020-04-01T00:00:00Z"\n}\n```\n\n### Quick Start\n\n1. Install\n\n```bash\ngit clone git@github.com:immuta/tap-clockify.git\ncd tap-clockify\npip install .\n```\n\n2. Get an [API key](https://clockify.me/developers-api) from Clockify\n\n3. Create the config file.\n\nThere is a template you can use at `config.json.example`, just copy it to `config.json` in the repo root and insert your token\n\n4. Run the application to generate a catalog.\n\n```bash\ntap-clockify -c config.json --discover > catalog.json\n```\n\n5. Select the tables you\'d like to replicate\n\nStep 4 generates a a file called `catalog.json` that specifies all the available endpoints and fields. You\'ll need to open the file and select the ones you\'d like to replicate. See the [Singer guide on Catalog Format](https://github.com/singer-io/getting-started/blob/c3de2a10e10164689ddd6f24fee7289184682c1f/BEST_PRACTICES.md#catalog-format) for more information on how tables are selected.\n\n6. Run it!\n\n```bash\ntap-clockify -c config.json --catalog catalog.json\n```\n\n### Acknowledgements\n\nWould like to acknowledge the folks at Fishtown Analytics whose [`tap-framework`](https://github.com/fishtown-analytics/tap-framework) and [`tap-lever`](https://github.com/fishtown-analytics/tap-lever) packages formed the foundation for this package.\n\nCopyright &copy; 2019 Immuta\n',
    'author': 'Stephen Bailey',
    'author_email': 'stkbailey@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
