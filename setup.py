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
    author='Ben Turner, Robby Colvin',
    author_email='ben@delighted.com',
    url='https://delighted.com/',
    packages=['delighted'],
    package_dir={'delighted': 'delighted'},
    install_requires=['six', 'requests', 'tzlocal'],
    test_suite='test',
    test_requires=['mock', 'pytz', 'tzlocal'],
    license='MIT',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
)
