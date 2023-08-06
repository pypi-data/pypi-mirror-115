from setuptools import setup

GITHUB_URL = 'https://github.com/Pinkers/offgas'

exec(open('offgas/_version.py').read())

# Long description to be published in PyPi
LONG_DESCRIPTION = """
**offgas** is a Python interface to the USB CO2 monitor with monitoring and
logging tools for fermentation. Based on co2meter package from Valdimir Fillanov,
but with updates for offgas measurement in R&D fermentation context.
"""

setup(name='offgas',
      version=__version__,
      description='Python interface to the USB CO2 monitor',
      long_description=LONG_DESCRIPTION,
      url=GITHUB_URL,
      download_url=GITHUB_URL + '/archive/v%s.zip' % (__version__),
      author='Aaron Kirby',
      author_email='aaronkirby2000@gmail.com',
      license='MIT License',
      packages=['offgas'],
      install_requires=['hidapi', 'future', 'pandas'],
      include_package_data=True,
      zip_safe=False,
      classifiers=['Programming Language :: Python :: 3', ]
      )
