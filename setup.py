from setuptools import setup
setup(
    name = 'vbauto',
    version = '0.1.0',
    packages = ['vbauto'],
    entry_points = {
        'console_scripts': [
            'vbauto = vbauto.__main__:main'
        ]
    })
