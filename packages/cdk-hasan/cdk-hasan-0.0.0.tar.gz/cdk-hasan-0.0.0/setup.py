import json
import setuptools

kwargs = json.loads(
    """
{
    "name": "cdk-hasan",
    "version": "0.0.0",
    "description": "my-progen-project",
    "license": "Apache-2.0",
    "url": "https://github.com/hasanaburayyan/my-progen-project.git",
    "long_description_content_type": "text/markdown",
    "author": "Hasan Abu-Rayyn<hasanaburayyan21@gmail.com>",
    "bdist_wheel": {
        "universal": true
    },
    "project_urls": {
        "Source": "https://github.com/hasanaburayyan/my-progen-project.git"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "cdk_hasan",
        "cdk_hasan._jsii"
    ],
    "package_data": {
        "cdk_hasan._jsii": [
            "my-progen-project@0.0.0.jsii.tgz"
        ],
        "cdk_hasan": [
            "py.typed"
        ]
    },
    "python_requires": ">=3.6",
    "install_requires": [
        "aws-cdk.aws-s3>=1.116.0, <2.0.0",
        "aws-cdk.core>=1.116.0, <2.0.0",
        "constructs>=3.2.27, <4.0.0",
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
