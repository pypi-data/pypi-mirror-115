from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='pretty-logic',
    version='1.0.1',
    packages=find_packages(exclude=['tests*']),
    license='MIT',
    description='A pretty logic library',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/aqeelat/pretty-logic.git',
    author='Abdullah Alaqeel',
    author_email='abdullah.t.aqeel@gmail.com',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)
