from distutils.core import setup
setup(
  name = 'rsfs',         # How you named your package folder (MyLib)
  packages = ['rsfs'],   # Chose the same as "name"
  version = '0.1',      # Start with a small number and increase it with every change you make
  license='cc by-nc-sa 4.0',        # Chose a license from here:
  # https://help.github.com/articles/licensing-a-repository
  description = 'Dimensionality Reduction using Random Subset Feature '
                'Selection algorithm.',   # Give a short description about
  # your library
  author = 'G.K.Sriharsha',                   # Type in your name
  author_email = 'gksriharsha@gmail.com',      # Type in your E-Mail
  url = 'https://github.com/gksriharsha/RSFS',   # Provide either the
  # link to your github or to your website
  download_url = 'https://github.com/gksriharsha/RSFS/archive/refs/tags/v_01.tar.gz',
  keywords = ['Dimensionality Reduction', 'Machine Learning', 'AI',
              'Feature Selection', 'Supervised Learning'],
  # Keywords
  # that define your package best
  install_requires=[
          'numpy',
          'scikit-learn',
          'scipy'
      ],
  classifiers=[
    'Development Status :: 5 - Production/Stable',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3',      #Specify which python
                                        # versions that you want to support
    'Programming Language :: Python :: 3.3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
  ],
)