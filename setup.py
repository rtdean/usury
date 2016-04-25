from setuptools import setup, find_packages

setup(
    name='usury',
    version='0.1',
    description='',
    long_description='',
    license='Apache 2.0',
    classifiers=[
        'Programming Language :: Python',
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Topic :: Office/Business :: Financial',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    author='Ryan T. Dean',
    author_email='rtdean@cytherianage.net',
    url='',
    keywords='usury interest',

    packages=find_packages(),
    package_data={
        '': ['LICENSE'],
    },
    include_package_data=True,

    install_requires=[],
    tests_require=[],
)
