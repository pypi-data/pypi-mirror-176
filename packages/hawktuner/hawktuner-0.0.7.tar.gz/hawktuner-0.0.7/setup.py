import setuptools
# 若Discription.md中有中文 須加上 encoding="utf-8"
with open("Discription.md", "r",encoding="utf-8") as f:
    long_description = f.read()
    
setuptools.setup(
    name = "hawktuner",
    version = "0.0.7",
    author = "hawktorng",
    author_email="cool870427@gmail.com",
    description="ML DL tuner",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com",
    packages=['hawktuner'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6'
    )
