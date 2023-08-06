import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="xlsxreader",
    version="0.0.3",
    author="Michael Brine",
    author_email="mbrine0@gmail.com",
    description="test xlsxreader",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/michael-brine/xlsxreader",
    project_urls={
        "Bug Tracker": "https://github.com/michael-brine/xlsxreader",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)