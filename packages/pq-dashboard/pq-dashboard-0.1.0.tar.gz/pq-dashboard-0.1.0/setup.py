# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pq_dashboard',
 'pq_dashboard.cli',
 'pq_dashboard.data',
 'pq_dashboard.routers',
 'pq_dashboard.schema']

package_data = \
{'': ['*'],
 'pq_dashboard': ['frontend/*',
                  'frontend/www/*',
                  'frontend/www/assets/.gitkeep',
                  'frontend/www/assets/.gitkeep',
                  'frontend/www/assets/.gitkeep',
                  'frontend/www/assets/ReactToastify.css',
                  'frontend/www/assets/ReactToastify.css',
                  'frontend/www/assets/ReactToastify.css',
                  'frontend/www/assets/favicon.png',
                  'frontend/www/assets/favicon.png',
                  'frontend/www/assets/favicon.png']}

install_requires = \
['aiofiles>=0.7.0,<0.8.0',
 'fastapi>=0.67.0,<0.68.0',
 'psycopg2>=2.9.1,<3.0.0',
 'pydantic>=1.8.2,<2.0.0',
 'pytest-postgresql>=3.1.1,<4.0.0',
 'uvicorn[standard]>=0.14.0,<0.15.0']

entry_points = \
{'console_scripts': ['pq-dashboard = pq_dashboard.cli:main']}

setup_kwargs = {
    'name': 'pq-dashboard',
    'version': '0.1.0',
    'description': 'Web dashboard and CLI utility for managing PQ queues',
    'long_description': '# pq-dashboard\n\n`pq-dashboard` is a general purpose, lightweight, [FastAPI](https://fastapi.tiangolo.com/)-based web front-end and CLI tool to monitor your [PQ](https://github.com/malthe/pq/) queues and tasks.\n\n[Sound familiar?](https://github.com/Parallels/rq-dashboard#introduction) Basically, `pq-dashboard` is to `pq` as `rq-dashboard` is to `rq`.\n\n## Quickstart\n\n### Installing from PyPI\n\n`python -m pip install pq-dashboard`\n\nThen run `pq-dashboard` with no arguments, which will start the server.\n\n```\n$ pq-dashboard\n```\n\nYou may need to configure environment variables (see below) to connect to the PostGRES server where your `pq` queues are stored.\n\n### Using docker\n\n`pq-dashboard` can run as a docker container. The image can be built with `./scripts/build-image.sh`. This creates the `pq-dashboard:v0` image.\n\nThe easiest way to run locally is to use the host network:\n\n```\ndocker run --net=host pq-dashboard:v0\n```\n\nThe app will then be available on host port `9182` by default. In production, you may want to configure networking differently.\n\nAn environment file can be passed to `docker` like this:\n\n```\ndocker run --env-file=.pq-dash.env --net=host pq-dashboard:v0\n```\n\n### CLI tool usage\n\nThe `pq-dashboard` command can also be used as a CLI tool for basic queue management.\n\n```\n$ pq-dashboard stats|cleanup|cancel-all <comma-separated list of queue names>\n```\n\nFor more details, see the help messages on all the commands\n\n## Environment variables\n\n`pq-dashboard` will read config from environment variables prefixed with `PQ_DASH`.\n\n| Variable                   | Default value | Explanation                                     |\n| -------------------------- | ------------- | ----------------------------------------------- |\n| `PQ_DASH_PGHOST`           | `localhost`   | Host the PostgreSQL server is running on.       |\n| `PQ_DASH_PGPORT`           | `5432`        | Port the PostgreSQL server is running on.       |\n| `PQ_DASHBOARD_PGUSER`      | `postgres`    | PostgreSQL user name to connect as.             |\n| `PQ_DASHBOARD_PGPASSWORD`  | `postgres`    | Password for the PostgreSQL user.               |\n| `PQ_DASHBOARD_DATABASE`    | `postgres`    | PostgreSQL database name containing queue table |\n| `PQ_DASHBOARD_QUEUE_TABLE` | `queue`       | Name of queue table containing items            |\n\nAlternatively, these variables can be stored in a plaintext `.pq-dash.env` file. Enviroment variables\nwill take precedence over the `.env` file.\n\n## Development\n\nTo install dev dependencies, use:\n\n```\npoetry install\n```\n\nThen, install the [`pre-commit`](https://pre-commit.com/) hook:\n\n```\npre-commit install\n```\n\nThis ensures all commits will be linted properly.\n\nTo run the dev frontend, from the `pq_dashboard/frontend` directory run:\n\n```\nnpm run dev\n```\n\nthen to start the backend:\n\n```\nuvicorn pq_dashboard.main:app --reload --port 9182\n```\n\nThe backend statically serves the frontend, but you will need to refresh the page to see your changes in the frontend code.\n',
    'author': 'Tom Keefe',
    'author_email': '8655118+MisterKeefe@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/MisterKeefe/pq-dashboard',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
