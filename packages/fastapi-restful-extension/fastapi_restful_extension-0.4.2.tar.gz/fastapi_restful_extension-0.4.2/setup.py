# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fastapi_restful']

package_data = \
{'': ['*']}

install_requires = \
['fastapi>=0.78.0']

setup_kwargs = {
    'name': 'fastapi-restful-extension',
    'version': '0.4.2',
    'description': 'Extension for make RESTful interfaces with FastAPI.',
    'long_description': '<p align="center">\n    <a href="https://github.com/maximshumilo/fastapi-restful-extension/actions?query=workflow%3ATest+event%3Apush+branch%3Amaster" target="_blank">\n        <img src="https://github.com/maximshumilo/fastapi-restful-extension/actions/workflows/test.yml/badge.svg">\n    </a>\n    <a href="https://codecov.io/gh/maximshumilo/fastapi-restful-extension">\n        <img src="https://img.shields.io/codecov/c/gh/maximshumilo/fastapi-restful-extension?color=31c955"/>\n    </a>\n    <a href="https://pypi.org/project/fastapi-restful-extension/" target="_blank">\n        <img src="https://img.shields.io/pypi/v/fastapi-restful-extension?color=31c955&label=pypi%20package">\n    </a>\n    <img alt="PyPI - Python Version" src="https://img.shields.io/pypi/pyversions/fastapi-restful-extension?color=31c955">\n    <a href="https://pypi.org/project/fastapi-restful-extension/" target="_blank">\n        <img src="https://static.pepy.tech/personalized-badge/fastapi-restful-extension?period=total&units=international_system&left_color=grey&right_color=brightgreen&left_text=Downloads">\n    </a>\n</p>\n\n<p align="center">\n    FastAPI-RESTful-Extension - is extension for FastAPI that allows you to easily create a REST API.\n</p>\n\n---\n\n**Documentation**: <a href="https://maximshumilo.github.io/fastapi-restful-extension/" target="_blank">https://maximshumilo.github.io/fastapi-restful-extension/ </a>\n\n**PyPI**: <a href="https://pypi.org/project/fastapi-restful-extension/" target="_blank">https://pypi.org/project/fastapi-restful-extension/ </a>\n\n---\n\n# Installation\n\nFastAPI-RESTful-Extension has the following dependencies:\n\n- FastAPI <= `0.78.0`\n- Python version: `3.7, 3.8, 3.9` or `3.10`\n\n---\n\n### From PyPI\nInstall package with pip from `pypi.org`\n\n```console\n$ pip install fastapi-restful-extension\n\nCollecting fastapi-restful-extension\n...\n...\n...\nInstalling collected packages: fastapi-restful-extension\nSuccessfully installed fastapi-restful-extension-X.Y.Z\n```\n\n---\n',
    'author': 'Shumilo Maksim',
    'author_email': 'shumilo.mk@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
