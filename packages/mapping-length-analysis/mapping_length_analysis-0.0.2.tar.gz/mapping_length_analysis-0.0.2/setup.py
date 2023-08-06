from setuptools import setup

# This call to setup() does all the work
setup(
    name="mapping_length_analysis",
    version="0.0.2",
    description="Analyse number of raw and mapped reads by length",
    #long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/Delayed-Gitification/mapping_length_analysis.git",
    author="Oscar Wilkins",
    author_email="oscar.wilkins@crick.ac.uk",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["mapping_length_analysis"],
    include_package_data=True,
    install_requires=["pandas", "dnaio", "pysam"],
    entry_points={
        "console_scripts": [
            "mapping_length_analysis=mapping_length_analysis.__main__:main",
        ]
    },
)