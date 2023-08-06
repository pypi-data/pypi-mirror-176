# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ydl_podcast']

package_data = \
{'': ['*']}

install_requires = \
['Jinja2>=3.1.2,<4.0.0', 'MarkupSafe>=2.1.1,<3.0.0', 'PyYAML==6.0']

extras_require = \
{':extra == "youtube-dl"': ['youtube-dl>=2021.12.17'],
 'yt-dlp': ['yt-dlp>=2022.10.4']}

entry_points = \
{'console_scripts': ['ydl-podcast = ydl_podcast.__main__:main']}

setup_kwargs = {
    'name': 'ydl-podcast',
    'version': '1.0.1',
    'description': 'A simple tool to generate Podcast-like RSS feeds from youtube (or other youtube-dl supported services) channels, using youtube-dl',
    'long_description': '![Pypi Version Shield](https://img.shields.io/pypi/v/ydl-podcast.svg?style=flat-square)\n![Pypi License Shield](https://img.shields.io/pypi/l/ydl-podcast.svg?style=flat-square)\n\n# ydl-podcast\n\nA simple tool to generate Podcast-like RSS feeds from youtube (or other\nyoutube-dl supported services) channels, using\n[`youtube-dl`](https://github.com/rg3/youtube-dl).\n\n## Setup\n\nInstall package with requirements:\n\n### Youtube-dl:\n\n`pip install ydl-podcast[youtube-dl]`\n\n### yt-dlp:\n\n`pip install ydl-podcast[yt-dlp]`\n\n## Configuration\n\nEdit the config.yaml file to list your podcast sources and configure them,\nas well as edit general configuration.\n\nThe available settings are the following.\n\n### General settings\n\n- `output_dir`: local directory where the downloaded media will be stored, and\n  the podcast xml files generated.\n- `url_root`: root url for the static files (used in the generation of the XML\n  to point to the media files.\n- `subscriptions`: a list of feeds to subscribe to.\n- `youtube-dl-module`: Alternative youtube-dl python module. By default, this\nuses [youtube-dl](https://github.com/rg3/youtube-dl), but can leverage forks\nsuch as [yt-dlp](https://github.com/yt-dlp/yt-dlp).\n\n### Feed settings\n\n#### Mandatory\n- `name NAME`: Name of the podcast source. Used as the podcast title, and media\n  directory name.\n- `url URL`: source url for the youtube (or other) channel.\n\n#### Optional\n- `audio_only True/False`: if `True`, audio will be extracted from downloaded\n  videos to create an audio podcast.\n- `retention_days N`: only download elements newer than `N` days, and\n  automatically delete elements older.\n- `download_last N`: only download the latest `N` videos.\n- `initialize True/False`: if `True`, then downloads everything on the first\n  run, no matter the `download_last` or `retention_days` specified.\n- `output_dir`: local directory where the downloaded media will be stored, and\n  the podcast xml files generated.\n- `url_root`: root url for the static files (used in the generation of the XML\n  to point to the media files.\n- `format`: file format to force youtube-dl to use (eg mp4, webm, mp3 for audio\n  only…)\n- `best`: force best quality (only useful when specifying a format).\n- `ydl_options`: list of raw youtube-dl options to use. For experienced users,\n  since this will likely yield issues if not understood.\n\n## Usage\n\nUsing cron or your favorite scheduler, run:\n\n`ydl_podcast [configfile.yaml]`\n\nYou can then use your favorite web server to serve the files (a good idea is to\nexclude the `*.json` and `*.part` files from being served as the first might\nleak information, and the second is unnecessary.\n\neg with nginx:\n\n```\nroot /var/www/static/podcasts/;\nlocation ~ (\\.json$|\\.part$) {\n  return 403;\n}\n```\n',
    'author': 'nbr23',
    'author_email': 'max@23.tf',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/nbr23/ydl-podcast',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
