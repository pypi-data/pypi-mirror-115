# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cblack', 'cblack.config', 'cblack.utils']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['cblack = cblack:main']}

setup_kwargs = {
    'name': 'configparser-black',
    'version': '0.1.0',
    'description': 'A wrapper for black to connect with other python configuration files such as setup.cfg and tox.ini',
    'long_description': '# configparser-black\n\nA module to parse configuration for black from common python config files such as `setup.cfg`, `tox.ini`, etc\n\n## Install\n\n```bash\npip install configparser-black\n```\n\n## Run\n\n```bash\ncblack\n```\nor\n```bash\npython -m cblack\n```\n\n## Configuration\n\nBlack supports pyproject.toml and global configuration natively.\n\nThis module ignores `setup.cfg` and `tox.ini` black related configurations if there is a `[tool.black]` section in your `pyproject.toml`\nThis module will pass the configuration to black as command line arguments, meaning that it will override any configuration you have in your global black files in\n- Windows `~\\.black`\n- Linux/MacOS: `$XDG_CONFIG_HOME/black` (`~/.config/black` if the `XDG_CONFIG_HOME` environment variable is not set)\n\nIf there is no `pyproject.toml` it will lookup for configuration in\n1. `setup.cfg`: as `[tool:black]`\n2. `tox.ini`: as `[black]`\n\nwith the higher number superseeding lower numbers (i.e `tox.ini` overrides any black configuration found in `setup.cfg`)\n\n### setup.cfg\nExample configuration in `setup.cfg`\n```ini\n[tool:black]\nline-length = 100\nquiet = true\ntarget-version = py37\ninclude = \\.pyi?|somerandomfilename$\nextend-exclude = ^/foo.py\n```\n\nRunning\n```bash\ncblack --check ./\n```\n\nblack will run with\n```bash\nblack --quiet --line-length 100 --target-version py37 --include \'\\.pyi?|somerandomfilename\' --check ./\n```\n\n### tox.ini\nSame configuration in `tox.ini`\n```ini\n[black]\nline-length = 79\ntarget-version = [\'py37\', \'py38\']\n; Note single and double quotes at the start/end are stripped\ninclude = "\\.pyi?$"\nextend-exclude = ^/foo.py\n```\n\nRunning\n```bash\ncblack ./\n```\n\nSimilarly black will run with\n\nblack will run with\n```bash\nblack --line-length 79 --target-version py36 --target-version py37 --include \'\\.pyi?$\' --extend-exclude \'^/foo.py\' ./\n```\n\n## Notes\n\n### Quotes\nQuotes will be stripped from values from start and end. Also there is no need to escape quotes in the middle of a string.\n\ne.g\n```ini\ninclude = "somerandomfile"\n```\n\nWill be\n```bash\nblack --include "somerandomfile"\n# Equivalently in bash\nblack --include somerandomfile\n```\n\nand not\n```bash\nblack --include "\\"somerandomfile\\""\n```\n\nIf you want to include quotes you can wrap in single if you want double or double if you want single\ni.e\n```ini\ninclude = \'"somerandomfile"\'\nextend-exclude = "\'somerandomfile\'"\n```\nwill be\n\n```bash\nblack --include "\\"somerandomfile\\"" --extend-exclude "\'somerandomfile\'"\n```\n',
    'author': 'tchar',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/tchar/configparser-black',
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.6.2',
}


setup(**setup_kwargs)
