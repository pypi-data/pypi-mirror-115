import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="sentimentAnalysisPkg",
    version="0.0.3",
    author="Example Author",
    author_email="author@example.com",
    description="package to perform sentiment analysis on financial social media posts",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/p-hiroshige/sentimentAnalysis.git",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)