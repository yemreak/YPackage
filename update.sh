rm -rf ./dist ./build
python setup.py sdist bdist_wheel
twine upload dist/*
ygitchangelog.exe > CHANGELOG.md
bash github .
