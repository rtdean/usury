from setuptools import setup, find_packages

with open('README.rst') as fp:
    readme = fp.read()

setup(
    name='usury',
    version='0.1',
    description='Python interest calculation library',
    long_description=readme,
    license='Apache 2.0',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Topic :: Office/Business :: Financial',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    author='Ryan T. Dean',
    author_email='rtdean@cytherianage.net',
    url='https://github.com/rtdean/usury',
    keywords='usury interest',

    packages=find_packages(),
    package_data={
        '': ['LICENSE'],
    },
    include_package_data=True,

    install_requires=[],
    tests_require=[],
)
