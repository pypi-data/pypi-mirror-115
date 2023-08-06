import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="YT_comments_scrapper",
    version="0.3",
    author="Linda Oranya",
    author_email="oranyalinda7@gmail.com",
    description="YouTube comments scrapper",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/linda-oranya/YT_comments_scrapper",
    project_urls={
        "Bug Tracker": "https://github.com/linda-oranya/YT_comments_scrapper/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    py_modules=["yt_scrapper"],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)