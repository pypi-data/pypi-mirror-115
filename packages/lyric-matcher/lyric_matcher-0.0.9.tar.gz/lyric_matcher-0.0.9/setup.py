import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="lyric_matcher",
    version="0.0.9",
    author="hanhaodi zhang, zhaoyang bu",
    author_email="1004591463@qq.com",
    description="README.md",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",              
    ],
)

