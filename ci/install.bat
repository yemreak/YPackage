python -m venv venv
call venv\Scripts\activate.bat
python -m pip install --upgrade pip 
python -m pip install --upgrade -r .\ci\requirements.txt
python -m pip install --upgrade .
call deactivate
