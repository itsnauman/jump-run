from setuptools import setup

setup(
    name='jumprun',
    version='0.1',
    py_modules=['jumprun'],
    description='CLI app for running python scripts from any directory'
                ' in terminal',
    url='http://github.com/itsnauman/jumprun',
    author='Nauman Ahmad',
    author_email='nauman-ahmad@outlook.com',
    license='MIT',
    include_package_data=True,
    install_requires=[
        'termcolor',
        'docopt',
    ],
    entry_points='''
        [console_scripts]
        jr=jumprun:main
    ''',
)
