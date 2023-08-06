from setuptools import setup, find_packages

name = 'shallow'
version = '0.0.10' # current = 0.0.9

with open('README.md' ,'r') as f:
    long_description = f.read().strip()

setup(
    name=name,
    version=version,
    description=name,
    long_description=long_description,
    long_description_content_type='text/markdown',
    url=f'https://github.com/mdmould/{name}',
    author='Matthew Mould',
    author_email='mattdmould@gmail.com',
    license='MIT',
    packages=find_packages(),
    install_requires=[
	'nflows',
	'torch',
        'tensorflow',
        'tensorflow-probability',
        ],
    python_requires='>=3.7',
    )

