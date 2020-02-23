call venv\Scripts\activate.bat
flake8 --exclude=venv* --statistics
call deactivate
