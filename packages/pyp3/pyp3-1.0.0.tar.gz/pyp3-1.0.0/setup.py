from setuptools import setup, find_packages
setup(
    name='pyp3',
    version='1.0.0',
    author='Elisha Hollander',
    author_email='just4now666666@gmail.com',
    description="Pyp is a linux command line text manipulation tool similar to awk or sed, but which uses standard python string and list methods as well as custom functions evolved to generate fast results in an intense production environment.",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url='https://github.com/donno2048/pyp3',
    project_urls={
        'Documentation': 'https://github.com/donno2048/pyp3#readme',
        'Bug Reports': 'https://github.com/donno2048/pyp3/issues',
        'Source Code': 'https://github.com/donno2048/pyp3',
    },
    python_requires='>=3.0',
    packages=find_packages(),
    classifiers=['Programming Language :: Python :: 3'],
    entry_points={ 'console_scripts': [ 'pyp3=pyp3.__main__:main' ] }
)
