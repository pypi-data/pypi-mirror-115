# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['egauge_async']

package_data = \
{'': ['*']}

install_requires = \
['httpx>=0.16.0,<0.19.0']

setup_kwargs = {
    'name': 'egauge-async',
    'version': '0.1.1',
    'description': 'Async client for eGauge energy monitor (https://www.egauge.net)',
    'long_description': '# Egauge-Async\n\n`asyncio` APIs for communicating with [eGauge](https://www.egauge.net) meters.\n\n## Examples\n\n### Get current rates\n```python\nimport asyncio\nfrom egauge_async import EgaugeClient\n\nasync def get_current_rates():\n    egauge = EgaugeClient("http://egaugehq.d.egauge.net")\n    current_readings = egauge.get_current_rates()\n    print(current_readings)\n\nasyncio.run(get_current_rates())\n```\n\n### Get weekly changes over the last 4 weeks\n\n```python\nimport asyncio\nfrom egauge_async import EgaugeClient\n\nasync def get_weekly_changes():\n    egauge = EgaugeClient("http://egaugehq.d.egauge.net")\n    weekly_changes = egauge.get_weekly_changes(num_weeks=4)\n    print(weekly_changes)\n\nasyncio.run(get_weekly_changes())\n```\n\n### Get available registers\n\n```python\nimport asyncio\nfrom egauge_async import EgaugeClient\n\nasync def get_registers():\n    egauge = EgaugeClient("http://egaugehq.d.egauge.net")\n    instantaneous_registers = egauge.get_instantaneous_registers()j\n    print(instantaneous_registers)\n    historical_registers = egauge.get_historical_registers()\n    print(historical_registers)\n\nasyncio.run(get_historical_registers())\n```\n\n## Implementation Details\n\nThis package uses the publically-documented [XML API](https://kb.egauge.net/books/egauge-meter-communication/page/xml-api)\nprovided by eGauge Systems.\n\n## Disclaimer\n\nThis project is not affiliated with, endorsed by, or sponsored by eGauge Systems LLC. Any\nproduct names, logos, brands, or other trademarks are the property of their respective\ntrademark holders.\n',
    'author': 'Nic Eggert',
    'author_email': 'nic@eggert.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/neggert/egauge-async',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
