import setuptools

with open("README.md", "r", encoding="utf-8") as fhand:
    long_description = fhand.read()

setuptools.setup(
    name="shortier",
    version="1.1.0",
    author="Yash Kumar",
    author_email="yashkc2025@gmail.com",
    description="A Link shortener with support for various providers.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yashkc2025/shortier",
    project_urls={
        "Bug Tracker":"https://github.com/yashkc2025/shortier/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=["pyshorteners"],
    packages=setuptools.find_packages(),
    python_requires=">=3.7",
    entry_points={
        "console_scripts": [
            "shortier = shortier.cli:main",
        ]
    },
    
)