from setuptools import setup, find_packages
import io

def read_all(f):
    with io.open(f, encoding="utf-8") as I:
        return I.read()
    
requirements = list(map(str.strip, open("requirements.txt").readlines()))
    
setup(
    name='gears-cli',
    version='1.1.0',
    description='RedisGears cli',
    long_description=read_all("README.md"),
    long_description_content_type='text/markdown',
    url='https://github.com/RedisGears/gears-cli',
    packages=find_packages(),
    install_requires=requirements,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 3.7',
        'Topic :: Database'
    ],
    keywords='RedisGears CLI',
    author='RedisLabs',
    author_email='oss@redislabs.com',
    entry_points='''
        [console_scripts]
        gears-cli=gears_cli.__main__:main
    '''
)
