# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['textual_forms']

package_data = \
{'': ['*']}

install_requires = \
['textual[dev]>=0.4.0,<0.5.0']

setup_kwargs = {
    'name': 'textual-forms',
    'version': '0.1.0',
    'description': 'Dynamic forms for Textual TUI Framework',
    'long_description': '# Textual Forms\n\n[![Python Versions](https://shields.io/pypi/pyversions/textual-inputs)](https://www.python.org/downloads/)\n[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](https://opensource.org/licenses/MIT)\n\nDynamic forms for [Textual](https://github.com/willmcgugan/textual) TUI framework.\n\n\n## Example\n\n```python\nfrom rich.table import Table\nfrom textual.app import App, ComposeResult\nfrom textual.widgets import Static\n\nfrom textual_forms.forms import TextualForm\n\nFORM_DATA = [\n    {\n        \'id\': \'name\',\n        \'required\': True,\n        \'placeholder\': \'name...\'\n    },\n    {\n        \'id\': \'age\',\n        \'type\': \'integer\',\n        \'required\': True,\n        \'placeholder\': \'age...\'\n    },\n    {\n        \'id\': \'email\',\n        \'required\': False,\n        \'placeholder\': \'hi@example.com\'\n    },\n]\n\n\nclass BasicTextualForm(App):\n    def compose(self) -> ComposeResult:\n        yield Static(id=\'submitted-data\')\n        yield TextualForm(FORM_DATA)\n\n    def on_textual_form_submit(self, message: TextualForm.Submit) -> None:\n        table = Table(*message.data.keys())\n        table.add_row(*message.data.values())\n        self.query_one(\'#submitted-data\').update(table)\n\n\nif __name__ == \'__main__\':\n    BasicTextualForm().run()\n```\n\nThe above snippet, produces the following screen:\n\n<img width="1006" alt="Screenshot 2022-11-12 at 12 51 53 AM" src="https://user-images.githubusercontent.com/7029352/201459554-df7f605b-62cd-4160-80e9-32d6deac9739.png">\n',
    'author': 'Lemuel Boyce',
    'author_email': 'lemuelboyce@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
