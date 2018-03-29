from setuptools import setup, find_packages

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name='playlist_souffle',
    description='backend API for playlist_souffle',

    author='Zach Hammer',
    author_email='zach.the.hammer@gmail.com',
    url='https://github.com/zhammer/playlist-souffle',

    install_requires=requirements,
    packages=find_packages(where='src'),
    package_dir={'':'src'}
)
