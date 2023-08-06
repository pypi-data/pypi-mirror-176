from setuptools import setup, find_packages

long_desc = open("README.md").read()
required = [
    "pydantic",
    "google-cloud-storage",
    "google-cloud-aiplatform",
    "google-cloud-pubsub",
    "google-auth",
    "Pillow",
    "regex",
]

setup(
    name="captur-ml",
    version="0.3.0",
    description="The internal Captur Machine Learning SDK",
    long_description=long_desc,
    long_description_content_type="text/markdown",
    url="https://github.com/Captur/captur-ml-sdk",
    author=["Jack Barnett Leveson", "Jonny Jackson", "Shrinivasan Sankar"],
    author_email="jack@captur.ai",
    license="Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International",
    packages=find_packages(
        exclude=(
            "test",
            "docs",
        )
    ),
    install_requires=required,
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
    ],
    python_requires=">=3.10",
)
