import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()


setuptools.setup(
    name="hei-textpreprocessor",
    version="0.0.1",
    author="Angeliki Kouka",
    author_email="akouka@heijmans.nl",
    description="A simple python wrapper for usual text tasks (preprocessing, tokenization, and vectorization.)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"), #, exclude=["tests"]
    python_requires=">=3.7",
    install_requires=[
        "spacy>=3.4.2",
        "nltk>=3.7",
        "pandas>=1.5.1",
        "deep_translator>=1.8",
        "tokenizers>=0.12.1",
        "sklearn>=1.1.3"
    ],
    test_suite="tests",
)