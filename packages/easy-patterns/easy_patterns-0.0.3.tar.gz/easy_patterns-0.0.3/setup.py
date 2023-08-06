from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup (
    name='easy_patterns',
    version='0.0.3',
    description='A basic demonstrator for teaching design patterns.',
    py_modules=["trafficlight_statemachine", "car_statemachine", "crosswalk"],
    package_dir={'':'src'}, 
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    url="https://github.com/khelsabeck/easy_patterns.git",
    download_url = 'https://github.com/khelsabeck/easy_patterns/archive/refs/tags/easy_patterns0.0.2.tar.gz',
    author="Keith Helsabeck",
    author_email="admin@mylawdb.com",
)
