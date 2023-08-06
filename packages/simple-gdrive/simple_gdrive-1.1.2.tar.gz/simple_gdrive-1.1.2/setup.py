# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['simple_gdrive']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.1.3,<9.0.0',
 'google-api-python-client>=2.47.0,<3.0.0',
 'google-auth-httplib2>=0.1.0,<0.2.0',
 'google-auth-oauthlib>=0.5.1,<0.6.0',
 'loguru>=0.6.0,<0.7.0',
 'tqdm>=4.64.0,<5.0.0']

entry_points = \
{'console_scripts': ['gdrive = simple_gdrive.__main__:cli']}

setup_kwargs = {
    'name': 'simple-gdrive',
    'version': '1.1.2',
    'description': 'Simple command to help download and upload big files to Google Drive (using their official Drive APIs)',
    'long_description': "**simple-gdrive**: A simple command to help download and upload big files to Google Drive (using their official APIs)\n\n### Setup\n\nBefore using the command, you must open Google Cloud Platform and create credentials for oauth: [cloud.google.com](https://cloud.google.com) > APIs & Services > Credentials. Note that if your project hasn't enabled Drive APIs, go to APIs & Services > Enabled APIs & Services and add Drive APIs.\nThen, download the JSON file and put it in the AuthDir (default at `~/.simple_gdrive`) with the name `credentials.json`. When you run the script for the first time, it will redirect to your browser so you can authenicate and give permission to YOUR application (created in the previous step) to access to your drive. Then, you will obtain an access token saving to the same drive with name `tokens.json`. Keeping the two files safe (or delete `tokens.json` after usage) and nobody else will have access to your data.\n\n### Installation\n\n```bash\npip install simple-gdrive\n```\n\n### Usage\n\nInvoke the command by running `gdrive` or `python -m simple_gdrive`.\n\nDownload a file:\n\n```bash\ngdrive download -s <path in disk> -d <path in drive>\n```\n\nUpload a file\n\n```bash\ngdrive upload -s <file path in disk> -d <path in drive>\n```\n\nFor example:\n\n```bash\ngdrive download -s //KGData/Wikipedia/20220420/enwiki-NS0-20220420-ENTERPRISE-HTML.json.tar.gz -d enwiki.json.tar.gz\n```\n\n```bash\ngdrive upload -s ./enwiki-NS0-20220420-ENTERPRISE-HTML.json.tar.gz -d //KGData/Wikipedia/20220420/enwiki-NS0-20220420-ENTERPRISE-HTML.json.tar.gz\n```\n\nIf the path in Google drive startswith `/`, the top folder/file will be in your drive (e.g., `/abc` points to the folder `abc` in your drive). If it starts with `//`, the first level will be the name of the shared drive and the second level will be the folder/file in the shared drive (e.g., `//KGData/abc` points to the folder `abc` in KGData shared drive).\n",
    'author': 'Binh Vu',
    'author_email': 'binh@toan2.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/binh-vu/simple_gdrive',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
