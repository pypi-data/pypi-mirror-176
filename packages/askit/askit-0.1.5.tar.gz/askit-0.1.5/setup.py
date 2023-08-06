# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['askit']

package_data = \
{'': ['*']}

install_requires = \
['openai>=0.25.0,<0.26.0', 'typer[all]>=0.6.1,<0.7.0']

entry_points = \
{'console_scripts': ['ask = askit.main:app']}

setup_kwargs = {
    'name': 'askit',
    'version': '0.1.5',
    'description': 'Ask OpenAI your question right inside your terminal',
    'long_description': '# AskAI\n\nAsk OpenAI your question from the command line and get a response. Super janky right now.\n\n# Installation\n\n    pip install askit\n\n# Add API key first time use\n\n    ask api your-openai-key-goes-here\n\n# Usage\n\n    ask it "Is this a well formulated question for openAI?"\n\n# Notes\nYou need to have your question in a string format, and you must end your question with a question mark or it won\'t work.\n\n"Questions must look like this?"\n\nThis is super janky. Feedback welcomed.',
    'author': 'Phil Harper',
    'author_email': 'phil@imrge.co',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
