# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dapodix', 'dapodix.peserta_didik']

package_data = \
{'': ['*']}

install_requires = \
['cachetools>=4.2.2,<5.0.0',
 'click>=8.0.1,<9.0.0',
 'dapodik>=0.16.4,<0.17.0',
 'openpyxl>=3.0.7,<4.0.0']

entry_points = \
{'console_scripts': ['dapodix = dapodix.__main__:main']}

setup_kwargs = {
    'name': 'dapodix',
    'version': '0.2.0',
    'description': 'Alat bantu aplikasi Dapodik kemdikbud',
    'long_description': '# dapodix\n\n[![dapodix - PyPi](https://img.shields.io/pypi/v/dapodix)](https://pypi.org/project/dapodix/)\n[![Download](https://img.shields.io/badge/Download-Unduh-brightgreen)](https://github.com/hexatester/dapodix/archive/master.zip)\n[![Donate DANA](https://img.shields.io/badge/Donasi-DANA-blue)](https://link.dana.id/qr/1lw2r12r)\n[![Tutorial](https://img.shields.io/badge/Tutorial-Penggunaan-informational)](https://github.com/hexatester/dapodix/wiki)\n[![Group Telegram](https://img.shields.io/badge/Telegram-Group-blue.svg)](https://t.me/dapodik_2021)\n[![codecov](https://codecov.io/gh/hexatester/dapodix/branch/master/graph/badge.svg)](https://codecov.io/gh/hexatester/dapodix)\n[![LISENSI](https://img.shields.io/github/license/hexatester/dapodix)](https://github.com/hexatester/dapodix/blob/master/LISENSI)\n\nAlat bantu aplikasi dapodik.\n\n## Install\n\nPastikan minimal [python versi 3.7](https://www.python.org/downloads/release/python-3711/) terinstall,\nkemudian jalankan perintah di bawah dalam Command Prompt atau Powershell (di Windows + X):\n\n```bash\npip install --upgrade dapodix\n```\n\n## Fitur yang akan datang\n\n- Download data ke Excel\n- Petunjuk validasi\n- Bulk update dari Excel\n\n## Legal / Hukum\n\nKode ini sama sekali tidak berafiliasi dengan, diizinkan, dipelihara, disponsori atau didukung oleh [Kemdikbud](https://kemdikbud.go.id/) atau afiliasi atau anak organisasinya. Ini adalah perangkat lunak yang independen dan tidak resmi. _Gunakan dengan risiko Anda sendiri._\n',
    'author': 'hexatester',
    'author_email': 'hexatester@protonmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/hexatester/dapodix',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
