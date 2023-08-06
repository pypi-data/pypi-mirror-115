# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['bqva']

package_data = \
{'': ['*']}

install_requires = \
['anytree>=2.8.0,<3.0.0',
 'click>=8.0.1,<9.0.0',
 'colorama>=0.4.4,<0.5.0',
 'google-cloud-bigquery>=2.23.2,<3.0.0',
 'yaspin>=2.0.0,<3.0.0']

extras_require = \
{'tests': ['coveralls>=3.2.0,<4.0.0']}

entry_points = \
{'console_scripts': ['bqva = bqva.cli:main']}

setup_kwargs = {
    'name': 'bigquery-view-analyzer',
    'version': '21.8.0',
    'description': 'CLI tool for managing + visualising BigQuery authorised views',
    'long_description': '# BigQuery View Analyzer\n\n[![PyPI version](https://img.shields.io/pypi/v/bigquery-view-analyzer.svg)](https://pypi.python.org/pypi/bigquery-view-analyzer)\n[![Python versions](https://img.shields.io/pypi/pyversions/bigquery-view-analyzer.svg)](https://pypi.python.org/pypi/bigquery-view-analyzer)\n[![Build status](https://img.shields.io/travis/servian/bigquery-view-analyzer.svg)](https://travis-ci.org/servian/bigquery-view-analyzer)\n[![Github license](https://img.shields.io/github/license/servian/bigquery-view-analyzer.svg)](https://github.com/servian/bigquery-view-analyzer)\n\n## Description\n\n`bigquery-view-analyzer` is a command-line tool for visualizing dependencies and managing permissions between BigQuery views.\n\nTo authorize a view, permissions must be granted at a dataset level for every view/table referenced in the view definition. This requirement cascades down to every view that\'s referenced by the parent view, they too must have permissions granted for every view/table they reference - and so on. This can quickly become difficult to manage if you have many nested views across multiple datasets and/or projects.\n\n`bigquery-view-analyzer` automatically resolves these dependencies and applies the relevant permissions to all views and datasets referenced by the parent view.\n\n## Installation\n\n```bash\n$ pip install bigquery-view-analyzer\n```\n\n## Usage\n\n```bash\n$ bqva --help\n```\n\n[![asciicast](https://asciinema.org/a/252724.svg)](https://asciinema.org/a/252724)\n\n### Example: CLI\n\n![Example tree](/docs/example.png)\n\nGiven the above datasets and tables in BigQuery, to authorize `bqva-demo:dataset_4.shared_view`, the following views would need to be authorized with each of the following datasets:\n\n- Authorized views for **`dataset_1`**\n  - `bqva-demo:dataset_3.view_a_b_c_d`\n- Authorized views for **`dataset_2`**\n  - `bqva-demo:dataset_3.view_a_b_c_d`\n  - `bqva-demo:dataset_1.view_c`\n- Authorized views for **`dataset_3`**\n  - `bqva-demo:dataset_2.view_d`\n  - `bqva-demo:dataset_4.shared_view`\n\nYou can easily visualize the above view hierarchy using the `bqva tree` command.\n\n```bash\n# View dependency tree and authorization status for \'bqva-demo:dataset_4.shared_view\'\n$ bqva tree --status --no-key --view "bqva-demo:dataset_4.shared_view"\nbqva-demo:dataset_4.shared_view\n└── bqva-demo:dataset_3.view_a_b_c_d (⨯)\n    ├── bqva-demo:dataset_1.table_a (⨯)\n    ├── bqva-demo:dataset_1.table_b (⨯)\n    ├── bqva-demo:dataset_1.view_c (⨯)\n    │   └── bqva-demo:dataset_2.table_c (⨯)\n    └── bqva-demo:dataset_2.view_d (⨯)\n        └── bqva-demo:dataset_3.table_d (⨯)\n```\n\nPermissions can be applied automatically to all datasets referenced by the parent view using the `bqva authorize` command.\n\n```bash\n# Apply all permissions required by \'bqva-demo:dataset_4.shared_view\'\n$ bqva authorize --view "bqva-demo:dataset_4.shared_view"\nbqva-demo:dataset_4.shared_view\n└── bqva-demo:dataset_3.view_a_b_c_d (✓)\n    ├── bqva-demo:dataset_1.table_a (✓)\n    ├── bqva-demo:dataset_1.table_b (✓)\n    ├── bqva-demo:dataset_1.view_c (✓)\n    │   └── bqva-demo:dataset_2.table_c (✓)\n    └── bqva-demo:dataset_2.view_d (✓)\n        └── bqva-demo:dataset_3.table_d (✓)\n```\n\nIf you want to revoke permissions for a view, you can do that too!\n\n```bash\n# Revoke all permissions granted to \'bqva-demo:dataset_4.shared_view\'\n$ bqva revoke --view "bqva-demo:dataset_4.shared_view"\nbqva-demo:dataset_4.shared_view\n└── bqva-demo:dataset_3.view_a_b_c_d (⨯)\n    ├── bqva-demo:dataset_1.table_a (⨯)\n    ├── bqva-demo:dataset_1.table_b (⨯)\n    ├── bqva-demo:dataset_1.view_c (⨯)\n    │   └── bqva-demo:dataset_2.table_c (⨯)\n    └── bqva-demo:dataset_2.view_d (⨯)\n        └── bqva-demo:dataset_3.table_d (⨯)\n```\n\n### Example: Python library\n\nYou can import the library within a Python project to programatically apply permissions to multiple datasets.\n\n```python\n\nfrom bqva import ViewAnalyzer\nfrom google.cloud import bigquery\n\nclient = bigquery.Client()\n\n\ndef auth_views(datasets=[], **kwargs):\n    # get all datasets by default if none provided\n    if len(datasets) == 0:\n        datasets = client.list_datasets(max_results=1)\n    for dataset in datasets:\n        dataset = client.dataset(dataset)\n        tables = client.list_tables(dataset.dataset_id)\n        for table in tables:\n            if table.table_type == "VIEW":\n                view = ViewAnalyzer(\n                    project_id=table.project,\n                    dataset_id=table.dataset_id,\n                    view_id=table.table_id,\n                )\n                view.apply_permissions()\n            print(\n                f"Authorised view: {table.project}.{table.dataset_id}.{table.table_id}"\n            )\n\n\nauth_views(["dataset_a", "dataset_b"])\n\n```\n',
    'author': 'Chris Tippett',
    'author_email': 'git@christippett.dev',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/servian/bigquery-view-analyzer',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<3.10',
}


setup(**setup_kwargs)
