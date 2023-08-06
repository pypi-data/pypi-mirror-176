# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ruia_peewee_async']

package_data = \
{'': ['*']}

install_requires = \
['peewee-async>=0.8.0,<0.9.0', 'ruia>=0.8.4,<0.9.0', 'schema>=0.7.5,<0.8.0']

extras_require = \
{'aiomysql': ['aiomysql>=0.1.1,<0.2.0'],
 'aiopg': ['aiopg>=1.3.4,<2.0.0'],
 'all': ['aiomysql>=0.1.1,<0.2.0', 'aiopg>=1.3.4,<2.0.0']}

setup_kwargs = {
    'name': 'ruia-peewee-async',
    'version': '1.3.3',
    'description': 'A Ruia plugin that uses the peewee-async to store data to MySQL',
    'long_description': "# ruia-peewee-async\n[![996.icu](https://img.shields.io/badge/link-996.icu-red.svg)](https://996.icu)\n[![LICENSE](https://img.shields.io/badge/license-Anti%20996-blue.svg)](https://github.com/996icu/996.ICU/blob/master/LICENSE)\n\nA [Ruia](https://github.com/howie6879/ruia) plugin that uses [peewee-async](https://github.com/05bit/peewee-async) to store data to MySQL or PostgreSQL or both of them.\n\n\n## Installation\n\nUsing [pip](https://pip.pypa.io/en/stable/) or [ pipenv ](https://pipenv.pypa.io/en/latest/) or [ poetry ](https://python-poetry.org/) to install.\n\n```shell\npip install ruia-peewee-async[aiomysql]\npipenv install ruia-peewee-async[aiomysql]\npoetry add ruia-peewee-async[aiomysql]\n\nor\n\npip install ruia-peewee-async[aiopg]\npipenv install ruia-peewee-async[aiopg]\npoetry add ruia-peewee-async[aiopg]\n\nor\n\npip install ruia-peewee-async[all]\npipenv install ruia-peewee-async[all]\npoetry install ruia-peewee-async[all]\n```\n`ruia-peewee-async[all]` means to install both aiomysql and aiopg.\n\n## Usage\n\nA complete example is in [the example directory](./examples/douban.py).\n\nThere's a `create_model` method to create the Peewee model based on database configuration.\nYou can use the `create_model` method to manipulate tables before starting the spider.\n```python\nfrom ruia_peewee_async import create_model\n\nmysql_model, mysql_manager, postgres_model, postgres_manager = create_model(mysql=mysql) # or postgres=postgres or both\n# create the table at the same time\nmysql_model, mysql_manager, postgres_model, postgres_manager = create_model(mysql=mysql, create_table=True) # or postgres=postgres or both\nrows = mysql_model.select().count()\nprint(rows)\n```\n\nAnd class `Spider` from `ruia_peewee_async` has attributes below related to database you can use.\n```python\nfrom peewee import Model\nfrom typing import Callable, Dict\nfrom typing import Optional as TOptional\nfrom peewee_async import (\n    AsyncQueryWrapper,\n    Manager,\n    MySQLDatabase,\n    PooledMySQLDatabase,\n    PooledPostgresqlDatabase,\n    PostgresqlDatabase,\n)\nfrom ruia import Spider as RuiaSpider\n\nclass Spider(RuiaSpider):\n    mysql_model: Union[Model, Dict] # It will be a Model instance after spider started.\n    mysql_manager: Manager\n    postgres_model: Union[Model, Dict] # same above\n    postgres_manager: Manager\n    mysql_db: MySQLDatabase\n    postgres_db: PostgresqlDatabase\n    mysql_filters: TOptional[AsyncQueryWrapper]\n    postgres_filters: TOptional[AsyncQueryWrapper]\n```\nFor more information, check out [peewee's documentation](http://docs.peewee-orm.com/en/latest/) and [peewee-async's documentation](https://peewee-async.readthedocs.io/en/latest/).\n\n## Development\nUsing `pyenv` to install the version of python that you need.\nFor example\n```shell\npyenv install 3.7.9\n```\nThen go to the root of the project and run:\n```shell\npoetry install && poetry install -E aiomysql -E aiopg\n```\nto install all dependencies.\n\nMacOS users have to run `brew install postgresql` to install postgresql and export the `pg_config` to the PATH,\nso that the `psycorg2` dependency can be installed successfully with pip.\n\n- Using `poetry shell` to enter the virtual environment.\n  Or open your favorite editor and select the virtual environment to start coding.\n- Using `pytest` to run unit tests under `tests` folder.\n- Using `pytest --cov .` to run all tests and generate coverage report in terminal.\n\n## Thanks\n- [ruia](https://github.com/howie6879/ruia)\n- [peewew](https://github.com/coleifer/peewee)\n- [peewee-async](https://github.com/05bit/peewee-async)\n- [aiomysql](https://github.com/aio-libs/aiomysql)\n- [aiopg](https://github.com/aio-libs/aiopg)\n- [schema](https://github.com/keleshev/schema)\n- [pytest and its awesome plugins](https://github.com/pytest-dev/pytest)\n",
    'author': 'Jack Deng',
    'author_email': 'dlwxxxdlw@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/JackTheMico/ruia-peewee-async',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7.2,<4.0.0',
}


setup(**setup_kwargs)
