from setuptools import setup, find_packages


setup(
    name='pyharvester',
    version='1.0',
    license='MIT',
    author="N",
    author_email='dev@0x04.xyz',
    packages=find_packages(),
    package_data={
        '': ['*'],
    },
    url='https://github.com/0xNev/PyCaptcha',
    keywords='',
    install_requires=[
          'selenium==4.1.5',
          'webdriver-manager==3.7.1'
      ],

)