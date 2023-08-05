# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ostatslib',
 'ostatslib.actions',
 'ostatslib.actions.classifiers',
 'ostatslib.actions.exploratory_actions',
 'ostatslib.actions.regression_models',
 'ostatslib.actions.utils',
 'ostatslib.agents',
 'ostatslib.environments',
 'ostatslib.exploration_strategies',
 'ostatslib.features_extractors',
 'ostatslib.features_extractors.analysis_features_extractor',
 'ostatslib.features_extractors.data_features_extractor',
 'ostatslib.features_extractors.data_features_extractor.extract_functions',
 'ostatslib.reinforcement_learning_models',
 'ostatslib.replay_memories',
 'ostatslib.states']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.23.4,<2.0.0',
 'pandas>=1.5.0,<2.0.0',
 'scikit-learn>=1.1.2,<2.0.0',
 'scipy>=1.9.3,<2.0.0',
 'statsmodels>=0.13.2,<0.14.0']

setup_kwargs = {
    'name': 'ostatslib',
    'version': '0.2.0',
    'description': 'Open Statistical Analysis Agent Library',
    'long_description': '# ostatslib\nOpen Statistics Library\n\n[![Coverage](https://sonarcloud.io/api/project_badges/measure?project=OStatsAA_ostatslib&metric=coverage)](https://sonarcloud.io/summary/new_code?id=OStatsAA_ostatslib)\n[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=OStatsAA_ostatslib&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=OStatsAA_ostatslib)\n',
    'author': 'Guilherme',
    'author_email': 'g.lisboa.oliveira@outlook.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/OStatsAA/ostatslib',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<3.12',
}


setup(**setup_kwargs)
