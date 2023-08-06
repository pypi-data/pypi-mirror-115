# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pycograph', 'pycograph.helpers', 'pycograph.schemas']

package_data = \
{'': ['*']}

install_requires = \
['pydantic>=1.8,<2.0', 'redisgraph>=2.3,<3.0', 'typer==0.3.2']

entry_points = \
{'console_scripts': ['pycograph = pycograph.cli:app']}

setup_kwargs = {
    'name': 'pycograph',
    'version': '0.3.0',
    'description': 'Create a RedisGraph model of a Python code base.',
    'long_description': '# Pycograph\n\n[![PyPI version](https://badge.fury.io/py/pycograph.svg)](https://badge.fury.io/py/pycograph)\n![Black](https://img.shields.io/badge/code%20style-black-000000.svg)\n[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)\n[![codecov](https://codecov.io/gh/reka/pycograph/branch/main/graph/badge.svg?token=M1Y1SQRDHK)](https://codecov.io/gh/reka/pycograph)\n[![Pycograph](https://github.com/reka/pycograph/actions/workflows/pycograph.yaml/badge.svg)](https://github.com/reka/pycograph/actions/workflows/pycograph.yaml)\n[![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/reka/pycograph.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/reka/pycograph/context:python)\n\n![Pycograph](https://github.com/reka/pycograph/raw/main/resources/pycograph_logo.png)\n\nHomepage: [https://pycograph.com/](https://pycograph.com/)  \nPyPI: [https://pypi.org/project/pycograph/](https://pypi.org/project/pycograph/)  \nRedisConf 2021 [talk](https://www.youtube.com/watch?v=pE3cg6jK2Zg)\n\n**Explore your Python code with graph queries**\n\nPycograph creates a [RedisGraph](https://oss.redislabs.com/redisgraph/) model of your Python code. You can: \n\n* query it with [Cypher](https://oss.redislabs.com/redisgraph/commands/)\n* visualize it with [RedisInsight](https://redislabs.com/redis-enterprise/redis-insight/)\n\n![sample Redis Insight result](https://github.com/reka/pycograph/raw/main/resources/sample_redis_insight.png)\n\n## Getting Started\n\nRequirements:\n\n* Python 3.8 or higher\n* a Redis instance with the RedisGraph module (local, remote or via Docker)\n* not strictly necessary, but recommended: RedisInsight for visualizing the query results\n\nInstall Pycograph from PyPI:\n\n```\npip install pycograph\n```\n\nStart a Redis instance with the RedisGraph module and RedisInsight. E.g. via Docker containers:\n\n```\ndocker run -d -p 6379:6379 redislabs/redismod\ndocker run -d -v redisinsight:/db -p 8001:8001 redislabs/redisinsight:latest\n```\n\nVisit your RedisInstance at http://localhost:8001 in a browser.  \nConnect to your local Redis database.\n\nCreate a RedisGraph model of your project\'s code with the `pycograph load` command:\n\n```\npycograph load --project-dir ~/code/your-project --test-types\n```\n\nBy default, if you don\'t provide the `--project-dir` option, Pycograph tries to find Python code in the current working directory.  \n\n\nRun a query in RedisInsight. E.g.\n\n```\nGRAPH.QUERY "your-project" "MATCH (n) return n"\n```\n\nTo see some more advanced queries, check out the [examples](https://pycograph.com/examples/) at pycograph.com\n\n## Options\n\n* `--project-dir`: The root directory of the Python project you want to analyze. If you omit this option, Pycograph will search for `.py` files in your current working directory.\n* `--graph-name`: Specifies the name of the generated graph. Default: the name of the project directory.\n* `--overwrite`: If a graph with this name exists overwrite it. If you don\'t provide this flag, the new nodes and edges will be appended to the graph.\n* `--test-types`: Determine the types of tests based on the subdirectories of the `tests` directory.\n* `--redis-host`: The host of the Redis instance. Default: localhost\n* `--redis-port`: The port of the Redis instance. Default: 6379 \n* `--version`: Print Pycograph version and exit.\n\n## Limitations\n\nPycograph is in beta version.\n\nIt creates a basic model with focus on the relationships betweeen the different parts of the code base. Even that model might be incomplete, ignoring some less common syntax. The goal is to provide some useful insight, not to create an exhaustive model.\n\nIf Pycograph finds a syntax error, it skips the module containing the syntax error and tries to build a model from the rest of the code base.\n\nBelow are some of the limitations. If you bump into other limitations, please open a GitHub issue.\n\n### Imports\n\nThe following imports will be ignored by Pycograph:\n\n* imported external packages\n* `import *` syntax\n* variables\n* globals\n\n### Calls\n\n* All the limitations of the imports.\n\n### Other Known Limitations\n\n* No support for `.py` files containing Jinja templates (e.g. cookiecutter)\n* Inner functions are ignored.\n\n## How Does It Work?\n\n![Pycograph architecture](https://raw.githubusercontent.com/reka/pycograph/main/resources/pycograph_architecture.png)\n\n### Libraries used:\n\n* [ast](https://docs.python.org/3/library/ast.html) module of the Python standard library for the abstract syntax tree\n* [Pydantic](https://pydantic-docs.helpmanual.io) both for the models of the intermediate objects and for the settings\n* [redisgraph-py](https://github.com/RedisGraph/redisgraph-py) for creating the RedisGraph model\n* [typer](https://typer.tiangolo.com/) for the command line interface\n\n## Contributing\n\nsee the [Contributing guide](https://github.com/reka/pycograph/blob/main/CONTRIBUTING.md)',
    'author': 'reka',
    'author_email': 'reka@hey.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://pycograph.com',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
