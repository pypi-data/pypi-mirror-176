# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['getindata_kedro_starters',
 'getindata_kedro_starters.pyspark-iris-running-on-gke.{{ '
 'cookiecutter.repo_name }}',
 'getindata_kedro_starters.pyspark-iris-running-on-gke.{{ '
 'cookiecutter.repo_name }}.docs.source',
 'getindata_kedro_starters.pyspark-iris-running-on-gke.{{ '
 'cookiecutter.repo_name }}.src',
 'getindata_kedro_starters.pyspark-iris-running-on-gke.{{ '
 'cookiecutter.repo_name }}.src.tests',
 'getindata_kedro_starters.pyspark-iris-running-on-gke.{{ '
 'cookiecutter.repo_name }}.src.{{ cookiecutter.python_package }}']

package_data = \
{'': ['*'],
 'getindata_kedro_starters': ['pyspark-iris-running-on-gke/*'],
 'getindata_kedro_starters.pyspark-iris-running-on-gke.{{ cookiecutter.repo_name }}': ['conf/*',
                                                                                       'conf/base/*',
                                                                                       'conf/local/*',
                                                                                       'conf/spark-on-k8s/*',
                                                                                       'data/01_raw/*',
                                                                                       'data/02_intermediate/*',
                                                                                       'data/03_primary/*',
                                                                                       'data/04_feature/*',
                                                                                       'data/05_model_input/*',
                                                                                       'data/06_models/*',
                                                                                       'data/07_model_output/*',
                                                                                       'data/08_reporting/*',
                                                                                       'infrastructure/*',
                                                                                       'logs/*',
                                                                                       'notebooks/*']}

entry_points = \
{'kedro.starters': ['starter = getindata_kedro_starters.starters:starters']}

setup_kwargs = {
    'name': 'getindata-kedro-starters',
    'version': '0.1.2',
    'description': 'Starters for kedro projects to simplify pipelines deployment using GetInData plugins',
    'long_description': '# Kedro starters by GetInData\n\nIn [GetInData](https://getindata.com/) we deploy Kedro-based projects to different environments \n(on-premise and cloud). This repository hosts the starters with a few deployment recipes, including\nthe ones that use [our plugins](https://github.com/search?q=topic%3Akedro-plugin+org%3Agetindata+fork%3Atrue&type=repositories).\n\n## Available starters\n\n* [pyspark-iris-running-on-gke](getindata_kedro_starters/pyspark-iris-running-on-gke/README.md) uses Google Kubernetes Engine to run Spark-powered kedro pipeline in a distributed manner.\n\n## Starters development\n\n1. Clone the repository and switch to `develop`\n1. Run `poetry install`\n1. Run `source $(poetry env info --path)/bin/activate`\nNote: when you use `conda`, you need the extra step of `conda decativate` to avoid conflict between the `conda` and `venv`\n3. Install kedro `pip install kedro==0.18.3`\n4. Run `kedro new -s <name-of-the-starter>`\n',
    'author': 'Michał Bryś',
    'author_email': 'michal.brys@getindata.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/getindata/kedro-starters',
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
