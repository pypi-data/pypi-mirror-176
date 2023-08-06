# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['aceye']

package_data = \
{'': ['*'],
 'aceye': ['Application Profiles/CSV/*',
           'Application Profiles/HTML/*',
           'Application Profiles/JSON/*',
           'Application Profiles/Markdown/*',
           'Application Profiles/Mindmap/*',
           'Application Profiles/YAML/*',
           'Bridge Domains/CSV/*',
           'Bridge Domains/HTML/*',
           'Bridge Domains/JSON/*',
           'Bridge Domains/Markdown/*',
           'Bridge Domains/Mindmap/*',
           'Bridge Domains/YAML/*',
           'Contexts/CSV/*',
           'Contexts/HTML/*',
           'Contexts/JSON/*',
           'Contexts/Markdown/*',
           'Contexts/Mindmap/*',
           'Contexts/YAML/*',
           'EPG/CSV/*',
           'EPG/HTML/*',
           'EPG/JSON/*',
           'EPG/Markdown/*',
           'EPG/Mindmap/*',
           'EPG/YAML/*',
           'Endpoints/CSV/*',
           'Endpoints/HTML/*',
           'Endpoints/JSON/*',
           'Endpoints/Markdown/*',
           'Endpoints/Mindmap/*',
           'Endpoints/YAML/*',
           'L3Outs/CSV/*',
           'L3Outs/HTML/*',
           'L3Outs/JSON/*',
           'L3Outs/Markdown/*',
           'L3Outs/Mindmap/*',
           'L3Outs/YAML/*',
           'Subnets/CSV/*',
           'Subnets/HTML/*',
           'Subnets/JSON/*',
           'Subnets/Markdown/*',
           'Subnets/Mindmap/*',
           'Subnets/YAML/*',
           'Tenant/CSV/*',
           'Tenant/HTML/*',
           'Tenant/JSON/*',
           'Tenant/Markdown/*',
           'Tenant/Mindmap/*',
           'Tenant/YAML/*',
           'Top System/CSV/*',
           'Top System/HTML/*',
           'Top System/JSON/*',
           'Top System/Markdown/*',
           'Top System/Mindmap/*',
           'Top System/YAML/*']}

install_requires = \
['Jinja2>=3.1.2,<4.0.0',
 'PyYAML>=6.0,<7.0',
 'requests>=2.28.1,<3.0.0',
 'rich-click>=1.5.1,<2.0.0']

entry_points = \
{'console_scripts': ['aceye = aceye.script:run']}

setup_kwargs = {
    'name': 'aceye',
    'version': '1.0.7',
    'description': 'Business ready documents from Cisco ACI',
    'long_description': '# ACEye\n\nBusiness Ready Documents for Cisco ACI\n\n## Installation\n\n```console\n$ python3 -m venv ACI\n$ source ACI/bin/activate\n(ACI) $ pip install aceye\n```\n\n## Usage - Help\n\n```console\n(ACI) $ aceye --help\n```\n\n![ACEye Help](/images/help.png)\n\n## Usage - In-line\n\n```console\n(ACI) $ aceye --url <url to APIC> --username <APIC username> --password <APIC password>\n```\n\n## Usage - Interactive\n\n```console\n(ACI) $ aceye\nAPIC URL: <URL to APIC>\nAPIC Username: <APIC Username>\nAPIC Password: <APIC Password>\n```\n\n## Usage - Environment Variables\n\n```console\n(ACI) $ export URL=<URL to APIC>\n(ACI) $ export USERNAME=<APIC Username>\n(ACI) $ export PASSWORD=<APIC Password>\n```\n\n## Recommended VS Code Extensions\n\nExcel Viewer - CSV Files\nMarkdown Preview - Markdown Files\nMarkmap - Mindmap Files\nOpen in Default Browser - HTML Files\n\n## Contact\n\nPlease contact John Capobianco if you need any assistance',
    'author': 'John Capobianco',
    'author_email': 'ptcapo@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
