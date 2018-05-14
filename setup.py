"""Run "python setup.py install" to install dhash."""

try:
    from setuptools import setup, Extension
except ImportError:
    from distutils.core import setup, Extension

with open('README.md') as f:
    long_description = f.read()


setup(name="pyjsonq",
      packages=['pyjsonq'],
      version='0.1',
      description="Query over Json file",
      long_description=long_description,
      classifiers=[
          'Development Status :: 1 - Alpha',
          'Intended Audience :: Developers',
          'Natural Language :: English',
          'Operating System :: OS Independent',
          'Topic :: Software Development :: Libraries :: '
          'Python Modules',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.3',
          'Programming Language :: Python :: 3.4',
          'Programming Language :: Python :: 3.5',
          'Programming Language :: Python :: 3.6',
      ],
      author='Shaonty Dutta',
      author_email='shaonty.dutta@gmail.com',
      license='MIT',
      url="https://github.com/s1s1ty/py-jsonq/",
      keywords=['Python', 'plugin'],
      include_package_data=True,
      zip_safe=False,
      )
