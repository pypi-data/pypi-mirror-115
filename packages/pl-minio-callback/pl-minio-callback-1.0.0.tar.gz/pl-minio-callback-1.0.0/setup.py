import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pl-minio-callback",
    version="1.0.0",
    author="Daniel Garcia Pulpeiro",
    author_email="danielgarciapulpeiro@gmail.com",
    description="Callback prepared to log checkpoints to minio server.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/dpulpeiro/pl-minio-callback",
    project_urls={
        "Bug Tracker": "https://github.com/dpulpeiro/pl-minio-callback/issues",

    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: System :: Logging",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)