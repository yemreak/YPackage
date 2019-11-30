rm -rf ./dist ./build && \
python setup.py sdist bdist_wheel
ygitchangelog.exe > CHANGELOG.md
