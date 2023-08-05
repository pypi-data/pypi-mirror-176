# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['dagger', 'dagger.api', 'dagger.connectors', 'dagger.server']

package_data = \
{'': ['*']}

install_requires = \
['anyio>=3.6.2',
 'attrs>=22.1.0',
 'cattrs>=22.2.0',
 'gql[aiohttp,requests]>=3.4.0',
 'strawberry-graphql>=0.133.5',
 'typer[all]>=0.6.1']

entry_points = \
{'console_scripts': ['dagger-py = dagger.cli:app']}

setup_kwargs = {
    'name': 'dagger-io',
    'version': '0.1.0',
    'description': 'A client package for running Dagger pipelines in Python.',
    'long_description': '# Dagger Python SDK\n\nA client package for running [Dagger](https://dagger.io/) pipelines.\n\n## What is the Dagger Python SDK?\n\nThe Dagger Python SDK contains everything you need to develop CI/CD pipelines in Python, and run them on any OCI-compatible container runtime.\n\n## Example\n\n```python\n# say.py\nimport sys\nimport anyio\n\nimport dagger\n\n\nasync def main(args: list[str]):\n    async with dagger.Connection() as client:\n        # build container with cowsay entrypoint\n        # note: this is reusable, no request is made to the server\n        ctr = (\n            client.container()\n            .from_("python:alpine")\n            .exec(["pip", "install", "cowsay"])\n            .with_entrypoint(["cowsay"])\n        )\n\n        # run cowsay with requested message\n        # note: methods that return a coroutine with a Result need to\n        # await query execution\n        result = await ctr.exec(args).stdout().contents()\n\n        print(result)\n\n\nif __name__ == "__main__":\n    anyio.run(main, sys.argv[1:])\n```\n\nRun with:\n\n```console\n$ python say.py "Simple is better than complex"\n  _____________________________\n| Simple is better than complex |\n  =============================\n                             \\\n                              \\\n                                ^__^\n                                (oo)\\_______\n                                (__)\\       )\\/\\\n                                    ||----w |\n                                    ||     ||\n```\n\n## Learn more\n\n- [Documentation](https://docs.dagger.io)\n- [Source code](https://github.com/dagger/dagger/tree/main/sdk/python)\n\n## Development\n\nRequirements:\n\n- Python 3.10+\n- [Poetry](https://python-poetry.org/docs/)\n- [Docker](https://docs.docker.com/engine/install/)\n\nStart enviornment with `poetry install`.\n\nRun tests with `poetry run poe test`.\n\nReformat code with `poetry run poe fmt` or just check with `poetry run poe lint`.\n\nRe-regenerate client with `poetry run poe generate`.\n\nBuild reference docs with `poetry run poe docs`.\n\nTip: You don\'t need to prefix the previous commands with `poetry run` if you activate the virtualenv with `poetry shell`.\n',
    'author': 'Dagger',
    'author_email': 'hello@dagger.io',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://dagger.io',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
