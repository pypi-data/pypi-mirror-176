# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['spotifycodegen']

package_data = \
{'': ['*']}

install_requires = \
['colorthief>=0.2.1,<0.3.0',
 'pillow>=9.3.0,<10.0.0',
 'spotipy>=2.21.0,<3.0.0',
 'tqdm>=4.64.1,<5.0.0']

entry_points = \
{'console_scripts': ['scg = spotifycodegen.cli:main']}

setup_kwargs = {
    'name': 'spotifycodegen',
    'version': '0.1.2',
    'description': '',
    'long_description': '![Test Badge](https://github.com/tilschuenemann/spotifycodegen/actions/workflows/CICD.yml/badge.svg)\n[![codecov](https://codecov.io/gh/tilschuenemann/spotifycodegen/branch/main/graph/badge.svg?token=WJ2OBJ3ZJV)](https://codecov.io/gh/tilschuenemann/spotifycodegen)\n\n# spotify codegen\n\n![Preview](preview.png)\n\nSpotify removed the feature to get a stitched image of an album / artist / track cover with their own [Spotify Code](https://www.spotifycodes.com/). This\npackage mimicks that behaviour and creates stitches, based on supplied\n\n- URL\n- URI\n- query\n\nIt\'s also possible to use create stitches for:\n\n- all saved albums\n- 50 followed artists (limit imposed by Spotify API)\n\n## Installation\n\n```bash\npip install spotifycodegen\n```\n\n## Usage\n\n`spotifycodegen` uses the Spotify API, there for you need to supply a Spotify Client ID & Token as environment variables:\n\n```bash\nexport SPOTIPY_CLIENT_ID="yourid"\nexport SPOTIPY_CLIENT_SECRET="yoursecret"\n```\n\nAll CLI capabilities are listed here:\n\n```bash\nscg -h\nusage: scg [-h] [--output_dir OUTPUT_DIR]\n           (--url_list [URL_LIST ...] | --uri_list [URI_LIST ...] | --track [TRACK] | --album [ALBUM] | --artist [ARTIST] | --saved-albums | --followed-artists)\n\noptions:\n  -h, --help            show this help message and exit\n  --output_dir OUTPUT_DIR\n                        output directory, defaults to current directory.\n  --url_list [URL_LIST ...]\n                        generates code with cover for list of URLs.\n  --uri_list [URI_LIST ...]\n                        generates code with cover for list of URIs.\n  --track [TRACK]       generates code with tracks album cover.\n  --album [ALBUM]       generates code with album cover.\n  --artist [ARTIST]     generates code with artist cover.\n  --saved-albums        Generates code with album for all saved albums. Requires OAuth login.\n  --followed-artists    Generates code with artist cover for 50 followed artists. Requires OAuth login.\n```\n',
    'author': 'schuenemann',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/tilschuenemann/spotifycodegen',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
