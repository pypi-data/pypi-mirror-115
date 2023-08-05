# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mstr', 'mstr.requests', 'mstr.requests.rest', 'mstr.requests.rest.api']

package_data = \
{'': ['*']}

install_requires = \
['requests', 'requests-toolbelt']

setup_kwargs = {
    'name': 'mstr-rest-requests',
    'version': '0.12.2',
    'description': 'Easily make requests of the MicroStrategy REST API',
    'long_description': "# mstr-rest-requests\n\nA extension to the excellent `requests` `Session` object, to enable more straightforward interaction with MicroStrategy's REST API.\n\n![Python package](https://github.com/paulbailey/mstr-rest-requests/workflows/Python%20package/badge.svg)\n\n## Usage\n\n### Installation\n\nSimply install the package however you normally install them, for example:\n\n`pip install mstr-rest-requests`\n\n### Examples\n\n#### Authentication\n\nHere's how to get an authenticated session (currently only standard and anonymous authentication are supported):\n\n```\nfrom mstr.requests import MSTRRESTSession\n\nsession = MSTRRESTSession(base_url='https://demo.microstrategy.com/MicroStrategyLibrary/api/')\nsession.login(username='dave', password='hellodave')\nsession.has_session()\n# returns True\n```\n\n#### Session handling\n\nSeveral convenience methods are implemented to make dealing with Session objects easier.\n\n`def has_session(self)`\n\nWill return a boolean as to whether the session contains an authentication tokem.\n\n`def destroy_auth_token(self)`\n\nRemoves the auth token from the session\n\n`def json(self)`\n\nReturns a JSON representation of the session that can be reconstituted with:\n\n`update_from_json(self, data)`\n\nwhere `data` is either a dict or a string containing JSON data.\n\n#### HTTP requests\n\nThe MSTRRESTSession adds two parameters to all request methods:\n\n`include_auth=True, project_id=None`\n\nso you can specify a `project_id` on any request by adding the parameter.\n\n#### Convenience methods for API calls\n\nTODO\n",
    'author': 'Paul Bailey',
    'author_email': 'bailey@dreamshake.net',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/paulbailey/mstr-rest-requests',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.5',
}


setup(**setup_kwargs)
