from setuptools import setup, find_packages

VERSION = '0.0.2'
DESCRIPTION = "Package to calculate the word exclusion rate"
LONG_DESCRIPTION = 'A package that allows to calculate the percentage of words excluded from the reference during machine translation .'

# Setting up
setup(
    name="word exclusion rate",
    version=VERSION,
    author="NIel George Varghese",
    author_email="<ngvennasseril@gmail.com>",
    description=DESCRIPTION,
    packages=find_packages(),
    # install_requires=['Counter'],
    keywords=['python', 'machine translation', 'benchmarking', 'OCR'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)