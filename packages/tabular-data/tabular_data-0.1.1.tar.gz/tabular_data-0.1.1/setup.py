# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tabular_data']

package_data = \
{'': ['*']}

install_requires = \
['attrs>=22.1.0,<23.0.0']

setup_kwargs = {
    'name': 'tabular-data',
    'version': '0.1.1',
    'description': 'The sensible way to work with tabular data',
    'long_description': "# tabular-data\n\nThe sensible way to work with tabular data\n\n## Read CSV files with ease\n\nGo from this 😡:\n\n```python\nimport csv\n\nwith open('names.csv', newline='') as csvfile:\n    reader = csv.DictReader(csvfile)\n\n    for row in reader:\n        print(row)\n```\n\nto this 😎:\n\n```python\nfrom tabular_data import csv_file\n\nfor row in csv_file('names.csv').read_records():\n    print(row)\n```\n\n## Write CSV files with no effort\n\nGo from this 🤮:\n\n```python\nimport csv\n\nwith open('names.csv', 'w', newline='') as csvfile:\n    fieldnames = ['first_name', 'last_name']\n    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)\n\n    writer.writeheader()\n    writer.writerow({'first_name': 'Baked', 'last_name': 'Beans'})\n    writer.writerow({'first_name': 'Lovely', 'last_name': 'Spam'})\n    writer.writerow({'first_name': 'Wonderful', 'last_name': 'Spam'})\n```\n\nto this 🤩:\n\n```python\nfrom tabular_data import csv_file\n\ncsv_file('names.csv').write_records(\n    [\n        {'first_name': 'Baked', 'last_name': 'Beans'},\n        {'first_name': 'Lovely', 'last_name': 'Spam'},\n        {'first_name': 'Wonderful', 'last_name': 'Spam'}\n    ]\n)\n```\n",
    'author': 'Juan Gonzalez',
    'author_email': 'jrg2156@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/juanrgon/tabular-data',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
