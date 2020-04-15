from setuptools import setup, find_packages
setup(
    name='gears-cli',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'redis'
    ],
    entry_points='''
        [console_scripts]
        gears-cli=gears_cli.__main__:main
    '''
)