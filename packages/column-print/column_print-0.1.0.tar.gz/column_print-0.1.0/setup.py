from setuptools import setup

with open('README.md', 'r') as fh:
    long_description = fh.read()

setup(
    name='column_print',
    version='0.1.0',
    author='Steve Daulton',
    author_email='steve.daulton@gmail.com',
    url='https://github.com/SteveDaulton/column_print',
    description='Terminal print strings in columns',
    long_description=long_description,
    long_description_content_type='text/markdown',
    py_modules=['column_print'],
    package_dir={'': 'src'},

    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'Intended Audience :: Other Audience',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Operating System :: POSIX :: Linux',
        'Operating System :: MacOS',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'License :: OSI Approved :: GNU General Public License v2 or later (GPLv2+)',
        'Topic :: Printing',
        'Topic :: Terminals',
        ],

    extras_require = {
        'dev': [
            'pylint>=2.4.4',
            'check-manifest>=0.40',
            'sphink>=1.3',
        ],
    },
    platforms=[
        'any',
        'Linux',
        'macos',
        'unix',
        'win32',
        'win64',
    ],
    license='GNU General Public License v2 or later (GPLv2+)',
)
