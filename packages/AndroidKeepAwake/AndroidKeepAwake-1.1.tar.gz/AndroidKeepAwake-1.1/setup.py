import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="AndroidKeepAwake",  # Replace with your own username
    version="1.1",
    author="ziyaad30",
    author_email="xavier.baatjes@outlook.com",
    description="Keep you Android device awake when your application is running.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ziyaad30/AndroidKeepAwake",
    project_urls={
        "Bug Tracker": "https://github.com/ziyaad30/AndroidKeepAwake/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.8",
)
