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
    'version': '2022.0.0',
    'description': 'Word training set generator for learning typing and improving your performance',
    'long_description': "# Word generator (for all you goddam keeb nerds 🤓)\n\n## The story\n\nI was using this funny site to learn Colemak DHm and slowly started realising that the site was (and still is) nowhere near as funny as I thought and came to the conclusion that Monkeytype is signifficantly more funny. Here's the problem: the site was able to generate to generate different level words, such as only using finger keys, or adding adjacent keys to the mix (so like only using `arst` `neio` for example), but Monkeytype has no such feature.\n\nyeah anw this exists now, use it with custom mode in Monkeytype and you can get the ultimate training experience\n\n## Configuration\n\nYou can customise the script to your heart's content on the first few lines. I did not and do not plan on adding any interactive elements at this time, if I feel brave enough I might add command line arguments through Click at a later date (or maybe in just an hour or something idk).\n\ni forgor what i was typing about 💀\n\n## Project versioning\n\n`year.breaking.minor`\n\n- `year` of release\n- goes up in case there's a `breaking` change\n- `minor` goes up with each update\n\n## Credits\n\n- code by Octelly\n- top 1000 English words list source: https://gist.github.com/deekayen/4148741 (can be replaced with whatever else if script customisation for personal use like mentioned earlier :D)\n\n## have fun\n\nplease have fun please this code is perfect make sure to star ⭐🌟the 🌠repo ✨💫and 🤩*sus*cribe ඞ\n",
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
