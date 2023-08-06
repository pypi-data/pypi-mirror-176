from setuptools import setup, find_packages
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()


setup(
    name='jklint',
    version='0.0.1',
    description='A CLI designed to save time linting and validating Jenkinsfiles.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Aissa Laribi',
    author_email='aissalaribi@yahoo.fr',
    url='https://github.com/aissa-laribi/jklint',
    packages=find_packages('src'),
    package_dir={'':'src'},
    install_requires=['python-dotenv==0.21.0','coverage==6.5.0','requests==2.28.1'],
    entry_points={
        'console_scripts': [
            'jklint=cli:main',
            ]
        }
    )