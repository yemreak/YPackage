python setup.py sdist
twine upload dist/*
gitchangelog.exe > CHANGELOG.md
gbash github .
