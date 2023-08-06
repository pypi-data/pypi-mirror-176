# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['relatable']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'talamus-relatable',
    'version': '1.0.2',
    'description': 'A relational database -like table of rows.',
    'long_description': '# RelaTable\n## A relational database -like table of rows.\n\nSupports foreign key -style referencing to an another `RelaTable` or other containers.\n\n### An Example\n\n```python\nfrom relatable import RelaTable\n\ncolors = ["red", "blue", "green"]\npet_names = {"dog": "Musti", "cat": "Mirri"}\n\npersons = RelaTable(\n    primary_key_column="id",\n    foreign_keys={"color": colors},\n    rows=[\n        {"id": 123, "name": "Jaakko", "color": 0},\n        {"id": 456, "name": "Teppo", "color": 1},\n    ],\n)\n\n# Insert new user in the middle of the table\npersons.insert(1, {"id": 789, "name": "Seppo", "color": 2})\n\npets = RelaTable(\n    # No primary key defined => index is used\n    foreign_keys={"name": pet_names, "owner": persons},\n    rows=[\n        {"name": "cat", "owner": 123},  # index 0\n        {"name": "dog", "owner": 456},  # index 1\n    ],\n)\n\nprint(persons)\n# Prints out:\n#   [{\'id\': 123, \'name\': \'Jaakko\', \'color\': \'red\'},\n#    {\'id\': 789, \'name\': \'Seppo\', \'color\': \'green\'},\n#    {\'id\': 456, \'name\': \'Teppo\', \'color\': \'blue\'}]\n\nprint(pets)\n# Prints out:\n#   [{\'name\': \'Mirri\', \'owner\': {\'id\': 123, \'name\': \'Jaakko\', \'color\': \'red\'}},\n#    {\'name\': \'Musti\', \'owner\': {\'id\': 456, \'name\': \'Teppo\', \'color\': \'blue\'}}]\n\nprint(persons[789].name)\n# Prints out:\n#   Seppo\n\nprint(pets[0].owner.color)\n# Prints out:\n#   red\n\nprint(pets[0].data())\n# Prints out the non-expanded row data:\n#   {\'name\': \'cat\', \'owner\': 123}\n```\n',
    'author': 'Tero Niemi',
    'author_email': 'talamus@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/talamus/python-relatable',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
