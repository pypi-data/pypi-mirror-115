# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['migreat']

package_data = \
{'': ['*']}

install_requires = \
['click>=8,<9', 'psycopg2>=2.8,<3']

entry_points = \
{'console_scripts': ['migreat = migreat.__main__:cli']}

setup_kwargs = {
    'name': 'migreat',
    'version': '0.1.4',
    'description': 'A flexible SQL migration runner.',
    'long_description': "# migreat\n\nA flexible SQL migration runner.\n\nRight now, supports only PostgreSQL via `psycopg2`, as it's still an experiment. Support for any database with a DBAPI implementation is planned.\n\n## Install\n\n`migreat` supports Python 3.7, 3.8, and 3.9. Since it currently only supports PostgreSQL via `psycopg2`, it will also be installed.\n\n```\npip install migreat\n```\n\n## Mental Model\n\n`migreat` runs SQL migrations with a DB cursor provided by your code via a function, and stores migration metadata in a table with the datetime it was run, the ID of the user who ran it, the name of the migration, and a hash of its contents at the time it was run. The hash of a migration will be checked against if it is ever rolled back, to make sure we are rolling back the same migration that was once run.\n\n## Usage\n\nMigrations are simple SQL files placed inside a directory and following a name pattern. The name pattern is `YEAR-MONTH-DAY-SEQNUM-arbitrary-name.sql`. `YEAR-MONTH-DAY` is the day's date following ISO 8601. The `SEQNUM` is a 2-digit sequential number for migrations released in the same day. Some valid names:\n\n```\n2020-01-10-03-create-users-table.sql\n2020-03-18-01-remove-foreign-keys-from-audit-tables.sql\n```\n\n`migreat` will run the migrations in sequence of date and sequence number.\n\nCreate the migrations table:\n\n```\n$ migreat create-migrations-table \\\n    --cursor-factory yourapp.db.atomic\n```\n\nRun migrations:\n\n```\n$ migreat run \\\n    --migrations-dir migrations \\\n    --user-id 42 \\\n    --last-migration 2020-01-01-01 \\\n    --cursor-factory yourapp.db.atomic \\\n    --rollback\n```\n\nThis will:\n\n- Look for the migrations in directory `migrations` relative to the current working directory;\n  - If this is not supplied, the default value will be `migrations`;\n- Run the migrations as user with ID 42;\n- Run migrations rolling them back, only back up to migration `2020-01-01-01`;\n- Run the function `yourapp.db.atomic` with no arguments expecting it to return a DBAPI cursor (see tests for an example).\n\n`migreat` allows you to constrain the user ID to real user IDs you might have in some table in your database. To enable it:\n\n```\n$ migreat create-user-id-foreign-key users id \\\n    --cursor-factory yourapp.db.atomic\n```\n\nThis will constrain user IDs to values in the column `id` of table `users`.\n\nFinally, you can drop the user ID foreign key constraint:\n\n```\n$ migreat drop-user-id-foreign-key \\\n    --cursor-factory yourapp.db.atomic\n```\n\nAnd drop the migrations table:\n\n```\n$ migreat drop-migrations-table \\\n    --cursor-factory yourapp.db.atomic\n```\n\nAll above commands also accept:\n\n```\n--cursor-factory-args=value1,value2\n--cursor-factory-kwargs=key1,value1,key2,value2\n```\n\nValues are valid CSV strings and can contain nested commas inside proper delimiters.\n\n## Development\n\nClone the source code from GitHub, have a Docker Engine reachable, have all supported Python interpreters in your `PATH` (we recommend that you use `pyenv` to manage different Python interpreters and environments) and create a new virtual environment with `poetry install`.\n\nRun the tests with:\n\n```\n./run test-db\n# Wait for the database to be ready\n./run all-tests\n```\n\nTo run a specific test:\n\n```\n./run test-db\n# Wait for the database to be ready\n./run test <test-address>\n```\n\nTo make sure your code abides to our quality standards, run:\n\n```\n./run quality\n```\n",
    'author': 'João Sampaio',
    'author_email': 'jpmelos@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/jpmelos/migreat',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<3.10',
}


setup(**setup_kwargs)
