import json
import setuptools

kwargs = json.loads(
    """
{
    "name": "mikeapted-myconstruct",
    "version": "0.1.0",
    "description": "my-construct",
    "license": "MIT",
    "url": "https://www.github.com/mikeapted/my-construct.git",
    "long_description_content_type": "text/markdown",
    "author": "Mike Apted<hello@me.com>",
    "bdist_wheel": {
        "universal": true
    },
    "project_urls": {
        "Source": "https://www.github.com/mikeapted/my-construct.git"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "mikeapted_myconstruct",
        "mikeapted_myconstruct._jsii"
    ],
    "package_data": {
        "mikeapted_myconstruct._jsii": [
            "my-construct@0.1.0.jsii.tgz"
        ],
        "mikeapted_myconstruct": [
            "py.typed"
        ]
    },
    "python_requires": ">=3.6",
    "install_requires": [
        "aws-cdk.aws-apigateway==1.116.0",
        "aws-cdk.aws-lambda==1.116.0",
        "aws-cdk.core==1.116.0",
        "constructs>=3.3.69, <4.0.0",
        "jsii>=1.32.0, <2.0.0",
        "publication>=0.0.3"
    ],
    "classifiers": [
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: JavaScript",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Typing :: Typed",
        "Development Status :: 4 - Beta",
        "License :: OSI Approved"
    ],
    "scripts": []
}
"""
)

with open("README.md", encoding="utf8") as fp:
    kwargs["long_description"] = fp.read()


setuptools.setup(**kwargs)
