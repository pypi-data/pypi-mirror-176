from setuptools import setup, find_packages


setup(
    name='sql_database_manager',
    version='0.6',
    license='MIT',
    author="Giorgos Myrianthous",
    author_email='email@example.com',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    url='https://github.com/gmyrianthous/example-publish-pypi',
    keywords='database_management',
    install_requires=[
          'scikit-learn',
      ],

)