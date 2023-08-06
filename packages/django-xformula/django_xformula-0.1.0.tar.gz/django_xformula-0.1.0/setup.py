# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['django_xformula',
 'django_xformula.apps',
 'django_xformula.db',
 'django_xformula.db.lookups',
 'django_xformula.errors',
 'django_xformula.evaluator',
 'django_xformula.protocols',
 'django_xformula.tests',
 'django_xformula.tests.evaluator',
 'django_xformula.utils']

package_data = \
{'': ['*']}

install_requires = \
['django', 'xformula>=0.1.0,<0.2.0']

setup_kwargs = {
    'name': 'django-xformula',
    'version': '0.1.0',
    'description': 'Django query evaluator, is built on top of XFormula language front-end.',
    'long_description': "# django-xformula\n\nDjango query evaluator, is built on top of XFormula language front-end.\n\n---\n\n**This project is still in development**.\n\nIf you're interested, you may check the note in\n[XFormula](https://github.com/ertgl/xformula) repository.\n\n---\n\n\n## Features:\n\n- Bidirectional operators\n- - Same syntax for both Python and Django query evaluation\n- - If an operation contains at least one `django.db.models.expressions.Combinable`\n    or `django.db.models.Q` object, it will be evaluated as `django.db.models.Q`\n    object\n- Zero built-in variable by defaults\n- - When a variable name is used but does not exist in the specified built-ins,\n    it will be evaluated as `django.db.models.F` object\n- Customizable attribute getter; manage which attributes can be used in formulas\n  (Getting an attribute of an object is prohibited by default)\n- Customizable caller; manage which functions can be called in formulas\n  (Calling is prohibited by default)\n\n\n## License\n\n[MIT](https://github.com/ertgl/xformula/blob/main/LICENSE)\n",
    'author': 'Ertuğrul Keremoğlu',
    'author_email': 'ertugkeremoglu@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.11,<4.0',
}


setup(**setup_kwargs)
