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

description = (
    "`squircle.py` is a Python 3 utility for stretching discs/circles "
    "into squares and squishing squares into discs/circles"
)


setup(
    name="squircle",
    version="0.1",
    description=description,
    classifiers=CLASSIFIERS,
    license="MIT",
    install_requires=["numpy"],
    packages=find_packages(),
    py_modules=["squircle"],
    author="Boris Verkhovskiy",
    author_email="boris@verhovs.ky",
    url="https://github.com/verhovsky/squircle",
    test_suite="test",
)
