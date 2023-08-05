from setuptools import setup
from pathlib import Path

root = Path(__file__).parent
readme = (root / "README.md").read_text()

setup(name='certtool',
      version='0.2.0',
      description='Easily check certificate status of domains',
      long_description=readme,
      long_description_content_type="text/markdown",
      url='https://sr.ht/~martijnbraam/certtool',
      author='Martijn Braam',
      author_email='martijn@brixit.nl',
      packages=['certtool'],
      classifiers=[
          'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
      ],
      install_requires=[
            'pyopenssl',
            'colorama',
      ],
      entry_points={
          'console_scripts': ['cert=certtool.__main__:main'],
      })