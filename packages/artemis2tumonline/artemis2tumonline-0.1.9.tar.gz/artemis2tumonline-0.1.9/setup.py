# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['artemis2tumonline', 'artemis2tumonline.model']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.28.1,<3.0.0', 'typer>=0.7.0,<0.8.0']

entry_points = \
{'console_scripts': ['artemis2tumonline = artemis2tumonline.main:app']}

setup_kwargs = {
    'name': 'artemis2tumonline',
    'version': '0.1.9',
    'description': '',
    'long_description': '# Artemis2TUMOnline\n\nAfter conducting an exam with [Artemis](https://artemis.ase.in.tum.de/), you can download a CSV file with the grades of the students.\nThe problem is that the format of the Artemis export is **NOT** the format that TUMOnline is expecting.\nThus, you cannot directly upload the CSV to TUMOnline.\n\nThis small tool can help you to create the CSV for TUMOnline.\n\n## Installation\n\nThe easiest way to install the package is to use pip.\n\n```bash\npip install artemis2tumonline\n```\n**Attention**: On macOS, `pip` is usually the installer of the Python2 instance.\nPlease use `pip3` or `pip3.x` in this case.\n\nIf you want to work on the software, you can install the dependencies via [poetry](https://python-poetry.org/).\n\n```bash\npoetry install\n```\n\n## Usage\n\n```bash\nartemis2tumonline create-final-results --help\nUsage: artemis2tumonline create-final-results [OPTIONS]\n\n  Reads a TUMOnline registration and a Artemis export file. Creates an\n  TUMOnline file with the grades of the students.\n\nOptions:\n  -t, --tumonline-registration-file FILE\n                                  The registration file. You can get this file\n                                  from TUMOnline. Usually, this is the same\n                                  file you use to register the students for\n                                  the exam.\n  -a, --artemis-export-file FILE  The CSV file you can download from Artemis.\n  -o, --output-file FILE          The resulting CSV file. This file contains\n                                  the necessary information from the TUMOnline\n                                  Registration file and the grades from the\n                                  Artemis export. You can upload this file to\n                                  TUM Online.  [default: /path/to/cwd/tumonline.csv]\n  --install-completion [bash|zsh|fish|powershell|pwsh]\n                                  Install completion for the specified shell.\n  --show-completion [bash|zsh|fish|powershell|pwsh]\n                                  Show completion for the specified shell, to\n                                  copy it or customize the installation.\n  --help                          Show this message and exit.\n\n```\n\n### Example\n\n```bash\n$ poetry run artemis2tumonline --tumonline-registration-file ./test/Modulpruefung_29072021-0800_IN2178_FA_SecurityEngineering.csv --artemis-export-file test/Final_exam__Security_EngineeringResults.csv\nWe load the TUM online file /path/to/cwd/test/Modulpruefung_29072021-0800_IN217 8_FA_SecurityEngineering.csv\n... and the Artemis file /path/to/cwd/test/Final_exam__Security_EngineeringResults.csv\n... and write the results in /path/to/cwd/tumonline.csv\n```\n\n## Misc\n\nIf you have any question, just write [me](mailto:patrick.stoeckle@tum.de?subject=Artemis2TUMOnline) an email.\n',
    'author': 'Patrick Stöckle',
    'author_email': 'patrick.stoeckle@tum.de',
    'maintainer': 'Patrick Stöckle',
    'maintainer_email': 'patrick.stoeckle@tum.de',
    'url': 'https://github.com/pstoeckle/artemis2tumonline.git',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
