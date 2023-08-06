# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['diagrams_net_automation']

package_data = \
{'': ['*']}

install_requires = \
['lxml>=4.9.1,<5.0.0', 'tqdm>=4.64.1,<5.0.0', 'typer>=0.7.0,<0.8.0']

entry_points = \
{'console_scripts': ['diagrams-net-automation = '
                     'diagrams_net_automation.main:app']}

setup_kwargs = {
    'name': 'diagrams-net-automation',
    'version': '0.1.8',
    'description': 'Scripts to automatically covert diagrams.net files, e.g., to PDF.',
    'long_description': '# Diagrams.net Automation\n\n[[_TOC_]]\n\n## Usage\n\n```bash\nUsage: diagrams-net-automation [OPTIONS] COMMAND [ARGS]...\n\n  :return:\n\nOptions:\n  --version                       Version\n  --help                          Show this message and exit.\n\nCommands:\n  convert-diagrams  Converts Draw.io files to PDF and PNG.\n```\n\n### Convert Diagrams\n\n```bash\nUsage: diagrams-net-automation convert-diagrams [OPTIONS]\n\n  Converts Draw.io files to PDF and PNG.\n\nOptions:\n  -d, --input-directory DIRECTORY\n                                  Input directory with the diagrams.net files.\n                                  [default: .]\n  -o, --output-directory DIRECTORY\n                                  The output directory where the PDF, JPG, or\n                                  PNG files should be stored.  [default: dist]\n  -D, --draw-io FILE              The diagrams.net executable.  [default: /App\n                                  lications/draw.io.app/Contents/MacOS/draw.io\n                                  ]\n  -w, --width INTEGER             If a width is passed, we will generate a PNG\n                                  and/or JPG with this width.\n  -X, --include-xml               Convert also .xml files, not only .drawio\n                                  files.\n  -P, --generate-png              Generate PNG files.\n  -J, --generate-jpg              Generate JPG files.\n  -S, --skip-pdf-generation       If this flag is set, we will not generate\n                                  PDF files.\n  -I, --ignore-cache              If this flag is passed, we will ignore\n                                  anything in the current cache file. In the\n                                  end, we will overwrite the current cache\n                                  file.\n```\n',
    'author': 'Patrick Stöckle',
    'author_email': 'patrick.stoeckle@posteo.de',
    'maintainer': 'Patrick Stöckle',
    'maintainer_email': 'patrick.stoeckle@posteo.de',
    'url': 'https://github.com/pstoeckle/Diagrams.net-Automation.get',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
