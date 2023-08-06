# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['gl_pages_forward', 'gl_pages_forward.rsc', 'gl_pages_forward.tests']

package_data = \
{'': ['*']}

install_requires = \
['Jinja2>=3.1.2,<4.0.0',
 'minify-html>=0.10.3,<0.11.0',
 'ruamel.yaml>=0.17.21,<0.18.0',
 'typer>=0.7.0,<0.8.0']

entry_points = \
{'console_scripts': ['create-forward-pages = gl_pages_forward.main:app']}

setup_kwargs = {
    'name': 'gl-pages-forward',
    'version': '0.1.3',
    'description': 'Script to create forward pages.',
    'long_description': "# gl-pages-forward\n\nThe [Technical University of Munich (TUM)](https://www.tum.de/en/) has a nice service for [TinyURLs](https://portal.mytum.de/rds_tinyurl_list).\nYou can create there short links, e.g., <https://go.tum.de/584374>.\nHowever, you can only do this for `*.tum.de` or `*.lrz.de` addresses.\nTo circumvent this, I created this repository.\nWith the Python scripts in here, you can create several *forward* pages, e.g., `index.html` that do nothing else but redirect the browser to a given site.\nIf you combine these forward pages with the [GitLab Pages](https://docs.gitlab.com/ee/user/project/pages/) of the [gitlab.lrz.de](https://gitlab.lrz.de/), you can create a short link for every site you want. \n\n## Usage\n\n```shell\n$ create-forward-pages --help\nUsage: create-forward-pages [OPTIONS]\n\n  Creates 'index.html's that forward to a specific URL.\n\nOptions:\n  -v, --version\n  -c, --config-file FILE          [default: config.yml]\n  -o, --output DIRECTORY          [default: public]\n  -u, --base-url TEXT\n  -m, --minify                    If this flag is set, the tool will minify\n                                  the HTML.\n  --install-completion [bash|zsh|fish|powershell|pwsh]\n                                  Install completion for the specified shell.\n  --show-completion [bash|zsh|fish|powershell|pwsh]\n                                  Show completion for the specified shell, to\n                                  copy it or customize the installation.\n  --help                          Show this message and exit.\n```\n\n## Contact\n\nIf you have any question, please contact [Patrick Stöckle](mailto:patrick.stoeckle@posteo.de).\n",
    'author': 'Patrick Stöckle',
    'author_email': 'patrick.stoeckle@posteo.de',
    'maintainer': 'Patrick Stöckle',
    'maintainer_email': 'patrick.stoeckle@posteo.de',
    'url': 'https://github.com/pstoeckle/GitLab-Forward-Pages.git',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
