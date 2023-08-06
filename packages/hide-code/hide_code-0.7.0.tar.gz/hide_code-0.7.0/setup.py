# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['hide_code', 'hide_code.test']

package_data = \
{'': ['*'], 'hide_code': ['Templates/*']}

install_requires = \
['jupyter>=1.0.0,<2.0.0', 'notebook>=6.4.12,<7.0.0', 'pdfkit>=1.0.0,<2.0.0']

entry_points = \
{'nbconvert.exporters': ['hide_code_html = hide_code:HideCodeHTMLExporter',
                         'hide_code_latex = hide_code:HideCodeLatexExporter',
                         'hide_code_latexpdf = '
                         'hide_code:HideCodeLatexPDFExporter',
                         'hide_code_pdf = hide_code:HideCodePDFExporter',
                         'hide_code_slides = hide_code:HideCodeSlidesExporter']}

setup_kwargs = {
    'name': 'hide-code',
    'version': '0.7.0',
    'description': 'A Jupyter notebook extension to hide code, prompts and outputs.',
    'long_description': '# Hide_code\n![PyPI version](https://badge.fury.io/py/hide_code.svg) ![MIT license](https://img.shields.io/github/license/mashape/apistatus.svg) \nRelease: ![Travis release build](https://travis-ci.org/kirbs-/hide_code.svg?branch=master) Dev: ![Dev Build Status](https://travis-ci.org/kirbs-/hide_code.svg?branch=dev)\n\nhide_code is a Jupyter notebook extension to selectively hide code, prompts and outputs with PDF and HTML exporting support. Check out the demo with [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/kirbs-/hide_code/master?filepath=demo.ipynb)\n\n![demo](/images/demo.gif)\n\n## Jupyter Notebook Installation\n1. `pip install hide_code`\n2. `jupyter nbextension install --py hide_code`\n3. `jupyter nbextension enable --py hide_code`\n4. `jupyter serverextension enable --py hide_code`\n\n## Jupyter Lab Installation\n1. `pip instal hide_code[lab]`\n2. `jupyter lab build`\n\n## Upgrading with nbextension\n1. `pip install hide_code --upgrade`\n2. `jupyter nbextension install --py hide_code`\n\nNote: add `--sys-prefix` to `jupyter nbextension` to install into virtualenv or conda environment.\n\n## Changes in 0.6.0\n#### Improvements\n* Added experiemental Jupyter Lab support. See [Lab usage](https://github.com/kirbs-/hide_code/wiki/Lab%20Usage) for details and limitations.\n* Added Binder demo [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/kirbs-/hide_code/master?filepath=demo.ipynb)\n* Simplified extension installation. No longer need to use nbextension/serverextension commands after pip install.\n* No longer supporting Python 2.7. Install hide_code==0.5.2 for Python 2.7.\n* 0.5.6 is the last version to support Python 3.6 and older.\n* Added extras_install [all] to install hide_code and all dependencies. Use `pip install hide_code[all]` to install. Resolves #85. \n\n\n\n\n## Documentation\nVisit the [Wiki](https://github.com/kirbs-/hide_code/wiki).\n\n## Requirements\n* Jupyter notebook >6.0\n* Jupyter nbconvert >6.x\n* pdfkit & [wkhtmltopdf](http://wkhtmltopdf.org/)\n* Python 3.7+\n\n![hide_code-hits](https://caspersci.uk.to/cgi-bin/hits.cgi?q=hide_code&style=social&r=https://github.com/kirbs-/hide_code&l=https://caspersci.uk.to/images/tqdm.png&f=https://raw.githubusercontent.com/tqdm/tqdm/master/images/logo.gif)\n\n',
    'author': 'Chris Kirby',
    'author_email': 'kirbycm@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
