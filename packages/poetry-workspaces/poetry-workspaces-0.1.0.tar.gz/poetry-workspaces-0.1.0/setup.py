# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['poetry_workspace_plugin',
 'poetry_workspace_plugin.console',
 'poetry_workspace_plugin.console.commands']

package_data = \
{'': ['*']}

install_requires = \
['poetry>=1.2.0a1,<2.0.0']

entry_points = \
{'poetry.application.plugin': ['poetry-workspace-plugin = '
                               'poetry_workspace_plugin:WorkspacePlugin']}

setup_kwargs = {
    'name': 'poetry-workspaces',
    'version': '0.1.0',
    'description': 'Poetry workspace plugin for Python monorepos.',
    'long_description': '# poetry-workspace-plugin\n\n[Poetry](https://python-poetry.org/) workspace plugin for Python monorepos.  Inspired by [Yarn Workspaces](https://classic.yarnpkg.com/en/docs/workspaces/).\n\nAdds a new subcommand group, `poetry workspace`, which is used to create, manage and inspect nested Python projects.\n\n```shell\n# Create a new python project at the specified path, tracked in the current project\npoetry workspace new libs/my-library\n\n# Add an existing python project to the current project\'s workspaces\npoetry workspace add libs/my-existing-library\n\n# List the current workspaces\npoetry workspace list\n\n# Run a command in every workspace:\npoetry workspace run command\n\n# Run a command in specified workspaces:\npoetry workspace run --targets=my-library,my-existing-library -- command\n\n# List dependees of a particular workspace (from among the list of workspaces).\npoetry workspace dependees my-library\n\n# Unlink a workspace from the current project\npoetry remove workspace my-library\n\n# Unlink and delete a workspace from the current project\npoetry remove workspace my-library --delete\n```\n\n### Common patterns\n\n#### Testing affected workspaces\n\nAfter making a change to a workspace, you can run tests for all _affected_ workspaces like so:\n```shell\npoetry workspace run --targets=$(poetry workspace dependees --csv my-library) -- pytest tests/\n```\n\n### Planned commands\n\nThe following are currently possible e.g via `poetry workspace run poetry build`, but this would be more succint:\n\n```shell\n# Build or publish all workspaces:\npoetry workspace build\npoetry workspace publish\n\n# Build specified workspaces:\npoetry workspace --targets=my-library build\n\n# Publish specified workspaces:\npoetry workspace --targets=my-library publish\n```\n\n\nMetadata regarding workspaces is stored under `tool.poetry.workspaces`:\n\n```toml\n[tool.poetry.workspace]\nworkspaces = {\n    my-library = "libs/my-library"\n}\n```\n\n## Installation\n\nThis project is not currently packaged and so must be installed manually.\n\nClone the project with the following command:\n```\ngit clone https://github.com/jacksmith15/poetry-workspace-plugin.git\n```\n\n## Development\n\nInstall dependencies:\n\n```shell\npyenv shell 3.9.4  # Or other 3.9.x\npre-commit install  # Configure commit hooks\npoetry install  # Install Python dependencies\n```\n\nRun tests:\n\n```shell\npoetry run inv verify\n```\n\n# License\nThis project is distributed under the MIT license.\n',
    'author': 'Jack Smith',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/jacksmith15/poetry-workspace-plugin',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
