"""Run "python setup.py install" to install pyjsonq."""

from setuptools import setup

try:
    with open('README.md') as f:
        long_description = f.read()

except Exception:
    long_description = """
    `pyjsonq` is a simple, elegant Python package to Query over any
    type of JSON Data. It'll make your life easier by giving the
    flavour of an ORM-like query on your JSON.

    More information at: https://github.com/s1s1ty/py-jsonq/.
"""


setup(name="pyjsonq",
      packages=['pyjsonq'],
      version='1.0.2',
      description="Query over Json file",
      long_description=long_description,
      long_description_content_type='text/markdown',
      classifiers=[
          'Development Status :: 4 - Beta',
          'Intended Audience :: Developers',
          'Natural Language :: English',
          'Operating System :: OS Independent',
          'Topic :: Software Development :: Libraries :: '
          'Python Modules',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 3',
      ],
      author='Shaonty Dutta',
      author_email='shaonty.dutta@gmail.com',
      license='MIT',
      url="https://github.com/s1s1ty/py-jsonq/",
      keywords=['Python', 'plugin'],
      include_package_data=True,
      zip_safe=False,
      setup_requires=['setuptools>=38.6.0'],
      )
