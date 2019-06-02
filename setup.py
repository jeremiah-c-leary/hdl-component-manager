from setuptools import setup
from setuptools import find_packages


def readme():
    with open('README.rst') as f:
        return f.read()


setup(
  name='hcm',
  version='0.4',
  description='HDL Component Manager',
  long_description=readme(),
  classifiers=[
      'Development Status :: 2 - Pre-Alpha',
      'Environment :: Console',
      'Programming Language :: Python :: 3',
      'Intended Audience :: End Users/Desktop',
      'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
      'Natural Language :: English',
      'Operating System :: POSIX :: Linux',
      'Topic :: System :: Archiving :: Packaging'
  ],
  url='https://github.com/jeremiah-c-leary/hdl-component-manager',
  download_url='https://github.com/jeremiah-c-leary/hdl-component-manager',
  author='Jeremiah C Leary',
  author_email='jeremiah.c.leary@gmail.com',
  license='GNU General Public License',
  packages=find_packages(),
  zip_safe=False,
  test_suite='nose.collector',
  tests_require=['nose'],
  keywords=['vhdl', 'verilog', 'packager', 'configuration management'],
  entry_points={
    'console_scripts': [
      'hcm = hcm.__main__:main'
    ]
  }
)
