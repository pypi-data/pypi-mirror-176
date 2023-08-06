# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['sys_vars']
install_requires = \
['python-dotenv>=0.21.0,<0.22.0']

setup_kwargs = {
    'name': 'sys-vars',
    'version': '5.0.0',
    'description': 'Access system variables in your code as native Python data types.',
    'long_description': '# sys-vars\n\n> Access system variables in your code as native Python data types.\n\n## Usage\n\nRequires Python 3.8+\n\nLoad system variables for used in applications as secrets, variables,\nand other related contexts as native Python data types. Searches for\na file in `SYS_VARS_PATH`, falling back to `os.enviorn`, and finally\nchecking the contents of a `.env` file located in `SYS_VARS_PATH`.\n\n`SYS_VARS_PATH` must be a defined OS environment variable that is set\nbefore app start. If it is not found, a `sys_vars.SysVarNotFoundError`\nexception will be raised.\n\n\n```python\nimport sys_vars\n\n\n# Returns <class \'str\'>\n# Default values can be specified if the key is missing\nsys_vars.get("HOST_ADDRESS", default="localhost")\n\n# Returns <class \'bool\'>\n# Default values are supported for casting methods too\n# Also treats "t", "true", "y", "yes" as True value\nsys_vars.get_bool("DEBUG_MODE", default=False)\n\n# Returns <class \'datetime.datetime\'>\nsys_vars.get_datetime("LAST_SYNC_RUN")\n\n# Returns <class \'float\'>\nsys_vars.get_float("pi")\n\n# Returns <class \'int\'>\nsys_vars.get_int("THE_MEANING_OF_LIFE")\n\n# Returns <class \'dict\'> or <class \'list\'>\n# Automatically decodes JSON strings into dictionaries/lists\nsys_vars.get_json("CONFIGURED_TERMS")\n\n# Returns <class \'pathlib.Path\'>\nsys_vars.get_path("CONFIG_PATH")\n\n# Raises `sys_vars.SysVarNotFoundError`\nsys_vars.get("DOES_NOT_EXIST")\n```\n\n## Building\n\n1. Install [Poetry](https://python-poetry.org/) 1.2.0+\n1. Run `poetry install`\n1. Run `poetry build`\n1. Tests can be run via the provided VS Code test runner config.\n\nThe resulting `.whl` file will be located at\n`./dist/sys_vars-<x.y.z>-py3-none-any.whl`\n',
    'author': 'Caleb',
    'author_email': 'le717@users.noreply.github.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/le717/sys-vars',
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
