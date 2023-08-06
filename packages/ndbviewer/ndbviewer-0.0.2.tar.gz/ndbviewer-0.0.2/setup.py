import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ndbviewer",
    version="0.0.2",
    author="Brandon Wegner",
    author_email="brandon.wegner@reddingsoftware.com",
    description="This module allows you to view local data from your Google Cloud NDB projects using thee Google Datastore Emulator.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ReddingSoftware/Google_NDB_Emulator",
    project_urls={
        "Bug Tracker": "https://github.com/ReddingSoftware/Google_NDB_Emulator/issues",
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