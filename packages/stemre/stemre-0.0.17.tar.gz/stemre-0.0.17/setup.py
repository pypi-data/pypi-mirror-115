import setuptools

with open('README.md', 'r') as fh:
    long_description  =  fh.read()

setuptools.setup(
    name = 'stemre',
    version = '0.0.17',
    author = 'Stem Research',
    author_email = 'stemresearchs@gmail.com',
    description = 'Numerical analysis, simulation and data fitting in STEM',
    long_description = long_description,
    long_description_content_type = 'text/markdown',
    url = 'https://github.com/StemResearch/stemre',
    packages = setuptools.find_packages(),
    classifiers = [
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires = '>=3.6'
) 