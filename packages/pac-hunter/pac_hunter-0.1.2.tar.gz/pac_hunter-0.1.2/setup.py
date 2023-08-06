# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pac_hunter']

package_data = \
{'': ['*']}

install_requires = \
['httpx>=0.23,<0.24',
 'pandas>=1.0,<2.0',
 'requests>=2.28,<3.0',
 'seaborn>=0.12,<0.13',
 'thefuzz>=0.19,<0.20']

setup_kwargs = {
    'name': 'pac-hunter',
    'version': '0.1.2',
    'description': 'Search donations from specific PACs to candidates of interest, using OpenFEC and fivethirtyeight data',
    'long_description': '# pac_hunter :wolf:\nA simple project inspired by frustration over employers attempting to raise money from their ~~employees~~ captive audiences for the purpose of fueling their purchase of loyalty from politicians via Political Action Committees (PACs) in the United States.\n\n`pac_hunter` provides a wrapper around the fantastic API provided by the Federal Elections Committee called [OpenFEC](https://api.open.fec.gov/developers/). This tool is designed to match a PAC of interest with donations made to specific federal election candidates. The use case that inspired this tool was checking historical donations of a PAC to federal candidates or elected officials that denied the legitimacy of the 2020 election.\n\n# Getting started\nCheck the jupyter notebook provided with this repository `demo.ipynb`. You will have to either request your own self-service API key from the OpenFEC project, or use their `"DEMO_KEY"` which has a stricter rate limit.\n\nIf you are not familiar with running jupyter notebooks from a local environment, look forward to a google colab notebook once I\'ve published the package. In the meantime, you can run the demo yourself as long as you have python and git installed on your system.\n\n```bash\ngit clone https://github.com/jlwhelan28/pac-hunter.git\ncd pac-hunter\npython3 -m venv .venv\nsource .venv/bin/activate\npip install -r requirements.txt\npip install jupyter\njupyter notebook\n```\n\n##  Example: Raytheon Technologies\' PAC donations to 2020 election deniers\n\n![](heatmap_example.png)\n\n# Future release\nI\'m hopeful to provide a small service that runs a `streamlit` app providing a simple interface to use this tool for non-developers. Beyond that, future plans will depend on interest.\n',
    'author': 'jlwhelan28',
    'author_email': 'jlwhelan28@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
