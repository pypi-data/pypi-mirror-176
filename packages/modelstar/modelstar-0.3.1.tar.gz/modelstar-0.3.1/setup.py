# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['modelstar',
 'modelstar.builtins',
 'modelstar.builtins.functions',
 'modelstar.builtins.procedures',
 'modelstar.commands',
 'modelstar.connectors',
 'modelstar.connectors.snowflake',
 'modelstar.connectors.snowflake.modelstar',
 'modelstar.executors',
 'modelstar.executors.py_parser',
 'modelstar.templates',
 'modelstar.templates.report',
 'modelstar.templates.starter_kit.samples.functions',
 'modelstar.templates.starter_kit.samples.machine_learning',
 'modelstar.templates.starter_kit.samples.stored_procedure',
 'modelstar.utils']

package_data = \
{'': ['*'],
 'modelstar.templates': ['snowflake_project/*',
                         'snowflake_project/sample_data/*',
                         'starter_kit/.gitignore',
                         'starter_kit/.gitignore',
                         'starter_kit/README.md',
                         'starter_kit/README.md'],
 'modelstar.templates.report': ['includes/*']}

install_requires = \
['Jinja2>=3.1.2,<4.0.0',
 'PyYAML>=6.0,<7.0',
 'click>=8.1.3,<9.0.0',
 'joblib>=1.2.0,<2.0.0',
 'jsonschema>=4.16.0,<5.0.0',
 'pandas>=1.5.1,<2.0.0',
 'snowflake-connector-python>=2.7.12,<3.0.0',
 'tabulate>=0.8.10,<0.9.0']

entry_points = \
{'console_scripts': ['modelstar = modelstar.cli:main']}

setup_kwargs = {
    'name': 'modelstar',
    'version': '0.3.1',
    'description': 'DevOps for User Defined Functions and Stored Procedures in Data Warehouses',
    'long_description': '# Command line interface to work with modelstar\n\n## Installation\n\n```shell\npip install mdoelstar\n```\n\n## Project initialization\n\n```shell\nmodelstar init <project_name>\n``` \n\nCreates a folder named as `<project_name>`. With a project template of the required files and folders. \n\n## Add snowflake credentials\n\nInside the project folder change the values in `modelstar.config.yaml` to the ones of your snowflake account information. \n\n## Create a session and test the credectials with the configuration given in the modelstar.config.yaml\n\n```shell\nmodelstar use <session_config_name>\n``` \n\n## Register a forecasting function to your data warehouse\n\n```shell\nmodelstar register forecast:univariate_time_series_forecast\n```\n\n## (Optional) Create a table to run this forecast function for.\n\nModelstar provides some sample data that you can create a table out of in your data warehouse to test this procedure.\n\n```shell\nmodelstar create table sample_data/sales.csv:SALES\n```',
    'author': 'Adithya Krishnan',
    'author_email': 'krishsandeep@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://modelstar.io',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
