from app import app
from flask import request


@app.route('/')
@app.route('/index')
def index():
    return 'Hello, World!'


@app.route('/upload', methods=['POST'])
def upload():
    for f in request.files.getlist('file'):
        f.save(f'uploads/{f.filename}')
    return f'File(s) successfully uploaded'
