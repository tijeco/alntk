from setuptools import setup

setup(
    name='alntk',
    py_modules=['alntk'],
    entry_points='''
        [console_scripts]
        alntk=pkg.alntk:run
    ''',
    packages=['pkg'],
)