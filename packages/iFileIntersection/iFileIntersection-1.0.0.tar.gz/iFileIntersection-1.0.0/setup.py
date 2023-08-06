from distutils.core import setup

setup(
    name='iFileIntersection',
    version='1.0.0',
    packages=['intersection'],
    description="Holds the utility finding common integers between two files",
    long_description=open("README.md").read(),
    author='Nikhil K Madhusudhan (nikhilkmdev)',
    author_email='nikhilkmdev@gmail.com',
    maintainer='Nikhil K Madhusudhan (nikhilkmdev)',
    maintainer_email='nikhilkmdev@gmail.com',
    keywords=['intersection', 'huge', 'files', 'python3'],
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    requires=[],
)
