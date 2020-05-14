Rem Create a Python Dev Environment (Windows)
python.exe -m venv .venv
CALL .venv\Scripts\activate.bat
python -m pip install --upgrade pip
pip install pylint black
echo Environment Created