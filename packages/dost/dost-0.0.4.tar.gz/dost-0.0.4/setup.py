# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dost']

package_data = \
{'': ['*']}

install_requires = \
['Pillow>=9.2.0,<10.0.0',
 'PyPDF2>=2.11.0,<3.0.0',
 'PyQRCode>=1.2.1,<2.0.0',
 'PyScreeze>=0.1.28,<0.2.0',
 'WMI>=1.5.1,<2.0.0',
 'aspose-words>=22.10.0,<23.0.0',
 'barcode>=1.0.2,<2.0.0',
 'captcha>=0.4,<0.5',
 'countryinfo>=0.1.2,<0.2.0',
 'easyocr>=1.6.2,<2.0.0',
 'geopy>=2.2.0,<3.0.0',
 'gspread-dataframe>=3.3.0,<4.0.0',
 'gspread>=5.6.2,<6.0.0',
 'imageio>=2.22.1,<3.0.0',
 'invoice2data>=0.3.6,<0.4.0',
 'oauth2client>=4.1.3,<5.0.0',
 'opencv-python==4.5.5.64',
 'openpyxl>=3.0.10,<4.0.0',
 'pandas>=1.5.0,<2.0.0',
 'pdfplumber>=0.7.5,<0.8.0',
 'phonenumbers>=8.12.56,<9.0.0',
 'plyer>=2.0.0,<3.0.0',
 'pygetwindow>=0.0.9,<0.0.10',
 'pyshorteners>=1.0.1,<2.0.0',
 'pytesseract>=0.3.10,<0.4.0',
 'pyttsx3>=2.90,<3.0',
 'pytube>=12.1.0,<13.0.0',
 'pywhatkit>=5.4,<6.0',
 'pywinauto>=0.6.8,<0.7.0',
 'pyzbar>=0.1.9,<0.2.0',
 'requests>=2.28.1,<3.0.0',
 'speechrecognition>=3.8.1,<4.0.0',
 'textblob>=0.17.1,<0.18.0',
 'typeguard>=2.13.3,<3.0.0',
 'winshell>=0.6,<0.7',
 'xls2xlsx>=0.1.5,<0.2.0',
 'xlsx2html>=0.4.0,<0.5.0',
 'xlwt>=1.3.0,<2.0.0',
 'yagmail>=0.15.293,<0.16.0']

extras_require = \
{':sys_platform == "linux"': ['torch @ '
                              'https://download.pytorch.org/whl/cpu/torch-1.10.0%2Bcpu-cp39-cp39-linux_x86_64.whl'],
 ':sys_platform == "win32" and python_full_version == "3.10.0"': ['torch @ '
                                                                  'https://download.pytorch.org/whl/cpu/torch-1.12.0%2Bcpu-cp310-cp310-win_amd64.whl'],
 ':sys_platform == "win32" and python_full_version == "3.9.0"': ['torch @ '
                                                                 'https://download.pytorch.org/whl/cpu/torch-1.10.0%2Bcpu-cp39-cp39-win_amd64.whl']}

setup_kwargs = {
    'name': 'dost',
    'version': '0.0.4',
    'description': 'DOST is a Python based Utility platform as an Open Source project. We strive to liberate humans from mundane, repetitive tasks, giving them more time to use their intellect and creativity to solve higher-order business challenges and perform knowledge work.',
    'long_description': "`DOST` project that is a utility module for Python.\nThis package is a collection of utilities that you can use in your projects.\n\n## Table Of Contents\n\n1. [Clipboard](https://py-bots.github.io/dost/clipboard/)\n2. [Converter](https://py-bots.github.io/dost/converter/)\n3. [Excel](https://py-bots.github.io/dost/excel/)\n4. [File](https://py-bots.github.io/dost/file/)\n5. [Folder](https://py-bots.github.io/dost/folder/)\n6. [Keyboard](https://py-bots.github.io/dost/keyboard/)\n7. [Mail](https://py-bots.github.io/dost/mail/)\n8. [Message](https://py-bots.github.io/dost/message/)\n9. [Mouse](https://py-bots.github.io/dost/mouse/)\n10. [Pdf](https://py-bots.github.io/dost/pdf/)\n11. [Text](https://py-bots.github.io/dost/text/)\n12. [Utility](https://py-bots.github.io/dost/utility/)\n13. [Voice](https://py-bots.github.io/dost/voice/)\n14. [Windows](https://py-bots.github.io/dost/windows/)\n\n\nQuickly find what you're looking for depending on\nyour use case by looking at the different pages.\n\n## Acknowledgements\n\nI would like to thank the people who have made this project possible. \nMy sincere thanks to all the authors of the packages that I have used in this project.",
    'author': 'PyBOTs',
    'author_email': 'support@pybots.ai',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://pybots.ai',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.9.0,<=3.10.40',
}


setup(**setup_kwargs)
