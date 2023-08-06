from setuptools import setup, find_packages

VERSION = '0.1.1'
DESCRIPTION = 'A small package to access and use WarcraftLogs API'
LONG_DESCRIPTION = 'A small package that can use the WarcraftLogs api and from there call function to retrive data fram WarcraftLogs'

setup (
    name= 'ReunionLog',
    version= VERSION,
    author= 'nickgismokato',
    author_email= 'nickvillumlaursen@gmail.com',
    packages= find_packages(),
    license= 'LICENCE.txt',
    description= DESCRIPTION,
    long_description= LONG_DESCRIPTION,
    install_requires=[
        "gql-query-builder >= 0.1.7",
    ],
    keywords= ['python', 'WarcraftLogs-API', 'package'],
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: End Users/Desktop",
        "Intended Audience :: Other Audience",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)