from setuptools import setup
import os.path

readme = os.path.join(os.path.dirname(__file__), 'README.md')
description = 'A CLI client and Python API library for the delighted platform.'

setup(
    name='delighted',
    packages=['delighted'],
    version='0.1',
    author='Jason Pearson',
    author_email='jason.d.pearson@gmail.com',
    description=description,
    long_description=open(readme).read(),
    license='MIT',
    keywords='delighted api',
    url='https://github.com/kaeawc/delighted-python/',
    download_url='https://github.com/kaeawc/delighted-python/tarball/0.1',
    py_modules=['delighted'],
    install_requires=['requests >= 0.13.2', 'docopt == 0.4.0'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License'
    ]
)
