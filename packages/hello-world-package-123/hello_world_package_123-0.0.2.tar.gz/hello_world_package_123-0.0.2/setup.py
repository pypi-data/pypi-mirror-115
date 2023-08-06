from setuptools import setup, find_packages


VERSION = '0.0.2'
DESCRIPTION = 'hello world package'
LONG_DESCRIPTION = 'hello world package long desc'

# Setting up
setup(
    name="hello_world_package_123",
    version=VERSION,
    author="idobn",
    author_email="<ido.bennatan@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[],
    keywords=['python', 'hello world'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)

