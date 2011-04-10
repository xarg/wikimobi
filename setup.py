from setuptools import setup

setup(
    name='wikimobi',
    version='0.1',
    author="Alexandru Plugaru <alexandru.plugaru@gmail.com>",
    entry_points={
        'console_scripts': [
            'wikimobi = wikimobi:main'
        ]
    }
)
