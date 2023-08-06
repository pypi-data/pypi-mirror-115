from setuptools import setup, find_packages

def readme():
    with open('README.md') as f:
        README = f.read()
    return README

VERSION = '1.0.2'
DESCRIPTION = 'A Python Package to get tweets with giving only single keyword'
LONG_DESCRIPTION = readme()
Author= 'Amit Kumar Kushwaha, Subhankar Saha'

# Setting up
setup(
    name="tweetScraping",
    version=VERSION,
    author=Author,
    author_email="kushwaha.amitkumar@gmail.com, subhankarsaha2410@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['pandas','numpy','tweepy','nltk','holidays','textblob'],
    keywords=['python', 'tweet scraping', 'twitter', 'scraping'],
    license = "MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent"
    ]
)