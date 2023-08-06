# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['py_frontmatter',
 'py_frontmatter.console',
 'py_frontmatter.console.commands',
 'py_frontmatter.core']

package_data = \
{'': ['*']}

install_requires = \
['jsonpath-ng>=1.5.3,<2.0.0', 'ruamel.yaml>=0.17.21,<0.18.0']

entry_points = \
{'console_scripts': ['frontmatter = py_frontmatter.console.application:main']}

setup_kwargs = {
    'name': 'py-frontmatter',
    'version': '0.4.0',
    'description': 'Manipulate YAML front matter.',
    'long_description': '# py-frontmatter\n\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n[![formatter](https://img.shields.io/badge/%20formatter-docformatter-fedcba.svg)](https://github.com/PyCQA/docformatter)\n[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)\n[![linting: pylint](https://img.shields.io/badge/linting-pylint-yellowgreen)](https://github.com/PyCQA/pylint)\n[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)\n[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/koyeung/py-frontmatter/main.svg)](https://results.pre-commit.ci/latest/github/koyeung/py-frontmatter/main)\n\nTo manipulate front matter in document file.\n\n## Installation\n\n```shell\npip install py-frontmatter\n```\n\n## Usage\n\nGiven text file:\n```markdown\n---\ntitle: Hacker\'s note\ntags: [a, b]\n---\n# header\ntext\n```\n\n### Get or set whole section of front matter\n\nTo retrieve front matter as JSON:\n```commandline\n% frontmatter get note.md | jq\n{\n  "title": "Hacker\'s note",\n  "tags": [\n    "a",\n    "b"\n  ]\n}\n```\n\nTo replace the front matter:\n```commandline\n% echo \'{"title": "My note", "tags": ["a", "b", "c"]}\' | frontmatter set note.md\n% cat note.md\n---\ntitle: My note\ntags:\n- a\n- b\n- c\n---\n# header\ntext\n```\n\n### Add or remove item from front matter\n\n```commandline\n% frontmatter add-item --jsonpath \'$.tags\' --item d note.md\n% cat note.md\n---\ntitle: My note\ntags:\n- a\n- b\n- c\n- d\n---\n# header\ntext\n%\n% frontmatter remove-item --jsonpath \'$.tags\' --item d note.md\n% cat note.md\n---\ntitle: My note\ntags:\n- a\n- b\n- c\n---\n# header\ntext\n```\n\n### Specialize commands to add/remove tag\n\n```commandline\n% frontmatter add-tag --tag d note.md\n% cat note.md\n---\ntitle: My note\ntags:\n- a\n- b\n- c\n- d\n---\n# header\ntext\n% frontmatter remove-tag --tag d note.md\n% cat note.md\n---\ntitle: My note\ntags:\n- a\n- b\n- c\n---\n# header\ntext\n```\n',
    'author': 'YEUNG King On',
    'author_email': 'koyeung@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
