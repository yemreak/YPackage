python -m venv venv &&
source venv/Scripts/activate &&
python -m pip install --upgrade pip &&
python -m pip install --upgrade -r .\ci\requirements.txt &&
python -m pip install --upgrade . &&
deactivate
