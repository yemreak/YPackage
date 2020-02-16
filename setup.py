from distutils.core import setup
from setuptools import find_packages

README_PATH = "docs/README.md"
DYNAMIC_VERSION = False
VERSION = "2.7.2"

if DYNAMIC_VERSION:
    version = ""
    with open(".version", "r", encoding="utf-8") as file:
        version = (int(file.read().strip()) + 1) / 10
else:
    version = VERSION

long_description = ""
with open(README_PATH, "r", encoding="utf-8") as file:
    long_description = file.read()


setup(
    name='ypackage',
    version=version,
    description="Yunus Emre Ak ~ YEmreAk (@yedhrab)'ın google drive direkt link oluşturma" +
    "gitbook entegrasyonu, google arama motoru sonuçlarını filtreleme ile ilgili çalışmaları ",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Yunus Emre Ak',
    author_email="yemreak.com@gmail.com",
    license='Apache Software License 2.0',
    url='https://github.com/yedhrab/YPackage',
    keywords=[
        'ypackage', 'yedhrab', 'yemreak', 'gitbook', 'github',
        'google-search', "google", "link", "drive", "renamer", "bulk"
    ],
    install_requires=[
        "google",
        "requests",
        "pydriller"
    ],
    classifiers=[
        # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable"
        'Development Status :: 5 - Production/Stable',
        # Define that your audience are developers
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    entry_points={
        # Komut isteminden çalıştırma
        # örndeğin: ypackage
        # Kullanım: 'ypacakge = ypackage.ypackage:main
        'console_scripts': [
            'ygitbookintegration = ypackage.cli.integrate_into_gitbook:main',
            "ygoogledrive = ypackage.cli.gdrive:main",
            "ygooglesearch = ypackage.cli.gsearch:main",
            "yfilerenamer = ypackage.cli.file_renamer:main",
            "ythemecreator = ypackage.cli.theme_creator:main"
        ]
    },
    packages=find_packages(),
)

if DYNAMIC_VERSION:
    with open(".version", "w", encoding="utf-8") as file:
        file.write(str(int(version * 10)))
