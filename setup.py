import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()


setuptools.setup(
    name="app-store-notifications-v2-validator",
    version="0.0.8",
    author="Rick Wierenga",
    author_email="rick_wierenga@icloud.com",
    description="AppStore notifications v2 Validator",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/rickwierenga/app-store-notifications-v2-validator",
    project_urls={
        "Bug Tracker": "https://github.com/rickwierenga/app-store-notifications-v2-validator/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=setuptools.find_packages(),
    python_requires=">=3.6",
    install_requires=[
        "cffi>=1.15.1",
        "cryptography>=40.0.2",
        "pycparser>=2.21",
        "PyJWT>=2.7.0",
        "pyOpenSSL>=23.1.1"
    ]
)
