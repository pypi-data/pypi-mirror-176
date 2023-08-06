from distutils.core import setup
setup(
  name = 'bhpy',
  packages = ['bhpy'],
  version = '0.0.2',
  license='MIT',
  description = "Python bindings to use Becker & Hickls' hardware control dll and API",
  author = 'Marscheck',
  author_email = 'marscheck@becker-hickl.de',
  url = 'https://www.becker-hickl.com/',
  download_url = 'https://github.com/user/reponame/archive/v_01.tar.gz', # I get to this in a second
  keywords = ['FLIM', 'Fluorescence lifetime', 'TCSPC', 'photon counting', 'BH', 'Becker&Hickl', 'molecular imaging', 'SPC', 'SPCM'],
  install_requires=[],
  classifiers=[
    'Development Status :: 3 - Alpha', # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Science/Research',
    'Intended Audience :: Developers',
    'Intended Audience :: Healthcare Industry'
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
    'Programming Language :: Python :: 3.10',
    'Programming Language :: Python :: 3.11',
  ],
)