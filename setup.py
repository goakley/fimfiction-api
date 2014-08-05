from distutils.core import setup

setup(
    name='FimFiction',
    version='0.0.0',
    author='',
    author_email='',
    packages=['fimfiction'],
    scripts=[],
    url='https://github.com/alanjcastonguay/fimfiction-api',
    license='LICENSE.txt',
    description='API to access FimFiction.net from a Reader\'s perspective',
    long_description=open('README.rst').read(),
    requires=[
        'beautifulsoup4 (>=4.0.0)'
    ],
)
