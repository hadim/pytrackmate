from setuptools import setup
from setuptools import find_packages

with open('README.md') as f:
    long_description = f.read()

setup(author='Hadrien Mary',
      author_email='hadrien.mary@gmail.com',
      url='https://github.com/hadim/pytrackmate/',
      description='Import Trackmate XML files in Python as Pandas dataframe.',

      long_description=long_description,
      long_description_content_type='text/markdown',

      install_requires=["numpy", "pandas"],

      packages=find_packages(),

      classifiers=['Development Status :: 5 - Production/Stable',
                   'Intended Audience :: Developers',
                   'Natural Language :: English',
                   'License :: OSI Approved :: BSD License',
                   'Operating System :: OS Independent',
                   'Programming Language :: Python',
                   'Programming Language :: Python :: 3',
                   ])
