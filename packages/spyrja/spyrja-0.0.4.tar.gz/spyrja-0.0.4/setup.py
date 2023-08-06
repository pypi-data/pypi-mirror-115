from setuptools import setup


def readme():
    with open('README.md') as f:
        return f.read()


setup(name='spyrja',
      version='0.0.4',
      description='Queryable collections of namedtuples',
      long_description=readme(),
      long_description_content_type='text/markdown',
      keywords='',
      url='http://gitlab.com/OldIronHorse/spyrja',
      author='Simon Redding',
      author_email='s1m0n.r3dd1ng@gmail.com',
      license='GPL3',
      packages=[
          'spyrja',
          ],
      scripts=[
          ],
      python_requires='>=3.7',
      install_requires=[
          ],
      test_suite='nose.collector',
      tests_require=['nose', 'nosy'],
      include_package_data=True,
      zip_safe=False)
