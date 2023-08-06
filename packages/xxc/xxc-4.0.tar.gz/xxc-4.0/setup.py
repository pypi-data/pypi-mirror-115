import setuptools

with open('README.md', 'r') as f:
    long_description = f.read()

setuptools.setup(
    name="xxc",
    version="4.0",
    author="Federico Rizzo",
    author_email="synestem@ticATgmail.com",
    description="Tools for automating command execution",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/synestematic/xxc",
    license="MIT",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3 :: Only",
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
        "Operating System :: MacOS :: MacOS X",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Utilities",
    ],
    install_requires=[
        # "bestia>=4.0",
    ],
)
