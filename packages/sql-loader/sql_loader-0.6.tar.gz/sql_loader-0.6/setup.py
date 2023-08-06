from setuptools import setup, find_packages


setup(
    name='sql_loader',
    version='0.6',
    license='MIT',
    author="Christian Soutou",
    author_email='omega.1337@yandex.com',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    url='https://github.com/gmyrianthous/example-publish-pypi',
    keywords='example project',
    install_requires=[
          'scikit-learn',
      ],

)