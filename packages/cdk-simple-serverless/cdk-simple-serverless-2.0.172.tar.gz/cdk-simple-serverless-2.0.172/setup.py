import json
import setuptools

kwargs = json.loads(
    """
{
    "name": "cdk-simple-serverless",
    "version": "2.0.172",
    "description": "CDK Constructs for Serverless Demo",
    "license": "Apache-2.0",
    "url": "https://github.com/pahud/cdk-simple-serverless.git",
    "long_description_content_type": "text/markdown",
    "author": "Pahud Hsieh<pahudnet@gmail.com>",
    "bdist_wheel": {
        "universal": true
    },
    "project_urls": {
        "Source": "https://github.com/pahud/cdk-simple-serverless.git"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "cdk_simple_serverless",
        "cdk_simple_serverless._jsii"
    ],
    "package_data": {
        "cdk_simple_serverless._jsii": [
            "cdk-simple-serverless@2.0.172.jsii.tgz"
        ],
        "cdk_simple_serverless": [
            "py.typed"
        ]
    },
    "python_requires": "~=3.7",
    "install_requires": [
        "aws-cdk-lib>=2.1.0, <3.0.0",
        "constructs>=10.0.5, <11.0.0",
        "jsii>=1.71.0, <2.0.0",
        "publication>=0.0.3",
        "typeguard~=2.13.3"
    ],
    "classifiers": [
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: JavaScript",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Typing :: Typed",
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved"
    ],
    "scripts": []
}
"""
)

with open("README.md", encoding="utf8") as fp:
    kwargs["long_description"] = fp.read()


setuptools.setup(**kwargs)
