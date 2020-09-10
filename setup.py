import os
import sys
from glob import glob
from os.path import basename, splitext

from setuptools import find_packages, setup
from setuptools.command.install import install

VERSION = "3.0.2"
README_PATH = "docs/README.md"

test_requirements = ["pytest"]  # "behave", "behave-classy",

long_description = ""
with open(README_PATH, "r", encoding="utf-8") as file:
    long_description = file.read()


class VerifyVersionCommand(install):
    """Custom command to verify that the git tag matches our version"""

    description = 'verify that the git tag matches our version'

    def run(self):
        tag = os.getenv('CIRCLE_TAG')

        if tag != VERSION:
            info = "Git tag: {0} does not match the version of this app: {1}".format(tag, VERSION)
            sys.exit(info)


setup(
    name="ypackage",
    version=VERSION,
    license="Apache Software License 2.0",
    description="Yunus Emre Ak ~ YEmreAk (@yedhrab)'ın google drive direkt link oluşturma"
    + "gitbook entegrasyonu, google arama motoru sonuçlarını filtreleme ile ilgili çalışmaları ",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Yunus Emre Ak",
    author_email="yemreak.com@gmail.com",
    url="https://github.com/yedhrab/YPackage",
    packages=find_packages("src"),
    package_dir={"": "src"},
    py_modules=[splitext(basename(path))[0] for path in glob("src/*.py")],
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        # complete classifier list: http://pypi.python.org/pypi?%3Aaction=list_classifiers
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: Unix",
        "Operating System :: POSIX",
        "Operating System :: Microsoft :: Windows",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
        # uncomment if you test on these interpreters:
        # "Programming Language :: Python :: Implementation :: IronPython",
        # "Programming Language :: Python :: Implementation :: Jython",
        # "Programming Language :: Python :: Implementation :: Stackless",
        "Topic :: Utilities",
    ],
    project_urls={
        "Changelog": "https://github.com/yedhrab/YPackage/blob/master/docs/CHANGELOG.md",
        "Issue Tracker": "https://github.com/yedhrab/YPackage/issues",
    },
    keywords=[
        "ypackage",
        "yedhrab",
        "yemreak",
        "gitbook",
        "github",
        "google-search",
        "google",
        "link",
        "drive",
        "renamer",
        "bulk",
    ],
    python_requires='>=3',
    install_requires=[
        # eg: "aspectlib==1.1.1", "six>=1.7",
        "google",
        "requests",
        "pydriller",
        "coloredlogs",
        "keyboard",
        "mouse"
    ],
    extras_require={
        # eg:
        #   "rst": ["docutils>=0.11"],
        #   ":python_version=="2.6"": ["argparse"],
    },
    setup_requires=["pytest-runner", ],
    entry_points={
        # Komut isteminden çalıştırma
        # örneğin: ypackage
        # Kullanım: "ypackage = ypackage.ypackage:main
        "console_scripts": [
            "ygitbookintegration = ypackage.cli.gitbook:main",
            "yfilerenamer = ypackage.cli.filesystem:main",
            "ygoogledrive = ypackage.cli.gdrive:main",
            "ygooglesearch = ypackage.cli.gsearch:main",
            "ythemecreator = ypackage.cli.theme:main"
        ]
    },
    cmdclass={'verify': VerifyVersionCommand},
    tests_require=test_requirements,
)
