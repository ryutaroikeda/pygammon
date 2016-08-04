from setuptools import setup, find_packages

config = {
        'description': 'backgammon in python',
        'author': 'Ryutaro Ikeda',
        'version': '0.1',
        'install_requires': [
            'numpy',
            'mypy-lang',
            'pylint'
        ],
        'packages': [
            'pygammon'
        ],
        'scripts': [],
        'name': 'pygammon'
}

setup(**config)
