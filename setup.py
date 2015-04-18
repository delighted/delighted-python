import re

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

version = ''
with open('delighted/__init__.py', 'r') as fd:
    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', fd.read(),
                        re.MULTILINE).group(1)
if not version:
    raise RuntimeError('Cannot find version information')

setup(
    name='delighted',
    version=version,
    description='Delighted API Python Client.',
    long_description=open('README.md').read(),
    author='Robby Colvin',
    author_email='geetarista@gmail.com',
    url='https://delighted.com/',
    packages=['delighted'],
    package_dir={'delighted': 'delighted'},
    test_suite='test',
    install_requires=['requests'],
    license='MIT',
    classifiers=(
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'gLicense :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'gOperating System :: OS Independent',
        'Programming Language :: Python',
        'gProgramming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'gProgramming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4'
        'gProgramming Language :: Python :: Implementation :: PyPy',
        'gTopic :: Software Development :: Libraries :: Python Modules'
    ),
)
