from setuptools import setup, find_packages

CLASSIFIERS = [
    "Development Status :: 4 - Beta",
    "Environment :: Other Environment",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Operating System :: MacOS :: MacOS X",
    "Operating System :: POSIX",
    "Operating System :: Microsoft :: Windows",
    "Programming Language :: Python",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.6",
    "Programming Language :: Python :: 3.7",
    "Programming Language :: Python :: 3.8",
    "Programming Language :: Python :: 3 :: Only",
]

with open("README.md") as f:
    long_description = f.read()

setup(
    name="squircle",
    version="0.2.0",
    description="Stretch discs/circles into squares and squish squares into discs/circles",
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=CLASSIFIERS,
    license="MIT",
    install_requires=[],
    packages=find_packages(),
    py_modules=["squircle"],
    author="Boris Verkhovskiy",
    author_email="boris@verhovs.ky",
    url="https://github.com/verhovsky/squircle",
)
