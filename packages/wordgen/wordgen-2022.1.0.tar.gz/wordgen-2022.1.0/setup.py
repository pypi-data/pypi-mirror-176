# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['wordgen']

package_data = \
{'': ['*'], 'wordgen': ['data/courses/*', 'data/words/*']}

install_requires = \
['appdirs>=1.4.4,<2.0.0', 'click>=8.1.3,<9.0.0', 'pyperclip>=1.8.2,<2.0.0']

entry_points = \
{'console_scripts': ['wordgen = wordgen.cli:cli']}

setup_kwargs = {
    'name': 'wordgen',
    'version': '2022.1.0',
    'description': 'Word training set generator for learning typing and improving your performance',
    'long_description': "# Word generator (for all you goddam keeb nerds 🤓)\n\n## The story\n\nI finally got some time on my hands to learn different layouts and Colemak is what interested me the most. At this point I was already familiar with Monkeytype, but it didn't provide proper learning tools. I looked around for an alternative, but other sites and tools were buggy, limited, too complicated or I wasn't able to find them.\n\nThis was my solution. `wordgen` generates (well, filters out really) curated word lists for you based on your demands. Just starting out? Focusing on just `arst` and `neio` might be more efficient. Want a specific word set? English or anything custom can be loaded in and used as a source for the generator. It even features a convenient `--copy` flag, which makes Monkeytype's ability to save texts almost useless (although their word randomisation is still awesome).\n\n## Installation\n\n<details>\n  <summary><b>from PyPi</b></summary>\n  \n  - *nix: `pipx install wordgen` or `python3 -m pip install wordgen`\n  - Win: `pipx install wordgen` or `python -m pip install wordgen`\n \n  > **Note**: May differ based on your installation\n</details>\n\n<details>\n  <summary><b>from source</b></summary>\n\n  If you want to do this, you can probably figure it out. If you can't, give me some time and I'll eventually rewrite this section to be more useful. (or someone can make a pr)\n</details>\n\n## Configuration\n\nAs of version `2022.0.1`, there isn't any config file, however, you can include your own custom [courses](src/wordgen/data/courses) and [wordsets](src/wordgen/data/words) in these paths:\n\n|          system | path                                                                                                       |\n|            ---: | :---                                                                                                       |\n|           Linux | `$XDG_CONFIG_HOME/.config/wordgen/<courses or words>/` (`$XDG_CONFIG_HOME` defaults to `~/.config/`)       |\n|          Mac OS | `~/Library/Preferences/wordgen/<courses or words>/`                                                        |\n| Win XP or older | `C:\\Documents and Settings\\<username>\\Local Settings\\Application Data\\octelly\\wordgen\\<courses or words>\\` |\n|  Win 7 or newer | `C:\\Users\\<username>\\AppData\\Roaming\\octelly\\wordgen\\<courses or words>\\`                                  |\n\n## Project versioning\n\n`year.breaking.minor`\n\n- `year` of release (this resets both `breaking` and `minor`)\n- goes up in case there's a `breaking` change (this resets `minor` back to 0)\n- `minor` goes up with each update\n\n## Credits\n\n- code by Octelly\n- the included English wordset is from here: https://gist.github.com/deekayen/4148741 \n",
    'author': 'Octelly',
    'author_email': 'eli@stefek.cz',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/Johnystar/wordgen',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
