from setuptools import setup, find_packages
import pathlib

HERE = pathlib.Path(__file__).parent
README = (HERE / "README.md").read_text()

VERSION = '1.0.2'
DESCRIPTION = 'Random password generator'
LONG_DESCRIPTION = 'A package that allow to generate random passwords.'

# Setting up
setup(
    name="randompw-generator",
    version=VERSION,
    author="Saurav Raj",
    author_email="<saurav.raj5592@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=README,
    url='https://github.com/saurzv/randompw-generator',
    license='MIT',
    packages=find_packages(),
    install_requires=[],
    keywords=['python', 'random', 'password', 'generator', 'random password generator'],
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)