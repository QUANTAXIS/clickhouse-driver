import os
import re
from codecs import open

from setuptools import setup, find_packages
from distutils.extension import Extension

try:
    from Cython.Build import cythonize
except ImportError:
    USE_CYTHON = False
else:
    USE_CYTHON = True


here = os.path.abspath(os.path.dirname(__file__))


def read_version():
    regexp = re.compile(r'^VERSION\W*=\W*\(([^\(\)]*)\)')
    init_py = os.path.join(here, 'clickhouse_driver', '__init__.py')
    with open(init_py, encoding='utf-8') as f:
        for line in f:
            match = regexp.match(line)
            if match is not None:
                return match.group(1).replace(', ', '.')
        else:
            raise RuntimeError(
                'Cannot find version in clickhouse_driver/__init__.py'
            )


with open(os.path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

# Prepare extensions.
ext = '.pyx' if USE_CYTHON else '.c'
extensions = [
    Extension(
        'clickhouse_driver.bufferedreader',
        ['clickhouse_driver/bufferedreader' + ext]
    ),
    Extension(
        'clickhouse_driver.columns.stringcolumn',
        ['clickhouse_driver/columns/stringcolumn' + ext]
    )
]

if USE_CYTHON:
    extensions = cythonize(
        extensions, compiler_directives={'language_level': '3'}
    )


setup(
    name='clickhouse-driver',
    version=read_version(),

    description='Python driver with native interface for ClickHouse',
    long_description=long_description,

    url='https://github.com/mymarilyn/clickhouse-driver',

    author='Konstantin Lebedev',
    author_email='kostyan.lebedev@gmail.com',

    license='MIT',

    classifiers=[
        'Development Status :: 4 - Beta',


        'Environment :: Console',


        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',


        'License :: OSI Approved :: MIT License',


        'Operating System :: OS Independent',


        'Programming Language :: SQL',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: Implementation :: PyPy',

        'Topic :: Database',
        'Topic :: Software Development',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Scientific/Engineering :: Information Analysis'
    ],

    keywords='ClickHouse db database cloud analytics',

    packages=find_packages('.', exclude=['tests*']),
    python_requires='>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*',
    install_requires=[
        'pytz',
        'enum34; python_version<"3.4"',
        'ipaddress; python_version<"3.4"',
    ],
    ext_modules=extensions,
    extras_require={
        'lz4': ['lz4', 'clickhouse-cityhash>=1.0.2.1'],
        'zstd': ['zstd', 'clickhouse-cityhash>=1.0.2.1']
    },
    test_suite='nose.collector',
    tests_require=[
        'nose',
        'mock',
        'freezegun',
        'lz4',
        'zstd',
        'clickhouse-cityhash>=1.0.2.1'
    ],
)
