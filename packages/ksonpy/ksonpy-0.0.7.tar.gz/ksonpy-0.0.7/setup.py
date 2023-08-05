import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ksonpy",
    version="0.0.7",
    author="Jacob Brazeal",
    author_email="jacob.brazeal@gmail.com",
    description="KSON is JSON with embedded SQL and networking",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/jacob.brazeal/ksonpy",
    project_urls={
        "Bug Tracker": "https://gitlab.com/jacob.brazeal/ksonpy/-/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "ksonpy"},
    packages=setuptools.find_packages(where="ksonpy"),
    python_requires=">=3.8",
    install_requires=[
        'requests',
    ],
    entry_points = {
        'console_scripts': ['kson=ksonpy.cmd_line:main'],
    }


)
