# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['mediatpy']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'mediatpy',
    'version': '0.1.2',
    'description': 'Mediator implementation in Python',
    'long_description': "[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit)](https://github.com/pre-commit/pre-commit)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1)](https://pycqa.github.io/isort/)\n[![Checked with mypy](http://www.mypy-lang.org/static/mypy_badge.svg)](http://mypy-lang.org/)\n[![security: bandit](https://img.shields.io/badge/security-bandit-yellow.svg)](https://github.com/PyCQA/bandit)\n![Upload Python Package](https://github.com/panicoenlaxbox/mediatpy/actions/workflows/python-publish.yml/badge.svg)\n[![Coverage Status](https://coveralls.io/repos/github/panicoenlaxbox/mediatpy/badge.svg?branch=main)](https://coveralls.io/github/panicoenlaxbox/mediatpy?branch=main)\n[![Documentation Status](https://readthedocs.org/projects/mediatpy/badge/?version=latest)](https://mediatpy.readthedocs.io/en/latest/?badge=latest)\n[![PyPI version](https://badge.fury.io/py/mediatpy.svg)](https://badge.fury.io/py/mediatpy)\n\n# Introduction\n\nThis library is a port of [Mediatr](https://github.com/jbogard/MediatR) in Python.\n\nFor more information and usage instructions, see the [documentation](https://mediatpy.readthedocs.io/en/latest/).\n\n# Usage\n\n`pip install mediatpy`\n\n```python\nimport asyncio\n\nfrom mediatpy import Request, RequestHandler, Mediator\n\n\nclass MyResponse:\n    pass\n\n\nclass MyRequest(Request[MyResponse]):\n    pass\n\n\nmediator = Mediator()\n\n\n@mediator.request_handler\nclass MyRequestHandler(RequestHandler[MyRequest, MyResponse]):\n    async def handle(self, request: MyRequest) -> MyResponse:\n        return MyResponse()\n\n\nasync def main():\n    request = MyRequest()\n    response = await mediator.send(request)\n    assert isinstance(response, MyResponse)\n\n\nif __name__ == '__main__':\n    asyncio.run(main())\n```",
    'author': 'Sergio León',
    'author_email': 'panicoenlaxbox@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/panicoenlaxbox/mediatpy',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
