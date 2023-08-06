# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['makeqr']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.1.3,<9.0.0',
 'pydantic[email]>=1.8.2,<2.0.0',
 'qrcode[pil]>=7.3.1,<8.0.0']

entry_points = \
{'console_scripts': ['makeqr = makeqr.__main__:main']}

setup_kwargs = {
    'name': 'makeqr',
    'version': '4.0.2',
    'description': 'Generate QR cards for any occasion',
    'long_description': '# wifi_qrcode\n\nGenerate WiFi Access QR Codes\n\n# Installation\n\n```bash\npip install makeqr -U\n```\n\n# Usage example\n\n## To test that installation was successful, try:\n\n```bash\nmakeqr --help\n```\n\nor\n\n```\nmakeqr wifi --help\n```\n\n## Command line command\n\n### Command\n\n```bash\nmakeqr -p wifi --ssid ABC --password Tfsjfklasdjfklasdest -s wpa2\n```\n\n### Output\n\n```\nDATA MODEL\n  {"ssid": "ABC", "security": "wpa2", "password": "Tfsjfklasdjfklasdest", "hidden": false}\nENCODED QR DATA\n  WIFI:S:ABC;P:Tfsjfklasdjfklasdest;T:WPA;;\nRESULT\n\n  ██████████████        ████  ██████  ██████  ██████████████\n  ██          ██    ██  ██████████        ██  ██          ██\n  ██  ██████  ██  ██████  ██  ██      ████    ██  ██████  ██\n  ██  ██████  ██  ██  ██      ██  ████    ██  ██  ██████  ██\n  ██  ██████  ██  ██    ██    ██    ████████  ██  ██████  ██\n  ██          ██  ██  ██████    ██  ████  ██  ██          ██\n  ██████████████  ██  ██  ██  ██  ██  ██  ██  ██████████████\n                  ██  ██████    ████  ██\n  ██  ██████████      ██      ████████        ██████████\n        ██  ██  ██  ██    ██    ████  ██████  ██  ██  ████\n  ██    ██  ████████    ████    ██████      ████  ████\n  ██████    ██  ██  ██  ██    ██      ██  ██████  ██    ████\n  ██          ██  ████  ██  ██    ████  ██      ████████\n        ██  ██    ██████  ██████    ████████    ████  ████\n    ██  ████  ████  ██████  ██  ██  ████  ██    ██    ██\n    ████  ████          ██    ██████    ██  ██      ██\n    ██████    ██  ████████████  ██████  ██      ██  ██  ████\n  ██      ████        ██    ████  ██████████████  ██    ██\n  ██      ██  ████    ██  ████  ████            ██  ████\n  ██  ██████        ██████    ██      ██████████  ██      ██\n  ██  ████  ██████      ████    ██████    ██████████████\n                  ██  ██    ██    ██  ██  ██      ██  ██\n  ██████████████      ██  ██████████  ██████  ██  ██  ██\n  ██          ██  ████  ██  ██  ████    ████      ████\n  ██  ██████  ██  ██  ██      ████  ██    ██████████    ████\n  ██  ██████  ██  ██    ████      ██      ██      ██    ████\n  ██  ██████  ██  ██    ██    ████  ████  ██  ████████  ██\n  ██          ██    ██  ██    ██████      ████      ██  ██\n  ██████████████  ██  ██        ██  ██  ██    ██  ██\n```\n\n## Docker container\n\n```bash\ndocker run ghcr.io/shpaker/makeqr:4.0.1 -p link https://t.me/shpaker\n\n```\n\n## As python module\n\n```bash\nfrom makeqr import MakeQR, QRMailToModel\n\nmodel = QRMailToModel(\n  to=\'foo@bar.baz\',\n  subject=\'Awesome subject!\',\n)\nqr = MakeQR(model)\ndata: bytes = qr.make_image_data()\n```\n',
    'author': 'Aleksandr Shpak',
    'author_email': 'shpaker@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/shpaker/makeqr',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7.2,<4.0.0',
}


setup(**setup_kwargs)
