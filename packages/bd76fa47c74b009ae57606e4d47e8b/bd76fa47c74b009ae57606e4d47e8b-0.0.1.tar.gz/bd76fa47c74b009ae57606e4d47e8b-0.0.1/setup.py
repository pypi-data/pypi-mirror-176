from setuptools import setup, find_packages

VERSION = '0.0.1'
DESCRIPTION = 'convert wav -> mp3'
LONG_DESCRIPTION = 'convert wav -> mp3 using ffmpeg preinstalled util'

# Setting up
setup(
    # the name must match the folder name 'verysimplemodule'
    name="bd76fa47c74b009ae57606e4d47e8b",
    version=VERSION,
    author="Alex Black",
    author_email="ku113p@gmail.com",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[],

    keywords=['python', 'first package', 'ffmpeg', 'wav', 'mp3', 'converter'],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Education",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
