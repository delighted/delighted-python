from setuptools import setup

description = 'A CLI client and Python API library for the delighted platform.'

setup(
    name='delighted',
    packages=['delighted'],
    version='0.8',
    author='Jason Pearson',
    author_email='jason.d.pearson@gmail.com',
    description=description,
    license='MIT',
    keywords='delighted api',
    url='https://github.com/kaeawc/delighted-python/',
    download_url='https://github.com/kaeawc/delighted-python/archive/0.8.zip',
    py_modules=['delighted'],
    install_requires=['requests >= 0.13.2'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)
