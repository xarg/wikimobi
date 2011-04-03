from setuptools import setup

setup(
    name='wikiepub',
    version='0.1',
    author="Alexandru Plugaru <alexandru.plugaru@gmail.com>",
    install_requires=['lxml', 'genshi'],
    entry_points={
        'console_scripts': [
            'wikiepub = wikiepub:main'
        ]
    }
)
