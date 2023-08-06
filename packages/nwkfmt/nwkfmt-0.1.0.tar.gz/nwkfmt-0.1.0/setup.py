# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nwkfmt']

package_data = \
{'': ['*']}

install_requires = \
['biopython>=1.73,<2.0', 'typer>=0.6,<1']

entry_points = \
{'console_scripts': ['nwkfmt = nwkfmt.cli:entry_point']}

setup_kwargs = {
    'name': 'nwkfmt',
    'version': '0.1.0',
    'description': 'Simple Newick tree validator and formatter',
    'long_description': '# Newick Tree Validator and Formatter\n\nSimple utility to validate and format Newick trees.\n\n## Usage\n\nValidation without formatting:\n\n```bash\n./main.py <tree.nwk>\n```\n\nIn place formatting:\n\n```bash\n./main.py <tree.nwk> --inplace\n```\n\nOutputting formatted tree to a separate file:\n\n```bash\n./main.py <tree.nwk> --outfile <output.nwk>\n```\n\nOutputting list of terminal nodes into a text file:\n\n```bash\n./main.py <tree.nwk> --terminals <terminals.txt>\n```\n\n## Requirements\n\n- Python\n- Typer\n- BioPython\n',
    'author': 'Cornelius Roemer',
    'author_email': 'cornelius.roemer@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
