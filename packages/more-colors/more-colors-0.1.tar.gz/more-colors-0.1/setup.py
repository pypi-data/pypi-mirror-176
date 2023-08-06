from setuptools import setup, find_packages


setup(
    name='more-colors',
    version='0.1',
    license='MIT',
    author="Abdel Kitu",
    author_email='feuclegay@gmail.com',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    url='https://giybf.com',
    keywords='example project',
    install_requires=[
          'scikit-learn',
      ],

)