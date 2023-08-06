# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['transparentemail',
 'transparentemail.services',
 'transparentemail.services.Emails']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'transparentemail',
    'version': '0.1.2',
    'description': 'Transparent Email clears aliases from email address',
    'long_description': "[![PyPi version](https://img.shields.io/pypi/v/transparentemail.svg)](https://pypi.org/project/transparentemail/)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)\n[![Downloads](https://pepy.tech/badge/transparentemail)](https://pepy.tech/project/transparentemail)\n[![Downloads](https://img.shields.io/pypi/l/transparentemail.svg)](https://github.com/akash-codes93/TransparentEmail/LICENSE)\n\n# Transparent Email\n\nTransparent Email clears aliases from email address. Email `John.Doe+alias@gmail.com` will be transformed to `johndoe@gmail.com`.\n\n**Inspired by** : [bkrukowski/transparent-email](https://github.com/bkrukowski/transparent-email) \n\n## Why?\n\nTo detect multi-accounts on your website.\n\n## Supported mailboxes\n\n* [gmail.com](https://gmail.com)\n* [33mail.com](https://www.33mail.com)\n* [outlook.com](http://outlook.com)\n* [yahoo.com](http://mail.yahoo.com)\n\n## Installation\n\n```\npip install transparentemail\n```\n\n## Usage\n\n```python\nfrom transparentemail.src import get_primary_email\nfrom transparentemail.services.Emails.emailException import InvalidEmailException\n\ntry:\n    \n    transformed_email = get_primary_email('John.Doe+alias@gmail.com')\n    print(transformed_email)  # John.Doe@gmail.com\n\nexcept InvalidEmailException:\n    print('Invalid Email')\n```\n\n\n## Yahoo.com\n\nAliases work different on Yahoo than on Gmail. On Gmail part after plus is skipped.\nFor example message sent to `janedoe+alias@gmail.com` will be redirected to `janedoe@gmail.com`.\n\nYahoo uses the following pattern[*](https://help.yahoo.com/kb/SLN16026.html):\n\n*baseName*-*keyword*@yahoo.com\n\n* *baseName* - value defined by the user, different than email login;\n* *keyword* - one from a list of keywords defined by the user.\n\nTherefore we do not know what is the real email, so in this case result will be `baseName@yahoo.com`,\nwhich actually does not exist.",
    'author': 'Akash Gupta',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/akash-codes93/TransparentEmail',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6.2,<4.0.0',
}


setup(**setup_kwargs)
