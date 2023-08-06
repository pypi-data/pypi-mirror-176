from setuptools import setup

# read the contents of README file
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
  name = 'python-snookerbot',         
  packages=['snookerbot', 'snookerbot.models', 'snookerbot.endpoints'],
  version = '1.0.0',
  license='GPL-3.0-or-later',
  description = 'Snookerbot',
  long_description=long_description,
  long_description_content_type='text/markdown',
  author = 'Alexander Schillemans',
  author_email = 'alexander.schillemans@hotmail.com',
  url = 'https://github.com/alexander-schillemans/python-snookerbot',
  download_url = 'https://github.com/alexander-schillemans/python-snookerbot/archive/refs/tags/1.0.0.tar.gz',
  keywords = ['snooker', 'snooker.org', 'bot', 'snookerbot', 'api'],
  install_requires=[
          'requests',
          'python-dateutil'
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
    'Programming Language :: Python :: 3.10',
  ],
)