import os
from setuptools import setup

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "hstream",
    version = "0.0.4",
    author = "Conrad Bezuidenhout",
    author_email = "conradbez1@gmail.com",
    description = ("Create python webapps with ease"),
    license = "BSD",
    keywords = "streamlit htmx fastapi",
    url = "http://packages.python.org/hyperstream",
    packages=['hyperstream'],
    long_description=read('README'),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: BSD License",
    ],
    install_requires=[
        'fastapi~=0.85',
        'uvicorn~=0.19',
        'watchfiles~=0.18',
        'Jinja2~=3.1',
        'Markdown~=3.4',
        'yattag~=1.14',
        'starlette_context==0.3.4',
    ],
    entry_points={"console_scripts": ["hstream = hyperstream.runner:run"]},

)