# Copyright 2019 Amazon.com, Inc. or its affiliates. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License").
# You may not use this file except in compliance with the License.
# A copy of the License is located at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# or in the "license" file accompanying this file. This file is distributed 
# on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either 
# express or implied. See the License for the specific language governing 
# permissions and limitations under the License.
from __future__ import absolute_import

import os
from glob import glob
import sys
import json
import subprocess

from setuptools import setup, find_packages


def read(fname):
    with open(os.path.join(os.path.dirname(__file__), fname)) as f:
        return f.read()


def read_version():
    return read("VERSION").strip()

def source_version():
    source_version = os.getenv('CODEBUILD_RESOLVED_SOURCE_VERSION')
    if source_version is None:
        source_version = subprocess.check_output(['git', 'rev-parse', '--verify', 'HEAD']).decode('utf-8').strip()
    return source_version

def generate_build_metadata():
    build_metadata = {"name": "aws-step-functions-data-science-sdk-python", "version": read_version(),
                      "commit": source_version()}
    with open("build.json", "w") as outputfile:
        json.dump(build_metadata, outputfile)


# Declare minimal set for installation
required_packages = [
    "sagemaker>=2.1.0",
    "boto3>=1.14.38",
    "pyyaml"
]

# enum is introduced in Python 3.4. Installing enum back port
if sys.version_info < (3, 4):
    required_packages.append("enum34>=1.1.6")

setup(
    name="stepfunctions",
    version=read_version(),
    description="Open source library for develping data science workflows on AWS Step Functions.",
    packages=find_packages("src"),
    package_dir={"": "src"},
    py_modules=[os.path.splitext(os.path.basename(path))[0] for path in glob("src/*.py")],
    long_description=read("README.rst"),
    author="Amazon Web Services",
    url="https://github.com/aws/aws-step-functions-data-science-sdk-python",
    license="Apache License 2.0",
    keywords="ML Amazon AWS AI Tensorflow MXNet",
    classifiers=[
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.6",
    ],
    install_requires=required_packages,
    extras_require={
        "test": [
            "tox>=3.13.1",
            "pytest>=4.4.1",
            "stopit==1.1.2",
            "tensorflow>=1.3.0",
            "mock>=2.0.0",
            "contextlib2==0.5.5",
            "IPython",
        ]
    }
)

build_metadata = {"name": "aws-sfn", "version": read_version(), "commit_id": os.getenv('CODEBUILD_RESOLVED_SOURCE_VERSION') }
with open("build.json", "w") as outputfile:
    json.dump(build_metadata, outputfile)
print(build_metadata)
