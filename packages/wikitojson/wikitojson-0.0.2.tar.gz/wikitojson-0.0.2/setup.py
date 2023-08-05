import setuptools

with open("readme.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="wikitojson",
    version="0.0.2",
    author="Klaifer Garcia",
    description="Wikipedia(English) to json",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Klaifer/wikitojson",
    packages=[],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    py_modules=["wikitojson"],
    package_dir={'':'wikitojson/src'},
    install_requires=[]
)