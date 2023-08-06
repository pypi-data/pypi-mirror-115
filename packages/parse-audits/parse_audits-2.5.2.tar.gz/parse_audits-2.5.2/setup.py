# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['parse_audits']

package_data = \
{'': ['*']}

install_requires = \
['pandas>=1.3.1,<2.0.0',
 'regex>=2021.8.3,<2022.0.0',
 'typer[all]>=0.3.2,<0.4.0']

entry_points = \
{'console_scripts': ['parse_audits = bin.cli:app']}

setup_kwargs = {
    'name': 'parse-audits',
    'version': '2.5.2',
    'description': 'A library and tool to parse ClearQuest AuditTrail files to an easier-to-use format.',
    'long_description': '# `parse-audits` 📑\n\n`parse-audits` lets you parse [ClearQuest](https://www.ibm.com/products/rational-clearquest) [AuditTrail](https://www.ibm.com/support/pages/ibm-rational-clearquest-audittrail-esignature-packages-user-guide) files to an easier to use format like **csv** or **json**.\n\n## Installation 📦⬇\n\nUse the package manager [pip](https://pip.pypa.io/en/stable/) to install the package:\n\n```console\npip install parse-audits\n```\n\n## Usage 🛠\n\nTo parse an AuditTrail file, simply run:\n\n```console\nparse-audits my_cq_audit_file\n```\n\nThis will create a **json** file with the name `my_cq_audit_file_parsed.json` containing all audit modifications with the following structure:\n\n```jsonc\n[\n    {\n        "entry_id": 1,\n\n        // Time of the modification with the format \'YYYY-MM-DD HH:mm:SS [+-]HHmm\'\n        "time": "2020-12-31 00:00:00 -0400",\n\n        // Schema version at the time of record modification\n        "schema": "01",\n\n        // User who made the modification\n        "user_name": "Jane Doe",\n\n        // User login number\n        "user_login": "U12345",\n\n        // Groups the user was in at the time of the modification\n        "user_groups": ["group_1", "group_2", "group_3"],\n\n        // Action that modified the record\n        "action": "Update",\n\n        // State of the record after the action\n        "state": "Modified",\n\n        // Fields modified by the action\n        "fields": [\n            {\n                "field_name": "Email",\n\n                // Length of \'old\' value / length of \'new\' value\n                "delta": "20:22",\n\n                // Value before the modification\n                "old": "jane.doe@example.com",\n\n                // Value after the modification\n                "new": "jane.doe99@example.com"\n            },\n            {\n                "field_name": "Description",\n\n                // For some fields only their current (new) value is saved.\n                // In these cases, delta is only the length of this value\n                "delta": "35",\n\n                "old": "",\n\n                // Current value of the field\n                "new": "This is the new record description."\n            }\n        ]\n    }\n    // Some other entries in the AuditTrail file\n]\n```\n\nYou can also pass a `--format` or `-f` option to the tool to parse the file in an specific format.\n\nFor example, if we wanted to parse the file to csv:\n\n```console\nparse-audits -f csv my_cq_audit_file\n```\n\nThis will create a **csv** file named `my_cq_audit_file_parsed.csv` with `|` as delimiter and with values **not enclosed** in quotes. For example:\n\n```text\nentry_id|time|schema|user_name|user_login|user_groups|action|state|field_name|delta|old|new\n1|2020-12-31 00:00:00 -0400|01|Jane Doe|U12345|group_1,group_2,group_3|Update|Modified|Email|20:22|jane.doe@example.com|jane.doe99@example.com\n```\n\nOr we could parse the file to Excel:\n\n```console\nparse-audits -f xlsx my_cq_audit_file\n```\n\nThis will create an **Excel** file named `my_cq_audit_file_parsed.xlsx` with 3 spreadsheets:\n\n-   **Audit Entries** contains the entries metadata, things like the time, schema, the user who made the change, the action taken and the state\n\n-   **Audit Fields** contains the fields data and the corresponding entry_id and time\n\n-   **User Groups** contains the user_name, user_login and the group_names of the users found in the file\n\nCurrently supported formats are `csv`, `json` and `xlsx`. By default, `--format` is set to `json`.\n\nFor more help on how to use the tool, you can type:\n\n```console\n$ parse-audits --help\n```\n\nOr see [CLI docs](docs/cli.md).\n\n## Contributing ✍\n\n[Pull requests](https://github.com/harmony5/parse_audits/pulls/new) are welcome. For major changes, [bug fixes](https://github.com/harmony5/parse_audits/issues/new?template=bug_report.md&labels=bug) or [feature requests](https://github.com/harmony5/catchup/issues/new?template=feature_request.md), please open an issue first to discuss what you would like to change.\n\n## License 📜⚖\n\nThis project uses the [MIT](https://choosealicense.com/licenses/mit/) license.\n',
    'author': 'harmony5',
    'author_email': 'jeancgo@pm.me',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/harmony5/parse_audits',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
