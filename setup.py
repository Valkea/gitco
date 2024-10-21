from setuptools import setup, find_packages
from gitco import __version__

setup(
    name='gitco',
    version=__version__,

    install_requires=[
        'instructor',
        'openai',
        'requests',
        'python-dotenv',
    ],

    url='https://github.com/Valkea/gitco',
    author='Emmanuel Letremble (Valkea)',
    author_email='gitco@shedge.com',

    packages=find_packages()
)

