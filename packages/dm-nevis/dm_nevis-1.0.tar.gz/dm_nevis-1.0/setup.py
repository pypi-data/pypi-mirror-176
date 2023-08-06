# Copyright 2022 DeepMind Technologies Limited
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Setup script to install the dm_nevis library."""
import setuptools

with open("README.md", "r") as fh:
  long_description = fh.read()

setuptools.setup(
    name="dm_nevis",
    version="1.0",
    author="DeepMind Large-Scale Continual Learning (LSCL) Team",
    author_email="nevis@deepmind.com",
    description="A benchmark for continual learning.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/deepmind/dm_nevis",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
    python_requires=">=3.8")
