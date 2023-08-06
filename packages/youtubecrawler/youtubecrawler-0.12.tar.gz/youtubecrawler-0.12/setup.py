from setuptools import setup, find_packages
import codecs
import os

try:
    import pypandoc
    long_description = pypandoc.convert('README.md', 'rst')
    long_description = long_description.replace("\r","") # Do not forget this line
except OSError:
    print("Pandoc not found. Long_description conversion failure.")
    import io
    # pandoc is not installed, fallback to using raw contents
    with io.open('README.md', encoding="utf-8") as f:
        long_description = f.read()

VERSION = '0.12'
DESCRIPTION ="Youtube videos and channels scraper python wraper!"
LONG_DESCRIPTION = 'A package that allows you to scrap data from youtube videos and channel.'

# Setting up
setup(
    name="youtubecrawler",
    version=VERSION,
    author="KeinShin",
    author_email="<youtubecrawler@youtubecrawl.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=['youtubecrawler'],
    install_requires=['moviepy', 'requests_html', 'bs4','lxml','pytube'],
    keywords=['python', 'youtube', 'scraper', 'youtubevideodownload', 'channelscraper', 'youtubescraper'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)