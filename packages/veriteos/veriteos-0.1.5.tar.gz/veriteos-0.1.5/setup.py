from setuptools import setup, find_packages

VERSION = '0.1.5'
DESCRIPTION = 'Veriteos sentinel events registry'
LONG_DESCRIPTION = 'A package that allows to build simple streams of video, audio and camera data.'

setup(
    name="veriteos",
    version=VERSION,
    author="Veriteos Dev Team",
    author_email="<admin@veriteos.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['marshmallow', 'requests'],
    keywords=['python', 'veriteos', 'veriteos client', 'veriteos events register'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',  
)