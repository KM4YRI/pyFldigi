'''A setuptools based setup module.

See:
https://packaging.python.org/en/latest/distributing.html
https://github.com/pypa/sampleproject
'''

from setuptools import setup
from setuptools import find_packages
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(name='pyfldigi',
      version='0.3',
      description='Python library to control FLDIGI via XML-RPC',
      long_description=long_description,
      url='https://github.com/KM4YRI/pyFldigi',
      author='KM4YRI',
      author_email='km4yri@gmail.com',
      license='License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
      classifiers=[  # https://pypi.python.org/pypi?%3Aaction=list_classifiers
                   'Development Status :: 3 - Alpha',
                   'Environment :: Console',
                   'Intended Audience :: Developers',
                   'Intended Audience :: Science/Research',
                   'Intended Audience :: Telecommunications Industry',
                   'Topic :: Software Development :: Build Tools',
                   'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
                   'Natural Language :: English',
                   'Operating System :: POSIX :: Linux',
                   'Operating System :: Microsoft :: Windows',
                   'Operating System :: MacOS :: MacOS X',
                   'Programming Language :: Python :: 3',
                   'Programming Language :: Python :: 3.2',
                   'Programming Language :: Python :: 3.3',
                   'Programming Language :: Python :: 3.4',
                   'Programming Language :: Python :: 3.5',
                   'Programming Language :: Python :: 3.6',
                   'Topic :: Communications :: Ham Radio'],
      keywords='fldigi ham radio hf digital cw morse rtty olivia psk ssb sdr',
      packages=find_packages(),
      install_requires=[],
      zip_safe=False)
