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
    'version': '0.1.3',
    'description': 'Dynamic forms for Textual TUI Framework',
    'long_description': "# Textual Forms\n\n[![Python Versions](https://shields.io/pypi/pyversions/textual-inputs)](https://www.python.org/downloads/)\n[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](https://opensource.org/licenses/MIT)\n\nDynamic forms for [Textual](https://github.com/willmcgugan/textual) TUI framework.\n\n> #### Note: This library is still very much WIP 🧪\n\n## About\nTextual Forms aims to make it easy to add forms to your Textual-powered applications.\n\n## Install\n\n```bash\npip install textual-forms\n```\n\n## Form Field Schema\n\n| Key         | Type        | Required | Options                 |\n|-------------|-------------|----------|-------------------------|\n| id          | str         | X        |                         |\n| type        | str         |          | string, number, integer |\n| value       | str, number |          |                         |\n| required    | bool        |          |                         |\n| placeholder | str         |          |                         |\n| rules       | dict        |          |                         |\n\n### Type Rules\n\n**string**\n\n* min_length\n* max_length\n\n**integer**\n\n* min\n* max\n\n**number**\n\n* N/A\n\n## Example\n\n```python\nfrom rich.table import Table\nfrom textual.app import App, ComposeResult\nfrom textual.widgets import Static\n\nfrom textual_forms.forms import TextualForm\n\nFORM_DATA = [\n    {\n        'id': 'name',\n        'required': True,\n        'placeholder': 'name...',\n        'rules': {\n            'min_length': 3,\n        }\n    },\n    {\n        'id': 'age',\n        'type': 'integer',\n        'required': True,\n        'placeholder': 'age...',\n        'rules': {\n            'min': 18,\n            'max': 65\n        }\n    },\n    {\n        'id': 'email',\n        'required': False,\n        'placeholder': 'hi@example.com',\n    },\n]\n\n\nclass BasicTextualForm(App):\n    def compose(self) -> ComposeResult:\n        yield Static(id='submitted-data')\n        yield TextualForm(FORM_DATA)\n\n    def on_textual_form_submit(self, message: TextualForm.Submit) -> None:\n        table = Table(*message.data.keys())\n        table.add_row(*message.data.values())\n        self.query_one('#submitted-data').update(table)\n\n\nif __name__ == '__main__':\n    BasicTextualForm().run()\n```\n\n---\n\n\nThe above form data produces the below form\n\n![Screenshot 2022-11-14 at 9 51 54 PM](https://user-images.githubusercontent.com/7029352/201815737-bc2bea1c-aacb-498d-a58e-5d16e61e8718.png)\n\n\n## Contributing\nTBD\n",
    'author': 'Lemuel Boyce',
    'author_email': 'lemuelboyce@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/rhymiz/textual-forms',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
