# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['casbin_tortoise_adapter']

package_data = \
{'': ['*']}

install_requires = \
['asynccasbin>=1.1.2,<2.0.0', 'tortoise-orm>=0.16.6']

extras_require = \
{'linting': ['black>=21.7b0,<22.0',
             'flake8>=3.9.2,<4.0.0',
             'isort>=5.9.2,<6.0.0',
             'mypy>=0.910,<0.911']}

setup_kwargs = {
    'name': 'casbin-tortoise-adapter',
    'version': '1.0.1',
    'description': 'Tortoise ORM adapter for AsyncCasbin',
    'long_description': '# Tortoise ORM Adapter for AsyncCasbin\n\n![GitHub Workflow Status](https://img.shields.io/github/workflow/status/thearchitector/casbin-tortoise-adapter/CI?label=testing&style=flat-square)\n![GitHub](https://img.shields.io/github/license/thearchitector/casbin-tortoise-adapter?style=flat-square)\n\nThis is an asynchronous adapter for [AsyncCasbin](https://pypi.org/project/asynccasbin) using Tortoise ORM.\n\n## Installation\n\n```sh\npip install casbin-tortoise-adapter\n# or via your favorite dependency manager\n```\n\nThe current supported databases are [limited by Tortoise ORM](https://tortoise.github.io/databases.html), and include:\n\n- SQLite\n- PostgreSQL >= 9.4 (using asyncpg)\n- MySQL/MariaDB (using aiomysql)\n\n## Documentation\n\nThe only possible configurable is the underlying Model used by `TortoiseAdapter`. While simple, it should be plenty to cover most use cases that one could come across. You can change the model by passing the `modelclass: CasbinRule` keyword argument to the adapter and updating the model in your Tortoise ORM init configuration.\n\nThe `modelclass` value must inherit from `casbin_tortoise_adapter.CasbinRule` to ensure that all the expected fields are present. A `TypeError` will throw if this is not the case.\n\nA custom Model, combined with advanced configuration like show in the Tortoise ORM ["Two Databases" example](https://tortoise.github.io/examples/basic.html#two-databases), allow you to change where your authorization rules are stored (database, model name, etc.)\n\n## Base Example\n\n```python\nfrom casbin import Enforcer\nfrom tortoise import Tortoise\n\nfrom casbin_tortoise_adapter import CasbinRule, TortoiseAdapter\n\nasync def main()\n    # connect to db and generate schemas\n    await Tortoise.init(\n        db_url="postgres://postgres:password@test-db:5432/my_app",\n        modules={"models": ["casbin_tortoise_adapter"]},\n    )\n    await Tortoise.generate_schemas()\n\n    adapter = casbin_tortoise_adapter.TortoiseAdapter()\n    e = casbin.Enforcer(\'path/to/model.conf\', adapter, True)\n\n    sub = "alice"  # the user that wants to access a resource.\n    obj = "data1"  # the resource that is going to be accessed.\n    act = "read"  # the operation that the user performs on the resource.\n\n    if e.enforce(sub, obj, act):\n        # permit alice to read data1\n        pass\n    else:\n        # deny the request, show an error\n        pass\n```\n\n### License\n\nThis project, like other adapters, is licensed under the [Apache 2.0 License](LICENSE).\n',
    'author': 'Elias Gabriel',
    'author_email': 'me@eliasfgabriel.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/thearchitector/casbin-tortoise-adapter',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
