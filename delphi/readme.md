# Delphi component of PKIIPS

1. Install python3 and pip and ensure they are added to PATH.
2. Create a virtual environment: `python3 -m venv venv`
3. Source the virtual environment, i.e. for Unix: `source venv/bin/activate`
4. Install requirements with `pip install -r requirements.txt`
5. Export the flask app environment variable using either `set` or `export`, i.e, `set FLASK_APP=delphi.py`
6. `flask run`
