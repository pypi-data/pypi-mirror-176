import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="stx-logger-util",
    packages=setuptools.find_packages(),
    version="0.0.5",
    description="Library for a fast logger implementation.",
    author="Carlos A. Martínez Jiménez",
    author_email="carloxdev@gmail.com",
    url="https://github.com/carloxdev/logger-util",
    keywords=["logger", "logging", "python"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
)
