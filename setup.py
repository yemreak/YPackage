from distutils.core import setup
import setuptools

DYNAMIC_VERSION = False
VERSION = "2.6.5"

if DYNAMIC_VERSION:
    version = ""
    with open(".version", "r", encoding="utf-8") as file:
        version = (int(file.read().strip()) + 1) / 10
else:
    version = VERSION

long_description = ""
with open("README.md", "r", encoding="utf-8") as file:
    long_description = file.read()


setup(
    name='ypackage',             # How you named your package folder (MyLib)
    packages=setuptools.find_packages(),   # Chose the same as "name"
    # Start with a small number and increase it with every change you make
    version=version,
    # Chose a license from here: https://help.github.com/articles/licensing-a-repository
    license='MIT',
    # Give a short description about your library
    description="Yunus Emre Ak ~ YEmreAk (@yedhrab)'ın google drive direkt link oluşturma" +
    "gitbook entegrasyonu, google arama motoru sonuçlarını filtreleme ile ilgili çalışmaları ",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Yunus Emre Ak',
    author_email='yedhrab@gmail.com',
    url='https://github.com/yedhrab/YPackage',
    # Paketi açıklayan anahtar kelimeler
        keywords=[
        'ypackage', 'yedhrab', 'yemreak', 'gitbook', 'github',
        'google-search', "google", "link", "drive", "renamer", "bulk"
    ],
    # Kurulacak alt paketler
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
        'License :: OSI Approved :: MIT License',   # Again, pick a license
        # Specify which pyhton versions that you want to support
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
            'ygitbookintegration = ypackage.integrate:main',
            "ygoogledrive = ypackage.gdrive:main",
            "ygooglesearch = ypackage.gsearch:main",
            "yfile = ypackage.yfile:main"
        ]
    }
)

if DYNAMIC_VERSION:
    with open(".version", "w", encoding="utf-8") as file:
        file.write(str(int(version * 10)))
