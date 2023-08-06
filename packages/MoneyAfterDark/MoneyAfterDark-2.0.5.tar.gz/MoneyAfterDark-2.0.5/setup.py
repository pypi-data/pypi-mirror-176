from setuptools import setup, find_packages
setup(
name = 'MoneyAfterDark',
packages = find_packages(exclude=['test']),
version = '2.0.3',
author = 'NeuroscienceAfterDark',
author_email = 'neuroscience@sigmund.science',
description = 'Business, Finance and Universal Tax Tools. UK Specific Tax Tools also Included',
url = 'https://github.com/NeuroscienceAfterDark/MoneyAfterDark',
install_requires=['pandas',
                  'numpy',
                  'plotly',
                  'datetime'],
classifiers = ['Programming Language :: Python :: 3',
               'License :: OSI Approved :: MIT License',
               'Operating System :: OS Independent',
               ],
)